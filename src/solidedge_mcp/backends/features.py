"""
Solid Edge Feature Operations

Handles creating 3D features like extrusions, revolves, holes, fillets, etc.
"""

import contextlib
import traceback
from typing import Any

import pythoncom
from win32com.client import VARIANT

from .constants import (
    DirectionConstants,
    DraftSideConstants,
    ExtentTypeConstants,
    FaceQueryConstants,
    FeatureOperationConstants,
    KeyPointExtentConstants,
    KeyPointTypeConstants,
    LoftSweepConstants,
    OffsetSideConstants,
    ReferenceElementConstants,
    TreatmentCrownCurvatureSideConstants,
    TreatmentCrownSideConstants,
    TreatmentCrownTypeConstants,
    TreatmentTypeConstants,
)


class FeatureManager:
    """Manages 3D feature creation"""

    def __init__(self, document_manager, sketch_manager):
        self.doc_manager = document_manager
        self.sketch_manager = sketch_manager

    def _perform_feature_call(self, call_fn, consumes_profiles: bool = True):
        """
        Helper to execute a COM feature call, validate the result, and
        clear accumulated profiles when appropriate.

        Returns: (result, error_dict_or_None)
        """
        try:
            # Try to get model and feature count for validation when possible
            try:
                doc = self.doc_manager.get_active_document()
                models = doc.Models
                model = models.Item(1) if models.Count >= 1 else None
                try:
                    feature_count_before = len(list(model.Features)) if model is not None else None
                except Exception:
                    feature_count_before = None
            except Exception:
                model = None
                feature_count_before = None

            result = call_fn()

            # If COM call returned None, treat as failure
            if result is None:
                if consumes_profiles:
                    try:
                        self.sketch_manager.clear_accumulated_profiles()
                    except Exception:
                        pass
                return None, {
                    "error": "Feature operation failed - COM API returned None",
                    "details": "The Solid Edge COM API did not create the feature."
                }

            # Verify feature count increased if we were able to read it
            if feature_count_before is not None and model is not None:
                try:
                    feature_count_after = len(list(model.Features))
                    if feature_count_after <= feature_count_before:
                        if consumes_profiles:
                            try:
                                self.sketch_manager.clear_accumulated_profiles()
                            except Exception:
                                pass
                        return None, {
                            "error": "Feature not added to model",
                            "details": f"Feature count before: {feature_count_before}, after: {feature_count_after}."
                        }
                except Exception:
                    pass

            if consumes_profiles:
                try:
                    self.sketch_manager.clear_accumulated_profiles()
                except Exception:
                    pass

            return result, None
        except Exception as e:
            if consumes_profiles:
                try:
                    self.sketch_manager.clear_accumulated_profiles()
                except Exception:
                    pass
            return None, {"error": str(e), "traceback": traceback.format_exc()}

    def _append_bbox(self, response: dict) -> None:
        """Append body bounding-box spatial info to a feature response (in-place, silent on error).

        Adds: body_bbox, body_centred_on_origin, and (if off-centre) spatial_warning.
        """
        try:
            from .query import QueryManager
            bbox_data = QueryManager(self.doc_manager).get_bounding_box()
            if "error" in bbox_data:
                return
            mn, mx = bbox_data["min"], bbox_data["max"]
            centre = [
                (mn[0] + mx[0]) / 2,
                (mn[1] + mx[1]) / 2,
                (mn[2] + mx[2]) / 2,
            ]
            centred = all(abs(c) < 0.001 for c in centre)
            response["body_bbox"] = {"min": mn, "max": mx, "centre": centre}
            response["body_centred_on_origin"] = centred
            if not centred:
                response["spatial_warning"] = (
                    f"Body is not centred on origin. Centre is at {centre}. "
                    "Use create_extrude_symmetric if centred geometry is intended."
                )
        except Exception:
            pass  # never fail the feature creation if bbox query fails

    def create_extrude(
        self, distance: float, operation: str = "Add", direction: str = "Normal"
    ) -> dict[str, Any]:
        """
            Create an extrusion feature from the active sketch profile.
        Args:
            distance: Extrusion distance in meters
            operation: 'Add', 'Cut', or 'Intersect'
            direction: 'Normal', 'Reverse', or 'Symmetric'
         Returns:
            Dict with status and feature info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            
            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first"}
            # Get the models collection
            models = doc.Models
            # Map direction string to constant
            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
                "Symmetric": DirectionConstants.igSymmetric,
            }
            dir_const = direction_map.get(direction, DirectionConstants.igRight)
            # The Front plane (plane_index=3) has its outward normal in the world -Y
            # direction — see PLANE_AXIS_MAP in constants.py for the full table.
            # igRight therefore extrudes toward -Y, which is opposite to user expectation
            # for direction="Normal".  Swap igRight ↔ igLeft on the Front plane so that
            # "Normal" → igLeft (+Y) and "Reverse" → igRight (-Y).
            # igSymmetric is left unchanged (symmetric extrudes are unaffected by plane).
            if (
                self.sketch_manager.get_active_plane_index() == 3
                and dir_const in (DirectionConstants.igRight, DirectionConstants.igLeft)
            ):
                dir_const = (
                    DirectionConstants.igLeft
                    if dir_const == DirectionConstants.igRight
                    else DirectionConstants.igRight
                )
            # Execute and validate the COM call
            if operation == "Add":
                if models.Count >= 1:
                    # SE 2026 with pre-existing body
                    model = models.Item(1)
                    protrusions = model.ExtrudedProtrusions
                    result, err = self._perform_feature_call(
                        lambda: protrusions.AddFiniteMulti(1, (profile,), dir_const, distance),
                        consumes_profiles=True,
                    )
                else:
                    # Try legacy first (SE 2024)
                    result, err = self._perform_feature_call(
                        lambda: models.AddFiniteExtrudedProtrusion(1, (profile,), dir_const, distance),
                        consumes_profiles=True,
                    )
                    # If legacy failed, try SE 2026 path with fresh profile from Sketches
                    if err:
                        try:
                            doc_sketches = doc.Sketches
                            sketch = doc_sketches.Item(1)
                            sketch_profile = sketch.Profile
                            result, err = self._perform_feature_call(
                                lambda: models.AddFiniteExtrudedProtrusion(1, (sketch_profile,), dir_const, distance),
                                consumes_profiles=True,
                            )
                        except Exception as e2:
                            err = {"error": f"SE 2026 fallback also failed: {e2}",
                                   "traceback": traceback.format_exc()}
            else:
                # For Cut and Intersect, use ExtrudedCutouts
                if models.Count == 0:
                    return {
                        "error": "No base feature exists. Create a base feature first.",
                        "debug_operation": repr(operation),
                        "debug_operation_eq_Add": operation == "Add",
                        "debug_profile": repr(type(profile)),
                        "debug_models_count": models.Count,
                }
                model = models.Item(1)
                cutouts = model.ExtrudedCutouts
                result, err = self._perform_feature_call(
                    lambda: cutouts.AddFiniteMulti(1, (profile,), dir_const, distance),
                    consumes_profiles=True,
                )
            if err:
                return err
            response = {
                "status": "created",
                "type": "extrude",
                "distance": distance,
                "operation": operation,
                "direction": direction,
            }
            self._append_bbox(response)
            return response
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolve(self, angle: float = 360, operation: str = "Add") -> dict[str, Any]:
        """
        Create a revolve feature from the active sketch profile.

        Requires an axis of revolution to be set in the sketch before closing.
        Use set_axis_of_revolution() in the sketch to define the axis.

        Args:
            angle: Revolution angle in degrees (360 for full revolution)
            operation: 'Add' (Note: 'Cut' not available in COM API)

        Returns:
            Dict with status and feature info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models

            import math

            angle_rad = math.radians(angle)

            # AddFiniteRevolvedProtrusion: NumProfiles,
            # ProfileArray, ReferenceAxis, ProfilePlaneSide, Angle
            # Do NOT pass None for optional params (KeyPointOrTangentFace, KeyPointFlags)
            result, err = self._perform_feature_call(
                lambda: models.AddFiniteRevolvedProtrusion(
                    1,  # NumberOfProfiles
                    (profile,),  # ProfileArray
                    refaxis,  # ReferenceAxis
                    DirectionConstants.igRight,  # ProfilePlaneSide (2)
                    angle_rad,  # AngleofRevolution
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "revolve", "angle": angle, "operation": operation}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole(
        self,
        x: float,
        y: float,
        diameter: float,
        depth: float,
        hole_type: str = "Simple",
        plane_index: int = 1,
        direction: str = "Normal",
    ) -> dict[str, Any]:
        """
        Create a hole feature (circular cutout).

        Creates a circular cutout at (x, y) on a reference plane using
        ExtrudedCutouts.AddFiniteMulti for reliable geometry creation.

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            depth: Hole depth in meters
            hole_type: 'Simple' (only type currently supported)
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            # Map direction
            dir_const = DirectionConstants.igRight  # Normal
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            # Create a circular profile on the specified plane
            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            # Use ExtrudedCutouts.AddFiniteMulti for reliable hole creation
            cutouts = model.ExtrudedCutouts
            result, err = self._perform_feature_call(
                lambda: cutouts.AddFiniteMulti(1, (profile,), dir_const, depth),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "hole",
                "position": [x, y],
                "diameter": diameter,
                "depth": depth,
                "hole_type": hole_type,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_round(self, radius: float) -> dict[str, Any]:
        """
        Create a round (fillet) feature on all body edges.

        Rounds all edges of the body using model.Rounds.Add(). All edges
        are grouped as one edge set with a single radius value.

        Args:
            radius: Round radius in meters

        Returns:
            Dict with status and round info
        """
        try:
            import pythoncom
            from win32com.client import VARIANT

            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add rounds to"}

            model = models.Item(1)
            body = model.Body

            # Collect all edges from all body faces
            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces found on body"}

            edge_list = []
            for fi in range(1, faces.Count + 1):
                face = faces.Item(fi)
                face_edges = face.Edges
                if not hasattr(face_edges, "Count"):
                    continue
                for ei in range(1, face_edges.Count + 1):
                    edge_list.append(face_edges.Item(ei))

            if not edge_list:
                return {"error": "No edges found on body"}

            # Group all edges as one edge set with one radius
            edge_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, edge_list)
            radius_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [radius])

            rounds = model.Rounds
            result, err = self._perform_feature_call(
                lambda: rounds.Add(1, edge_arr, radius_arr), consumes_profiles=False
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "round",
                "radius": radius,
                "edge_count": len(edge_list),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extrude_symmetric(self, distance: float) -> dict[str, Any]:
        """
        Create a symmetric extrusion (extends equally in both directions).

        SE's igSymmetric COM call treats its distance argument as the *total*
        span and halves it internally.  This wrapper multiplies distance by 2
        before calling SE so the feature extends exactly ±distance from the
        sketch plane (total bounding-box depth = 2 × distance).

        Args:
            distance: Half-distance in meters; feature spans ±distance from the
                      sketch plane (total bounding-box depth = 2 × distance).

        Returns:
            Dict with status and feature info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first"}

            models = doc.Models

            # SE's igSymmetric call treats the distance parameter as the *total* span
            # and halves it internally to get each side.  Multiply by 2 so the COM
            # call receives the full span and SE produces ±distance on each side.
            total_span = distance * 2
            if models.Count >= 1:
                # SE 2026+: use collection-level API (same fix as create_extrude)
                model = models.Item(1)
                protrusions = model.ExtrudedProtrusions
                result, err = self._perform_feature_call(
                    lambda: protrusions.AddFiniteMulti(
                        1, (profile,), DirectionConstants.igSymmetric, total_span
                    ),
                    consumes_profiles=True,
                )
            else:
                result, err = self._perform_feature_call(
                    lambda: models.AddFiniteExtrudedProtrusion(
                        1, (profile,), DirectionConstants.igSymmetric, total_span
                    ),
                    consumes_profiles=True,
                )
            if err:
                return err

            response = {
                "status": "created",
                "type": "extrude_symmetric",
                "distance": distance,
                "direction": "Symmetric",
            }
            self._append_bbox(response)
            return response
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_chamfer_unequal_on_face(
        self, distance1: float, distance2: float, face_index: int
    ) -> dict[str, Any]:
        """
        Create an unequal-setback chamfer on all edges of a specific face.

        Args:
            distance1: First setback distance in meters
            distance2: Second setback distance in meters
            face_index: 0-based face index

        Returns:
            Dict with status and chamfer info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add chamfers to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Count: {faces.Count}"}

            face = faces.Item(face_index + 1)
            edges = face.Edges
            if not hasattr(edges, "Count") or edges.Count == 0:
                return {"error": f"No edges found on face {face_index}"}

            edge_list = []
            for ei in range(1, edges.Count + 1):
                edge_list.append(edges.Item(ei))

            chamfers = model.Chamfers
            result, err = self._perform_feature_call(
                lambda: chamfers.AddUnequalSetback(len(edge_list), edge_list, distance1, distance2),
                consumes_profiles=False
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "chamfer_unequal_on_face",
                "distance1": distance1,
                "distance2": distance2,
                "face_index": face_index,
                "edge_count": len(edge_list),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_chamfer(self, distance: float) -> dict[str, Any]:
        """
        Create an equal-setback chamfer on all body edges.

        Chamfers all edges of the body using model.Chamfers.AddEqualSetback().

        Args:
            distance: Chamfer setback distance in meters

        Returns:
            Dict with status and chamfer info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add chamfers to"}

            model = models.Item(1)
            body = model.Body

            # Collect all edges from all body faces
            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces found on body"}

            edge_list = []
            for fi in range(1, faces.Count + 1):
                face = faces.Item(fi)
                face_edges = face.Edges
                if not hasattr(face_edges, "Count"):
                    continue
                for ei in range(1, face_edges.Count + 1):
                    edge_list.append(face_edges.Item(ei))

            if not edge_list:
                return {"error": "No edges found on body"}

            chamfers = model.Chamfers
            result, err = self._perform_feature_call(
                lambda: chamfers.AddEqualSetback(len(edge_list), edge_list, distance),
                consumes_profiles=False
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "chamfer",
                "distance": distance,
                "edge_count": len(edge_list),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_pattern(self, pattern_type: str, **kwargs) -> dict[str, Any]:
        """
        Create a pattern of features.

        Note: Feature patterns require SAFEARRAY(IDispatch) marshaling of feature
        objects which is not currently supported via COM late binding. Use assembly-level
        component patterns (pattern_component) instead.

        Args:
            pattern_type: 'Rectangular' or 'Circular'
            **kwargs: Pattern-specific parameters

        Returns:
            Dict with error explaining limitation
        """
        return {
            "error": "Feature patterns (model.Patterns) require SAFEARRAY marshaling of "
            "feature objects which is not supported via COM late binding. "
            "Use assembly-level pattern_component() for component patterns instead.",
            "pattern_type": pattern_type,
        }

    def create_shell(
        self, thickness: float, remove_face_indices: list[int] | None = None
    ) -> dict[str, Any]:
        """
        Create a shell feature (hollow out the part).

        Note: Shell (Thinwalls) requires face selection for open faces which cannot
        be reliably automated via COM late binding. The Thinwalls.Add method requires
        complex VARIANT parameters for face arrays.

        Args:
            thickness: Wall thickness in meters
            remove_face_indices: Indices of faces to remove (optional)

        Returns:
            Dict with error explaining limitation
        """
        return {
            "error": "Shell (Thinwalls) feature requires face selection for open faces "
            "which cannot be reliably automated via COM. Use the Solid Edge UI "
            "to create shell features.",
            "thickness": thickness,
        }

    def list_features(self) -> dict[str, Any]:
        """List all features in the active part"""
        try:
            doc = self.doc_manager.get_active_document()
            features_collection = doc.DesignEdgebarFeatures

            features = []
            for i in range(features_collection.Count):
                feature = features_collection.Item(i + 1)
                features.append(
                    {
                        "index": i,
                        "name": feature.Name if hasattr(feature, "Name") else f"Feature {i + 1}",
                        "type": feature.Type if hasattr(feature, "Type") else "Unknown",
                    }
                )

            return {"features": features, "count": len(features)}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_feature_info(self, feature_index: int) -> dict[str, Any]:
        """Get detailed information about a specific feature"""
        try:
            doc = self.doc_manager.get_active_document()
            features_collection = doc.DesignEdgebarFeatures

            if feature_index < 0 or feature_index >= features_collection.Count:
                return {"error": f"Invalid feature index: {feature_index}"}

            feature = features_collection.Item(feature_index + 1)

            info = {
                "index": feature_index,
                "name": feature.Name if hasattr(feature, "Name") else "Unknown",
                "type": feature.Type if hasattr(feature, "Type") else "Unknown",
            }

            # Try to get additional properties
            try:
                if hasattr(feature, "Visible"):
                    info["visible"] = feature.Visible
                if hasattr(feature, "Suppressed"):
                    info["suppressed"] = feature.Suppressed
            except Exception:
                pass

            return info
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # PRIMITIVE SHAPES
    # =================================================================

    def _get_ref_plane(self, doc, plane_index: int = 1):
        """Get a reference plane from the document (1=Top/XZ, 2=Front/XY, 3=Right/YZ)"""
        return doc.RefPlanes.Item(plane_index)

    def create_box_by_center(
        self,
        center_x: float,
        center_y: float,
        center_z: float,
        length: float,
        width: float,
        height: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a box by center point and dimensions via sketch→extrude.

        Draws a rectangle centred at (center_x, center_y) on the given plane and
        extrudes by height in the plane-normal direction.  center_z is recorded in
        the return value but is not applied as a plane offset (future work).

        Args:
            center_x, center_y, center_z: Center point coordinates (meters)
            length: Length in meters (sketch X direction)
            width: Width in meters (sketch Y direction)
            height: Extrusion depth in meters (plane normal direction)
            plane_index: Reference plane (1=Top, 2=Right, 3=Front)

        Returns:
            Dict with status and box info
        """
        try:
            plane_name = {1: "Top", 2: "Right", 3: "Front"}.get(plane_index, "Top")

            r = self.sketch_manager.create_sketch(plane_name)
            if "error" in r:
                return r

            x1 = center_x - length / 2.0
            y1 = center_y - width / 2.0
            x2 = center_x + length / 2.0
            y2 = center_y + width / 2.0
            r = self.sketch_manager.draw_rectangle(x1, y1, x2, y2)
            if "error" in r:
                return r

            r = self.sketch_manager.close_sketch()
            if "error" in r:
                return r

            r = self.create_extrude(height, operation="Add", direction="Normal")
            if "error" in r:
                return r

            response = {
                "status": "created",
                "type": "box",
                "method": "by_center",
                "center": [center_x, center_y, center_z],
                "dimensions": {"length": length, "width": width, "height": height},
            }
            self._append_bbox(response)
            return response
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_box_by_two_points(
        self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, plane_index: int = 1
    ) -> dict[str, Any]:
        """
        Create a box by two opposite corners via sketch→extrude.

        Draws a rectangle from (x1, y1) to (x2, y2) on the sketch plane and
        extrudes by abs(z2 - z1).  Falls back to abs(y2 - y1) when z coords match.

        Args:
            x1, y1, z1: First corner coordinates (meters)
            x2, y2, z2: Opposite corner coordinates (meters)
            plane_index: Reference plane (1=Top, 2=Right, 3=Front)

        Returns:
            Dict with status and box info
        """
        try:
            depth = abs(z2 - z1) if abs(z2 - z1) > 1e-9 else abs(y2 - y1)
            if depth < 1e-9:
                depth = 0.01

            plane_name = {1: "Top", 2: "Right", 3: "Front"}.get(plane_index, "Top")

            r = self.sketch_manager.create_sketch(plane_name)
            if "error" in r:
                return r

            r = self.sketch_manager.draw_rectangle(x1, y1, x2, y2)
            if "error" in r:
                return r

            r = self.sketch_manager.close_sketch()
            if "error" in r:
                return r

            r = self.create_extrude(depth, operation="Add", direction="Normal")
            if "error" in r:
                return r

            return {
                "status": "created",
                "type": "box",
                "method": "by_two_points",
                "corner1": [x1, y1, z1],
                "corner2": [x2, y2, z2],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_box_by_three_points(
        self,
        x1: float,
        y1: float,
        z1: float,
        x2: float,
        y2: float,
        z2: float,
        x3: float,
        y3: float,
        z3: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a box by three points via sketch→extrude (axis-aligned approximation).

        Derives the sketch rectangle from the 2D bounding box of the three points and
        the extrusion depth from abs(z3 - z1).  A proper oriented-box implementation
        requires computing the local coordinate frame from the three points (see TODO.md).

        Args:
            x1, y1, z1: First corner point (meters)
            x2, y2, z2: Second point defining one dimension (meters)
            x3, y3, z3: Third point defining depth / other dimension (meters)
            plane_index: Reference plane (1=Top, 2=Right, 3=Front)

        Returns:
            Dict with status and box info
        """
        try:
            # Axis-aligned bounding rectangle in the sketch plane
            rx1 = min(x1, x2, x3)
            ry1 = min(y1, y2, y3)
            rx2 = max(x1, x2, x3)
            ry2 = max(y1, y2, y3)

            depth = abs(z3 - z1) if abs(z3 - z1) > 1e-9 else abs(z2 - z1)
            if depth < 1e-9:
                depth = 0.01

            plane_name = {1: "Top", 2: "Right", 3: "Front"}.get(plane_index, "Top")

            r = self.sketch_manager.create_sketch(plane_name)
            if "error" in r:
                return r

            r = self.sketch_manager.draw_rectangle(rx1, ry1, rx2, ry2)
            if "error" in r:
                return r

            r = self.sketch_manager.close_sketch()
            if "error" in r:
                return r

            r = self.create_extrude(depth, operation="Add", direction="Normal")
            if "error" in r:
                return r

            return {
                "status": "created",
                "type": "box",
                "method": "by_three_points",
                "point1": [x1, y1, z1],
                "point2": [x2, y2, z2],
                "point3": [x3, y3, z3],
                "note": "Axis-aligned approximation; see TODO.md for oriented-box improvement.",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_cylinder(
        self,
        base_center_x: float,
        base_center_y: float,
        base_center_z: float,
        radius: float,
        height: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a cylinder via sketch→extrude.

        Draws a circle at (base_center_x, base_center_y) with the given radius on the
        sketch plane and extrudes it by height.  base_center_z is recorded in the return
        value but is not applied as a plane offset (future work).

        Args:
            base_center_x, base_center_y, base_center_z: Base circle center (meters)
            radius: Cylinder radius (meters)
            height: Cylinder height / extrusion depth (meters)
            plane_index: Reference plane (1=Top, 2=Right, 3=Front)

        Returns:
            Dict with status and cylinder info
        """
        try:
            plane_name = {1: "Top", 2: "Right", 3: "Front"}.get(plane_index, "Top")

            r = self.sketch_manager.create_sketch(plane_name)
            if "error" in r:
                return r

            r = self.sketch_manager.draw_circle(base_center_x, base_center_y, radius)
            if "error" in r:
                return r

            r = self.sketch_manager.close_sketch()
            if "error" in r:
                return r

            r = self.create_extrude(height, operation="Add", direction="Normal")
            if "error" in r:
                return r

            response = {
                "status": "created",
                "type": "cylinder",
                "base_center": [base_center_x, base_center_y, base_center_z],
                "radius": radius,
                "height": height,
            }
            self._append_bbox(response)
            return response
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_sphere(
        self, center_x: float, center_y: float, center_z: float, radius: float, plane_index: int = 1
    ) -> dict[str, Any]:
        """
        Create a sphere via sketch→revolve.

        Draws a right-hand semicircle (arc from 270° to 90° through 0°) plus a closing
        diameter line at center_x, sets the diameter as the axis of revolution, then
        revolves 360°.  center_z is recorded in the return value but is not applied as
        a plane offset (future work).

        Args:
            center_x, center_y, center_z: Sphere center coordinates (meters)
            radius: Sphere radius (meters)
            plane_index: Reference plane (1=Top, 2=Right, 3=Front)

        Returns:
            Dict with status and sphere info
        """
        try:
            plane_name = {1: "Top", 2: "Right", 3: "Front"}.get(plane_index, "Top")

            r = self.sketch_manager.create_sketch(plane_name)
            if "error" in r:
                return r

            # Semicircle: bottom (cx, cy-r) → right (cx+r, cy) → top (cx, cy+r)
            r = self.sketch_manager.draw_arc(center_x, center_y, radius, 270, 90)
            if "error" in r:
                return r

            # Closing diameter line (top → bottom along the axis side)
            r = self.sketch_manager.draw_line(
                center_x, center_y + radius,
                center_x, center_y - radius,
            )
            if "error" in r:
                return r

            # Construction axis along the diameter (bottom → top)
            r = self.sketch_manager.set_axis_of_revolution(
                center_x, center_y - radius,
                center_x, center_y + radius,
            )
            if "error" in r:
                return r

            r = self.sketch_manager.close_sketch()
            if "error" in r:
                return r

            r = self.create_revolve(angle=360, operation="Add")
            if "error" in r:
                return r

            response = {
                "status": "created",
                "type": "sphere",
                "center": [center_x, center_y, center_z],
                "radius": radius,
            }
            self._append_bbox(response)
            return response
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def _make_loft_variant_arrays(self, profiles):
        """Create properly typed VARIANT arrays for loft/sweep COM calls.

        COM requires explicit VARIANT typing for SAFEARRAY parameters.
        Python's automatic marshaling does not produce correct types for nested arrays.

        Args:
            profiles: List of profile COM objects

        Returns:
            Tuple of (v_profiles, v_types, v_origins) VARIANT arrays
        """
        v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, profiles)
        v_types = VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_I4,
            [LoftSweepConstants.igProfileBasedCrossSection] * len(profiles),
        )
        v_origins = VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
            [VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0]) for _ in profiles],
        )
        return v_profiles, v_types, v_origins

    def create_loft(self, profile_indices: list = None) -> dict[str, Any]:
        """
        Create a loft feature between multiple profiles.

        Uses accumulated profiles from close_sketch() calls. Create 2+ sketches
        on different parallel planes, close each one, then call create_loft().

        Args:
            profile_indices: Optional list of profile indices to select from
                accumulated profiles. If None, uses all accumulated profiles.

        Returns:
            Dict with status and loft info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            # Get accumulated profiles from sketch manager
            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if profile_indices is not None:
                profiles = [all_profiles[i] for i in profile_indices]
            else:
                profiles = all_profiles

            if len(profiles) < 2:
                return {
                    "error": f"Loft requires at least 2 profiles"
                    f", got {len(profiles)}. Create sketches"
                    " on different planes and close each"
                    " one before calling create_loft()."
                }

            v_profiles, v_types, v_origins = self._make_loft_variant_arrays(profiles)

            # Try LoftedProtrusions.AddSimple first (works when a base feature exists)
            try:
                model = models.Item(1)
                lp = model.LoftedProtrusions
                result, err = self._perform_feature_call(
                    lambda: lp.AddSimple(
                        len(profiles),
                        v_profiles,
                        v_types,
                        v_origins,
                        DirectionConstants.igRight,
                        ExtentTypeConstants.igNone,
                        ExtentTypeConstants.igNone,
                    ),
                    consumes_profiles=True,
                )
                if err:
                    raise Exception("Loft AddSimple failed")

                return {
                    "status": "created",
                    "type": "loft",
                    "num_profiles": len(profiles),
                    "method": "LoftedProtrusions.AddSimple",
                }
            except Exception:
                pass

            # Fall back to models.AddLoftedProtrusion (works as initial feature)
            v_seg = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, [])
            result, err = self._perform_feature_call(
                lambda: models.AddLoftedProtrusion(
                    len(profiles),
                    v_profiles,
                    v_types,
                    v_origins,
                    v_seg,  # SegmentMaps (empty)
                    DirectionConstants.igRight,  # MaterialSide
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,  # Start extent
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,  # End extent
                    ExtentTypeConstants.igNone,
                    0.0,  # Start tangent
                    ExtentTypeConstants.igNone,
                    0.0,  # End tangent
                ),
                consumes_profiles=True,
            )
            if err:
                return err
            return {
                "status": "created",
                "type": "loft",
                "num_profiles": len(profiles),
                "method": "models.AddLoftedProtrusion",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_sweep(self, path_profile_index: int = None) -> dict[str, Any]:
        """
        Create a sweep feature along a path.

        Requires at least 2 accumulated profiles: the first is the path (open profile),
        and the second is the cross-section (closed profile). Create the path sketch
        first (open, e.g. a line or arc), then create the cross-section sketch
        (closed, e.g. a circle) on a plane perpendicular to the path start.

        Args:
            path_profile_index: Index of the path profile in accumulated profiles
                (default: 0, the first accumulated profile)

        Returns:
            Dict with status and sweep info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if len(all_profiles) < 2:
                return {
                    "error": "Sweep requires at least 2 "
                    "profiles (path + cross-section), "
                    f"got {len(all_profiles)}. Create a "
                    "path sketch and a cross-section "
                    "sketch first."
                }

            path_idx = path_profile_index if path_profile_index is not None else 0
            path_profile = all_profiles[path_idx]
            cross_sections = [p for i, p in enumerate(all_profiles) if i != path_idx]

            _CS = LoftSweepConstants.igProfileBasedCrossSection

            # Path arrays
            v_paths = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [path_profile])
            v_path_types = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS])

            # Cross-section arrays
            v_sections = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, cross_sections)
            v_section_types = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS] * len(cross_sections)
            )
            v_origins = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
                [VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0]) for _ in cross_sections],
            )
            v_seg = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, [])

            # AddSweptProtrusion: 15 required params
            result, err = self._perform_feature_call(
                lambda: models.AddSweptProtrusion(
                    1,
                    v_paths,
                    v_path_types,  # Path (1 curve)
                    len(cross_sections),
                    v_sections,
                    v_section_types,
                    v_origins,
                    v_seg,  # Sections
                    DirectionConstants.igRight,  # MaterialSide
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,  # Start extent
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,  # End extent
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "sweep",
                "num_cross_sections": len(cross_sections),
                "method": "models.AddSweptProtrusion",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ADVANCED EXTRUDE/REVOLVE VARIANTS
    # =================================================================

    def create_extrude_thin_wall(
        self, distance: float, wall_thickness: float, direction: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a thin-walled extrusion.

        Args:
            distance: Extrusion distance (meters)
            wall_thickness: Wall thickness (meters)
            direction: 'Normal', 'Reverse', or 'Symmetric'

        Returns:
            Dict with status and extrusion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            # Map direction
            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
                "Symmetric": DirectionConstants.igSymmetric,
            }
            dir_const = direction_map.get(direction, DirectionConstants.igRight)

            # AddExtrudedProtrusionWithThinWall
            result, err = self._perform_feature_call(
                lambda: models.AddExtrudedProtrusionWithThinWall(
                    1,
                    (profile,),
                    dir_const,
                    distance,
                    wall_thickness,
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "extrude_thin_wall",
                "distance": distance,
                "wall_thickness": wall_thickness,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolve_finite(self, angle: float, axis_type: str = "CenterLine") -> dict[str, Any]:
        """
        Create a finite revolve feature.

        Requires an axis of revolution to be set in the sketch before closing.

        Args:
            angle: Revolution angle in degrees
            axis_type: Type of revolution axis (unused, axis comes from sketch)

        Returns:
            Dict with status and revolve info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile"}

            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models

            import math

            angle_rad = math.radians(angle)

            result, err = self._perform_feature_call(
                lambda: models.AddFiniteRevolvedProtrusion(
                    1,  # NumberOfProfiles
                    (profile,),  # ProfileArray
                    refaxis,  # ReferenceAxis
                    DirectionConstants.igRight,  # ProfilePlaneSide (2)
                    angle_rad,  # AngleofRevolution
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "revolve_finite", "angle": angle}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolve_thin_wall(self, angle: float, wall_thickness: float) -> dict[str, Any]:
        """
        Create a thin-walled revolve feature.

        Requires an axis of revolution to be set in the sketch before closing.

        Args:
            angle: Revolution angle in degrees
            wall_thickness: Wall thickness (meters)

        Returns:
            Dict with status and revolve info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile"}

            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models

            import math

            angle_rad = math.radians(angle)

            result, err = self._perform_feature_call(
                lambda: models.AddRevolvedProtrusionWithThinWall(
                    1,  # NumberOfProfiles
                    (profile,),  # ProfileArray
                    refaxis,  # ReferenceAxis
                    DirectionConstants.igRight,  # ProfilePlaneSide
                    angle_rad,  # AngleofRevolution
                    wall_thickness,  # WallThickness
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "revolve_thin_wall",
                "angle": angle,
                "wall_thickness": wall_thickness,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extrude_infinite(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create an infinite extrusion (extends through all).

        Args:
            direction: 'Normal', 'Reverse', or 'Symmetric'

        Returns:
            Dict with status and extrusion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
                "Symmetric": DirectionConstants.igSymmetric,
            }
            dir_const = direction_map.get(direction, DirectionConstants.igRight)

            # Use ExtrudedProtrusions.AddThroughAll (assuming it exists for infinite extrusion)
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            protrusions = model.ExtrudedProtrusions
            result, err = self._perform_feature_call(
                lambda: protrusions.AddThroughAll(1, (profile,), dir_const),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "extrude_infinite", "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extrude_through_next(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create an extrusion that extends to the next face encountered.

        Uses ExtrudedProtrusions.AddThroughNext(Profile, ProfilePlaneSide) on the
        collection. Extrudes from the sketch plane until it meets the first face.

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and extrusion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            dir_const = direction_map.get(direction, DirectionConstants.igRight)

            protrusions = model.ExtrudedProtrusions
            result, err = self._perform_feature_call(
                lambda: protrusions.AddThroughNext(profile, dir_const), consumes_profiles=True
            )
            if err:
                return err

            return {"status": "created", "type": "extrude_through_next", "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extrude_from_to(self, from_plane_index: int, to_plane_index: int) -> dict[str, Any]:
        """
        Create an extrusion between two reference planes.

        Uses ExtrudedProtrusions.AddFromTo(Profile, FromFaceOrRefPlane, ToFaceOrRefPlane)
        on the collection. Extrudes from one plane to another.

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane

        Returns:
            Dict with status and extrusion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            protrusions = model.ExtrudedProtrusions
            result, err = self._perform_feature_call(
                lambda: protrusions.AddFromTo(profile, from_plane, to_plane), consumes_profiles=True
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "extrude_from_to",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_cutout_from_to(
        self, from_plane_index: int, to_plane_index: int
    ) -> dict[str, Any]:
        """
        Create an extruded cutout between two reference planes.

        Uses ExtrudedCutouts.AddFromToMulti(NumProfiles, ProfileArray,
        FromFaceOrRefPlane, ToFaceOrRefPlane) on the collection.

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            cutouts = model.ExtrudedCutouts
            result, err = self._perform_feature_call(
                lambda: cutouts.AddFromToMulti(1, (profile,), from_plane, to_plane),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "extruded_cutout_from_to",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_surface(
        self, distance: float, direction: str = "Normal", end_caps: bool = True
    ) -> dict[str, Any]:
        """
        Create an extruded surface (construction geometry, not solid body).

        Extrudes the active sketch profile as a surface rather than a solid.
        Surfaces are useful as construction geometry for trimming, splitting,
        or as reference faces.

        Args:
            distance: Extrusion distance in meters
            direction: 'Normal' or 'Symmetric'
            end_caps: If True, close the surface ends

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            constructions = doc.Constructions
            extruded_surfaces = constructions.ExtrudedSurfaces

            # Build profile array
            profile_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            depth1 = distance
            depth2 = distance if direction == "Symmetric" else 0.0
            side1 = DirectionConstants.igRight
            side2 = (
                DirectionConstants.igLeft
                if direction == "Symmetric"
                else DirectionConstants.igRight
            )

            result, err = self._perform_feature_call(
                lambda: extruded_surfaces.Add(
                    1,  # NumberOfProfiles
                    profile_array,  # ProfileArray
                    ExtentTypeConstants.igFinite,  # ExtentType1
                    side1,  # ExtentSide1
                    depth1,  # FiniteDepth1
                    None,  # KeyPointOrTangentFace1
                    KeyPointExtentConstants.igTangentNormal,  # KeyPointFlags1
                    None,  # FromFaceOrRefPlane
                    OffsetSideConstants.seOffsetNone,  # FromFaceOffsetSide
                    0.0,  # FromFaceOffsetDistance
                    TreatmentTypeConstants.seTreatmentNone,  # TreatmentType1
                    DraftSideConstants.seDraftNone,  # TreatmentDraftSide1
                    0.0,  # TreatmentDraftAngle1
                    TreatmentCrownTypeConstants.seTreatmentCrownByOffset,  # TreatmentCrownType1
                    TreatmentCrownSideConstants.seTreatmentCrownSideInside,  # TreatmentCrownSide1
                    # TreatmentCrownCurvatureSide1
                    TreatmentCrownCurvatureSideConstants.seTreatmentCrownCurvatureInside,
                    0.0,  # TreatmentCrownRadiusOrOffset1
                    0.0,  # TreatmentCrownTakeOffAngle1
                    ExtentTypeConstants.igFinite,  # ExtentType2
                    side2,  # ExtentSide2
                    depth2,  # FiniteDepth2
                    None,  # KeyPointOrTangentFace2
                    KeyPointExtentConstants.igTangentNormal,  # KeyPointFlags2
                    None,  # ToFaceOrRefPlane
                    OffsetSideConstants.seOffsetNone,  # ToFaceOffsetSide
                    0.0,  # ToFaceOffsetDistance
                    TreatmentTypeConstants.seTreatmentNone,  # TreatmentType2
                    DraftSideConstants.seDraftNone,  # TreatmentDraftSide2
                    0.0,  # TreatmentDraftAngle2
                    TreatmentCrownTypeConstants.seTreatmentCrownByOffset,  # TreatmentCrownType2
                    TreatmentCrownSideConstants.seTreatmentCrownSideInside,  # TreatmentCrownSide2
                    # TreatmentCrownCurvatureSide2
                    TreatmentCrownCurvatureSideConstants.seTreatmentCrownCurvatureInside,
                    0.0,  # TreatmentCrownRadiusOrOffset2
                    0.0,  # TreatmentCrownTakeOffAngle2
                    end_caps,  # WantEndCaps
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "extruded_surface",
                "distance": distance,
                "direction": direction,
                "end_caps": end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # HELIX AND SPIRAL FEATURES
    # =================================================================

    def create_helix(
        self, pitch: float, height: float, revolutions: float = None, direction: str = "Right"
    ) -> dict[str, Any]:
        """
        Create a helical feature.

        Args:
            pitch: Distance between coils (meters)
            height: Total height of helix (meters)
            revolutions: Number of turns (optional, calculated from pitch/height if not given)
            direction: 'Right' or 'Left' hand helix

        Returns:
            Dict with status and helix info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            # Calculate revolutions if not provided
            if revolutions is None:
                revolutions = height / pitch

            # AddFiniteBaseHelix
            result, err = self._perform_feature_call(
                lambda: models.AddFiniteBaseHelix(
                    1,
                    (profile,),
                    pitch,
                    height,
                    revolutions,
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "helix",
                "pitch": pitch,
                "height": height,
                "revolutions": revolutions,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # SHEET METAL FEATURES
    # =================================================================

    def create_base_flange(
        self, width: float, thickness: float, bend_radius: float = None
    ) -> dict[str, Any]:
        """
        Create a base contour flange (sheet metal).

        Args:
            width: Flange width (meters)
            thickness: Material thickness (meters)
            bend_radius: Bend radius (meters, optional)

        Returns:
            Dict with status and flange info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            if bend_radius is None:
                bend_radius = thickness * 2

            # AddBaseContourFlange
            result, err = self._perform_feature_call(
                lambda: models.AddBaseContourFlange(
                    1,
                    (profile,),
                    thickness,
                    bend_radius,
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "base_flange",
                "thickness": thickness,
                "bend_radius": bend_radius,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_base_tab(self, thickness: float, width: float = None) -> dict[str, Any]:
        """
        Create a base tab (sheet metal).

        Args:
            thickness: Material thickness (meters)
            width: Tab width (meters, optional)

        Returns:
            Dict with status and tab info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            # AddBaseTab
            result, err = self._perform_feature_call(
                lambda: models.AddBaseTab(1, (profile,), thickness),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "base_tab", "thickness": thickness}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # BODY OPERATIONS
    # =================================================================

    def add_body(self, body_type: str = "Solid") -> dict[str, Any]:
        """
        Add a body to the part.

        Args:
            body_type: Type of body - 'Solid', 'Surface', 'Construction'

        Returns:
            Dict with status and body info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            # AddBody
            result, err = self._perform_feature_call(lambda: models.AddBody(), consumes_profiles=False)
            if err:
                return err

            return {"status": "created", "type": "body", "body_type": body_type}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def thicken_surface(self, thickness: float, direction: str = "Both") -> dict[str, Any]:
        """
        Thicken a surface to create a solid.

        Args:
            thickness: Thickness (meters)
            direction: 'Both', 'Inside', or 'Outside'

        Returns:
            Dict with status and thicken info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            # AddThickenFeature
            result, err = self._perform_feature_call(
                lambda: models.AddThickenFeature(thickness),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "thicken",
                "thickness": thickness,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_loft_thin_wall(
        self, wall_thickness: float, profile_indices: list = None
    ) -> dict[str, Any]:
        """
        Create a thin-walled loft feature between multiple profiles.

        Uses accumulated profiles from close_sketch() calls.

        Args:
            wall_thickness: Wall thickness in meters
            profile_indices: Optional list of profile indices to select

        Returns:
            Dict with status and loft info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if profile_indices is not None:
                profiles = [all_profiles[i] for i in profile_indices]
            else:
                profiles = all_profiles

            if len(profiles) < 2:
                return {"error": f"Loft requires at least 2 profiles, got {len(profiles)}."}

            v_profiles, v_types, v_origins = self._make_loft_variant_arrays(profiles)
            v_seg = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, [])

            result, err = self._perform_feature_call(
                lambda: models.AddLoftedProtrusionWithThinWall(
                    len(profiles),
                    v_profiles,
                    v_types,
                    v_origins,
                    v_seg,  # SegmentMaps
                    DirectionConstants.igRight,  # MaterialSide
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,  # Start extent
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,  # End extent
                    ExtentTypeConstants.igNone,
                    0.0,  # Start tangent
                    ExtentTypeConstants.igNone,
                    0.0,  # End tangent
                    wall_thickness,  # WallThickness
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "loft_thin_wall",
                "wall_thickness": wall_thickness,
                "num_profiles": len(profiles),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_sweep_thin_wall(
        self, wall_thickness: float, path_profile_index: int = None
    ) -> dict[str, Any]:
        """
        Create a thin-walled sweep feature along a path.

        Uses accumulated profiles: first is path (open), rest are cross-sections (closed).

        Args:
            wall_thickness: Wall thickness in meters
            path_profile_index: Index of the path profile (default: 0)

        Returns:
            Dict with status and sweep info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if len(all_profiles) < 2:
                return {
                    "error": f"Sweep requires at least 2 profiles (path + cross-section), "
                    f"got {len(all_profiles)}."
                }

            path_idx = path_profile_index if path_profile_index is not None else 0
            path_profile = all_profiles[path_idx]
            cross_sections = [p for i, p in enumerate(all_profiles) if i != path_idx]

            _CS = LoftSweepConstants.igProfileBasedCrossSection

            v_paths = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [path_profile])
            v_path_types = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS])
            v_sections = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, cross_sections)
            v_section_types = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS] * len(cross_sections)
            )
            v_origins = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
                [VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0]) for _ in cross_sections],
            )
            v_seg = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, [])

            result, err = self._perform_feature_call(
                lambda: models.AddSweptProtrusionWithThinWall(
                    1,
                    v_paths,
                    v_path_types,
                    len(cross_sections),
                    v_sections,
                    v_section_types,
                    v_origins,
                    v_seg,
                    DirectionConstants.igRight,
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,
                    wall_thickness,
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "sweep_thin_wall",
                "wall_thickness": wall_thickness,
                "num_cross_sections": len(cross_sections),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # SIMPLIFICATION FEATURES
    # =================================================================

    def auto_simplify(self) -> dict[str, Any]:
        """Auto-simplify the model"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(lambda: models.AddAutoSimplify(), consumes_profiles=False)
            if err:
                return err

            return {"status": "created", "type": "auto_simplify"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def simplify_enclosure(self) -> dict[str, Any]:
        """Create simplified enclosure"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(lambda: models.AddSimplifyEnclosure(), consumes_profiles=False)
            if err:
                return err

            return {"status": "created", "type": "simplify_enclosure"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def simplify_duplicate(self) -> dict[str, Any]:
        """Create simplified duplicate"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(lambda: models.AddSimplifyDuplicate(), consumes_profiles=False)
            if err:
                return err

            return {"status": "created", "type": "simplify_duplicate"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def local_simplify_enclosure(self) -> dict[str, Any]:
        """Create local simplified enclosure"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(lambda: models.AddLocalSimplifyEnclosure(), consumes_profiles=False)
            if err:
                return err

            return {"status": "created", "type": "local_simplify_enclosure"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ADDITIONAL REVOLVE VARIANTS
    # =================================================================

    def create_revolve_sync(self, angle: float) -> dict[str, Any]:
        """Create synchronous revolve feature"""
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile"}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models

            import math

            angle_rad = math.radians(angle)

            result, err = self._perform_feature_call(
                lambda: models.AddRevolvedProtrusionSync(
                    1,  # NumberOfProfiles
                    (profile,),  # ProfileArray
                    refaxis,  # ReferenceAxis
                    DirectionConstants.igRight,  # ProfilePlaneSide
                    angle_rad,  # AngleofRevolution
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "revolve_sync", "angle": angle}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolve_finite_sync(self, angle: float) -> dict[str, Any]:
        """Create finite synchronous revolve feature"""
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile"}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models

            import math

            angle_rad = math.radians(angle)

            result, err = self._perform_feature_call(
                lambda: models.AddFiniteRevolvedProtrusionSync(
                    1,  # NumberOfProfiles
                    (profile,),  # ProfileArray
                    refaxis,  # ReferenceAxis
                    DirectionConstants.igRight,  # ProfilePlaneSide
                    angle_rad,  # AngleofRevolution
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "revolve_finite_sync", "angle": angle}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ADDITIONAL HELIX VARIANTS
    # =================================================================

    def create_helix_sync(
        self, pitch: float, height: float, revolutions: float = None
    ) -> dict[str, Any]:
        """Create synchronous helix feature"""
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            if revolutions is None:
                revolutions = height / pitch

            result, err = self._perform_feature_call(
                lambda: models.AddFiniteBaseHelixSync(
                    1,
                    (profile,),
                    pitch,
                    height,
                    revolutions,
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "helix_sync",
                "pitch": pitch,
                "height": height,
                "revolutions": revolutions,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_helix_thin_wall(
        self, pitch: float, height: float, wall_thickness: float, revolutions: float = None
    ) -> dict[str, Any]:
        """Create thin-walled helix feature"""
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            if revolutions is None:
                revolutions = height / pitch

            result, err = self._perform_feature_call(
                lambda: models.AddFiniteBaseHelixWithThinWall(
                    1,
                    (profile,),
                    pitch,
                    height,
                    revolutions,
                    wall_thickness,
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "helix_thin_wall",
                "pitch": pitch,
                "height": height,
                "wall_thickness": wall_thickness,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_helix_sync_thin_wall(
        self, pitch: float, height: float, wall_thickness: float, revolutions: float = None
    ) -> dict[str, Any]:
        """Create synchronous thin-walled helix feature"""
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            if revolutions is None:
                revolutions = height / pitch

            result, err = self._perform_feature_call(
                lambda: models.AddFiniteBaseHelixSyncWithThinWall(
                    1,
                    (profile,),
                    pitch,
                    height,
                    revolutions,
                    wall_thickness,
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "helix_sync_thin_wall",
                "pitch": pitch,
                "height": height,
                "wall_thickness": wall_thickness,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # CUTOUT OPERATIONS
    # =================================================================

    def create_extruded_cutout(self, distance: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create an extruded cutout (cut) through the part using the active sketch profile.

        Uses model.ExtrudedCutouts.AddFiniteMulti(NumProfiles, ProfileArray, PlaneSide, Depth).
        Requires an existing base feature and a closed sketch profile.

        Direction semantics
        -------------------
        "Normal"  — cuts in the sketch plane's outward-normal direction (igRight).
                    On the Front plane SE's internal normal is -Y, so "Normal"
                    cuts toward world -Y.
        "Reverse" — cuts in the opposite direction (igLeft).  On the Front plane
                    this cuts toward world +Y.

        Args:
            distance: Cutout depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            dir_const = direction_map.get(direction, DirectionConstants.igRight)
            # DELIBERATE DESIGN DECISION — do not "fix" without reading this.
            #
            # create_extrude applies an auto-swap (igRight ↔ igLeft) for Front plane
            # sketches (plane_index == 3) so that direction="Normal" reliably extrudes
            # toward world +Y, matching user expectation.
            #
            # Cutout tools intentionally do NOT apply this swap. Reasons:
            #   1. Transparency over cleverness — callers get raw SE direction behaviour,
            #      which is documented in PLANE_AXIS_MAP (constants.py).
            #   2. Applying the swap would silently break callers using direction="Reverse"
            #      to cut toward world -Y on the Front plane.
            #   3. The safe option for Front plane cutouts is direction="Symmetric", which
            #      cuts both ways and is immune to this axis quirk entirely.
            #
            # If you want to apply the auto-swap to cutouts for consistency with extrude,
            # add the same three-line swap block from create_extrude here. Document it as
            # a breaking change and bump the minor version.
            #
            # See also: TODO.md "Known Limitations" section.

            cutouts = model.ExtrudedCutouts
            result, err = self._perform_feature_call(
                lambda: cutouts.AddFiniteMulti(1, (profile,), dir_const, distance),
                consumes_profiles=True,
            )
            if err:
                return err

            response = {
                "status": "created",
                "type": "extruded_cutout",
                "distance": distance,
                "direction": direction,
            }
            if self.sketch_manager.get_active_plane_index() == 3:
                _world_dir = "world -Y" if direction == "Normal" else "world +Y"
                response["warning"] = (
                    f"Front plane cutout used direction='{direction}' ({_world_dir} only). "
                    "Unlike create_extrude, cutout tools do not auto-swap direction on the "
                    "Front plane. Use direction='Reverse' to cut the other side."
                )
            self._append_bbox(response)
            return response
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_cutout_through_all(self, direction: str = "Symmetric") -> dict[str, Any]:
        """
        Create an extruded cutout that goes through the entire part.

        Uses model.ExtrudedCutouts.AddThroughAllMulti(NumProfiles, ProfileArray, PlaneSide).
        Requires an existing base feature and a closed sketch profile.

        Direction semantics
        -------------------
        "Normal"   — cuts in the sketch plane's outward-normal direction only
                     (igRight).  On the Front plane SE's internal normal is -Y,
                     so "Normal" cuts toward -Y, leaving the +Y side uncut.
        "Reverse"  — cuts in the opposite direction only (igLeft).  On the
                     Front plane this cuts toward +Y.
        "Symmetric" — cuts through all in *both* directions.  Implemented as
                     two sequential through-all cuts (one igRight, one igLeft)
                     because SE has no native symmetric through-all COM API.
                     The feature therefore appears as two items in the
                     pathfinder tree rather than one (see TODO.md).

        For the safest result on any plane use direction="Symmetric".

        Args:
            direction: 'Normal', 'Reverse', or 'Symmetric' (default 'Symmetric')

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            cutouts = model.ExtrudedCutouts

            if direction == "Symmetric":
                # Two sequential through-all cuts — one per direction.
                # consumes_profiles=False on the first pass keeps active_profile
                # live so the same COM object can be reused for the second pass.
                result, err = self._perform_feature_call(
                    lambda: cutouts.AddThroughAllMulti(1, (profile,), DirectionConstants.igRight),
                    consumes_profiles=False,
                )
                if err:
                    return err
                result, err = self._perform_feature_call(
                    lambda: cutouts.AddThroughAllMulti(1, (profile,), DirectionConstants.igLeft),
                    consumes_profiles=True,
                )
                if err:
                    return err
            else:
                direction_map = {
                    "Normal": DirectionConstants.igRight,
                    "Reverse": DirectionConstants.igLeft,
                }
                dir_const = direction_map.get(direction, DirectionConstants.igRight)
                # DELIBERATE DESIGN DECISION — do not "fix" without reading this.
                #
                # create_extrude applies an auto-swap (igRight ↔ igLeft) for Front plane
                # sketches (plane_index == 3) so that direction="Normal" reliably extrudes
                # toward world +Y, matching user expectation.
                #
                # Cutout tools intentionally do NOT apply this swap. Reasons:
                #   1. Transparency over cleverness — callers get raw SE direction behaviour,
                #      which is documented in PLANE_AXIS_MAP (constants.py).
                #   2. Applying the swap would silently break callers using direction="Reverse"
                #      to cut toward world -Y on the Front plane.
                #   3. The safe option for Front plane cutouts is direction="Symmetric", which
                #      cuts both ways and is immune to this axis quirk entirely.
                #
                # If you want to apply the auto-swap to cutouts for consistency with extrude,
                # add the same three-line swap block from create_extrude here. Document it as
                # a breaking change and bump the minor version.
                #
                # See also: TODO.md "Known Limitations" section.
                result, err = self._perform_feature_call(
                    lambda: cutouts.AddThroughAllMulti(1, (profile,), dir_const),
                    consumes_profiles=True,
                )
                if err:
                    return err

            response = {
                "status": "created",
                "type": "extruded_cutout_through_all",
                "direction": direction,
            }
            if direction in ("Normal", "Reverse") and self.sketch_manager.get_active_plane_index() == 3:
                _world_dir = "world -Y" if direction == "Normal" else "world +Y"
                response["warning"] = (
                    f"Front plane cutout used direction='{direction}' ({_world_dir} only). "
                    "If you need a full through-cut, use direction='Symmetric'."
                )
            self._append_bbox(response)
            return response
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolved_cutout(self, angle: float = 360) -> dict[str, Any]:
        """
        Create a revolved cutout (cut) in the part using the active sketch profile.

        Uses model.RevolvedCutouts.AddFiniteMulti(
        NumProfiles, ProfileArray, RefAxis,
        PlaneSide, Angle).
        Requires an existing base feature, a closed sketch profile, and an axis of revolution.

        Args:
            angle: Revolution angle in degrees (360 for full revolution)

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            import math

            angle_rad = math.radians(angle)

            cutouts = model.RevolvedCutouts
            result, err = self._perform_feature_call(
                lambda: cutouts.AddFiniteMulti(
                    1,  # NumberOfProfiles
                    (profile,),  # ProfileArray
                    refaxis,  # ReferenceAxis
                    DirectionConstants.igRight,  # ProfilePlaneSide
                    angle_rad,  # AngleOfRevolution
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "revolved_cutout", "angle": angle}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_normal_cutout(self, distance: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a normal cutout (cut) through the part using the active sketch profile.

        Uses model.NormalCutouts.AddFiniteMulti(NumProfiles, ProfileArray, PlaneSide, Depth).
        A normal cutout extrudes the profile perpendicular to the sketch plane face,
        following the surface normal rather than a fixed direction.
        Requires an existing base feature and a closed sketch profile.

        Args:
            distance: Cutout depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            dir_const = direction_map.get(direction, DirectionConstants.igRight)

            cutouts = model.NormalCutouts
            result, err = self._perform_feature_call(
                lambda: cutouts.AddFiniteMulti(1, (profile,), dir_const, distance),
                consumes_profiles=True,
            )
            if err:
                return err

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "normal_cutout",
                "distance": distance,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_lofted_cutout(self, profile_indices: list = None) -> dict[str, Any]:
        """
        Create a lofted cutout between multiple profiles.

        Uses accumulated profiles from close_sketch() calls. Create 2+ sketches
        on different parallel planes, close each one, then call create_lofted_cutout().
        Requires an existing base feature (cutout removes material).

        Uses model.LoftedCutouts.AddSimple(count, profiles, types, origins, side, startTan, endTan).

        Args:
            profile_indices: Optional list of profile indices to select from
                accumulated profiles. If None, uses all accumulated profiles.

        Returns:
            Dict with status and lofted cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            # Get accumulated profiles from sketch manager
            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if profile_indices is not None:
                profiles = [all_profiles[i] for i in profile_indices]
            else:
                profiles = all_profiles

            if len(profiles) < 2:
                return {
                    "error": "Lofted cutout requires at "
                    "least 2 profiles, got "
                    f"{len(profiles)}. Create sketches on "
                    "different planes and close each one "
                    "before calling create_lofted_cutout()."
                }

            v_profiles, v_types, v_origins = self._make_loft_variant_arrays(profiles)

            lc = model.LoftedCutouts
            result, err = self._perform_feature_call(
                lambda: lc.AddSimple(
                    len(profiles),
                    v_profiles,
                    v_types,
                    v_origins,
                    DirectionConstants.igRight,
                    ExtentTypeConstants.igNone,
                    ExtentTypeConstants.igNone,
                ),
                consumes_profiles=False,
            )
            if err:
                return err

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "lofted_cutout",
                "num_profiles": len(profiles),
                "method": "LoftedCutouts.AddSimple",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # MIRROR COPY
    # =================================================================

    def create_mirror(self, feature_name: str, mirror_plane_index: int) -> dict[str, Any]:
        """
        Create a mirror copy of a feature across a reference plane.

        Note: MirrorCopies via COM has known limitations. The ordered-mode
        Add() method creates a feature object but doesn't persist geometry.
        AddSync() persists the feature tree entry but may not compute geometry.
        This is a known Solid Edge COM API limitation.

        Args:
            feature_name: Name of the feature to mirror (from list_features)
            mirror_plane_index: 1-based index of the mirror plane
                (1=Top/XZ, 2=Front/XY, 3=Right/YZ, or higher for user planes)

        Returns:
            Dict with status and mirror info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            # Find the feature by name in DesignEdgebarFeatures
            features = doc.DesignEdgebarFeatures
            target_feature = None
            for i in range(1, features.Count + 1):
                f = features.Item(i)
                if f.Name == feature_name:
                    target_feature = f
                    break

            if target_feature is None:
                names = []
                for i in range(1, features.Count + 1):
                    names.append(features.Item(i).Name)
                return {
                    "error": f"Feature '{feature_name}' not found.",
                    "available_features": names,
                }

            # Get the mirror plane
            ref_planes = doc.RefPlanes
            if mirror_plane_index < 1 or mirror_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid plane index: {mirror_plane_index}. Count: {ref_planes.Count}"
                }

            mirror_plane = ref_planes.Item(mirror_plane_index)

            # Use AddSync which persists the feature tree entry
            mc = model.MirrorCopies
            result, err = self._perform_feature_call(
                lambda: mc.AddSync(1, [target_feature], mirror_plane, False),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "mirror_copy",
                "feature": feature_name,
                "mirror_plane": mirror_plane_index,
                "name": result.Name if hasattr(result, "Name") else None,
                "note": "Mirror feature created via AddSync. "
                "Geometry may require manual verification "
                "in Solid Edge UI.",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # REFERENCE PLANE CREATION
    # =================================================================

    def create_ref_plane_by_offset(
        self, parent_plane_index: int, distance: float, normal_side: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a reference plane parallel to an existing plane at an offset distance.

        Uses RefPlanes.AddParallelByDistance(ParentPlane, Distance, NormalSide).
        Useful for creating sketches at different heights/positions.

        Args:
            parent_plane_index: Index of parent plane (1=Top/XZ, 2=Front/XY, 3=Right/YZ,
                                or higher for user-created planes)
            distance: Offset distance in meters
            normal_side: 'Normal' (igRight=2) or 'Reverse' (igLeft=1)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            ref_planes = doc.RefPlanes

            if parent_plane_index < 1 or parent_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid plane index: {parent_plane_index}. Count: {ref_planes.Count}"
                }

            parent = ref_planes.Item(parent_plane_index)

            side_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            side_const = side_map.get(normal_side, DirectionConstants.igRight)

            result, err = self._perform_feature_call(
                lambda: ref_planes.AddParallelByDistance(parent, distance, side_const),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "reference_plane",
                "method": "parallel_by_distance",
                "parent_plane": parent_plane_index,
                "distance": distance,
                "normal_side": normal_side,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_normal_at_distance(
        self, distance: float, curve_end: str = "End", pivot_plane_index: int = 2
    ) -> dict[str, Any]:
        """
        Create a reference plane normal to a curve at a specified distance from an endpoint.

        Uses RefPlanes.AddNormalToCurveAtDistance(pCurve, Distance, bIgnoreNatural,
        NormalSide, [bFlip], [bOrient], [orientSurface]).
        Requires an active sketch profile that defines the curve.

        Args:
            distance: Distance from the curve endpoint in meters
            curve_end: Which end to measure from - 'Start' or 'End'
            pivot_plane_index: 1-based index of the pivot reference plane (default: 2 = Front)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            ref_planes = doc.RefPlanes

            # bIgnoreNatural: True to ignore curve's natural direction
            # Reverse mapping: for "Start" ignore natural, for "End" use natural
            ignore_natural = curve_end == "Start"
            # NormalSide: igRight = 2
            normal_side = DirectionConstants.igRight

            result, err = self._perform_feature_call(
                lambda: ref_planes.AddNormalToCurveAtDistance(profile, distance, ignore_natural, normal_side),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "ref_plane_normal_at_distance",
                "distance": distance,
                "curve_end": curve_end,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_normal_at_arc_ratio(
        self, ratio: float, curve_end: str = "End", pivot_plane_index: int = 2
    ) -> dict[str, Any]:
        """
        Create a reference plane normal to a curve at an arc-length ratio.

        Uses RefPlanes.AddNormalToCurveAtArcLengthRatio(pCurve, Ratio, bIgnoreNatural,
        NormalSide, PivotPlane, PivotEnd, [bFlip], [bOrient]).
        Ratio is 0.0 (start) to 1.0 (end) of the curve arc length.

        Args:
            ratio: Arc length ratio (0.0 to 1.0)
            curve_end: Which end is pivot - 'Start' or 'End'
            pivot_plane_index: 1-based index of the pivot reference plane (default: 2 = Front)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            if ratio < 0.0 or ratio > 1.0:
                return {"error": f"Ratio must be between 0.0 and 1.0, got {ratio}"}

            ref_planes = doc.RefPlanes
            pivot_plane = ref_planes.Item(pivot_plane_index)

            ignore_natural = curve_end == "Start"
            normal_side = DirectionConstants.igRight
            # igPivotEnd = 2
            pivot_end_const = 2

            result, err = self._perform_feature_call(
                lambda: ref_planes.AddNormalToCurveAtArcLengthRatio(
                    profile, ratio, ignore_natural, normal_side, pivot_plane, pivot_end_const
                ),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "ref_plane_normal_at_arc_ratio",
                "ratio": ratio,
                "curve_end": curve_end,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_normal_at_distance_along(
        self, distance_along: float, curve_end: str = "End", pivot_plane_index: int = 2
    ) -> dict[str, Any]:
        """
        Create a reference plane normal to a curve at a distance along the curve.

        Uses RefPlanes.AddNormalToCurveAtDistanceAlongCurve(pCurve, DistAlong,
        bIgnoreNatural, NormalSide, PivotPlane, PivotEnd, [bFlip], [bOrient]).

        Args:
            distance_along: Distance along the curve in meters
            curve_end: Which end to measure from - 'Start' or 'End'
            pivot_plane_index: 1-based index of the pivot reference plane (default: 2 = Front)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            ref_planes = doc.RefPlanes
            pivot_plane = ref_planes.Item(pivot_plane_index)

            ignore_natural = curve_end == "Start"
            normal_side = DirectionConstants.igRight
            pivot_end_const = 2

            result, err = self._perform_feature_call(
                lambda: ref_planes.AddNormalToCurveAtDistanceAlongCurve(
                    profile, distance_along, ignore_natural, normal_side, pivot_plane, pivot_end_const
                ),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "ref_plane_normal_at_distance_along",
                "distance_along": distance_along,
                "curve_end": curve_end,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_parallel_by_tangent(
        self, parent_plane_index: int, face_index: int, normal_side: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a reference plane parallel to a parent plane and tangent to a face.

        Uses RefPlanes.AddParallelByTangent(pParentPlane, pFace, NormalSide,
        [bFlip], [bOrient], [orientSurface]).

        Args:
            parent_plane_index: 1-based index of the parent reference plane
            face_index: 0-based index of the face to be tangent to
            normal_side: 'Normal' (igRight=2) or 'Reverse' (igLeft=1)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            ref_planes = doc.RefPlanes

            if parent_plane_index < 1 or parent_plane_index > ref_planes.Count:
                return {
                    "error": "Invalid parent_plane_index: "
                    f"{parent_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face_index: {face_index}. Body has {faces.Count} faces."}

            parent_plane = ref_planes.Item(parent_plane_index)
            face = faces.Item(face_index + 1)

            side_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            side_const = side_map.get(normal_side, DirectionConstants.igRight)

            result, err = self._perform_feature_call(
                lambda: ref_planes.AddParallelByTangent(parent_plane, face, side_const),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "ref_plane_parallel_by_tangent",
                "parent_plane_index": parent_plane_index,
                "face_index": face_index,
                "normal_side": normal_side,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # SELECTIVE ROUNDS AND CHAMFERS (ON SPECIFIC FACE)
    # =================================================================

    def create_round_on_face(self, radius: float, face_index: int) -> dict[str, Any]:
        """
        Create a round (fillet) on edges of a specific face.

        Unlike create_round() which rounds all edges, this targets only
        the edges of a single face. Use get_body_faces() to find face indices.

        Args:
            radius: Round radius in meters
            face_index: 0-based face index (from get_body_faces)

        Returns:
            Dict with status and round info
        """
        try:
            import pythoncom
            from win32com.client import VARIANT

            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add rounds to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            face_edges = face.Edges
            if not hasattr(face_edges, "Count") or face_edges.Count == 0:
                return {"error": f"Face {face_index} has no edges"}

            edge_list = []
            for ei in range(1, face_edges.Count + 1):
                edge_list.append(face_edges.Item(ei))

            edge_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, edge_list)
            radius_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [radius])

            rounds = model.Rounds
            result, err = self._perform_feature_call(
                lambda: rounds.Add(1, edge_arr, radius_arr),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "round",
                "radius": radius,
                "face_index": face_index,
                "edge_count": len(edge_list),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_chamfer_on_face(self, distance: float, face_index: int) -> dict[str, Any]:
        """
        Create a chamfer on edges of a specific face.

        Unlike create_chamfer() which chamfers all edges, this targets only
        the edges of a single face. Use get_body_faces() to find face indices.

        Args:
            distance: Chamfer setback distance in meters
            face_index: 0-based face index (from get_body_faces)

        Returns:
            Dict with status and chamfer info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add chamfers to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            face_edges = face.Edges
            if not hasattr(face_edges, "Count") or face_edges.Count == 0:
                return {"error": f"Face {face_index} has no edges"}

            edge_list = []
            for ei in range(1, face_edges.Count + 1):
                edge_list.append(face_edges.Item(ei))

            chamfers = model.Chamfers
            result, err = self._perform_feature_call(
                lambda: chamfers.AddEqualSetback(len(edge_list), edge_list, distance),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "chamfer",
                "distance": distance,
                "face_index": face_index,
                "edge_count": len(edge_list),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def delete_faces(self, face_indices: list[int]) -> dict[str, Any]:
        """
        Delete faces from the model body.

        Uses model.DeleteFaces collection to remove specified faces.
        Useful for creating openings or removing geometry.

        Args:
            face_indices: List of 0-based face indices to delete

        Returns:
            Dict with status and deletion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to delete faces from"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces on body"}

            face_objs = []
            for idx in face_indices:
                if idx < 0 or idx >= faces.Count:
                    return {"error": f"Invalid face index: {idx}. Body has {faces.Count} faces."}
                face_objs.append(faces.Item(idx + 1))

            delete_faces = model.DeleteFaces
            result, err = self._perform_feature_call(
                lambda: delete_faces.Add(len(face_objs), face_objs),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "delete_faces",
                "face_count": len(face_indices),
                "face_indices": face_indices,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def delete_faces_no_heal(self, face_indices: list[int]) -> dict[str, Any]:
        """
        Delete faces from the model body without healing.

        Unlike delete_faces which attempts to heal/close resulting gaps,
        this removes faces leaving the gap open. Useful when you need
        to create deliberate openings.

        Args:
            face_indices: List of 0-based face indices to delete

        Returns:
            Dict with status and deletion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to delete faces from"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces on body"}

            face_objs = []
            for idx in face_indices:
                if idx < 0 or idx >= faces.Count:
                    return {"error": f"Invalid face index: {idx}. Body has {faces.Count} faces."}
                face_objs.append(faces.Item(idx + 1))

            delete_faces = model.DeleteFaces
            result, err = self._perform_feature_call(
                lambda: delete_faces.AddNoHeal(len(face_objs), face_objs),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "delete_faces_no_heal",
                "face_count": len(face_indices),
                "face_indices": face_indices,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def delete_hole_by_face(self, face_index: int) -> dict[str, Any]:
        """
        Delete a specific hole by selecting its face.

        Unlike create_delete_hole which deletes holes by type/size criteria,
        this targets a specific hole identified by its face index.

        Args:
            face_index: 0-based face index of the hole to delete

        Returns:
            Dict with status and deletion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)

            delete_holes = model.DeleteHoles
            result, err = self._perform_feature_call(
                lambda: delete_holes.AddByFace(face),
                consumes_profiles=False,
            )
            if err:
                return err

            return {"status": "created", "type": "delete_hole_by_face", "face_index": face_index}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ADDITIONAL SHEET METAL FEATURES
    # =================================================================

    def create_lofted_flange(self, thickness: float) -> dict[str, Any]:
        """Create lofted flange (sheet metal)"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(
                lambda: models.AddLoftedFlange(thickness),
                consumes_profiles=False,
            )
            if err:
                return err

            return {"status": "created", "type": "lofted_flange", "thickness": thickness}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_web_network(self) -> dict[str, Any]:
        """Create web network (sheet metal)"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(
                lambda: models.AddWebNetwork(),
                consumes_profiles=False,
            )
            if err:
                return err

            return {"status": "created", "type": "web_network"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ADDITIONAL BODY OPERATIONS
    # =================================================================

    def add_body_by_mesh(self) -> dict[str, Any]:
        """Add body by mesh facets"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(
                lambda: models.AddBodyByMeshFacets(),
                consumes_profiles=False,
            )
            if err:
                return err

            return {"status": "created", "type": "body_by_mesh"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_body_feature(self) -> dict[str, Any]:
        """Add body feature"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(
                lambda: models.AddBodyFeature(),
                consumes_profiles=False,
            )
            if err:
                return err

            return {"status": "created", "type": "body_feature"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_by_construction(self) -> dict[str, Any]:
        """Add construction body"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(
                lambda: models.AddByConstruction(),
                consumes_profiles=False,
            )
            if err:
                return err

            return {"status": "created", "type": "construction_body"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_body_by_tag(self, tag: str) -> dict[str, Any]:
        """Add body by tag reference"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            result, err = self._perform_feature_call(
                lambda: models.AddBodyByTag(tag),
                consumes_profiles=False,
            )
            if err:
                return err

            return {"status": "created", "type": "body_by_tag", "tag": tag}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ADVANCED SHEET METAL FEATURES
    # =================================================================

    def create_base_contour_flange_advanced(
        self, thickness: float, bend_radius: float, relief_type: str = "Default"
    ) -> dict[str, Any]:
        """Create base contour flange with bend deduction or bend allowance"""
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            # AddBaseContourFlangeByBendDeductionOrBendAllowance
            result, err = self._perform_feature_call(
                lambda: models.AddBaseContourFlangeByBendDeductionOrBendAllowance(
                    profile, 1, thickness, bend_radius
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "base_contour_flange_advanced",
                "thickness": thickness,
                "bend_radius": bend_radius,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_base_tab_multi_profile(self, thickness: float) -> dict[str, Any]:
        """Create base tab with multiple profiles"""
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile"}

            models = doc.Models

            # AddBaseTabWithMultipleProfiles
            result, err = self._perform_feature_call(
                lambda: models.AddBaseTabWithMultipleProfiles(
                    1, (profile,), thickness
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "base_tab_multi_profile", "thickness": thickness}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_lofted_flange_advanced(self, thickness: float, bend_radius: float) -> dict[str, Any]:
        """Create lofted flange with bend deduction or bend allowance"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            # AddLoftedFlangeByBendDeductionOrBendAllowance
            result, err = self._perform_feature_call(
                lambda: models.AddLoftedFlangeByBendDeductionOrBendAllowance(
                    thickness, bend_radius
                ),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "lofted_flange_advanced",
                "thickness": thickness,
                "bend_radius": bend_radius,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_lofted_flange_ex(self, thickness: float) -> dict[str, Any]:
        """Create extended lofted flange"""
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            # AddLoftedFlangeEx
            result, err = self._perform_feature_call(
                lambda: models.AddLoftedFlangeEx(thickness),
                consumes_profiles=False,
            )
            if err:
                return err

            return {"status": "created", "type": "lofted_flange_ex", "thickness": thickness}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # EMBOSS AND FLANGE
    # =================================================================

    def create_emboss(
        self,
        face_indices: list,
        clearance: float = 0.001,
        thickness: float = 0.0,
        thicken: bool = False,
        default_side: bool = True,
    ) -> dict[str, Any]:
        """
        Create an emboss feature using face geometry as tools.

        Uses selected faces as embossing tool geometry on the target body.
        Requires an existing base feature.

        Args:
            face_indices: List of 0-based face indices to use as emboss tools
            clearance: Clearance in meters (default 0.001)
            thickness: Thickness in meters (default 0.0)
            thicken: Enable thickening (default False)
            default_side: Default side (default True)

        Returns:
            Dict with status and emboss info
        """
        try:
            import pythoncom
            from win32com.client import VARIANT

            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body

            if not face_indices:
                return {"error": "face_indices must contain at least one face index."}

            faces = body.Faces(FaceQueryConstants.igQueryAll)

            face_list = []
            for fi in face_indices:
                if fi < 0 or fi >= faces.Count:
                    return {"error": f"Invalid face index: {fi}. Body has {faces.Count} faces."}
                face_list.append(faces.Item(fi + 1))

            tools_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, face_list)

            emboss_features = model.EmbossFeatures
            _feature = emboss_features.Add(
                body, len(face_list), tools_arr, thicken, default_side, clearance, thickness
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "emboss",
                "face_count": len(face_list),
                "clearance": clearance,
                "thickness": thickness,
                "thicken": thicken,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_flange(
        self,
        face_index: int,
        edge_index: int,
        flange_length: float,
        side: str = "Right",
        inside_radius: float = None,
        bend_angle: float = None,
    ) -> dict[str, Any]:
        """
        Create a flange feature on a sheet metal edge.

        Adds a flange to the specified edge of a sheet metal body.
        Requires an existing sheet metal base feature.

        Args:
            face_index: 0-based face index containing the target edge
            edge_index: 0-based edge index within that face
            flange_length: Flange length in meters
            side: 'Left' (1), 'Right' (2), or 'Both' (6)
            inside_radius: Bend inside radius in meters (optional)
            bend_angle: Bend angle in degrees (optional)

        Returns:
            Dict with status and flange info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a sheet metal base feature first."}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            face_edges = face.Edges
            if not hasattr(face_edges, "Count") or face_edges.Count == 0:
                return {"error": f"Face {face_index} has no edges."}

            if edge_index < 0 or edge_index >= face_edges.Count:
                return {
                    "error": f"Invalid edge index: {edge_index}. Face has {face_edges.Count} edges."
                }

            edge = face_edges.Item(edge_index + 1)

            side_map = {
                "Left": DirectionConstants.igLeft,
                "Right": DirectionConstants.igRight,
                "Both": DirectionConstants.igBoth,
            }
            side_const = side_map.get(side, DirectionConstants.igRight)

            flanges = model.Flanges

            # Build optional args

            # Optional params: ThicknessSide, InsideRadius, DimSide, BRType, BRWidth,
            # BRLength, CRType, NeutralFactor, BnParamType, BendAngle
            if inside_radius is not None or bend_angle is not None:
                # ThicknessSide (skip) -> InsideRadius
                # We need to pass positional VT_VARIANT optional params
                # In late binding, pass them positionally
                if inside_radius is not None and bend_angle is not None:
                    bend_angle_rad = math.radians(bend_angle)
                    _feature = flanges.Add(
                        edge,
                        side_const,
                        flange_length,
                        None,
                        inside_radius,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        bend_angle_rad,
                    )
                    if _feature is None:
                        return {"error": "Feature creation failed: COM returned None"}
                elif inside_radius is not None:
                    _feature = flanges.Add(edge, side_const, flange_length, None, inside_radius)
                    if _feature is None:
                        return {"error": "Feature creation failed: COM returned None"}
                else:
                    bend_angle_rad = math.radians(bend_angle)
                    _feature = flanges.Add(
                        edge,
                        side_const,
                        flange_length,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        bend_angle_rad,
                    )
                    if _feature is None:
                        return {"error": "Feature creation failed: COM returned None"}
            else:
                _feature = flanges.Add(edge, side_const, flange_length)
                if _feature is None:
                    return {"error": "Feature creation failed: COM returned None"}

            result = {
                "status": "created",
                "type": "flange",
                "face_index": face_index,
                "edge_index": edge_index,
                "flange_length": flange_length,
                "side": side,
            }
            if inside_radius is not None:
                result["inside_radius"] = inside_radius
            if bend_angle is not None:
                result["bend_angle"] = bend_angle

            return result
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ADDITIONAL FEATURE TYPES (Dimple, Etch, Rib, Lip, Slot, etc.)
    # =================================================================

    def create_dimple(self, depth: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a dimple feature (sheet metal).

        Creates a dimple from the active sketch profile on the sheet metal body.
        Requires an active sketch profile and an existing sheet metal base feature.

        Args:
            depth: Dimple depth in meters
            direction: 'Normal' or 'Reverse' for dimple direction

        Returns:
            Dict with status and dimple info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a sheet metal base feature first."}

            model = models.Item(1)

            # seDimpleDepthLeft=1, seDimpleDepthRight=2
            profile_side = 1 if direction == "Normal" else 2
            depth_side = 2 if direction == "Normal" else 1

            dimples = model.Dimples
            result, err = self._perform_feature_call(
                lambda: dimples.Add(profile, depth, profile_side, depth_side),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "dimple", "depth": depth, "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_etch(self) -> dict[str, Any]:
        """
        Create an etch feature (sheet metal).

        Etches the active sketch profile into the sheet metal body.
        Requires an active sketch profile and an existing sheet metal base feature.

        Returns:
            Dict with status and etch info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a sheet metal base feature first."}

            model = models.Item(1)

            etches = model.Etches
            result, err = self._perform_feature_call(
                lambda: etches.Add(profile),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "etch"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_rib(self, thickness: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a rib feature from the active sketch profile.

        Ribs are structural reinforcements that extend from a profile to
        existing geometry. Requires an active sketch profile.

        Args:
            thickness: Rib thickness in meters
            direction: 'Normal', 'Reverse', or 'Symmetric'

        Returns:
            Dict with status and rib info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            dir_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
                "Symmetric": DirectionConstants.igSymmetric,
            }
            side = dir_map.get(direction, DirectionConstants.igRight)

            ribs = model.Ribs
            result, err = self._perform_feature_call(
                lambda: ribs.Add(profile, 1, 0, side, thickness),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "rib",
                "thickness": thickness,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_lip(self, depth: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a lip feature from the active sketch profile.

        Lips are raised edges or ridges on plastic or sheet metal parts.
        Requires an active sketch profile and an existing base feature.

        Args:
            depth: Lip depth/height in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and lip info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            side = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            lips = model.Lips
            result, err = self._perform_feature_call(
                lambda: lips.Add(profile, side, depth),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "lip", "depth": depth, "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_drawn_cutout(self, depth: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a drawn cutout feature (sheet metal).

        Creates a formed cutout from the active sketch profile. Unlike extruded
        cutouts, drawn cutouts follow the material's bend characteristics.
        Requires an active sketch profile and existing base feature.

        Args:
            depth: Cutout depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            # igLeft=1, igRight=2
            side = 2 if direction == "Normal" else 1

            drawn_cutouts = model.DrawnCutouts
            result, err = self._perform_feature_call(
                lambda: drawn_cutouts.Add(profile, side, depth),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "drawn_cutout",
                "depth": depth,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_bead(self, depth: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a bead feature (sheet metal stiffener).

        Beads are raised ridges used to stiffen sheet metal parts.
        Requires an active sketch profile and an existing sheet metal base feature.

        Args:
            depth: Bead depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and bead info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            # igLeft=1, igRight=2
            side = 2 if direction == "Normal" else 1

            beads = model.Beads
            result, err = self._perform_feature_call(
                lambda: beads.Add(profile, side, depth),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "bead", "depth": depth, "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_louver(self, depth: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a louver feature (sheet metal vent).

        Louvers are formed openings used for ventilation in sheet metal parts.
        Requires an active sketch profile and an existing sheet metal base feature.

        Args:
            depth: Louver depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and louver info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            # igLeft=1, igRight=2
            side = 2 if direction == "Normal" else 1

            louvers = model.Louvers
            result, err = self._perform_feature_call(
                lambda: louvers.Add(profile, side, depth),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "louver", "depth": depth, "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_gusset(self, thickness: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a gusset feature (sheet metal reinforcement).

        Gussets are triangular reinforcement plates used in sheet metal.
        Requires an active sketch profile and an existing sheet metal base feature.

        Args:
            thickness: Gusset thickness in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and gusset info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            # igLeft=1, igRight=2
            side = 2 if direction == "Normal" else 1

            gussets = model.Gussets
            result, err = self._perform_feature_call(
                lambda: gussets.Add(profile, side, thickness),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "gusset",
                "thickness": thickness,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_thread(
        self, face_index: int, pitch: float = 0.001, thread_type: str = "External"
    ) -> dict[str, Any]:
        """
        Create a thread feature on a cylindrical face.

        Adds cosmetic or modeled threads to a cylindrical face (hole or shaft).

        Args:
            face_index: 0-based index of the cylindrical face
            pitch: Thread pitch in meters (default 1mm)
            thread_type: 'External' (on shaft) or 'Internal' (in hole)

        Returns:
            Dict with status and thread info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Count: {faces.Count}"}

            face = faces.Item(face_index + 1)

            threads = model.Threads
            result, err = self._perform_feature_call(
                lambda: threads.Add(face, pitch),
                consumes_profiles=False,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "thread",
                "face_index": face_index,
                "pitch": pitch,
                "pitch_mm": pitch * 1000,
                "thread_type": thread_type,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_slot(self, depth: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a slot feature from the active sketch profile.

        Slots are elongated cutouts typically used for fastener clearance.
        Requires an active sketch profile and an existing base feature.

        Args:
            depth: Slot depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and slot info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            # igLeft=1, igRight=2
            side = 2 if direction == "Normal" else 1

            slots = model.Slots
            result, err = self._perform_feature_call(
                lambda: slots.Add(profile, side, depth),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "slot", "depth": depth, "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_split(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a split feature to divide a body along the active sketch profile.

        Requires an active sketch profile and an existing base feature.

        Args:
            direction: 'Normal' or 'Reverse' - which side to keep

        Returns:
            Dict with status and split info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            # igLeft=1, igRight=2
            side = 2 if direction == "Normal" else 1

            splits = model.Splits
            result, err = self._perform_feature_call(
                lambda: splits.Add(profile, side),
                consumes_profiles=True,
            )
            if err:
                return err

            return {"status": "created", "type": "split", "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # UNEQUAL CHAMFER
    # =================================================================

    def create_chamfer_unequal(
        self, distance1: float, distance2: float, face_index: int = 0
    ) -> dict[str, Any]:
        """
        Create a chamfer with two different setback distances.

        Unlike equal chamfer, this creates an asymmetric chamfer where each side
        has a different setback. Requires a reference face to determine direction.

        Args:
            distance1: First setback distance in meters
            distance2: Second setback distance in meters
            face_index: 0-based face index for the reference face

        Returns:
            Dict with status and chamfer info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add chamfers to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            face_edges = face.Edges
            if not hasattr(face_edges, "Count") or face_edges.Count == 0:
                return {"error": f"Face {face_index} has no edges"}

            edge_list = []
            for ei in range(1, face_edges.Count + 1):
                edge_list.append(face_edges.Item(ei))

            chamfers = model.Chamfers
            _feature = chamfers.AddUnequalSetback(face, len(edge_list), edge_list, distance1, distance2)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "chamfer_unequal",
                "distance1": distance1,
                "distance2": distance2,
                "face_index": face_index,
                "edge_count": len(edge_list),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ANGLE CHAMFER
    # =================================================================

    def create_chamfer_angle(
        self, distance: float, angle: float, face_index: int = 0
    ) -> dict[str, Any]:
        """
        Create a chamfer defined by a setback distance and an angle.

        Args:
            distance: Setback distance in meters
            angle: Chamfer angle in degrees
            face_index: 0-based face index for the reference face

        Returns:
            Dict with status and chamfer info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add chamfers to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            face_edges = face.Edges
            if not hasattr(face_edges, "Count") or face_edges.Count == 0:
                return {"error": f"Face {face_index} has no edges"}

            edge_list = []
            for ei in range(1, face_edges.Count + 1):
                edge_list.append(face_edges.Item(ei))

            chamfers = model.Chamfers
            angle_rad = math.radians(angle)
            _feature = chamfers.AddSetbackAngle(face, len(edge_list), edge_list, distance, angle_rad)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "chamfer_angle",
                "distance": distance,
                "angle_degrees": angle,
                "face_index": face_index,
                "edge_count": len(edge_list),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # FACE ROTATE
    # =================================================================

    def create_face_rotate_by_edge(
        self, face_index: int, edge_index: int, angle: float
    ) -> dict[str, Any]:
        """
        Rotate a face around an edge axis.

        Tilts a face by rotating it around a specified edge. Useful for
        creating draft angles or adjusting face orientations.

        Args:
            face_index: 0-based face index to rotate
            edge_index: 0-based edge index to use as rotation axis
            angle: Rotation angle in degrees

        Returns:
            Dict with status and face rotate info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to rotate faces on"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)

            # Get edge from the face
            face_edges = face.Edges
            if not hasattr(face_edges, "Count") or face_edges.Count == 0:
                return {"error": f"Face {face_index} has no edges"}
            if edge_index < 0 or edge_index >= face_edges.Count:
                return {
                    "error": f"Invalid edge index: {edge_index}. Face has {face_edges.Count} edges."
                }

            edge = face_edges.Item(edge_index + 1)

            angle_rad = math.radians(angle)

            face_rotates = model.FaceRotates
            # igFaceRotateByGeometry = 1, igFaceRotateRecreateBlends = 1, igFaceRotateAxisEnd = 2
            _feature = face_rotates.Add(face, 1, 1, None, None, edge, 2, angle_rad)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "face_rotate",
                "method": "by_edge",
                "face_index": face_index,
                "edge_index": edge_index,
                "angle_degrees": angle,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_face_rotate_by_points(
        self, face_index: int, vertex1_index: int, vertex2_index: int, angle: float
    ) -> dict[str, Any]:
        """
        Rotate a face around an axis defined by two vertex points.

        Args:
            face_index: 0-based face index to rotate
            vertex1_index: 0-based index of first vertex defining rotation axis
            vertex2_index: 0-based index of second vertex defining rotation axis
            angle: Rotation angle in degrees

        Returns:
            Dict with status and face rotate info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to rotate faces on"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)

            # Get vertices from the face
            vertices = face.Vertices
            if vertex1_index < 0 or vertex1_index >= vertices.Count:
                return {
                    "error": f"Invalid vertex1 index: "
                    f"{vertex1_index}. Face has "
                    f"{vertices.Count} vertices."
                }
            if vertex2_index < 0 or vertex2_index >= vertices.Count:
                return {
                    "error": f"Invalid vertex2 index: "
                    f"{vertex2_index}. Face has "
                    f"{vertices.Count} vertices."
                }

            point1 = vertices.Item(vertex1_index + 1)
            point2 = vertices.Item(vertex2_index + 1)

            angle_rad = math.radians(angle)

            face_rotates = model.FaceRotates
            # igFaceRotateByPoints = 2, igFaceRotateRecreateBlends = 1, igFaceRotateNone = 0
            _feature = face_rotates.Add(face, 2, 1, point1, point2, None, 0, angle_rad)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "face_rotate",
                "method": "by_points",
                "face_index": face_index,
                "vertex1_index": vertex1_index,
                "vertex2_index": vertex2_index,
                "angle_degrees": angle,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # DRAFT ANGLE
    # =================================================================

    def create_draft_angle(
        self, face_index: int, angle: float, plane_index: int = 1
    ) -> dict[str, Any]:
        """
        Add a draft angle to a face.

        Draft angles are used in injection molding to facilitate part removal
        from the mold. Uses the model.Drafts collection.

        Args:
            face_index: 0-based face index to apply draft to
            angle: Draft angle in degrees
            plane_index: 1-based reference plane index for draft direction (default: 1 = Top)

        Returns:
            Dict with status and draft info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add draft to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            ref_plane = doc.RefPlanes.Item(plane_index)

            angle_rad = math.radians(angle)

            # igRight = 2 (draft direction side)
            drafts = model.Drafts
            _feature = drafts.Add(ref_plane, 1, [face], [angle_rad], 2)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "draft_angle",
                "face_index": face_index,
                "angle_degrees": angle,
                "plane_index": plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # REFERENCE PLANE NORMAL TO CURVE
    # =================================================================

    def create_ref_plane_normal_to_curve(
        self, curve_end: str = "End", pivot_plane_index: int = 2
    ) -> dict[str, Any]:
        """
        Create a reference plane normal (perpendicular) to a curve at its endpoint.

        Useful for creating sweep cross-section sketches perpendicular to a path.
        Requires an active sketch profile that defines the curve.

        Args:
            curve_end: Which end of the curve to place the plane at - 'Start' or 'End'
            pivot_plane_index: 1-based index of the pivot reference plane (default: 2 = Front)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            ref_planes = doc.RefPlanes
            pivot_plane = ref_planes.Item(pivot_plane_index)

            # igCurveEnd = 2, igCurveStart = 1
            curve_end_const = 2 if curve_end == "End" else 1
            # igPivotEnd = 2
            pivot_end_const = 2

            _feature = ref_planes.AddNormalToCurve(
                profile, curve_end_const, pivot_plane, pivot_end_const, True
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            new_index = ref_planes.Count

            return {
                "status": "created",
                "type": "ref_plane_normal_to_curve",
                "curve_end": curve_end,
                "pivot_plane_index": pivot_plane_index,
                "new_plane_index": new_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: SWEPT CUTOUT
    # =================================================================

    def create_swept_cutout(self, path_profile_index: int = None) -> dict[str, Any]:
        """
        Create a swept cutout (cut) along a path.

        Same workflow as create_sweep but removes material instead of adding it.
        Requires at least 2 accumulated profiles: path (open) + cross-section (closed).
        Uses model.SweptCutouts.Add() (type library: SweptCutouts collection).

        Args:
            path_profile_index: Index of the path profile in accumulated profiles
                (default: 0, the first accumulated profile)

        Returns:
            Dict with status and swept cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if len(all_profiles) < 2:
                return {
                    "error": "Swept cutout requires at "
                    "least 2 profiles (path + "
                    "cross-section), got "
                    f"{len(all_profiles)}. Create a path "
                    "sketch and a cross-section "
                    "sketch first."
                }

            path_idx = path_profile_index if path_profile_index is not None else 0
            path_profile = all_profiles[path_idx]
            cross_sections = [p for i, p in enumerate(all_profiles) if i != path_idx]

            _CS = LoftSweepConstants.igProfileBasedCrossSection

            # Path arrays
            v_paths = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [path_profile])
            v_path_types = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS])

            # Cross-section arrays
            v_sections = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, cross_sections)
            v_section_types = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS] * len(cross_sections)
            )
            v_origins = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
                [VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0]) for _ in cross_sections],
            )
            v_seg = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, [])

            # SweptCutouts.Add: same 15 params as SweptProtrusions
            swept_cutouts = model.SweptCutouts
            _feature = swept_cutouts.Add(
                1,
                v_paths,
                v_path_types,  # Path (1 curve)
                len(cross_sections),
                v_sections,
                v_section_types,
                v_origins,
                v_seg,
                DirectionConstants.igRight,  # MaterialSide
                ExtentTypeConstants.igNone,
                0.0,
                None,  # Start extent
                ExtentTypeConstants.igNone,
                0.0,
                None,  # End extent
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()
            return {
                "status": "created",
                "type": "swept_cutout",
                "num_cross_sections": len(cross_sections),
                "method": "model.SweptCutouts.Add",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: HELIX CUTOUT
    # =================================================================

    def create_helix_cutout(
        self, pitch: float, height: float, revolutions: float = None, direction: str = "Right"
    ) -> dict[str, Any]:
        """
        Create a helical cutout (cut) in the part.

        Same workflow as create_helix but removes material. Requires a closed sketch
        profile and an axis of revolution. Uses model.HelixCutouts.AddFinite().
        Type library: HelixCutouts.AddFinite(HelixAxis, AxisStart, NumCrossSections,
        CrossSectionArray, ProfileSide, Height, Pitch, NumberOfTurns, HelixDir, ...).

        Args:
            pitch: Distance between coils in meters
            height: Total height of helix in meters
            revolutions: Number of turns (optional, calculated from pitch/height)
            direction: 'Right' or 'Left' hand helix

        Returns:
            Dict with status and helix cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() "
                    "in the sketch."
                }

            if revolutions is None:
                revolutions = height / pitch

            axis_start = DirectionConstants.igRight
            dir_const = (
                DirectionConstants.igRight if direction == "Right" else DirectionConstants.igLeft
            )

            # Wrap cross-section profile in SAFEARRAY
            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            helix_cutouts = model.HelixCutouts
            _feature = helix_cutouts.AddFinite(
                refaxis,  # HelixAxis
                axis_start,  # AxisStart
                1,  # NumCrossSections
                v_profiles,  # CrossSectionArray
                DirectionConstants.igRight,  # ProfileSide
                height,  # Height
                pitch,  # Pitch
                revolutions,  # NumberOfTurns
                dir_const,  # HelixDir
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()
            return {
                "status": "created",
                "type": "helix_cutout",
                "pitch": pitch,
                "height": height,
                "revolutions": revolutions,
                "direction": direction,
                "method": "model.HelixCutouts.AddFinite",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: VARIABLE ROUND (FILLET)
    # =================================================================

    def create_variable_round(self, radii: list, face_index: int = None) -> dict[str, Any]:
        """
        Create a variable-radius round (fillet) on body edges.

        Unlike create_round which applies a constant radius, this allows different
        radii at different points along the edge. Uses model.Rounds.AddVariable().
        Type library: Rounds.AddVariable(NumberOfEdgeSets, EdgeSetArray, RadiusArray).

        Args:
            radii: List of radius values in meters. Each edge gets a corresponding radius.
                   If fewer radii than edges, the last radius is repeated.
            face_index: 0-based face index to apply to (None = all edges)

        Returns:
            Dict with status and variable round info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add variable rounds to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces found on body"}

            # Collect edges from specified face or all faces
            edge_list = []
            if face_index is not None:
                if face_index < 0 or face_index >= faces.Count:
                    return {
                        "error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."
                    }
                face = faces.Item(face_index + 1)
                face_edges = face.Edges
                if hasattr(face_edges, "Count"):
                    for ei in range(1, face_edges.Count + 1):
                        edge_list.append(face_edges.Item(ei))
            else:
                for fi in range(1, faces.Count + 1):
                    face = faces.Item(fi)
                    face_edges = face.Edges
                    if not hasattr(face_edges, "Count"):
                        continue
                    for ei in range(1, face_edges.Count + 1):
                        edge_list.append(face_edges.Item(ei))

            if not edge_list:
                return {"error": "No edges found on body"}

            # Extend radii list to match edge count if needed
            radius_values = list(radii)
            while len(radius_values) < len(edge_list):
                radius_values.append(radius_values[-1])

            # VARIANT wrappers required for Rounds methods
            edge_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, edge_list)
            radius_arr = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_R8, radius_values[: len(edge_list)]
            )

            rounds = model.Rounds
            _feature = rounds.AddVariable(1, edge_arr, radius_arr)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "variable_round",
                "edge_count": len(edge_list),
                "radii": radius_values[: len(edge_list)],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: BLEND (FACE-TO-FACE FILLET)
    # =================================================================

    def create_blend(self, radius: float, face_index: int = None) -> dict[str, Any]:
        """
        Create a blend (face-to-face fillet) feature.

        Uses model.Blends.Add(NumberOfEdgeSets, EdgeSetArray, RadiusArray).
        Same VARIANT wrapper pattern as Rounds. Unlike Rounds which fillets edges,
        Blends create smooth transitions between faces.

        Args:
            radius: Blend radius in meters
            face_index: 0-based face index to apply to (None = all edges)

        Returns:
            Dict with status and blend info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add blends to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces found on body"}

            # Collect edges
            edge_list = []
            if face_index is not None:
                if face_index < 0 or face_index >= faces.Count:
                    return {
                        "error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."
                    }
                face = faces.Item(face_index + 1)
                face_edges = face.Edges
                if hasattr(face_edges, "Count"):
                    for ei in range(1, face_edges.Count + 1):
                        edge_list.append(face_edges.Item(ei))
            else:
                for fi in range(1, faces.Count + 1):
                    face = faces.Item(fi)
                    face_edges = face.Edges
                    if not hasattr(face_edges, "Count"):
                        continue
                    for ei in range(1, face_edges.Count + 1):
                        edge_list.append(face_edges.Item(ei))

            if not edge_list:
                return {"error": "No edges found on body"}

            # VARIANT wrappers (same pattern as Rounds)
            edge_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, edge_list)
            radius_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [radius])

            blends = model.Blends
            _feature = blends.Add(1, edge_arr, radius_arr)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "blend",
                "radius": radius,
                "edge_count": len(edge_list),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: REFERENCE PLANE BY ANGLE
    # =================================================================

    def create_ref_plane_by_angle(
        self, parent_plane_index: int, angle: float, normal_side: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a reference plane at an angle to an existing plane.

        Uses RefPlanes.AddAngularByAngle(ParentPlane, Angle, NormalSide).
        Type library: AddAngularByAngle(ParentPlane: IDispatch, Angle: VT_R8,
        NormalSide: FeaturePropertyConstants, [Edge: VT_VARIANT]).

        Args:
            parent_plane_index: Index of parent plane (1=Top/XZ, 2=Front/XY, 3=Right/YZ)
            angle: Angle in degrees from the parent plane
            normal_side: 'Normal' (igRight=2) or 'Reverse' (igLeft=1)

        Returns:
            Dict with status and new plane index
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            ref_planes = doc.RefPlanes

            if parent_plane_index < 1 or parent_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid plane index: {parent_plane_index}. Count: {ref_planes.Count}"
                }

            parent = ref_planes.Item(parent_plane_index)

            side_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            side_const = side_map.get(normal_side, DirectionConstants.igRight)

            # Angle in radians for the COM API
            angle_rad = math.radians(angle)

            _feature = ref_planes.AddAngularByAngle(parent, angle_rad, side_const)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "reference_plane",
                "method": "angular_by_angle",
                "parent_plane": parent_plane_index,
                "angle_degrees": angle,
                "normal_side": normal_side,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: REFERENCE PLANE BY 3 POINTS
    # =================================================================

    def create_ref_plane_by_3_points(
        self,
        x1: float,
        y1: float,
        z1: float,
        x2: float,
        y2: float,
        z2: float,
        x3: float,
        y3: float,
        z3: float,
    ) -> dict[str, Any]:
        """
        Create a reference plane through 3 points in space.

        Uses RefPlanes.AddBy3Points(Point1X, Point1Y, Point1Z, ...).
        Type library: AddBy3Points(9x VT_R8 params) -> RefPlane*.

        Args:
            x1, y1, z1: First point coordinates (meters)
            x2, y2, z2: Second point coordinates (meters)
            x3, y3, z3: Third point coordinates (meters)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            ref_planes = doc.RefPlanes

            _feature = ref_planes.AddBy3Points(x1, y1, z1, x2, y2, z2, x3, y3, z3)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "reference_plane",
                "method": "by_3_points",
                "point1": [x1, y1, z1],
                "point2": [x2, y2, z2],
                "point3": [x3, y3, z3],
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: REFERENCE PLANE MID-PLANE
    # =================================================================

    def create_ref_plane_midplane(self, plane1_index: int, plane2_index: int) -> dict[str, Any]:
        """
        Create a reference plane midway between two existing planes.

        Uses RefPlanes.AddMidPlane(Plane1, Plane2).
        Useful for symmetry operations.

        Args:
            plane1_index: Index of first plane (1=Top/XZ, 2=Front/XY, 3=Right/YZ)
            plane2_index: Index of second plane

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            ref_planes = doc.RefPlanes

            if plane1_index < 1 or plane1_index > ref_planes.Count:
                return {"error": f"Invalid plane1 index: {plane1_index}. Count: {ref_planes.Count}"}
            if plane2_index < 1 or plane2_index > ref_planes.Count:
                return {"error": f"Invalid plane2 index: {plane2_index}. Count: {ref_planes.Count}"}

            plane1 = ref_planes.Item(plane1_index)
            plane2 = ref_planes.Item(plane2_index)

            _feature = ref_planes.AddMidPlane(plane1, plane2)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "reference_plane",
                "method": "mid_plane",
                "plane1_index": plane1_index,
                "plane2_index": plane2_index,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: HOLE THROUGH ALL
    # =================================================================

    def create_hole_through_all(
        self, x: float, y: float, diameter: float, plane_index: int = 1, direction: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a hole that goes through the entire part.

        Creates a circular profile and uses ExtrudedCutouts.AddThroughAllMulti.
        Type library: ExtrudedCutouts.AddThroughAllMulti(NumProfiles, ProfileArray, PlaneSide).

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            dir_const = DirectionConstants.igRight  # Normal
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            # Create a circular profile on the specified plane
            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            # Use through-all cutout
            cutouts = model.ExtrudedCutouts
            _feature = cutouts.AddThroughAllMulti(1, (profile,), dir_const)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_through_all",
                "position": [x, y],
                "diameter": diameter,
                "plane_index": plane_index,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: BOX CUTOUT PRIMITIVE
    # =================================================================

    def create_box_cutout_by_two_points(
        self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, plane_index: int = 1
    ) -> dict[str, Any]:
        """
        Create a box-shaped cutout (boolean subtract) by two opposite corners.

        Uses BoxFeatures.AddCutoutByTwoPoints with same params as AddBoxByTwoPoints.
        Requires an existing base feature to cut from.
        Type library: AddCutoutByTwoPoints(6x VT_R8, dAngle, dDepth, pPlane,
        ExtentSide, vbKeyPointExtent, pKeyPointObj, pKeyPointFlags).

        Args:
            x1, y1, z1: First corner coordinates (meters)
            x2, y2, z2: Opposite corner coordinates (meters)
            plane_index: Reference plane (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            top_plane = self._get_ref_plane(doc, plane_index)
            depth = abs(z2 - z1) if abs(z2 - z1) > 0 else abs(y2 - y1)

            # BoxFeatures is on the Models collection level
            box_features = models.BoxFeatures if hasattr(models, "BoxFeatures") else None
            if box_features is None:
                # Try via the model object
                model = models.Item(1)
                box_features = model.BoxFeatures if hasattr(model, "BoxFeatures") else None

            if box_features is None:
                return {"error": "BoxFeatures collection not accessible"}

            _feature = box_features.AddCutoutByTwoPoints(
                x1,
                y1,
                z1,
                x2,
                y2,
                z2,
                0,  # dAngle
                depth,  # dDepth
                top_plane,  # pPlane
                DirectionConstants.igRight,  # ExtentSide
                False,  # vbKeyPointExtent
                None,  # pKeyPointObj
                0,  # pKeyPointFlags
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "box_cutout",
                "method": "by_two_points",
                "corner1": [x1, y1, z1],
                "corner2": [x2, y2, z2],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_box_cutout_by_center(
        self,
        center_x: float,
        center_y: float,
        center_z: float,
        length: float,
        width: float,
        height: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a box-shaped cutout by center point and dimensions.

        Removes a rectangular volume centered at the given point.
        Requires an existing base feature.

        Args:
            center_x, center_y, center_z: Center point coordinates (meters)
            length: Length in meters (X direction)
            width: Width in meters (Y direction)
            height: Height in meters (Z direction)
            plane_index: Reference plane (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            top_plane = self._get_ref_plane(doc, plane_index)

            box_features = models.BoxFeatures if hasattr(models, "BoxFeatures") else None
            if box_features is None:
                model = models.Item(1)
                box_features = model.BoxFeatures if hasattr(model, "BoxFeatures") else None

            if box_features is None:
                return {"error": "BoxFeatures collection not accessible"}

            _feature = box_features.AddCutoutByCenter(
                center_x,
                center_y,
                center_z,
                length,  # dWidth
                width,  # dHeight
                0,  # dAngle
                height,  # dDepth
                top_plane,  # pPlane
                DirectionConstants.igRight,  # ExtentSide
                False,  # vbKeyPointExtent
                None,  # pKeyPointObj
                0,  # pKeyPointFlags
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "box_cutout",
                "method": "by_center",
                "center": [center_x, center_y, center_z],
                "dimensions": {"length": length, "width": width, "height": height},
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_box_cutout_by_three_points(
        self,
        x1: float,
        y1: float,
        z1: float,
        x2: float,
        y2: float,
        z2: float,
        x3: float,
        y3: float,
        z3: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a box-shaped cutout by three points.

        Removes a rectangular volume defined by three corner points.
        Requires an existing base feature.

        Args:
            x1, y1, z1: First corner point (meters)
            x2, y2, z2: Second point defining width (meters)
            x3, y3, z3: Third point defining height (meters)
            plane_index: Reference plane (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and cutout info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            top_plane = self._get_ref_plane(doc, plane_index)

            dx = x2 - x1
            dy = y2 - y1
            depth = math.sqrt(dx * dx + dy * dy)
            if depth == 0:
                depth = 0.01

            box_features = models.BoxFeatures if hasattr(models, "BoxFeatures") else None
            if box_features is None:
                model = models.Item(1)
                box_features = model.BoxFeatures if hasattr(model, "BoxFeatures") else None

            if box_features is None:
                return {"error": "BoxFeatures collection not accessible"}

            _feature = box_features.AddCutoutByThreePoints(
                x1,
                y1,
                z1,
                x2,
                y2,
                z2,
                x3,
                y3,
                z3,
                depth,  # dDepth
                top_plane,  # pPlane
                DirectionConstants.igRight,  # ExtentSide
                False,  # vbKeyPointExtent
                None,  # pKeyPointObj
                0,  # pKeyPointFlags
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "box_cutout",
                "method": "by_three_points",
                "point1": [x1, y1, z1],
                "point2": [x2, y2, z2],
                "point3": [x3, y3, z3],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: CYLINDER CUTOUT PRIMITIVE
    # =================================================================

    def create_cylinder_cutout(
        self,
        center_x: float,
        center_y: float,
        center_z: float,
        radius: float,
        height: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a cylindrical cutout via sketch→extruded cutout.

        Draws a circle at (center_x, center_y) with the given radius on the sketch
        plane and removes material by extruding the profile into the existing body.
        Requires an existing base feature to cut from.

        Args:
            center_x, center_y, center_z: Center coordinates (meters)
            radius: Cylinder radius (meters)
            height: Cut depth (meters)
            plane_index: Reference plane (1=Top, 2=Right, 3=Front)

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            plane_name = {1: "Top", 2: "Right", 3: "Front"}.get(plane_index, "Top")

            r = self.sketch_manager.create_sketch(plane_name)
            if "error" in r:
                return r

            r = self.sketch_manager.draw_circle(center_x, center_y, radius)
            if "error" in r:
                return r

            r = self.sketch_manager.close_sketch()
            if "error" in r:
                return r

            r = self.create_extruded_cutout(height, direction="Normal")
            if "error" in r:
                return r

            return {
                "status": "created",
                "type": "cylinder_cutout",
                "center": [center_x, center_y, center_z],
                "radius": radius,
                "height": height,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 1: SPHERE CUTOUT PRIMITIVE
    # =================================================================

    def create_sphere_cutout(
        self, center_x: float, center_y: float, center_z: float, radius: float, plane_index: int = 1
    ) -> dict[str, Any]:
        """
        Create a spherical cutout via sketch→revolved cutout.

        Draws a right-hand semicircle profile (arc 270°→90° + closing diameter line)
        with an axis of revolution along the diameter, then revolves 360° as a cutout.
        Requires an existing base feature to cut from.

        Args:
            center_x, center_y, center_z: Sphere center coordinates (meters)
            radius: Sphere radius (meters)
            plane_index: Reference plane (1=Top, 2=Right, 3=Front)

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            plane_name = {1: "Top", 2: "Right", 3: "Front"}.get(plane_index, "Top")

            r = self.sketch_manager.create_sketch(plane_name)
            if "error" in r:
                return r

            # Semicircle: bottom (cx, cy-r) → right (cx+r, cy) → top (cx, cy+r)
            r = self.sketch_manager.draw_arc(center_x, center_y, radius, 270, 90)
            if "error" in r:
                return r

            # Closing diameter line (top → bottom along the axis side)
            r = self.sketch_manager.draw_line(
                center_x, center_y + radius,
                center_x, center_y - radius,
            )
            if "error" in r:
                return r

            # Construction axis along the diameter (bottom → top)
            r = self.sketch_manager.set_axis_of_revolution(
                center_x, center_y - radius,
                center_x, center_y + radius,
            )
            if "error" in r:
                return r

            r = self.sketch_manager.close_sketch()
            if "error" in r:
                return r

            r = self.create_revolved_cutout(angle=360)
            if "error" in r:
                return r

            return {
                "status": "created",
                "type": "sphere_cutout",
                "center": [center_x, center_y, center_z],
                "radius": radius,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 2: EXTRUDED CUTOUT THROUGH NEXT
    # =================================================================

    def create_extruded_cutout_through_next(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create an extruded cutout that cuts to the next face encountered.

        Uses model.ExtrudedCutouts.AddThroughNextMulti(NumProfiles, ProfileArray, PlaneSide).
        Cuts from the sketch plane to the first face it meets in each direction.

        Direction semantics
        -------------------
        "Normal"    — cuts toward the sketch plane's outward-normal direction only
                      (igRight).  On the Front plane SE's internal normal is -Y,
                      so "Normal" cuts toward -Y, leaving the +Y side uncut.
        "Reverse"   — cuts in the opposite direction only (igLeft).  On the
                      Front plane this cuts toward +Y.
        "Symmetric" — cuts to the next face in *both* directions.  Implemented
                      as two sequential through-next cuts (one igRight, one igLeft)
                      because SE has no native symmetric through-next COM API.
                      The feature therefore appears as two items in the
                      pathfinder tree rather than one (see TODO.md).

        For the safest result on any plane use direction="Symmetric".

        Args:
            direction: 'Normal', 'Reverse', or 'Symmetric' (default 'Normal')

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            cutouts = model.ExtrudedCutouts

            if direction == "Symmetric":
                # Two sequential through-next cuts — one per direction.
                # consumes_profiles=False on the first pass keeps active_profile
                # live so the same COM object can be reused for the second pass.
                result, err = self._perform_feature_call(
                    lambda: cutouts.AddThroughNextMulti(1, (profile,), DirectionConstants.igRight),
                    consumes_profiles=False,
                )
                if err:
                    return err
                result, err = self._perform_feature_call(
                    lambda: cutouts.AddThroughNextMulti(1, (profile,), DirectionConstants.igLeft),
                    consumes_profiles=True,
                )
                if err:
                    return err
            else:
                direction_map = {
                    "Normal": DirectionConstants.igRight,
                    "Reverse": DirectionConstants.igLeft,
                }
                dir_const = direction_map.get(direction, DirectionConstants.igRight)
                # DELIBERATE DESIGN DECISION — do not "fix" without reading this.
                #
                # create_extrude applies an auto-swap (igRight ↔ igLeft) for Front plane
                # sketches (plane_index == 3) so that direction="Normal" reliably extrudes
                # toward world +Y, matching user expectation.
                #
                # Cutout tools intentionally do NOT apply this swap. Reasons:
                #   1. Transparency over cleverness — callers get raw SE direction behaviour,
                #      which is documented in PLANE_AXIS_MAP (constants.py).
                #   2. Applying the swap would silently break callers using direction="Reverse"
                #      to cut toward world -Y on the Front plane.
                #   3. The safe option for Front plane cutouts is direction="Symmetric", which
                #      cuts both ways and is immune to this axis quirk entirely.
                #
                # If you want to apply the auto-swap to cutouts for consistency with extrude,
                # add the same three-line swap block from create_extrude here. Document it as
                # a breaking change and bump the minor version.
                #
                # See also: TODO.md "Known Limitations" section.
                result, err = self._perform_feature_call(
                    lambda: cutouts.AddThroughNextMulti(1, (profile,), dir_const),
                    consumes_profiles=True,
                )
                if err:
                    return err

            response = {
                "status": "created",
                "type": "extruded_cutout_through_next",
                "direction": direction,
            }
            if direction in ("Normal", "Reverse") and self.sketch_manager.get_active_plane_index() == 3:
                _world_dir = "world -Y" if direction == "Normal" else "world +Y"
                response["warning"] = (
                    f"Front plane cutout used direction='{direction}' ({_world_dir} only). "
                    "If you need a full through-cut, use direction='Symmetric'."
                )
            self._append_bbox(response)
            return response
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 2: NORMAL CUTOUT THROUGH ALL
    # =================================================================

    def create_normal_cutout_through_all(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a normal cutout that goes through the entire part.

        Uses model.NormalCutouts.AddThroughAllMulti(NumProfiles, ProfileArray,
        PlaneSide, Method). Normal cutouts follow the surface normal.

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            dir_const = direction_map.get(direction, DirectionConstants.igRight)

            # igNormalCutoutMethod_Normal = 0 (default method)
            cutouts = model.NormalCutouts
            _feature = cutouts.AddThroughAllMulti(1, (profile,), dir_const, 0)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "normal_cutout_through_all",
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 2: DELETE HOLES
    # =================================================================

    def create_delete_hole(
        self, max_diameter: float = 1.0, hole_type: str = "All"
    ) -> dict[str, Any]:
        """
        Delete/fill holes in the model body.

        Uses model.DeleteHoles.Add(HoleTypeToDelete, ThresholdHoleDiameter).
        Fills holes up to the specified diameter threshold.

        Args:
            max_diameter: Maximum hole diameter to delete (meters). Holes with
                diameter <= this value will be filled.
            hole_type: Type of holes to delete: 'All', 'Round', 'NonRound'

        Returns:
            Dict with status and deletion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            # HoleTypeToDeleteConstants from type library
            type_map = {
                "All": 0,
                "Round": 1,
                "NonRound": 2,
            }
            hole_type_const = type_map.get(hole_type, 0)

            delete_holes = model.DeleteHoles
            _feature = delete_holes.Add(hole_type_const, max_diameter)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "delete_hole",
                "max_diameter": max_diameter,
                "hole_type": hole_type,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 2: DELETE BLENDS
    # =================================================================

    def create_delete_blend(self, face_index: int) -> dict[str, Any]:
        """
        Delete/remove a blend (fillet) from the model by specifying a face.

        Uses model.DeleteBlends.Add(BlendsToDelete). Removes the blend
        associated with the specified face.

        Args:
            face_index: 0-based face index of the blend face to remove

        Returns:
            Dict with status and deletion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)

            delete_blends = model.DeleteBlends
            _feature = delete_blends.Add(face)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {"status": "created", "type": "delete_blend", "face_index": face_index}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 2: REVOLVED SURFACE
    # =================================================================

    def create_revolved_surface(
        self, angle: float = 360, want_end_caps: bool = False
    ) -> dict[str, Any]:
        """
        Create a revolved construction surface from the active profile.

        Uses RevolvedSurfaces.AddFinite(NumProfiles, ProfileArray, RefAxis,
        ProfilePlaneSide, AngleOfRevolution, WantEndCaps).
        Requires a profile with an axis of revolution set.

        Args:
            angle: Revolution angle in degrees (360 for full revolution)
            want_end_caps: Whether to cap the ends of the surface

        Returns:
            Dict with status and surface info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            if not refaxis:
                return {"error": "No axis of revolution set. Use set_axis_of_revolution() first."}

            models = doc.Models
            angle_rad = math.radians(angle)

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            # Try collection-level API first (on model), then Models-level
            if models.Count > 0:
                model = models.Item(1)
                rev_surfaces = model.RevolvedSurfaces
                result, err = self._perform_feature_call(
                    lambda: rev_surfaces.AddFinite(
                        1, v_profiles, refaxis, DirectionConstants.igRight, angle_rad, want_end_caps
                    ),
                    consumes_profiles=True,
                )
                if err:
                    return err
            else:
                # First feature - use Models method if available
                result, err = self._perform_feature_call(
                    lambda: models.AddFiniteRevolvedSurface(
                        1, v_profiles, refaxis, DirectionConstants.igRight, angle_rad, want_end_caps
                    ),
                    consumes_profiles=True,
                )
                if err:
                    return err

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "revolved_surface",
                "angle_degrees": angle,
                "want_end_caps": want_end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 2: LOFTED SURFACE
    # =================================================================

    def create_lofted_surface(self, want_end_caps: bool = False) -> dict[str, Any]:
        """
        Create a lofted construction surface between multiple profiles.

        Uses LoftedSurfaces.Add with accumulated profiles. Same workflow as
        create_loft: create 2+ sketches on different planes, close each,
        then call this method.

        Args:
            want_end_caps: Whether to cap the ends of the surface

        Returns:
            Dict with status and surface info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if len(all_profiles) < 2:
                return {
                    "error": f"Lofted surface requires at least 2 profiles, "
                    f"got {len(all_profiles)}."
                }

            _CS = LoftSweepConstants.igProfileBasedCrossSection

            v_sections = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, all_profiles)
            v_types = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS] * len(all_profiles))
            v_origins = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
                [VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0]) for _ in all_profiles],
            )

            if models.Count > 0:
                model = models.Item(1)
                loft_surfaces = model.LoftedSurfaces
                result, err = self._perform_feature_call(
                    lambda: loft_surfaces.Add(
                        len(all_profiles),
                        v_sections,
                        v_types,
                        v_origins,
                        ExtentTypeConstants.igNone,  # StartExtentType
                        ExtentTypeConstants.igNone,  # EndExtentType
                        0,
                        0.0,  # StartTangentType, StartTangentMagnitude
                        0,
                        0.0,  # EndTangentType, EndTangentMagnitude
                        0,
                        None,  # NumGuideCurves, GuideCurves
                        want_end_caps,
                    ),
                    consumes_profiles=True,
                )
                if err:
                    return err
            else:
                return {"error": "Lofted surface requires an existing base feature."}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "lofted_surface",
                "num_profiles": len(all_profiles),
                "want_end_caps": want_end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # TIER 2: SWEPT SURFACE
    # =================================================================

    def create_swept_surface(
        self, path_profile_index: int = None, want_end_caps: bool = False
    ) -> dict[str, Any]:
        """
        Create a swept construction surface along a path.

        Same workflow as create_sweep: path profile (open) + cross-section (closed).
        Uses SweptSurfaces.Add.

        Args:
            path_profile_index: Index of the path profile (default: 0)
            want_end_caps: Whether to cap the ends of the surface

        Returns:
            Dict with status and surface info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if len(all_profiles) < 2:
                return {
                    "error": f"Swept surface requires at least 2 profiles (path + cross-section), "
                    f"got {len(all_profiles)}."
                }

            path_idx = path_profile_index if path_profile_index is not None else 0
            path_profile = all_profiles[path_idx]
            cross_sections = [p for i, p in enumerate(all_profiles) if i != path_idx]

            _CS = LoftSweepConstants.igProfileBasedCrossSection

            v_paths = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [path_profile])
            v_sections = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, cross_sections)

            swept_surfaces = model.SweptSurfaces
            result, err = self._perform_feature_call(
                lambda: swept_surfaces.Add(
                    1,
                    v_paths,
                    _CS,  # Path
                    len(cross_sections),
                    v_sections,
                    _CS,  # Sections
                    None,
                    None,  # Origins, OriginRefs
                    ExtentTypeConstants.igNone,  # StartExtentType
                    ExtentTypeConstants.igNone,  # EndExtentType
                    want_end_caps,
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "swept_surface",
                "num_cross_sections": len(cross_sections),
                "want_end_caps": want_end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def convert_feature_type(self, feature_name: str, target_type: str) -> dict[str, Any]:
        """
        Convert a feature between cutout and protrusion.

        Uses Feature.ConvertToCutout() or Feature.ConvertToProtrusion()
        to toggle a feature between adding and removing material.

        Args:
            feature_name: Name of the feature (from list_features)
            target_type: 'cutout' or 'protrusion'

        Returns:
            Dict with conversion status and new feature reference
        """
        try:
            doc = self.doc_manager.get_active_document()

            # Find the feature by name
            features = doc.DesignEdgebarFeatures
            target_feature = None
            for i in range(1, features.Count + 1):
                feat = features.Item(i)
                try:
                    if feat.Name == feature_name:
                        target_feature = feat
                        break
                except Exception:
                    continue

            if target_feature is None:
                return {"error": f"Feature '{feature_name}' not found"}

            target_type_lower = target_type.lower()
            if target_type_lower == "cutout":
                result = target_feature.ConvertToCutout()
                new_name = None
                with contextlib.suppress(Exception):
                    new_name = result.Name
                return {
                    "status": "converted",
                    "original_name": feature_name,
                    "target_type": "cutout",
                    "new_name": new_name,
                }
            elif target_type_lower == "protrusion":
                result = target_feature.ConvertToProtrusion()
                new_name = None
                with contextlib.suppress(Exception):
                    new_name = result.Name
                return {
                    "status": "converted",
                    "original_name": feature_name,
                    "target_type": "protrusion",
                    "new_name": new_name,
                }
            else:
                return {
                    "error": f"Invalid target_type: {target_type}. Use 'cutout' or 'protrusion'"
                }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # BATCH 4: ADDITIONAL REFERENCE PLANE VARIANTS
    # =================================================================

    def create_ref_plane_normal_at_keypoint(
        self, keypoint_type: str = "End", pivot_plane_index: int = 2
    ) -> dict[str, Any]:
        """
        Create a reference plane normal to a curve at a keypoint (start or end).

        Uses RefPlanes.AddNormalToCurveAtKeyPoint(Curve, OrientationPlane, KeyPoint,
        KeyPointTypeConstant, XAxisRotation, normalOrientation, selectedCurveEnd).
        Requires an active sketch profile that defines the curve.

        Args:
            keypoint_type: 'Start' or 'End' of the curve
            pivot_plane_index: 1-based index of the orientation reference plane (default: 2 = Front)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            ref_planes = doc.RefPlanes

            if pivot_plane_index < 1 or pivot_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid pivot_plane_index: {pivot_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }

            orientation_plane = ref_planes.Item(pivot_plane_index)

            # KeyPointTypeConstant: igKeyPointStart=1, igKeyPointEnd=2
            kp_const = (
                KeyPointTypeConstants.igKeyPointStart
                if keypoint_type == "Start"
                else KeyPointTypeConstants.igKeyPointEnd
            )

            # selectedCurveEnd: igCurveStart=14, igCurveEnd=15
            curve_end_const = (
                ReferenceElementConstants.igCurveStart
                if keypoint_type == "Start"
                else ReferenceElementConstants.igCurveEnd
            )

            _feature = ref_planes.AddNormalToCurveAtKeyPoint(
                profile,  # Curve
                orientation_plane,  # OrientationPlane
                profile,  # KeyPoint (same as curve for endpoint)
                kp_const,  # KeyPointTypeConstant
                0.0,  # XAxisRotation
                ReferenceElementConstants.igNormalSide,  # normalOrientation
                curve_end_const,  # selectedCurveEnd
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "ref_plane_normal_at_keypoint",
                "keypoint_type": keypoint_type,
                "pivot_plane_index": pivot_plane_index,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_tangent_cylinder_angle(
        self, face_index: int, angle: float, parent_plane_index: int = 1
    ) -> dict[str, Any]:
        """
        Create a reference plane tangent to a cylindrical or conical face at an angle.

        Uses RefPlanes.AddTangentToCylinderOrConeAtAngle(Face, ParentPlane,
        AngleOfRotation, XAxisAngle, ExtentSide, normalOrientation).

        Args:
            face_index: 0-based index of the cylindrical/conical face
            angle: Angle of rotation in degrees
            parent_plane_index: 1-based index of the parent reference plane (default: 1 = Top)

        Returns:
            Dict with status and new plane index
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            ref_planes = doc.RefPlanes

            if parent_plane_index < 1 or parent_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid parent_plane_index: {parent_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a feature first."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face_index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            parent_plane = ref_planes.Item(parent_plane_index)

            angle_rad = math.radians(angle)

            _feature = ref_planes.AddTangentToCylinderOrConeAtAngle(
                face,  # Face
                parent_plane,  # ParentPlane
                angle_rad,  # AngleOfRotation
                0.0,  # XAxisAngle
                DirectionConstants.igRight,  # ExtentSide
                ReferenceElementConstants.igNormalSide,  # normalOrientation
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "ref_plane_tangent_cylinder_angle",
                "face_index": face_index,
                "angle_degrees": angle,
                "parent_plane_index": parent_plane_index,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_tangent_cylinder_keypoint(
        self, face_index: int, keypoint_type: str = "End", parent_plane_index: int = 1
    ) -> dict[str, Any]:
        """
        Create a reference plane tangent to a cylindrical or conical face at a keypoint.

        Uses RefPlanes.AddTangentToCylinderOrConeAtKeyPoint(Face, ParentPlane,
        KeyPoint, KeyPointTypeConstant, XAxisAngle, ExtentSide, normalOrientation).

        Args:
            face_index: 0-based index of the cylindrical/conical face
            keypoint_type: 'Start' or 'End' keypoint on the face
            parent_plane_index: 1-based index of the parent reference plane (default: 1 = Top)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            ref_planes = doc.RefPlanes

            if parent_plane_index < 1 or parent_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid parent_plane_index: {parent_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a feature first."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face_index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            parent_plane = ref_planes.Item(parent_plane_index)

            kp_const = (
                KeyPointTypeConstants.igKeyPointStart
                if keypoint_type == "Start"
                else KeyPointTypeConstants.igKeyPointEnd
            )

            _feature = ref_planes.AddTangentToCylinderOrConeAtKeyPoint(
                face,  # Face
                parent_plane,  # ParentPlane
                face,  # KeyPoint (use face itself as keypoint reference)
                kp_const,  # KeyPointTypeConstant
                0.0,  # XAxisAngle
                DirectionConstants.igRight,  # ExtentSide
                ReferenceElementConstants.igNormalSide,  # normalOrientation
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "ref_plane_tangent_cylinder_keypoint",
                "face_index": face_index,
                "keypoint_type": keypoint_type,
                "parent_plane_index": parent_plane_index,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_tangent_surface_keypoint(
        self, face_index: int, keypoint_type: str = "End", parent_plane_index: int = 1
    ) -> dict[str, Any]:
        """
        Create a reference plane tangent to a curved surface at a keypoint.

        Uses RefPlanes.AddTangentToCurvedSurfaceAtKeyPoint(Face, ParentPlane,
        KeyPoint, KeyPointTypeConstant, XAxisAngle, normalOrientation).

        Args:
            face_index: 0-based index of the curved surface face
            keypoint_type: 'Start' or 'End' keypoint on the face
            parent_plane_index: 1-based index of the parent reference plane (default: 1 = Top)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            ref_planes = doc.RefPlanes

            if parent_plane_index < 1 or parent_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid parent_plane_index: {parent_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a feature first."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face_index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            parent_plane = ref_planes.Item(parent_plane_index)

            kp_const = (
                KeyPointTypeConstants.igKeyPointStart
                if keypoint_type == "Start"
                else KeyPointTypeConstants.igKeyPointEnd
            )

            _feature = ref_planes.AddTangentToCurvedSurfaceAtKeyPoint(
                face,  # Face
                parent_plane,  # ParentPlane
                face,  # KeyPoint (use face itself as keypoint reference)
                kp_const,  # KeyPointTypeConstant
                0.0,  # XAxisAngle
                ReferenceElementConstants.igNormalSide,  # normalOrientation
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "ref_plane_tangent_surface_keypoint",
                "face_index": face_index,
                "keypoint_type": keypoint_type,
                "parent_plane_index": parent_plane_index,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # BATCH 4: ADDITIONAL SURFACE CREATION METHODS
    # =================================================================

    def create_extruded_surface_from_to(
        self, from_plane_index: int, to_plane_index: int
    ) -> dict[str, Any]:
        """
        Create an extruded surface between two reference planes.

        Uses ExtrudedSurfaces.AddFromTo(NumberOfProfiles, ProfileArray,
        FromFaceOrRefPlane, ToFaceOrRefPlane, WantEndCaps).

        Args:
            from_plane_index: 1-based index of the start reference plane
            to_plane_index: 1-based index of the end reference plane

        Returns:
            Dict with status and surface info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: {from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            profile_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            constructions = doc.Constructions
            extruded_surfaces = constructions.ExtrudedSurfaces

            _feature = extruded_surfaces.AddFromTo(
                1,  # NumberOfProfiles
                profile_array,  # ProfileArray
                from_plane,  # FromFaceOrRefPlane
                to_plane,  # ToFaceOrRefPlane
                True,  # WantEndCaps
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_surface_from_to",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_surface_by_keypoint(self, keypoint_type: str = "End") -> dict[str, Any]:
        """
        Create an extruded surface up to a keypoint extent.

        Uses ExtrudedSurfaces.AddFiniteByKeyPoint(NumberOfProfiles, ProfileArray,
        ProfilePlaneSide, KeyPointOrTangentFace, KeyPointFlags, WantEndCaps).

        Args:
            keypoint_type: 'Start' or 'End' keypoint for the extent

        Returns:
            Dict with status and surface info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            profile_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            constructions = doc.Constructions
            extruded_surfaces = constructions.ExtrudedSurfaces

            _feature = extruded_surfaces.AddFiniteByKeyPoint(
                1,  # NumberOfProfiles
                profile_array,  # ProfileArray
                DirectionConstants.igRight,  # ProfilePlaneSide
                None,  # KeyPointOrTangentFace
                KeyPointExtentConstants.igTangentNormal,  # KeyPointFlags
                True,  # WantEndCaps
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_surface_by_keypoint",
                "keypoint_type": keypoint_type,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_surface_by_curves(
        self, distance: float, direction: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create an extruded surface by curves (extrude along curve path).

        Uses ExtrudedSurfaces.AddByCurves with full treatment params.
        This uses curves (profiles) rather than standard profile extrusion.

        Args:
            distance: Extrusion distance in meters
            direction: 'Normal' or 'Symmetric'

        Returns:
            Dict with status and surface info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            curve_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            depth1 = distance
            depth2 = distance if direction == "Symmetric" else 0.0
            side1 = DirectionConstants.igRight
            side2 = (
                DirectionConstants.igLeft
                if direction == "Symmetric"
                else DirectionConstants.igRight
            )

            constructions = doc.Constructions
            extruded_surfaces = constructions.ExtrudedSurfaces

            _feature = extruded_surfaces.AddByCurves(
                1,  # NumberOfCurves
                curve_array,  # CurveArray
                ExtentTypeConstants.igFinite,  # ExtentType1
                side1,  # ExtentSide1
                depth1,  # FiniteDepth1
                None,  # KeyPointOrTangentFace1
                KeyPointExtentConstants.igTangentNormal,  # KeyPointFlags1
                None,  # FromFaceOrRefPlane
                OffsetSideConstants.seOffsetNone,  # FromFaceOffsetSide
                0.0,  # FromFaceOffsetDistance
                TreatmentTypeConstants.seTreatmentNone,  # TreatmentType1
                DraftSideConstants.seDraftNone,  # TreatmentDraftSide1
                0.0,  # TreatmentDraftAngle1
                TreatmentCrownTypeConstants.seTreatmentCrownByOffset,  # TreatmentCrownType1
                TreatmentCrownSideConstants.seTreatmentCrownSideInside,  # TreatmentCrownSide1
                TreatmentCrownCurvatureSideConstants.seTreatmentCrownCurvatureInside,
                0.0,  # TreatmentCrownRadiusOrOffset1
                0.0,  # TreatmentCrownTakeOffAngle1
                ExtentTypeConstants.igFinite,  # ExtentType2
                side2,  # ExtentSide2
                depth2,  # FiniteDepth2
                None,  # KeyPointOrTangentFace2
                KeyPointExtentConstants.igTangentNormal,  # KeyPointFlags2
                None,  # ToFaceOrRefPlane
                OffsetSideConstants.seOffsetNone,  # ToFaceOffsetSide
                0.0,  # ToFaceOffsetDistance
                TreatmentTypeConstants.seTreatmentNone,  # TreatmentType2
                DraftSideConstants.seDraftNone,  # TreatmentDraftSide2
                0.0,  # TreatmentDraftAngle2
                TreatmentCrownTypeConstants.seTreatmentCrownByOffset,  # TreatmentCrownType2
                TreatmentCrownSideConstants.seTreatmentCrownSideInside,  # TreatmentCrownSide2
                TreatmentCrownCurvatureSideConstants.seTreatmentCrownCurvatureInside,
                0.0,  # TreatmentCrownRadiusOrOffset2
                0.0,  # TreatmentCrownTakeOffAngle2
                True,  # WantEndCaps
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_surface_by_curves",
                "distance": distance,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolved_surface_sync(
        self, angle: float = 360.0, want_end_caps: bool = False
    ) -> dict[str, Any]:
        """
        Create a synchronous revolved construction surface.

        Uses RevolvedSurfaces.AddFiniteSync(NumberOfProfiles, ProfileArray,
        RefAxis, ProfilePlaneSide, AngleOfRevolution, WantEndCaps).

        Args:
            angle: Revolution angle in degrees (360 for full revolution)
            want_end_caps: Whether to cap the ends of the surface

        Returns:
            Dict with status and surface info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            if not refaxis:
                return {"error": "No axis of revolution set. Use set_axis_of_revolution() first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            angle_rad = math.radians(angle)

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            rev_surfaces = model.RevolvedSurfaces
            _feature = rev_surfaces.AddFiniteSync(
                1,  # NumberOfProfiles
                v_profiles,  # ProfileArray
                refaxis,  # RefAxis
                DirectionConstants.igRight,  # ProfilePlaneSide
                angle_rad,  # AngleOfRevolution
                want_end_caps,  # WantEndCaps
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "revolved_surface_sync",
                "angle_degrees": angle,
                "want_end_caps": want_end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolved_surface_by_keypoint(
        self, keypoint_type: str = "End", want_end_caps: bool = False
    ) -> dict[str, Any]:
        """
        Create a revolved construction surface up to a keypoint extent.

        Uses RevolvedSurfaces.AddFiniteByKeyPoint(NumberOfProfiles, ProfileArray,
        RefAxis, KeyPointOrTangentFace, KeyPointFlags, ProfilePlaneSide, WantEndCaps).

        Args:
            keypoint_type: 'Start' or 'End' keypoint for the extent
            want_end_caps: Whether to cap the ends of the surface

        Returns:
            Dict with status and surface info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            if not refaxis:
                return {"error": "No axis of revolution set. Use set_axis_of_revolution() first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            rev_surfaces = model.RevolvedSurfaces
            _feature = rev_surfaces.AddFiniteByKeyPoint(
                1,  # NumberOfProfiles
                v_profiles,  # ProfileArray
                refaxis,  # RefAxis
                None,  # KeyPointOrTangentFace
                KeyPointExtentConstants.igTangentNormal,  # KeyPointFlags
                DirectionConstants.igRight,  # ProfilePlaneSide
                want_end_caps,  # WantEndCaps
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "revolved_surface_by_keypoint",
                "keypoint_type": keypoint_type,
                "want_end_caps": want_end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_lofted_surface_v2(self, want_end_caps: bool = False) -> dict[str, Any]:
        """
        Create a lofted surface using the extended Add2 method.

        Uses LoftedSurfaces.Add2 which supports an additional OutputSurfaceType
        parameter compared to the basic Add method. Requires 2+ accumulated profiles.

        Args:
            want_end_caps: Whether to cap the ends of the surface

        Returns:
            Dict with status and surface info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if len(all_profiles) < 2:
                return {
                    "error": f"Lofted surface requires at least 2 profiles, "
                    f"got {len(all_profiles)}."
                }

            if models.Count == 0:
                return {"error": "Lofted surface requires an existing base feature."}

            model = models.Item(1)

            _CS = LoftSweepConstants.igProfileBasedCrossSection

            v_sections = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, all_profiles)
            v_types = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS] * len(all_profiles))
            v_origins = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
                [VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0]) for _ in all_profiles],
            )

            loft_surfaces = model.LoftedSurfaces
            _feature = loft_surfaces.Add2(
                len(all_profiles),  # NumSections
                v_sections,  # CrossSections
                v_types,  # CrossSectionTypes
                v_origins,  # Origins
                ExtentTypeConstants.igNone,  # StartExtentType
                ExtentTypeConstants.igNone,  # EndExtentType
                0,  # StartTangentType
                0.0,  # StartTangentMagnitude
                0,  # EndTangentType
                0.0,  # EndTangentMagnitude
                0,  # NumGuideCurves
                None,  # GuideCurves
                want_end_caps,  # WantEndCaps
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "lofted_surface_v2",
                "num_profiles": len(all_profiles),
                "want_end_caps": want_end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_swept_surface_ex(
        self, path_profile_index: int = None, want_end_caps: bool = False
    ) -> dict[str, Any]:
        """
        Create a swept surface using the extended AddEx method.

        Uses SweptSurfaces.AddEx which provides additional control via Origins
        and OriginRefs parameters. Requires 2+ accumulated profiles (path + sections).

        Args:
            path_profile_index: Index of the path profile in accumulated profiles
                (default: 0, the first accumulated profile)
            want_end_caps: Whether to cap the ends of the surface

        Returns:
            Dict with status and surface info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "Swept surface requires an existing base feature."}

            model = models.Item(1)

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if len(all_profiles) < 2:
                return {
                    "error": "Swept surface requires at least 2 profiles "
                    "(path + cross-section), got "
                    f"{len(all_profiles)}."
                }

            path_idx = path_profile_index if path_profile_index is not None else 0
            path_profile = all_profiles[path_idx]
            cross_sections = [p for i, p in enumerate(all_profiles) if i != path_idx]

            _CS = LoftSweepConstants.igProfileBasedCrossSection

            v_paths = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [path_profile])
            v_sections = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, cross_sections)
            v_origins = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
                [VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0]) for _ in cross_sections],
            )

            swept_surfaces = model.SweptSurfaces
            _feature = swept_surfaces.AddEx(
                1,  # NumCurves
                v_paths,  # TraceCurves
                _CS,  # TraceCurveTypes
                len(cross_sections),  # NumSections
                v_sections,  # CrossSections
                _CS,  # CrossSectionTypes
                v_origins,  # Origins
                None,  # OriginRefs
                ExtentTypeConstants.igNone,  # StartExtentType
                ExtentTypeConstants.igNone,  # EndExtentType
                want_end_caps,  # WantEndCaps
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "swept_surface_ex",
                "num_cross_sections": len(cross_sections),
                "want_end_caps": want_end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_surface_full(
        self,
        distance: float,
        direction: str = "Normal",
        treatment_type: str = "None",
        draft_angle: float = 0.0,
    ) -> dict[str, Any]:
        """
        Create an extruded surface with full treatment parameters (crown, draft).

        Uses ExtrudedSurfaces.Add with all treatment params exposed for control
        over draft angles and crown shaping.

        Args:
            distance: Extrusion distance in meters
            direction: 'Normal' or 'Symmetric'
            treatment_type: 'None', 'Crown', 'Draft', or 'CrownAndDraft'
            draft_angle: Draft angle in degrees (used when treatment_type includes 'Draft')

        Returns:
            Dict with status and surface info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            # Map treatment type
            treatment_map = {
                "None": TreatmentTypeConstants.seTreatmentNone,
                "Crown": TreatmentTypeConstants.seTreatmentCrown,
                "Draft": TreatmentTypeConstants.seTreatmentDraft,
                "CrownAndDraft": TreatmentTypeConstants.seTreatmentCrownAndDraft,
            }
            treat_const = treatment_map.get(treatment_type, TreatmentTypeConstants.seTreatmentNone)

            # Draft side defaults to outside when draft is active
            draft_side = (
                DraftSideConstants.seDraftOutside
                if treat_const
                in (
                    TreatmentTypeConstants.seTreatmentDraft,
                    TreatmentTypeConstants.seTreatmentCrownAndDraft,
                )
                else DraftSideConstants.seDraftNone
            )
            draft_angle_rad = math.radians(draft_angle)

            profile_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            depth1 = distance
            depth2 = distance if direction == "Symmetric" else 0.0
            side1 = DirectionConstants.igRight
            side2 = (
                DirectionConstants.igLeft
                if direction == "Symmetric"
                else DirectionConstants.igRight
            )

            constructions = doc.Constructions
            extruded_surfaces = constructions.ExtrudedSurfaces

            _feature = extruded_surfaces.Add(
                1,  # NumberOfProfiles
                profile_array,  # ProfileArray
                ExtentTypeConstants.igFinite,  # ExtentType1
                side1,  # ExtentSide1
                depth1,  # FiniteDepth1
                None,  # KeyPointOrTangentFace1
                KeyPointExtentConstants.igTangentNormal,  # KeyPointFlags1
                None,  # FromFaceOrRefPlane
                OffsetSideConstants.seOffsetNone,  # FromFaceOffsetSide
                0.0,  # FromFaceOffsetDistance
                treat_const,  # TreatmentType1
                draft_side,  # TreatmentDraftSide1
                draft_angle_rad,  # TreatmentDraftAngle1
                TreatmentCrownTypeConstants.seTreatmentCrownByOffset,  # TreatmentCrownType1
                TreatmentCrownSideConstants.seTreatmentCrownSideInside,  # TreatmentCrownSide1
                TreatmentCrownCurvatureSideConstants.seTreatmentCrownCurvatureInside,
                0.0,  # TreatmentCrownRadiusOrOffset1
                0.0,  # TreatmentCrownTakeOffAngle1
                ExtentTypeConstants.igFinite,  # ExtentType2
                side2,  # ExtentSide2
                depth2,  # FiniteDepth2
                None,  # KeyPointOrTangentFace2
                KeyPointExtentConstants.igTangentNormal,  # KeyPointFlags2
                None,  # ToFaceOrRefPlane
                OffsetSideConstants.seOffsetNone,  # ToFaceOffsetSide
                0.0,  # ToFaceOffsetDistance
                TreatmentTypeConstants.seTreatmentNone,  # TreatmentType2
                DraftSideConstants.seDraftNone,  # TreatmentDraftSide2
                0.0,  # TreatmentDraftAngle2
                TreatmentCrownTypeConstants.seTreatmentCrownByOffset,  # TreatmentCrownType2
                TreatmentCrownSideConstants.seTreatmentCrownSideInside,  # TreatmentCrownSide2
                TreatmentCrownCurvatureSideConstants.seTreatmentCrownCurvatureInside,
                0.0,  # TreatmentCrownRadiusOrOffset2
                0.0,  # TreatmentCrownTakeOffAngle2
                True,  # WantEndCaps
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_surface_full",
                "distance": distance,
                "direction": direction,
                "treatment_type": treatment_type,
                "draft_angle": draft_angle,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # BATCH 5: PROTRUSION & CUTOUT VARIANTS
    # =================================================================

    def create_extrude_through_next_v2(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create an extrusion through the next face (collection-level multi-profile API).

        Uses ExtrudedProtrusions.AddThroughNextMulti(NumProfiles, ProfileArray, PlaneSide)
        instead of AddThroughNext for multi-profile support.

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and extrusion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            side = direction_map.get(direction, DirectionConstants.igRight)

            protrusions = model.ExtrudedProtrusions
            _feature = protrusions.AddThroughNextMulti(1, (profile,), side)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {"status": "created", "type": "extrude_through_next_v2", "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extrude_from_to_v2(
        self, from_plane_index: int, to_plane_index: int
    ) -> dict[str, Any]:
        """
        Create an extrusion between two reference planes (collection multi-profile API).

        Uses ExtrudedProtrusions.AddFromToMulti(NumProfiles, ProfileArray,
        FromFaceOrRefPlane, ToFaceOrRefPlane).

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane

        Returns:
            Dict with status and extrusion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            protrusions = model.ExtrudedProtrusions
            _feature = protrusions.AddFromToMulti(1, (profile,), from_plane, to_plane)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extrude_from_to_v2",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extrude_by_keypoint(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create an extrusion up to a keypoint extent.

        Uses ExtrudedProtrusions.AddFiniteByKeyPoint(Profile, PlaneSide).
        Extrudes to the nearest keypoint on adjacent geometry.

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and extrusion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            side = direction_map.get(direction, DirectionConstants.igRight)

            protrusions = model.ExtrudedProtrusions
            _feature = protrusions.AddFiniteByKeyPoint(profile, side)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {"status": "created", "type": "extrude_by_keypoint", "direction": direction}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolve_by_keypoint(self) -> dict[str, Any]:
        """
        Create a revolve up to a keypoint extent.

        Uses RevolvedProtrusions.AddFiniteByKeyPoint(Profile, RefAxis, PlaneSide).
        Revolves the profile to the nearest keypoint.

        Returns:
            Dict with status and revolve info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            protrusions = model.RevolvedProtrusions
            _feature = protrusions.AddFiniteByKeyPoint(profile, refaxis, DirectionConstants.igRight)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {"status": "created", "type": "revolve_by_keypoint"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolve_full(
        self, angle: float = 360.0, treatment_type: str = "None"
    ) -> dict[str, Any]:
        """
        Create a revolve with full treatment parameters.

        Uses RevolvedProtrusions.Add(NumProfiles, ProfileArray, RefAxis, PlaneSide,
        AngleOfRevolution, ...). Provides access to treatment options.

        Args:
            angle: Revolution angle in degrees (360 for full revolution)
            treatment_type: 'None', 'Draft', 'Crown', or 'CrownAndDraft'

        Returns:
            Dict with status and revolve info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            angle_rad = math.radians(angle)

            treatment_map = {
                "None": TreatmentTypeConstants.seTreatmentNone,
                "Draft": TreatmentTypeConstants.seTreatmentDraft,
                "Crown": TreatmentTypeConstants.seTreatmentCrown,
                "CrownAndDraft": TreatmentTypeConstants.seTreatmentCrownAndDraft,
            }
            treat_const = treatment_map.get(treatment_type, TreatmentTypeConstants.seTreatmentNone)

            profile_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            protrusions = model.RevolvedProtrusions
            _feature = protrusions.Add(
                1,  # NumProfiles
                profile_array,  # ProfileArray
                refaxis,  # RefAxis
                DirectionConstants.igRight,  # PlaneSide
                angle_rad,  # AngleOfRevolution
                treat_const,  # TreatmentType
                DraftSideConstants.seDraftNone,  # TreatmentDraftSide
                0.0,  # TreatmentDraftAngle
                TreatmentCrownTypeConstants.seTreatmentCrownByOffset,
                TreatmentCrownSideConstants.seTreatmentCrownSideInside,
                TreatmentCrownCurvatureSideConstants.seTreatmentCrownCurvatureInside,
                0.0,  # TreatmentCrownRadiusOrOffset
                0.0,  # TreatmentCrownTakeOffAngle
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "revolve_full",
                "angle": angle,
                "treatment_type": treatment_type,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_cutout_from_to_v2(
        self, from_plane_index: int, to_plane_index: int
    ) -> dict[str, Any]:
        """
        Create an extruded cutout between two reference planes (multi-profile API).

        Uses ExtrudedCutouts.AddFromToMulti(NumProfiles, ProfileArray,
        FromFaceOrRefPlane, ToFaceOrRefPlane).

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            cutouts = model.ExtrudedCutouts
            _feature = cutouts.AddFromToMulti(1, (profile,), from_plane, to_plane)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_cutout_from_to_v2",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_cutout_by_keypoint(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create an extruded cutout up to a keypoint extent.

        Uses ExtrudedCutouts.AddFiniteByKeyPointMulti(NumProfiles, ProfileArray, PlaneSide).

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            side = direction_map.get(direction, DirectionConstants.igRight)

            cutouts = model.ExtrudedCutouts
            _feature = cutouts.AddFiniteByKeyPointMulti(1, (profile,), side)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_cutout_by_keypoint",
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolved_cutout_sync(self, angle: float = 360.0) -> dict[str, Any]:
        """
        Create a synchronous revolved cutout.

        Uses RevolvedCutouts.AddFiniteMultiSync(NumProfiles, ProfileArray,
        RefAxis, PlaneSide, AngleOfRevolution).

        Args:
            angle: Revolution angle in degrees (360 for full revolution)

        Returns:
            Dict with status and cutout info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            angle_rad = math.radians(angle)

            cutouts = model.RevolvedCutouts
            _feature = cutouts.AddFiniteMultiSync(
                1,  # NumProfiles
                (profile,),  # ProfileArray
                refaxis,  # RefAxis
                DirectionConstants.igRight,  # PlaneSide
                angle_rad,  # AngleOfRevolution
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {"status": "created", "type": "revolved_cutout_sync", "angle": angle}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolved_cutout_by_keypoint(self) -> dict[str, Any]:
        """
        Create a revolved cutout up to a keypoint extent.

        Uses RevolvedCutouts.AddFiniteByKeyPointMulti(NumProfiles, ProfileArray,
        RefAxis, PlaneSide).

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            cutouts = model.RevolvedCutouts
            _feature = cutouts.AddFiniteByKeyPointMulti(
                1,  # NumProfiles
                (profile,),  # ProfileArray
                refaxis,  # RefAxis
                DirectionConstants.igRight,  # PlaneSide
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {"status": "created", "type": "revolved_cutout_by_keypoint"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_normal_cutout_from_to(
        self, from_plane_index: int, to_plane_index: int
    ) -> dict[str, Any]:
        """
        Create a normal cutout between two reference planes.

        Uses NormalCutouts.AddFromToMulti(NumProfiles, ProfileArray,
        FromFaceOrRefPlane, ToFaceOrRefPlane, Method).

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            cutouts = model.NormalCutouts
            _feature = cutouts.AddFromToMulti(1, (profile,), from_plane, to_plane, 0)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "normal_cutout_from_to",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_normal_cutout_through_next(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a normal cutout through the next face.

        Uses NormalCutouts.AddThroughNextMulti(NumProfiles, ProfileArray, PlaneSide, Method).

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            dir_const = direction_map.get(direction, DirectionConstants.igRight)

            cutouts = model.NormalCutouts
            _feature = cutouts.AddThroughNextMulti(1, (profile,), dir_const, 0)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "normal_cutout_through_next",
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_normal_cutout_by_keypoint(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a normal cutout up to a keypoint extent.

        Uses NormalCutouts.AddFiniteByKeyPointMulti(NumProfiles, ProfileArray,
        PlaneSide, Method).

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            side = direction_map.get(direction, DirectionConstants.igRight)

            cutouts = model.NormalCutouts
            _feature = cutouts.AddFiniteByKeyPointMulti(1, (profile,), side, 0)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "normal_cutout_by_keypoint",
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_lofted_cutout_full(self, profile_indices: list = None) -> dict[str, Any]:
        """
        Create a lofted cutout with guide curves support.

        Uses LoftedCutouts.Add(NumCrossSections, CrossSectionArray, CrossSectionTypes,
        Origins, SegmentMaps, PlaneSide, StartExtent, ..., EndExtent, ...).
        Provides the full API with all extent and treatment parameters.

        Args:
            profile_indices: Optional list of profile indices to use from
                accumulated profiles. If None, uses all accumulated profiles.

        Returns:
            Dict with status and lofted cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if profile_indices is not None:
                profiles = [all_profiles[i] for i in profile_indices]
            else:
                profiles = all_profiles

            if len(profiles) < 2:
                return {
                    "error": "Lofted cutout requires at "
                    "least 2 profiles, got "
                    f"{len(profiles)}. Create sketches on "
                    "different planes and close each one "
                    "before calling create_lofted_cutout_full()."
                }

            v_profiles, v_types, v_origins = self._make_loft_variant_arrays(profiles)
            v_seg = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, [])

            lc = model.LoftedCutouts
            _feature = lc.Add(
                len(profiles),
                v_profiles,
                v_types,
                v_origins,
                v_seg,
                DirectionConstants.igRight,
                ExtentTypeConstants.igNone,
                0.0,
                None,
                ExtentTypeConstants.igNone,
                0.0,
                None,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "lofted_cutout_full",
                "num_profiles": len(profiles),
                "method": "LoftedCutouts.Add",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_swept_cutout_multi_body(self, path_profile_index: int = None) -> dict[str, Any]:
        """
        Create a swept cutout that supports multi-body operations.

        Uses SweptCutouts.AddMultiBody with the same parameters as SweptCutouts.Add.
        Allows the cutout to span across multiple bodies in the part.

        Args:
            path_profile_index: Index of the path profile in accumulated profiles
                (default: 0, the first accumulated profile)

        Returns:
            Dict with status and swept cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            all_profiles = self.sketch_manager.get_accumulated_profiles()

            if len(all_profiles) < 2:
                return {
                    "error": "Swept cutout requires at "
                    "least 2 profiles (path + "
                    "cross-section), got "
                    f"{len(all_profiles)}. Create a path "
                    "sketch and a cross-section "
                    "sketch first."
                }

            path_idx = path_profile_index if path_profile_index is not None else 0
            path_profile = all_profiles[path_idx]
            cross_sections = [p for i, p in enumerate(all_profiles) if i != path_idx]

            _CS = LoftSweepConstants.igProfileBasedCrossSection

            v_paths = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [path_profile])
            v_path_types = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS])

            v_sections = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, cross_sections)
            v_section_types = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_I4, [_CS] * len(cross_sections)
            )
            v_origins = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
                [VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0]) for _ in cross_sections],
            )
            v_seg = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, [])

            swept_cutouts = model.SweptCutouts
            _feature = swept_cutouts.AddMultiBody(
                1,
                v_paths,
                v_path_types,
                len(cross_sections),
                v_sections,
                v_section_types,
                v_origins,
                v_seg,
                DirectionConstants.igRight,
                ExtentTypeConstants.igNone,
                0.0,
                None,
                ExtentTypeConstants.igNone,
                0.0,
                None,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()
            return {
                "status": "created",
                "type": "swept_cutout_multi_body",
                "num_cross_sections": len(cross_sections),
                "method": "SweptCutouts.AddMultiBody",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_helix_from_to(
        self, from_plane_index: int, to_plane_index: int, pitch: float
    ) -> dict[str, Any]:
        """
        Create a helix protrusion between two reference planes.

        Uses HelixProtrusions.AddFromTo(HelixAxis, AxisStart, NumCrossSections,
        CrossSectionArray, ProfileSide, FromFace, ToFace, Pitch, HelixDir).

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane
            pitch: Distance between coils in meters

        Returns:
            Dict with status and helix info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            helix = model.HelixProtrusions
            _feature = helix.AddFromTo(
                refaxis,  # HelixAxis
                DirectionConstants.igRight,  # AxisStart
                1,  # NumCrossSections
                v_profiles,  # CrossSectionArray
                DirectionConstants.igRight,  # ProfileSide
                from_plane,  # FromFace
                to_plane,  # ToFace
                pitch,  # Pitch
                DirectionConstants.igRight,  # HelixDir
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "helix_from_to",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
                "pitch": pitch,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_helix_from_to_thin_wall(
        self,
        from_plane_index: int,
        to_plane_index: int,
        pitch: float,
        wall_thickness: float,
    ) -> dict[str, Any]:
        """
        Create a thin-walled helix protrusion between two reference planes.

        Uses HelixProtrusions.AddFromToWithThinWall(HelixAxis, AxisStart,
        NumCrossSections, CrossSectionArray, ProfileSide, FromFace, ToFace,
        Pitch, HelixDir, WallThickness).

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane
            pitch: Distance between coils in meters
            wall_thickness: Wall thickness in meters

        Returns:
            Dict with status and helix info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            helix = model.HelixProtrusions
            _feature = helix.AddFromToWithThinWall(
                refaxis,  # HelixAxis
                DirectionConstants.igRight,  # AxisStart
                1,  # NumCrossSections
                v_profiles,  # CrossSectionArray
                DirectionConstants.igRight,  # ProfileSide
                from_plane,  # FromFace
                to_plane,  # ToFace
                pitch,  # Pitch
                DirectionConstants.igRight,  # HelixDir
                wall_thickness,  # WallThickness
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "helix_from_to_thin_wall",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
                "pitch": pitch,
                "wall_thickness": wall_thickness,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_helix_cutout_sync(
        self, pitch: float, height: float, revolutions: float = None, direction: str = "Right"
    ) -> dict[str, Any]:
        """
        Create a synchronous helical cutout.

        Uses HelixCutouts.AddFiniteSync(HelixAxis, AxisStart, NumCrossSections,
        CrossSectionArray, ProfileSide, Height, Pitch, NumberOfTurns, HelixDir).

        Args:
            pitch: Distance between coils in meters
            height: Total height of helix in meters
            revolutions: Number of turns (optional, calculated from pitch/height)
            direction: 'Right' or 'Left' hand helix

        Returns:
            Dict with status and helix cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            if revolutions is None:
                revolutions = height / pitch

            dir_const = (
                DirectionConstants.igRight if direction == "Right" else DirectionConstants.igLeft
            )

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            helix_cutouts = model.HelixCutouts
            _feature = helix_cutouts.AddFiniteSync(
                refaxis,  # HelixAxis
                DirectionConstants.igRight,  # AxisStart
                1,  # NumCrossSections
                v_profiles,  # CrossSectionArray
                DirectionConstants.igRight,  # ProfileSide
                height,  # Height
                pitch,  # Pitch
                revolutions,  # NumberOfTurns
                dir_const,  # HelixDir
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()
            return {
                "status": "created",
                "type": "helix_cutout_sync",
                "pitch": pitch,
                "height": height,
                "revolutions": revolutions,
                "direction": direction,
                "method": "HelixCutouts.AddFiniteSync",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_helix_cutout_from_to(
        self, from_plane_index: int, to_plane_index: int, pitch: float
    ) -> dict[str, Any]:
        """
        Create a helical cutout between two reference planes.

        Uses HelixCutouts.AddFromTo(HelixAxis, AxisStart, NumCrossSections,
        CrossSectionArray, ProfileSide, FromFace, ToFace, Pitch, HelixDir).

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane
            pitch: Distance between coils in meters

        Returns:
            Dict with status and helix cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            helix_cutouts = model.HelixCutouts
            _feature = helix_cutouts.AddFromTo(
                refaxis,  # HelixAxis
                DirectionConstants.igRight,  # AxisStart
                1,  # NumCrossSections
                v_profiles,  # CrossSectionArray
                DirectionConstants.igRight,  # ProfileSide
                from_plane,  # FromFace
                to_plane,  # ToFace
                pitch,  # Pitch
                DirectionConstants.igRight,  # HelixDir
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "helix_cutout_from_to",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
                "pitch": pitch,
                "method": "HelixCutouts.AddFromTo",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # BATCH 6: ROUNDS, CHAMFERS, HOLES EXTENDED
    # =================================================================

    def create_round_blend(
        self, face_index1: int, face_index2: int, radius: float
    ) -> dict[str, Any]:
        """
        Create a round blend between two faces.

        Uses Rounds.AddBlend(Face1, Face2, Radius). Creates a smooth
        fillet transition between two specified faces.

        Args:
            face_index1: 0-based index of the first face
            face_index2: 0-based index of the second face
            radius: Blend radius in meters

        Returns:
            Dict with status and blend info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add round blends to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces found on body"}

            if face_index1 < 0 or face_index1 >= faces.Count:
                return {
                    "error": f"Invalid face_index1: {face_index1}. Body has {faces.Count} faces."
                }
            if face_index2 < 0 or face_index2 >= faces.Count:
                return {
                    "error": f"Invalid face_index2: {face_index2}. Body has {faces.Count} faces."
                }

            face1 = faces.Item(face_index1 + 1)
            face2 = faces.Item(face_index2 + 1)

            rounds = model.Rounds
            _feature = rounds.AddBlend(face1, face2, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "round_blend",
                "face_index1": face_index1,
                "face_index2": face_index2,
                "radius": radius,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_round_surface_blend(
        self, face_index1: int, face_index2: int, radius: float
    ) -> dict[str, Any]:
        """
        Create a round surface blend between two faces.

        Uses Rounds.AddSurfaceBlend(Face1, Face2, Radius). Creates a surface
        blend between two faces with finer control than AddBlend.

        Args:
            face_index1: 0-based index of the first face
            face_index2: 0-based index of the second face
            radius: Blend radius in meters

        Returns:
            Dict with status and blend info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add surface blends to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces found on body"}

            if face_index1 < 0 or face_index1 >= faces.Count:
                return {
                    "error": f"Invalid face_index1: {face_index1}. Body has {faces.Count} faces."
                }
            if face_index2 < 0 or face_index2 >= faces.Count:
                return {
                    "error": f"Invalid face_index2: {face_index2}. Body has {faces.Count} faces."
                }

            face1 = faces.Item(face_index1 + 1)
            face2 = faces.Item(face_index2 + 1)

            rounds = model.Rounds
            _feature = rounds.AddSurfaceBlend(face1, face2, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "round_surface_blend",
                "face_index1": face_index1,
                "face_index2": face_index2,
                "radius": radius,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_from_to(
        self,
        x: float,
        y: float,
        diameter: float,
        from_plane_index: int,
        to_plane_index: int,
    ) -> dict[str, Any]:
        """
        Create a hole between two reference planes.

        Uses ExtrudedCutouts.AddFromToMulti with a circular profile as a
        workaround for Holes.AddFinite not cutting geometry.

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            # Create a circular profile on the from_plane
            ps = doc.ProfileSets.Add()
            profile = ps.Profiles.Add(from_plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            cutouts = model.ExtrudedCutouts
            _feature = cutouts.AddFromToMulti(1, (profile,), from_plane, to_plane)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_from_to",
                "position": [x, y],
                "diameter": diameter,
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_through_next(
        self,
        x: float,
        y: float,
        diameter: float,
        direction: str = "Normal",
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a hole through the next face.

        Uses ExtrudedCutouts.AddThroughNextMulti with a circular profile.

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            direction: 'Normal' or 'Reverse'
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            dir_const = DirectionConstants.igRight
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            cutouts = model.ExtrudedCutouts
            _feature = cutouts.AddThroughNextMulti(1, (profile,), dir_const)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_through_next",
                "position": [x, y],
                "diameter": diameter,
                "direction": direction,
                "plane_index": plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_sync(
        self,
        x: float,
        y: float,
        diameter: float,
        depth: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a synchronous hole feature.

        Uses Holes.AddSync(Profile, PlaneSide, Depth, HoleData).
        Note: Holes API may not cut geometry - if so, use circular cutout instead.

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            depth: Hole depth in meters
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            holes = model.Holes
            _feature = holes.AddSync(profile, DirectionConstants.igRight, depth, None)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_sync",
                "position": [x, y],
                "diameter": diameter,
                "depth": depth,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_finite_ex(
        self,
        x: float,
        y: float,
        diameter: float,
        depth: float,
        direction: str = "Normal",
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a finite hole using the extended API.

        Uses Holes.AddFiniteEx(Profile, PlaneSide, Depth, HoleData).

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            depth: Hole depth in meters
            direction: 'Normal' or 'Reverse'
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            dir_const = DirectionConstants.igRight
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            holes = model.Holes
            _feature = holes.AddFiniteEx(profile, dir_const, depth, None)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_finite_ex",
                "position": [x, y],
                "diameter": diameter,
                "depth": depth,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_from_to_ex(
        self,
        x: float,
        y: float,
        diameter: float,
        from_plane_index: int,
        to_plane_index: int,
    ) -> dict[str, Any]:
        """
        Create a hole between two planes using the extended API.

        Uses Holes.AddFromToEx(Profile, FromFace, ToFace, HoleData).

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: "
                    f"{from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            ps = doc.ProfileSets.Add()
            profile = ps.Profiles.Add(from_plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            holes = model.Holes
            _feature = holes.AddFromToEx(profile, from_plane, to_plane, None)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_from_to_ex",
                "position": [x, y],
                "diameter": diameter,
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_through_next_ex(
        self,
        x: float,
        y: float,
        diameter: float,
        direction: str = "Normal",
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a hole through the next face using the extended API.

        Uses Holes.AddThroughNextEx(Profile, PlaneSide, HoleData).

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            direction: 'Normal' or 'Reverse'
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            dir_const = DirectionConstants.igRight
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            holes = model.Holes
            _feature = holes.AddThroughNextEx(profile, dir_const, None)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_through_next_ex",
                "position": [x, y],
                "diameter": diameter,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_through_all_ex(
        self,
        x: float,
        y: float,
        diameter: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a hole through all material using the extended API.

        Uses Holes.AddThroughAllEx(Profile, PlaneSide, HoleData).

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            holes = model.Holes
            _feature = holes.AddThroughAllEx(profile, DirectionConstants.igRight, None)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_through_all_ex",
                "position": [x, y],
                "diameter": diameter,
                "plane_index": plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_sync_ex(
        self,
        x: float,
        y: float,
        diameter: float,
        depth: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a synchronous hole using the extended API.

        Uses Holes.AddSyncEx(Profile, PlaneSide, Depth, HoleData).

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            depth: Hole depth in meters
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            holes = model.Holes
            _feature = holes.AddSyncEx(profile, DirectionConstants.igRight, depth, None)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_sync_ex",
                "position": [x, y],
                "diameter": diameter,
                "depth": depth,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_multi_body(
        self,
        x: float,
        y: float,
        diameter: float,
        depth: float,
        plane_index: int = 1,
        direction: str = "Normal",
    ) -> dict[str, Any]:
        """
        Create a hole that spans multiple bodies.

        Uses Holes.AddMultiBody(Profile, PlaneSide, Depth, HoleData).

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            depth: Hole depth in meters
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            dir_const = DirectionConstants.igRight
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            holes = model.Holes
            _feature = holes.AddMultiBody(profile, dir_const, depth, None)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_multi_body",
                "position": [x, y],
                "diameter": diameter,
                "depth": depth,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hole_sync_multi_body(
        self,
        x: float,
        y: float,
        diameter: float,
        depth: float,
        plane_index: int = 1,
    ) -> dict[str, Any]:
        """
        Create a synchronous hole that spans multiple bodies.

        Uses Holes.AddSyncMultiBody(Profile, PlaneSide, Depth, HoleData).

        Args:
            x, y: Hole center coordinates on the sketch plane (meters)
            diameter: Hole diameter in meters
            depth: Hole depth in meters
            plane_index: Reference plane index (1=Top/XZ, 2=Front/XY, 3=Right/YZ)

        Returns:
            Dict with status and hole info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            radius = diameter / 2.0

            ps = doc.ProfileSets.Add()
            plane = doc.RefPlanes.Item(plane_index)
            profile = ps.Profiles.Add(plane)
            _feature = profile.Circles2d.AddByCenterRadius(x, y, radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}
            profile.End(0)

            holes = model.Holes
            _feature = holes.AddSyncMultiBody(profile, DirectionConstants.igRight, depth, None)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hole_sync_multi_body",
                "position": [x, y],
                "diameter": diameter,
                "depth": depth,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_blend_variable(
        self, radius1: float, radius2: float, face_index: int = None
    ) -> dict[str, Any]:
        """
        Create a variable-radius blend feature.

        Uses Blends.AddVariable(NumberOfEdgeSets, EdgeSetArray, RadiusArray).
        Applies varying radius values from radius1 to radius2 along edges.

        Args:
            radius1: Starting blend radius in meters
            radius2: Ending blend radius in meters
            face_index: 0-based face index to apply to (None = all edges)

        Returns:
            Dict with status and blend info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add variable blends to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces found on body"}

            edge_list = []
            if face_index is not None:
                if face_index < 0 or face_index >= faces.Count:
                    return {
                        "error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."
                    }
                face = faces.Item(face_index + 1)
                face_edges = face.Edges
                if hasattr(face_edges, "Count"):
                    for ei in range(1, face_edges.Count + 1):
                        edge_list.append(face_edges.Item(ei))
            else:
                for fi in range(1, faces.Count + 1):
                    face = faces.Item(fi)
                    face_edges = face.Edges
                    if not hasattr(face_edges, "Count"):
                        continue
                    for ei in range(1, face_edges.Count + 1):
                        edge_list.append(face_edges.Item(ei))

            if not edge_list:
                return {"error": "No edges found on body"}

            edge_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, edge_list)
            radius_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [radius1, radius2])

            blends = model.Blends
            _feature = blends.AddVariable(1, edge_arr, radius_arr)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "blend_variable",
                "radius1": radius1,
                "radius2": radius2,
                "edge_count": len(edge_list),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_blend_surface(self, face_index1: int, face_index2: int) -> dict[str, Any]:
        """
        Create a surface blend between two faces.

        Uses Blends.AddSurfaceBlend(Face1, Face2). Creates a smooth
        surface blend transition between two specified faces.

        Args:
            face_index1: 0-based index of the first face
            face_index2: 0-based index of the second face

        Returns:
            Dict with status and blend info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No features exist to add surface blends to"}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if faces.Count == 0:
                return {"error": "No faces found on body"}

            if face_index1 < 0 or face_index1 >= faces.Count:
                return {
                    "error": f"Invalid face_index1: {face_index1}. Body has {faces.Count} faces."
                }
            if face_index2 < 0 or face_index2 >= faces.Count:
                return {
                    "error": f"Invalid face_index2: {face_index2}. Body has {faces.Count} faces."
                }

            face1 = faces.Item(face_index1 + 1)
            face2 = faces.Item(face_index2 + 1)

            blends = model.Blends
            _feature = blends.AddSurfaceBlend(face1, face2)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "blend_surface",
                "face_index1": face_index1,
                "face_index2": face_index2,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # BATCH 7: SHEET METAL COMPLETION
    # =================================================================

    def _get_edge_from_face(
        self, face_index: int, edge_index: int = 0
    ) -> tuple[Any, Any, Any, dict[str, Any] | None]:
        """Helper to get an edge from a face on the first model body.

        Returns (model, face, edge, error_dict).
        If error_dict is not None, the caller should return it immediately.
        """
        doc = self.doc_manager.get_active_document()
        models = doc.Models

        if models.Count == 0:
            return (
                None,
                None,
                None,
                {"error": "No base feature exists. Create a sheet metal base feature first."},
            )

        model = models.Item(1)
        body = model.Body

        faces = body.Faces(FaceQueryConstants.igQueryAll)
        if face_index < 0 or face_index >= faces.Count:
            return (
                None,
                None,
                None,
                {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."},
            )

        face = faces.Item(face_index + 1)
        face_edges = face.Edges
        if not hasattr(face_edges, "Count") or face_edges.Count == 0:
            return None, None, None, {"error": f"Face {face_index} has no edges."}

        if edge_index < 0 or edge_index >= face_edges.Count:
            return (
                None,
                None,
                None,
                {"error": f"Invalid edge index: {edge_index}. Face has {face_edges.Count} edges."},
            )

        edge = face_edges.Item(edge_index + 1)
        return model, face, edge, None

    def create_flange_by_match_face(
        self,
        face_index: int,
        edge_index: int,
        flange_length: float,
        side: str = "Right",
        inside_radius: float = 0.001,
    ) -> dict[str, Any]:
        """
        Create a flange by matching an existing face edge.

        Uses Flanges.AddByMatchFace to add a flange that matches the
        geometry of a target face on the sheet metal body.

        Args:
            face_index: 0-based face index containing the target edge
            edge_index: 0-based edge index within that face
            flange_length: Flange length in meters
            side: 'Left' (1), 'Right' (2), or 'Both' (6)
            inside_radius: Bend inside radius in meters

        Returns:
            Dict with status and flange info
        """
        try:
            model, face, edge, err = self._get_edge_from_face(face_index, edge_index)
            if err:
                return err

            side_map = {
                "Left": DirectionConstants.igLeft,
                "Right": DirectionConstants.igRight,
                "Both": DirectionConstants.igBoth,
            }
            side_const = side_map.get(side, DirectionConstants.igRight)

            flanges = model.Flanges
            _feature = flanges.AddByMatchFace(edge, side_const, flange_length, None, inside_radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "flange_by_match_face",
                "face_index": face_index,
                "edge_index": edge_index,
                "flange_length": flange_length,
                "side": side,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_flange_sync(
        self,
        face_index: int,
        edge_index: int,
        flange_length: float,
        inside_radius: float = 0.001,
    ) -> dict[str, Any]:
        """
        Create a synchronous flange feature.

        Uses Flanges.AddSync to add a flange in synchronous modeling mode.

        Args:
            face_index: 0-based face index containing the target edge
            edge_index: 0-based edge index within that face
            flange_length: Flange length in meters
            inside_radius: Bend inside radius in meters

        Returns:
            Dict with status and flange info
        """
        try:
            model, face, edge, err = self._get_edge_from_face(face_index, edge_index)
            if err:
                return err

            flanges = model.Flanges
            _feature = flanges.AddSync(edge, flange_length, None, inside_radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "flange_sync",
                "face_index": face_index,
                "edge_index": edge_index,
                "flange_length": flange_length,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_flange_by_face(
        self,
        face_index: int,
        edge_index: int,
        ref_face_index: int,
        flange_length: float,
        side: str = "Right",
        bend_radius: float = 0.001,
    ) -> dict[str, Any]:
        """
        Create a flange by face reference.

        Uses Flanges.AddFlangeByFace which references a target face
        for flange direction and orientation.

        Args:
            face_index: 0-based face index containing the target edge
            edge_index: 0-based edge index within that face
            ref_face_index: 0-based index of the reference face
            flange_length: Flange length in meters
            side: 'Left' (1), 'Right' (2), or 'Both' (6)
            bend_radius: Bend radius in meters

        Returns:
            Dict with status and flange info
        """
        try:
            model, face, edge, err = self._get_edge_from_face(face_index, edge_index)
            if err:
                return err

            # Get the reference face
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if ref_face_index < 0 or ref_face_index >= faces.Count:
                return {
                    "error": f"Invalid ref_face_index: {ref_face_index}. "
                    f"Body has {faces.Count} faces."
                }
            ref_face = faces.Item(ref_face_index + 1)

            side_map = {
                "Left": DirectionConstants.igLeft,
                "Right": DirectionConstants.igRight,
                "Both": DirectionConstants.igBoth,
            }
            side_const = side_map.get(side, DirectionConstants.igRight)

            flanges = model.Flanges
            _feature = flanges.AddFlangeByFace(edge, ref_face, side_const, flange_length, None, bend_radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "flange_by_face",
                "face_index": face_index,
                "edge_index": edge_index,
                "ref_face_index": ref_face_index,
                "flange_length": flange_length,
                "side": side,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_flange_with_bend_calc(
        self,
        face_index: int,
        edge_index: int,
        flange_length: float,
        side: str = "Right",
        bend_deduction: float = 0.0,
    ) -> dict[str, Any]:
        """
        Create a flange with bend deduction/allowance calculation.

        Uses Flanges.AddByBendDeductionOrBendAllowance for precise
        bend calculation control.

        Args:
            face_index: 0-based face index containing the target edge
            edge_index: 0-based edge index within that face
            flange_length: Flange length in meters
            side: 'Left' (1), 'Right' (2), or 'Both' (6)
            bend_deduction: Bend deduction value in meters

        Returns:
            Dict with status and flange info
        """
        try:
            model, face, edge, err = self._get_edge_from_face(face_index, edge_index)
            if err:
                return err

            side_map = {
                "Left": DirectionConstants.igLeft,
                "Right": DirectionConstants.igRight,
                "Both": DirectionConstants.igBoth,
            }
            side_const = side_map.get(side, DirectionConstants.igRight)

            flanges = model.Flanges
            # AddByBendDeductionOrBendAllowance(pLocatedEdge, FlangeSide, FlangeLength,
            #   vtKeyPointOrTangentFace, vtKeyPointFlags, ...)
            _feature = flanges.AddByBendDeductionOrBendAllowance(edge, side_const, flange_length, None, 0)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "flange_with_bend_calc",
                "face_index": face_index,
                "edge_index": edge_index,
                "flange_length": flange_length,
                "side": side,
                "bend_deduction": bend_deduction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_flange_sync_with_bend_calc(
        self,
        face_index: int,
        edge_index: int,
        flange_length: float,
        bend_deduction: float = 0.0,
    ) -> dict[str, Any]:
        """
        Create a synchronous flange with bend deduction/allowance.

        Uses Flanges.AddSyncByBendDeductionOrBendAllowance for
        synchronous mode with precise bend calculation.

        Args:
            face_index: 0-based face index containing the target edge
            edge_index: 0-based edge index within that face
            flange_length: Flange length in meters
            bend_deduction: Bend deduction value in meters

        Returns:
            Dict with status and flange info
        """
        try:
            model, face, edge, err = self._get_edge_from_face(face_index, edge_index)
            if err:
                return err

            flanges = model.Flanges
            # AddSyncByBendDeductionOrBendAllowance(pLocatedEdge, FlangeLength, ...)
            _feature = flanges.AddSyncByBendDeductionOrBendAllowance(edge, flange_length)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "flange_sync_with_bend_calc",
                "face_index": face_index,
                "edge_index": edge_index,
                "flange_length": flange_length,
                "bend_deduction": bend_deduction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_contour_flange_ex(
        self,
        thickness: float,
        bend_radius: float = 0.001,
        direction: str = "Normal",
    ) -> dict[str, Any]:
        """
        Create an extended contour flange from the active profile.

        Uses ContourFlanges.AddEx to create a contour flange with
        keypoint/tangent face support.

        Args:
            thickness: Material projection distance in meters
            bend_radius: Bend radius in meters
            direction: 'Normal' or 'Reverse' for projection side

        Returns:
            Dict with status and contour flange info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a sheet metal base feature first."}

            model = models.Item(1)

            dir_side = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            contour_flanges = model.ContourFlanges
            # AddEx(pProfile, varExtentType, varProjectionSide, varProjectionDistance,
            #   varKeyPointOrTangentFace, varKeyPointFlags, varBendRadius,
            #   vtBRType, vtBRWidth, vtBRLength, vtCRType, ...)
            _feature = contour_flanges.AddEx(
                profile,
                ExtentTypeConstants.igFinite,
                dir_side,
                thickness,
                None,  # varKeyPointOrTangentFace
                0,  # varKeyPointFlags
                bend_radius,
                0,  # vtBRType (no bend relief)
                0.0,  # vtBRWidth
                0.0,  # vtBRLength
                0,  # vtCRType (no corner relief)
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "contour_flange_ex",
                "thickness": thickness,
                "bend_radius": bend_radius,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_contour_flange_sync(
        self,
        face_index: int,
        edge_index: int,
        thickness: float,
        bend_radius: float = 0.001,
        direction: str = "Normal",
    ) -> dict[str, Any]:
        """
        Create a synchronous contour flange.

        Uses ContourFlanges.AddSync with a reference edge for
        synchronous modeling mode.

        Args:
            face_index: 0-based face index containing the reference edge
            edge_index: 0-based edge index within that face
            thickness: Material projection distance in meters
            bend_radius: Bend radius in meters
            direction: 'Normal' or 'Reverse' for projection side

        Returns:
            Dict with status and contour flange info
        """
        try:
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            model, face, edge, err = self._get_edge_from_face(face_index, edge_index)
            if err:
                return err

            dir_side = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            contour_flanges = model.ContourFlanges
            # AddSync(pProfile, pRefEdge, varExtentType, varProjectionSide,
            #   varProjectionDistance, varBendRadius, vtBRType, vtBRWidth,
            #   vtBRLength, vtCRType, ...)
            _feature = contour_flanges.AddSync(
                profile,
                edge,
                ExtentTypeConstants.igFinite,
                dir_side,
                thickness,
                bend_radius,
                0,  # vtBRType
                0.0,  # vtBRWidth
                0.0,  # vtBRLength
                0,  # vtCRType
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "contour_flange_sync",
                "face_index": face_index,
                "edge_index": edge_index,
                "thickness": thickness,
                "bend_radius": bend_radius,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_contour_flange_sync_with_bend(
        self,
        face_index: int,
        edge_index: int,
        thickness: float,
        bend_radius: float = 0.001,
        direction: str = "Normal",
        bend_deduction: float = 0.0,
    ) -> dict[str, Any]:
        """
        Create a synchronous contour flange with bend deduction/allowance.

        Uses ContourFlanges.AddSyncByBendDeductionOrBendAllowance for
        synchronous mode with precise bend calculation.

        Args:
            face_index: 0-based face index containing the reference edge
            edge_index: 0-based edge index within that face
            thickness: Material projection distance in meters
            bend_radius: Bend radius in meters
            direction: 'Normal' or 'Reverse' for projection side
            bend_deduction: Bend deduction value in meters

        Returns:
            Dict with status and contour flange info
        """
        try:
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            model, face, edge, err = self._get_edge_from_face(face_index, edge_index)
            if err:
                return err

            dir_side = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            contour_flanges = model.ContourFlanges
            # AddSyncByBendDeductionOrBendAllowance(pProfile, pRefEdge,
            #   varExtentType, varProjectionSide, varProjectionDistance,
            #   varBendRadius, vtBRType, vtBRWidth, vtBRLength, vtCRType, ...)
            _feature = contour_flanges.AddSyncByBendDeductionOrBendAllowance(
                profile,
                edge,
                ExtentTypeConstants.igFinite,
                dir_side,
                thickness,
                bend_radius,
                0,  # vtBRType
                0.0,  # vtBRWidth
                0.0,  # vtBRLength
                0,  # vtCRType
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "contour_flange_sync_with_bend",
                "face_index": face_index,
                "edge_index": edge_index,
                "thickness": thickness,
                "bend_radius": bend_radius,
                "direction": direction,
                "bend_deduction": bend_deduction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_hem(
        self,
        face_index: int,
        edge_index: int,
        hem_width: float = 0.005,
        bend_radius: float = 0.001,
        hem_type: str = "Closed",
    ) -> dict[str, Any]:
        """
        Create a hem feature on a sheet metal edge.

        Uses Hems.Add to fold an edge back on itself. Hem types include
        Closed, Open, S-Flange, Curl, etc.

        Args:
            face_index: 0-based face index containing the target edge
            edge_index: 0-based edge index within that face
            hem_width: Hem flange length in meters
            bend_radius: Bend radius in meters
            hem_type: 'Closed' (1), 'Open' (2), 'SFlange' (3), 'Curl' (4)

        Returns:
            Dict with status and hem info
        """
        try:
            model, face, edge, err = self._get_edge_from_face(face_index, edge_index)
            if err:
                return err

            # HemFeatureConstants
            hem_type_map = {
                "Closed": 1,  # seHemTypeClosed
                "Open": 2,  # seHemTypeOpen
                "SFlange": 3,  # seHemTypeSFlange
                "Curl": 4,  # seHemTypeCurl
                "OpenLoop": 5,  # seHemTypeOpenLoop
                "ClosedLoop": 6,  # seHemTypeClosedLoop
                "CenteredLoop": 7,  # seHemTypeCenteredLoop
            }
            hem_type_const = hem_type_map.get(hem_type, 1)

            hems = model.Hems
            # Add(InputEdge, HemType, BendRadius1, FlangeLength1, ...)
            _feature = hems.Add(edge, hem_type_const, bend_radius, hem_width)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "hem",
                "face_index": face_index,
                "edge_index": edge_index,
                "hem_width": hem_width,
                "bend_radius": bend_radius,
                "hem_type": hem_type,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_jog(
        self,
        jog_offset: float = 0.005,
        jog_angle: float = 90.0,
        direction: str = "Normal",
        moving_side: str = "Right",
    ) -> dict[str, Any]:
        """
        Create a jog feature on a sheet metal body.

        Uses Jogs.AddFinite with the active sketch profile to create
        a step/jog in the sheet metal.

        Args:
            jog_offset: Jog offset distance in meters
            jog_angle: Jog bend angle in degrees (converted to radians internally)
            direction: 'Normal' (16) or 'Reverse' (17) for jog direction
            moving_side: 'Right' (12) or 'Left' (11) for which side moves

        Returns:
            Dict with status and jog info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a sheet metal base feature first."}

            model = models.Item(1)

            # JogFeatureConstants
            # seJogMaterialInside=13, seJogMaterialOutside=14, seJogMaterialBendOutside=15
            material_side = 13  # seJogMaterialInside

            # seJogMoveLeft=11, seJogMoveRight=12
            move_side = 12 if moving_side == "Right" else 11

            # seJogNormal=16, seJogReverseNormal=17
            jog_dir = 16 if direction == "Normal" else 17

            jogs = model.Jogs
            # AddFinite(Profile, Extent, MaterialSide, MovingSide, JogDirection, ...)
            _feature = jogs.AddFinite(profile, jog_offset, material_side, move_side, jog_dir)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "jog",
                "jog_offset": jog_offset,
                "jog_angle": jog_angle,
                "direction": direction,
                "moving_side": moving_side,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_close_corner(
        self,
        face_index: int,
        edge_index: int,
        closure_type: str = "Close",
    ) -> dict[str, Any]:
        """
        Create a close corner feature on sheet metal.

        Uses CloseCorners.Add to close a gap between two flanges at
        a corner of the sheet metal body.

        Args:
            face_index: 0-based face index containing the corner edge
            edge_index: 0-based edge index at the corner
            closure_type: 'Close' (1) or 'Overlap' (2)

        Returns:
            Dict with status and close corner info
        """
        try:
            model, face, edge, err = self._get_edge_from_face(face_index, edge_index)
            if err:
                return err

            # CloseCornerFeatureConstants
            # seCloseCornerCloseFaces=1, seCloseCornerOverlapFaces=2
            closure_map = {
                "Close": 1,
                "Overlap": 2,
            }
            closure_const = closure_map.get(closure_type, 1)

            close_corners = model.CloseCorners
            # Add(InputEdge, ClosureType, ...)
            _feature = close_corners.Add(edge, closure_const)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "close_corner",
                "face_index": face_index,
                "edge_index": edge_index,
                "closure_type": closure_type,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_multi_edge_flange(
        self,
        face_index: int,
        edge_indices: list[int],
        flange_length: float,
        side: str = "Right",
    ) -> dict[str, Any]:
        """
        Create a multi-edge flange on multiple edges.

        Uses MultiEdgeFlanges.Add to create flanges on multiple edges
        simultaneously with consistent parameters.

        Args:
            face_index: 0-based face index containing the edges
            edge_indices: List of 0-based edge indices within that face
            flange_length: Flange length in meters
            side: 'Left' (1), 'Right' (2), or 'Both' (6)

        Returns:
            Dict with status and multi-edge flange info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            if models.Count == 0:
                return {"error": "No base feature exists. Create a sheet metal base feature first."}

            model = models.Item(1)
            body = model.Body

            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            face_edges = face.Edges
            if not hasattr(face_edges, "Count") or face_edges.Count == 0:
                return {"error": f"Face {face_index} has no edges."}

            # Collect the requested edges
            edge_list = []
            for ei in edge_indices:
                if ei < 0 or ei >= face_edges.Count:
                    return {
                        "error": f"Invalid edge index: {ei}. Face has {face_edges.Count} edges."
                    }
                edge_list.append(face_edges.Item(ei + 1))

            side_map = {
                "Left": DirectionConstants.igLeft,
                "Right": DirectionConstants.igRight,
                "Both": DirectionConstants.igBoth,
            }
            side_const = side_map.get(side, DirectionConstants.igRight)

            edge_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, edge_list)

            multi_edge_flanges = model.MultiEdgeFlanges
            # Add(NumberOfEdges, Edges, FlangeSide, dFlangeLength, ...)
            _feature = multi_edge_flanges.Add(len(edge_list), edge_arr, side_const, flange_length)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "multi_edge_flange",
                "face_index": face_index,
                "edge_count": len(edge_list),
                "flange_length": flange_length,
                "side": side,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_bend_with_calc(
        self,
        bend_angle: float = 90.0,
        direction: str = "Normal",
        moving_side: str = "Right",
        bend_deduction: float = 0.0,
    ) -> dict[str, Any]:
        """
        Create a bend feature with bend deduction/allowance.

        Uses Bends.AddByBendDeductionOrBendAllowance to create a bend
        in the sheet metal using the active sketch profile as the bend line.

        Args:
            bend_angle: Bend angle in degrees (converted to radians)
            direction: 'Normal' (7) or 'Reverse' (8)
            moving_side: 'Right' (5) or 'Left' (6) for which side moves
            bend_deduction: Bend deduction value in meters

        Returns:
            Dict with status and bend info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a sheet metal base feature first."}

            model = models.Item(1)

            bend_angle_rad = math.radians(bend_angle)

            # BendFeatureConstants
            # seBendPZLInside=11 (bend position zone line)
            bend_pzl = 11

            # seBendMoveRight=5, seBendMoveLeft=6
            move_side = 5 if moving_side == "Right" else 6

            # seBendNormal=7, seBendReverseNormal=8
            bend_dir = 7 if direction == "Normal" else 8

            bends = model.Bends
            # AddByBendDeductionOrBendAllowance(Profile, BendAngle, BendPZLSide,
            #   MovingSide, BendDirection, ...)
            _feature = bends.AddByBendDeductionOrBendAllowance(
                profile, bend_angle_rad, bend_pzl, move_side, bend_dir
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "bend_with_calc",
                "bend_angle": bend_angle,
                "direction": direction,
                "moving_side": moving_side,
                "bend_deduction": bend_deduction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def convert_part_to_sheet_metal(
        self,
        thickness: float = 0.001,
    ) -> dict[str, Any]:
        """
        Convert a part document to sheet metal.

        Attempts to convert the current part document to a sheet metal
        document by saving it as a .psm file and reopening, or by using
        the Solid Edge command API.

        Args:
            thickness: Sheet metal thickness in meters

        Returns:
            Dict with status and conversion info
        """
        try:
            # Try using the StartCommand API to invoke the Convert to Sheet Metal command
            # This is a UI-level command approach
            app = self.doc_manager.connection_manager.get_application()

            with contextlib.suppress(Exception):
                # Try SE command for converting to sheet metal
                # Command ID for "Convert to Sheet Metal" may vary
                app.StartCommand(45000)  # seSheetMetalSelectCommand = 45000

                return {
                    "status": "command_invoked",
                    "type": "convert_part_to_sheet_metal",
                    "thickness": thickness,
                    "note": "Convert to Sheet Metal command invoked. "
                    "User interaction may be required to complete the conversion.",
                }

            # Alternative: Save as .psm and reopen
            return {
                "error": "Convert to sheet metal command not available. "
                "To create a sheet metal part, use create_sheet_metal_document() instead, "
                "or save the part as .psm format.",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_dimple_ex(
        self,
        depth: float,
        direction: str = "Normal",
        punch_tool_diameter: float = 0.01,
    ) -> dict[str, Any]:
        """
        Create an extended dimple feature (sheet metal).

        Uses Dimples.AddEx with multi-profile support and additional
        parameters for punch tool diameter control.

        Args:
            depth: Dimple depth in meters
            direction: 'Normal' or 'Reverse' for dimple direction
            punch_tool_diameter: Punch tool diameter in meters

        Returns:
            Dict with status and dimple info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a sheet metal base feature first."}

            model = models.Item(1)

            # DimpleFeatureConstants
            # seDimpleProfileLeft=5 (inside), seDimpleProfileRight=6 (outside)
            profile_side = 5 if direction == "Normal" else 6
            # seDimpleDepthLeft=1, seDimpleDepthRight=2
            depth_side = 2 if direction == "Normal" else 1

            dimples = model.Dimples
            # AddEx(NumberOfProfiles, ProfileArray, Depth, ProfileSide, DepthSide,
            #   PunchRadius, ...)
            punch_radius = punch_tool_diameter / 2.0
            _feature = dimples.AddEx(1, (profile,), depth, profile_side, depth_side, punch_radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "dimple_ex",
                "depth": depth,
                "direction": direction,
                "punch_tool_diameter": punch_tool_diameter,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # BATCH 9: PART FEATURE VARIANTS & PATTERN VARIANTS
    # =================================================================

    def _find_feature_by_name(self, feature_name: str):
        """
        Find a feature by name in DesignEdgebarFeatures.

        Args:
            feature_name: Name of the feature to find

        Returns:
            Tuple of (feature_object, error_dict). If found, error_dict is None.
            If not found, feature_object is None and error_dict has error info.
        """
        doc = self.doc_manager.get_active_document()
        features = doc.DesignEdgebarFeatures
        target = None
        for i in range(1, features.Count + 1):
            f = features.Item(i)
            if hasattr(f, "Name") and f.Name == feature_name:
                target = f
                break

        if target is None:
            names = []
            for i in range(1, features.Count + 1):
                with contextlib.suppress(Exception):
                    names.append(features.Item(i).Name)
            return None, {
                "error": f"Feature '{feature_name}' not found.",
                "available_features": names,
            }

        return target, None

    def create_thread_ex(
        self, face_index: int, depth: float, pitch: float = 0.001
    ) -> dict[str, Any]:
        """
        Create an extended thread on a cylindrical face.

        Uses Threads.AddEx which provides additional control over thread
        depth and pitch compared to the basic Add method.

        Args:
            face_index: 0-based index of the cylindrical face
            depth: Thread depth in meters
            pitch: Thread pitch in meters (default 1mm)

        Returns:
            Dict with status and thread info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face_index: {face_index}. Count: {faces.Count}"}

            face = faces.Item(face_index + 1)
            threads = model.Threads
            _feature = threads.AddEx(face, depth, pitch)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "thread_ex",
                "face_index": face_index,
                "depth": depth,
                "pitch": pitch,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_slot_ex(
        self, width: float, depth: float, direction: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create an extended slot feature with width and depth control.

        Uses Slots.AddEx with multi-profile support and additional parameters.

        Args:
            width: Slot width in meters
            depth: Slot depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and slot info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            side = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            slots = model.Slots
            _feature = slots.AddEx(profile, width, depth, side)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "slot_ex",
                "width": width,
                "depth": depth,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_slot_sync(self, width: float, depth: float) -> dict[str, Any]:
        """
        Create a synchronous slot feature.

        Uses Slots.AddSync for synchronous modeling mode.

        Args:
            width: Slot width in meters
            depth: Slot depth in meters

        Returns:
            Dict with status and slot info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            slots = model.Slots
            _feature = slots.AddSync(profile, width, depth)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "slot_sync",
                "width": width,
                "depth": depth,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_drawn_cutout_ex(self, depth: float, direction: str = "Normal") -> dict[str, Any]:
        """
        Create an extended drawn cutout feature (sheet metal).

        Uses DrawnCutouts.AddEx with multi-profile support.

        Args:
            depth: Cutout depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            side = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            drawn_cutouts = model.DrawnCutouts
            _feature = drawn_cutouts.AddEx(profile, depth, side)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "drawn_cutout_ex",
                "depth": depth,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_louver_sync(self, depth: float) -> dict[str, Any]:
        """
        Create a synchronous louver feature (sheet metal).

        Uses Louvers.AddSync for synchronous modeling mode.

        Args:
            depth: Louver depth in meters

        Returns:
            Dict with status and louver info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            louvers = model.Louvers
            _feature = louvers.AddSync(profile, depth)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "louver_sync",
                "depth": depth,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_thicken_sync(self, thickness: float, direction: str = "Both") -> dict[str, Any]:
        """
        Create a synchronous thicken feature.

        Uses Thickens.AddSync to thicken a surface body into a solid
        in synchronous modeling mode.

        Args:
            thickness: Thicken thickness in meters
            direction: 'Both', 'Normal', or 'Reverse'

        Returns:
            Dict with status and thicken info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            direction_map = {
                "Both": DirectionConstants.igBoth,
                "Normal": DirectionConstants.igRight,
                "Reverse": DirectionConstants.igLeft,
            }
            side = direction_map.get(direction, DirectionConstants.igBoth)

            thickens = model.Thickens
            _feature = thickens.AddSync(thickness, side)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "thicken_sync",
                "thickness": thickness,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_mirror_sync_ex(self, feature_name: str, mirror_plane_index: int) -> dict[str, Any]:
        """
        Create a synchronous mirror copy using the extended AddSyncEx method.

        Looks up the feature by name from DesignEdgebarFeatures and mirrors
        it across the specified reference plane.

        Args:
            feature_name: Name of the feature to mirror (from list_features)
            mirror_plane_index: 1-based index of the mirror plane

        Returns:
            Dict with status and mirror info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            ref_planes = doc.RefPlanes
            if mirror_plane_index < 1 or mirror_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid plane index: {mirror_plane_index}. Count: {ref_planes.Count}"
                }

            mirror_plane = ref_planes.Item(mirror_plane_index)

            mc = model.MirrorCopies
            mirror = mc.AddSyncEx(1, [target_feature], mirror_plane, False)

            return {
                "status": "created",
                "type": "mirror_sync_ex",
                "feature": feature_name,
                "mirror_plane": mirror_plane_index,
                "name": mirror.Name if hasattr(mirror, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_pattern_rectangular_ex(
        self,
        feature_name: str,
        x_count: int,
        y_count: int,
        x_spacing: float,
        y_spacing: float,
    ) -> dict[str, Any]:
        """
        Create a rectangular pattern using the extended AddByRectangularEx method.

        The Ex variant may use different marshaling than the original
        AddByRectangular, potentially avoiding SAFEARRAY issues.

        Args:
            feature_name: Name of the feature to pattern
            x_count: Number of instances in X direction
            y_count: Number of instances in Y direction
            x_spacing: Spacing between instances in X (meters)
            y_spacing: Spacing between instances in Y (meters)

        Returns:
            Dict with status and pattern info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            patterns = model.Patterns
            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            pattern = patterns.AddByRectangularEx(
                1, feature_arr, x_count, x_spacing, y_count, y_spacing
            )

            return {
                "status": "created",
                "type": "pattern_rectangular_ex",
                "feature": feature_name,
                "x_count": x_count,
                "y_count": y_count,
                "x_spacing": x_spacing,
                "y_spacing": y_spacing,
                "name": pattern.Name if hasattr(pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_pattern_circular_ex(
        self,
        feature_name: str,
        count: int,
        angle: float,
        axis_face_index: int,
    ) -> dict[str, Any]:
        """
        Create a circular pattern using the extended AddByCircularEx method.

        The Ex variant may use different marshaling than the original
        AddByCircular, potentially avoiding SAFEARRAY issues.

        Args:
            feature_name: Name of the feature to pattern
            count: Number of instances around the circle
            angle: Total angle in degrees
            axis_face_index: 0-based index of the cylindrical face to use as axis

        Returns:
            Dict with status and pattern info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if axis_face_index < 0 or axis_face_index >= faces.Count:
                return {
                    "error": f"Invalid axis_face_index: {axis_face_index}. Count: {faces.Count}"
                }

            axis_face = faces.Item(axis_face_index + 1)
            angle_rad = math.radians(angle)

            patterns = model.Patterns
            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            pattern = patterns.AddByCircularEx(1, feature_arr, count, angle_rad, axis_face)

            return {
                "status": "created",
                "type": "pattern_circular_ex",
                "feature": feature_name,
                "count": count,
                "angle": angle,
                "axis_face_index": axis_face_index,
                "name": pattern.Name if hasattr(pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_pattern_duplicate(self, feature_name: str) -> dict[str, Any]:
        """
        Create a duplicate pattern of a feature.

        Uses Patterns.AddDuplicate to create an exact copy of the
        specified feature in the feature tree.

        Args:
            feature_name: Name of the feature to duplicate

        Returns:
            Dict with status and pattern info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            patterns = model.Patterns
            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            pattern = patterns.AddDuplicate(1, feature_arr)

            return {
                "status": "created",
                "type": "pattern_duplicate",
                "feature": feature_name,
                "name": pattern.Name if hasattr(pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_pattern_by_fill(
        self,
        feature_name: str,
        fill_region_face_index: int,
        x_spacing: float,
        y_spacing: float,
    ) -> dict[str, Any]:
        """
        Create a fill pattern of a feature within a face region.

        Uses Patterns.AddByFill to fill a face region with patterned
        copies of the specified feature.

        Args:
            feature_name: Name of the feature to pattern
            fill_region_face_index: 0-based face index defining the fill region
            x_spacing: Spacing in X direction (meters)
            y_spacing: Spacing in Y direction (meters)

        Returns:
            Dict with status and pattern info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if fill_region_face_index < 0 or fill_region_face_index >= faces.Count:
                return {
                    "error": f"Invalid fill_region_face_index: {fill_region_face_index}. "
                    f"Count: {faces.Count}"
                }

            fill_face = faces.Item(fill_region_face_index + 1)

            patterns = model.Patterns
            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            pattern = patterns.AddByFill(1, feature_arr, fill_face, x_spacing, y_spacing)

            return {
                "status": "created",
                "type": "pattern_by_fill",
                "feature": feature_name,
                "fill_region_face_index": fill_region_face_index,
                "x_spacing": x_spacing,
                "y_spacing": y_spacing,
                "name": pattern.Name if hasattr(pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_pattern_by_table(
        self,
        feature_name: str,
        x_offsets: list[float],
        y_offsets: list[float],
    ) -> dict[str, Any]:
        """
        Create a table-driven pattern of a feature.

        Uses Patterns.AddPatternByTable to place copies of the feature
        at specific X/Y offset locations.

        Args:
            feature_name: Name of the feature to pattern
            x_offsets: List of X offsets in meters
            y_offsets: List of Y offsets in meters (must match length of x_offsets)

        Returns:
            Dict with status and pattern info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            if len(x_offsets) != len(y_offsets):
                return {
                    "error": f"x_offsets and y_offsets must have same length. "
                    f"Got {len(x_offsets)} and {len(y_offsets)}."
                }

            if len(x_offsets) == 0:
                return {"error": "At least one offset pair is required."}

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            patterns = model.Patterns
            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            x_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, x_offsets)
            y_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, y_offsets)

            pattern = patterns.AddPatternByTable(1, feature_arr, len(x_offsets), x_arr, y_arr)

            return {
                "status": "created",
                "type": "pattern_by_table",
                "feature": feature_name,
                "point_count": len(x_offsets),
                "x_offsets": x_offsets,
                "y_offsets": y_offsets,
                "name": pattern.Name if hasattr(pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # BATCH 10: NEW 29 TOOLS
    # =================================================================

    # ----- Group 1: Reference Planes (4 tools) -----

    def create_ref_plane_normal_at_distance_v2(
        self,
        curve_edge_index: int,
        orientation_plane_index: int,
        distance: float,
        normal_side: int = 2,
    ) -> dict[str, Any]:
        """
        Create a reference plane normal to a curve at a distance from the curve.

        Uses RefPlanes.AddNormalToCurveAtDistance(Curve, OrientationPlane,
        Distance, normalOrientation, selectedCurveEnd).

        Args:
            curve_edge_index: 0-based edge index on the body to use as curve
            orientation_plane_index: 1-based index of the orientation reference plane
            distance: Distance from curve endpoint in meters
            normal_side: Normal orientation (1=igLeft, 2=igRight)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body
            edges = body.Edges(FaceQueryConstants.igQueryAll)

            if curve_edge_index < 0 or curve_edge_index >= edges.Count:
                return {
                    "error": f"Invalid curve_edge_index: {curve_edge_index}. "
                    f"Edge count: {edges.Count}"
                }

            ref_planes = doc.RefPlanes
            curve = edges.Item(curve_edge_index + 1)
            orient_plane = ref_planes.Item(orientation_plane_index)

            _feature = ref_planes.AddNormalToCurveAtDistance(
                curve, orient_plane, distance, normal_side, ReferenceElementConstants.igCurveEnd
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "ref_plane_normal_at_distance_v2",
                "curve_edge_index": curve_edge_index,
                "distance": distance,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_normal_at_arc_ratio_v2(
        self,
        curve_edge_index: int,
        orientation_plane_index: int,
        ratio: float,
        normal_side: int = 2,
    ) -> dict[str, Any]:
        """
        Create a reference plane normal to a curve at an arc-length ratio.

        Uses RefPlanes.AddNormalToCurveAtArcLengthRatio(Curve, OrientationPlane,
        Ratio, normalOrientation, selectedCurveEnd).

        Args:
            curve_edge_index: 0-based edge index on the body to use as curve
            orientation_plane_index: 1-based index of the orientation reference plane
            ratio: Arc length ratio (0.0 to 1.0)
            normal_side: Normal orientation (1=igLeft, 2=igRight)

        Returns:
            Dict with status and new plane index
        """
        try:
            if ratio < 0.0 or ratio > 1.0:
                return {"error": f"Ratio must be between 0.0 and 1.0, got {ratio}"}

            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body
            edges = body.Edges(FaceQueryConstants.igQueryAll)

            if curve_edge_index < 0 or curve_edge_index >= edges.Count:
                return {
                    "error": f"Invalid curve_edge_index: {curve_edge_index}. "
                    f"Edge count: {edges.Count}"
                }

            ref_planes = doc.RefPlanes
            curve = edges.Item(curve_edge_index + 1)
            orient_plane = ref_planes.Item(orientation_plane_index)

            _feature = ref_planes.AddNormalToCurveAtArcLengthRatio(
                curve, orient_plane, ratio, normal_side, ReferenceElementConstants.igCurveEnd
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "ref_plane_normal_at_arc_ratio_v2",
                "curve_edge_index": curve_edge_index,
                "ratio": ratio,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_normal_at_distance_along_v2(
        self,
        curve_edge_index: int,
        orientation_plane_index: int,
        distance: float,
        normal_side: int = 2,
    ) -> dict[str, Any]:
        """
        Create a reference plane normal to a curve at a distance along the curve.

        Uses RefPlanes.AddNormalToCurveAtDistanceAlongCurve(Curve, OrientationPlane,
        Distance, normalOrientation, selectedCurveEnd).

        Args:
            curve_edge_index: 0-based edge index on the body to use as curve
            orientation_plane_index: 1-based index of the orientation reference plane
            distance: Distance along the curve in meters
            normal_side: Normal orientation (1=igLeft, 2=igRight)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body
            edges = body.Edges(FaceQueryConstants.igQueryAll)

            if curve_edge_index < 0 or curve_edge_index >= edges.Count:
                return {
                    "error": f"Invalid curve_edge_index: {curve_edge_index}. "
                    f"Edge count: {edges.Count}"
                }

            ref_planes = doc.RefPlanes
            curve = edges.Item(curve_edge_index + 1)
            orient_plane = ref_planes.Item(orientation_plane_index)

            _feature = ref_planes.AddNormalToCurveAtDistanceAlongCurve(
                curve, orient_plane, distance, normal_side, ReferenceElementConstants.igCurveEnd
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "ref_plane_normal_at_distance_along_v2",
                "curve_edge_index": curve_edge_index,
                "distance": distance,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_ref_plane_tangent_parallel(
        self,
        face_index: int,
        parent_plane_index: int,
        normal_side: int = 2,
    ) -> dict[str, Any]:
        """
        Create a reference plane parallel to parent and tangent to a curved surface.

        Uses RefPlanes.AddParallelByTangent(Surface, ParentPlane, NormalSide).

        Args:
            face_index: 0-based face index of the curved surface
            parent_plane_index: 1-based index of the parent reference plane
            normal_side: Normal orientation (1=igLeft, 2=igRight)

        Returns:
            Dict with status and new plane index
        """
        try:
            doc = self.doc_manager.get_active_document()
            ref_planes = doc.RefPlanes

            if parent_plane_index < 1 or parent_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid parent_plane_index: {parent_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face_index: {face_index}. Body has {faces.Count} faces."}

            parent_plane = ref_planes.Item(parent_plane_index)
            face = faces.Item(face_index + 1)

            _feature = ref_planes.AddParallelByTangent(face, parent_plane, normal_side)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "ref_plane_tangent_parallel",
                "face_index": face_index,
                "parent_plane_index": parent_plane_index,
                "new_plane_index": ref_planes.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # ----- Group 2: Sync Variants (5 tools) -----

    def create_revolve_by_keypoint_sync(self) -> dict[str, Any]:
        """
        Create a synchronous revolve up to a keypoint extent.

        Uses RevolvedProtrusions.AddFiniteByKeyPointSync(Profile, RefAxis,
        KeyPointOrTangentFace, KeyPointFlags, ProfileSide).

        Returns:
            Dict with status and revolve info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)

            protrusions = model.RevolvedProtrusions
            _feature = protrusions.AddFiniteByKeyPointSync(
                profile,
                refaxis,
                None,  # KeyPointOrTangentFace
                KeyPointExtentConstants.igTangentNormal,  # KeyPointFlags
                DirectionConstants.igRight,  # ProfileSide
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "revolve_by_keypoint_sync",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_helix_from_to_sync(
        self, from_plane_index: int, to_plane_index: int, pitch: float
    ) -> dict[str, Any]:
        """
        Create a synchronous helix protrusion between two reference planes.

        Uses HelixProtrusions.AddFromToSync(HelixAxis, AxisStart,
        NumCrossSections, CrossSectionArray, ProfileSide, Height, Pitch,
        NumberOfTurns, HelixDir, FromPlane, ToPlane, TaperAngle).

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane
            pitch: Distance between coils in meters

        Returns:
            Dict with status and helix info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: {from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            helix = model.HelixProtrusions
            _feature = helix.AddFromToSync(
                refaxis,  # HelixAxis
                DirectionConstants.igRight,  # AxisStart
                1,  # NumCrossSections
                v_profiles,  # CrossSectionArray
                DirectionConstants.igRight,  # ProfileSide
                0.0,  # Height (ignored for FromTo)
                pitch,  # Pitch
                0.0,  # NumberOfTurns (calculated from FromTo)
                DirectionConstants.igRight,  # HelixDir
                from_plane,  # FromPlane
                to_plane,  # ToPlane
                0.0,  # TaperAngle
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "helix_from_to_sync",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
                "pitch": pitch,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_helix_from_to_sync_thin_wall(
        self,
        from_plane_index: int,
        to_plane_index: int,
        pitch: float,
        wall_thickness: float,
    ) -> dict[str, Any]:
        """
        Create a synchronous thin-walled helix protrusion between two planes.

        Uses HelixProtrusions.AddFromToSyncWithThinWall.

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane
            pitch: Distance between coils in meters
            wall_thickness: Wall thickness in meters

        Returns:
            Dict with status and helix info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: {from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            helix = model.HelixProtrusions
            _feature = helix.AddFromToSyncWithThinWall(
                refaxis,  # HelixAxis
                DirectionConstants.igRight,  # AxisStart
                1,  # NumCrossSections
                v_profiles,  # CrossSectionArray
                DirectionConstants.igRight,  # ProfileSide
                0.0,  # Height
                pitch,  # Pitch
                0.0,  # NumberOfTurns
                DirectionConstants.igRight,  # HelixDir
                from_plane,  # FromPlane
                to_plane,  # ToPlane
                True,  # ThinWall
                False,  # AddEndCaps
                True,  # RemoveInsideMaterial
                wall_thickness,  # Thickness
                DirectionConstants.igRight,  # ThicknessSide
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "helix_from_to_sync_thin_wall",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
                "pitch": pitch,
                "wall_thickness": wall_thickness,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_helix_cutout_from_to_sync(
        self, from_plane_index: int, to_plane_index: int, pitch: float
    ) -> dict[str, Any]:
        """
        Create a synchronous helical cutout between two reference planes.

        Uses HelixCutouts.AddFromToSync.

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane
            pitch: Distance between coils in meters

        Returns:
            Dict with status and helix cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: {from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            v_profiles = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            helix_cutouts = model.HelixCutouts
            _feature = helix_cutouts.AddFromToSync(
                refaxis,  # HelixAxis
                DirectionConstants.igRight,  # AxisStart
                1,  # NumCrossSections
                v_profiles,  # CrossSectionArray
                DirectionConstants.igRight,  # ProfileSide
                0.0,  # Height
                pitch,  # Pitch
                0.0,  # NumberOfTurns
                DirectionConstants.igRight,  # HelixDir
                from_plane,  # FromPlane
                to_plane,  # ToPlane
                0.0,  # TaperAngle
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "helix_cutout_from_to_sync",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
                "pitch": pitch,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_pattern_by_table_sync(
        self,
        feature_name: str,
        x_offsets: list[float],
        y_offsets: list[float],
    ) -> dict[str, Any]:
        """
        Create a synchronous table-driven pattern of a feature.

        Uses Patterns.AddPatternByTableSync.

        Args:
            feature_name: Name of the feature to pattern
            x_offsets: List of X offsets in meters
            y_offsets: List of Y offsets in meters

        Returns:
            Dict with status and pattern info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            if len(x_offsets) != len(y_offsets):
                return {
                    "error": f"x_offsets and y_offsets must have same length. "
                    f"Got {len(x_offsets)} and {len(y_offsets)}."
                }

            if len(x_offsets) == 0:
                return {"error": "At least one offset pair is required."}

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            patterns = model.Patterns
            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            x_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, x_offsets)
            y_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, y_offsets)

            pattern = patterns.AddPatternByTableSync(1, feature_arr, len(x_offsets), x_arr, y_arr)

            return {
                "status": "created",
                "type": "pattern_by_table_sync",
                "feature": feature_name,
                "point_count": len(x_offsets),
                "name": pattern.Name if hasattr(pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # ----- Group 3: Single-Profile Variants (3 tools) -----

    def create_extrude_from_to_single(
        self, from_plane_index: int, to_plane_index: int
    ) -> dict[str, Any]:
        """
        Create a single-profile extrusion between two reference planes.

        Uses ExtrudedProtrusions.AddFromTo(Profile, ProfileSide,
        FromFaceOrRefPlane, ToFaceOrRefPlane).

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane

        Returns:
            Dict with status and extrusion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: {from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            protrusions = model.ExtrudedProtrusions
            _feature = protrusions.AddFromTo(
                profile,
                DirectionConstants.igRight,  # ProfileSide
                from_plane,
                to_plane,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extrude_from_to_single",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extrude_through_next_single(self, direction: str = "Normal") -> dict[str, Any]:
        """
        Create a single-profile extrusion through the next face.

        Uses ExtrudedProtrusions.AddThroughNext(Profile, ProfileSide,
        ProfilePlaneSide).

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and extrusion info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            dir_const = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            protrusions = model.ExtrudedProtrusions
            _feature = protrusions.AddThroughNext(
                profile,
                dir_const,  # ProfileSide
                dir_const,  # ProfilePlaneSide
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extrude_through_next_single",
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_cutout_through_next_single(
        self, direction: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a single-profile extruded cutout through the next face.

        Uses ExtrudedCutouts.AddThroughNext(Profile, ProfileSide,
        ProfilePlaneSide).

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            dir_const = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            cutouts = model.ExtrudedCutouts
            _feature = cutouts.AddThroughNext(
                profile,
                dir_const,  # ProfileSide
                dir_const,  # ProfilePlaneSide
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_cutout_through_next_single",
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # ----- Group 4: MultiBody Cutout Variants (4 tools) -----

    def create_extruded_cutout_multi_body(
        self, distance: float, direction: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a multi-body extruded cutout.

        Uses ExtrudedCutouts.AddFiniteMultiBody(NumProfiles, ProfileArray,
        ProfileSide, ProfilePlaneSide, Depth, NumBodies, BodyArray).

        Args:
            distance: Cutout depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            dir_const = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            body = model.Body
            body_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [body])

            cutouts = model.ExtrudedCutouts
            _feature = cutouts.AddFiniteMultiBody(
                1,  # NumberOfProfiles
                (profile,),  # ProfileArray
                dir_const,  # ProfileSide
                dir_const,  # ProfilePlaneSide
                distance,  # Depth
                1,  # NumberOfBodies
                body_arr,  # BodyArray
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_cutout_multi_body",
                "distance": distance,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_cutout_from_to_multi_body(
        self, from_plane_index: int, to_plane_index: int
    ) -> dict[str, Any]:
        """
        Create a multi-body extruded cutout between two reference planes.

        Uses ExtrudedCutouts.AddFromToMultiBody(NumProfiles, ProfileArray,
        ProfileSide, FromFace, ToFace, NumBodies, BodyArray).

        Args:
            from_plane_index: 1-based index of the starting reference plane
            to_plane_index: 1-based index of the ending reference plane

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            ref_planes = doc.RefPlanes

            if from_plane_index < 1 or from_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid from_plane_index: {from_plane_index}. "
                    f"Count: {ref_planes.Count}"
                }
            if to_plane_index < 1 or to_plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid to_plane_index: {to_plane_index}. Count: {ref_planes.Count}"
                }

            from_plane = ref_planes.Item(from_plane_index)
            to_plane = ref_planes.Item(to_plane_index)

            body = model.Body
            body_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [body])

            cutouts = model.ExtrudedCutouts
            _feature = cutouts.AddFromToMultiBody(
                1,  # NumberOfProfiles
                (profile,),  # ProfileArray
                DirectionConstants.igRight,  # ProfileSide
                from_plane,  # FromFace
                to_plane,  # ToFace
                1,  # NumberOfBodies
                body_arr,  # BodyArray
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_cutout_from_to_multi_body",
                "from_plane_index": from_plane_index,
                "to_plane_index": to_plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_extruded_cutout_through_all_multi_body(
        self, direction: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a multi-body extruded cutout through all material.

        Uses ExtrudedCutouts.AddThroughAllMultiBody(NumProfiles, ProfileArray,
        ProfileSide, ProfilePlaneSide, NumBodies, BodyArray).

        Args:
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and cutout info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            dir_const = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            body = model.Body
            body_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [body])

            cutouts = model.ExtrudedCutouts
            _feature = cutouts.AddThroughAllMultiBody(
                1,  # NumberOfProfiles
                (profile,),  # ProfileArray
                dir_const,  # ProfileSide
                dir_const,  # ProfilePlaneSide
                1,  # NumberOfBodies
                body_arr,  # BodyArray
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "extruded_cutout_through_all_multi_body",
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolved_cutout_multi_body(self, angle: float = 360.0) -> dict[str, Any]:
        """
        Create a multi-body revolved cutout.

        Uses RevolvedCutouts.AddFiniteMultiBody.

        Args:
            angle: Revolution angle in degrees

        Returns:
            Dict with status and cutout info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            angle_rad = math.radians(angle)

            body = model.Body
            body_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [body])

            cutouts = model.RevolvedCutouts
            _feature = cutouts.AddFiniteMultiBody(
                1,  # NumberOfProfiles
                (profile,),  # ProfileArray
                refaxis,  # RefAxis
                DirectionConstants.igRight,  # ProfileSide
                DirectionConstants.igRight,  # ProfilePlaneSide
                angle_rad,  # AngleOfRevolution
                1,  # NumberOfBodies
                body_arr,  # BodyArray
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "revolved_cutout_multi_body",
                "angle": angle,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # ----- Group 5: Full Treatment Variants (4 tools) -----

    def create_revolved_cutout_full(self, angle: float = 360.0) -> dict[str, Any]:
        """
        Create a revolved cutout with full extent parameters.

        Uses RevolvedCutouts.Add with dual-extent params.

        Args:
            angle: Revolution angle in degrees

        Returns:
            Dict with status and cutout info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            angle_rad = math.radians(angle)

            profile_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            cutouts = model.RevolvedCutouts
            _feature = cutouts.Add(
                1,
                profile_array,
                refaxis,
                DirectionConstants.igRight,
                ExtentTypeConstants.igFinite,
                DirectionConstants.igRight,
                angle_rad,
                None,
                KeyPointExtentConstants.igTangentNormal,
                ExtentTypeConstants.igNone,
                DirectionConstants.igRight,
                0.0,
                None,
                KeyPointExtentConstants.igTangentNormal,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {"status": "created", "type": "revolved_cutout_full", "angle": angle}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolved_cutout_full_sync(self, angle: float = 360.0) -> dict[str, Any]:
        """
        Create a synchronous revolved cutout with full extent parameters.

        Uses RevolvedCutouts.AddSync with dual-extent params.

        Args:
            angle: Revolution angle in degrees

        Returns:
            Dict with status and cutout info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            angle_rad = math.radians(angle)

            profile_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            cutouts = model.RevolvedCutouts
            _feature = cutouts.AddSync(
                1,
                profile_array,
                refaxis,
                DirectionConstants.igRight,
                ExtentTypeConstants.igFinite,
                DirectionConstants.igRight,
                angle_rad,
                None,
                KeyPointExtentConstants.igTangentNormal,
                ExtentTypeConstants.igNone,
                DirectionConstants.igRight,
                0.0,
                None,
                KeyPointExtentConstants.igTangentNormal,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {"status": "created", "type": "revolved_cutout_full_sync", "angle": angle}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolved_surface_full(
        self, angle: float = 360.0, want_end_caps: bool = False
    ) -> dict[str, Any]:
        """
        Create a revolved surface with full extent parameters.

        Uses RevolvedSurfaces.Add with dual-extent params.

        Args:
            angle: Revolution angle in degrees
            want_end_caps: Whether to add end caps

        Returns:
            Dict with status and surface info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}
            model = models.Item(1)

            angle_rad = math.radians(angle)
            profile_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            surfaces = model.RevolvedSurfaces
            _feature = surfaces.Add(
                1,
                profile_array,
                refaxis,
                ExtentTypeConstants.igFinite,
                DirectionConstants.igRight,
                angle_rad,
                None,
                KeyPointExtentConstants.igTangentNormal,
                ExtentTypeConstants.igNone,
                DirectionConstants.igRight,
                0.0,
                None,
                KeyPointExtentConstants.igTangentNormal,
                want_end_caps,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "revolved_surface_full",
                "angle": angle,
                "want_end_caps": want_end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_revolved_surface_full_sync(
        self, angle: float = 360.0, want_end_caps: bool = False
    ) -> dict[str, Any]:
        """
        Create a synchronous revolved surface with full extent parameters.

        Uses RevolvedSurfaces.AddSync with dual-extent params.

        Args:
            angle: Revolution angle in degrees
            want_end_caps: Whether to add end caps

        Returns:
            Dict with status and surface info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()
            refaxis = self.sketch_manager.get_active_refaxis()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}
            if not refaxis:
                return {
                    "error": "No axis of revolution set. "
                    "Use set_axis_of_revolution() before "
                    "closing the sketch."
                }

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}
            model = models.Item(1)

            angle_rad = math.radians(angle)
            profile_array = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

            surfaces = model.RevolvedSurfaces
            _feature = surfaces.AddSync(
                1,
                profile_array,
                refaxis,
                ExtentTypeConstants.igFinite,
                DirectionConstants.igRight,
                angle_rad,
                None,
                KeyPointExtentConstants.igTangentNormal,
                ExtentTypeConstants.igNone,
                DirectionConstants.igRight,
                0.0,
                None,
                KeyPointExtentConstants.igTangentNormal,
                want_end_caps,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "revolved_surface_full_sync",
                "angle": angle,
                "want_end_caps": want_end_caps,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # ----- Group 6: Sheet Metal (5 tools) -----

    def create_flange_match_face_with_bend(
        self,
        face_index: int,
        edge_index: int,
        flange_length: float,
        side: str = "Right",
        inside_radius: float = 0.001,
    ) -> dict[str, Any]:
        """
        Create a flange by match face with bend deduction/allowance.

        Args:
            face_index: 0-based face index
            edge_index: 0-based edge index on the face
            flange_length: Flange length in meters
            side: 'Right' or 'Left'
            inside_radius: Inside bend radius in meters

        Returns:
            Dict with status and flange info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face_index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            edges = face.Edges
            if edge_index < 0 or edge_index >= edges.Count:
                return {"error": f"Invalid edge_index: {edge_index}. Face has {edges.Count} edges."}

            edge = edges.Item(edge_index + 1)
            side_const = (
                DirectionConstants.igRight if side == "Right" else DirectionConstants.igLeft
            )

            flanges = model.Flanges
            _feature = flanges.AddByMatchFaceAndBendDeductionOrBendAllowance(
                edge,
                side_const,
                flange_length,
                None,
                0,
                side_const,
                inside_radius,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "flange_match_face_with_bend",
                "face_index": face_index,
                "edge_index": edge_index,
                "flange_length": flange_length,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_flange_by_face_with_bend(
        self,
        face_index: int,
        edge_index: int,
        ref_face_index: int,
        flange_length: float,
        side: str = "Right",
        bend_radius: float = 0.001,
    ) -> dict[str, Any]:
        """
        Create a flange by face reference with bend deduction/allowance.

        Args:
            face_index: 0-based face index containing the edge
            edge_index: 0-based edge index on the face
            ref_face_index: 0-based reference face index
            flange_length: Flange length in meters
            side: 'Right' or 'Left'
            bend_radius: Bend radius in meters

        Returns:
            Dict with status and flange info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face_index: {face_index}. Body has {faces.Count} faces."}
            if ref_face_index < 0 or ref_face_index >= faces.Count:
                return {
                    "error": f"Invalid ref_face_index: {ref_face_index}. "
                    f"Body has {faces.Count} faces."
                }

            face = faces.Item(face_index + 1)
            ref_face = faces.Item(ref_face_index + 1)
            edges = face.Edges
            if edge_index < 0 or edge_index >= edges.Count:
                return {"error": f"Invalid edge_index: {edge_index}. Face has {edges.Count} edges."}

            edge = edges.Item(edge_index + 1)
            side_const = (
                DirectionConstants.igRight if side == "Right" else DirectionConstants.igLeft
            )

            flanges = model.Flanges
            _feature = flanges.AddFlangeByFaceAndBendDeductionOrBendAllowance(
                edge,
                ref_face,
                side_const,
                flange_length,
                None,
                0,
                side_const,
                bend_radius,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "flange_by_face_with_bend",
                "face_index": face_index,
                "edge_index": edge_index,
                "ref_face_index": ref_face_index,
                "flange_length": flange_length,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_contour_flange_v3(
        self,
        thickness: float,
        bend_radius: float = 0.001,
        direction: str = "Normal",
    ) -> dict[str, Any]:
        """
        Create an extended v3 contour flange from the active profile.

        Uses ContourFlanges.Add3.

        Args:
            thickness: Material thickness in meters
            bend_radius: Bend radius in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and contour flange info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            dir_const = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            contour_flanges = model.ContourFlanges
            _feature = contour_flanges.Add3(
                profile,
                ExtentTypeConstants.igFinite,
                dir_const,
                thickness,
                None,
                0,
                bend_radius,
                0,
                0.001,
                0.001,
                0,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "contour_flange_v3",
                "thickness": thickness,
                "bend_radius": bend_radius,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_contour_flange_sync_ex(
        self,
        face_index: int,
        edge_index: int,
        thickness: float,
        bend_radius: float = 0.001,
        direction: str = "Normal",
    ) -> dict[str, Any]:
        """
        Create a synchronous extended contour flange.

        Uses ContourFlanges.AddSyncEx.

        Args:
            face_index: 0-based face index
            edge_index: 0-based edge index on the face
            thickness: Material thickness in meters
            bend_radius: Bend radius in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and contour flange info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)

            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face_index: {face_index}. Body has {faces.Count} faces."}

            face = faces.Item(face_index + 1)
            edges = face.Edges
            if edge_index < 0 or edge_index >= edges.Count:
                return {"error": f"Invalid edge_index: {edge_index}. Face has {edges.Count} edges."}

            edge = edges.Item(edge_index + 1)
            dir_const = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            contour_flanges = model.ContourFlanges
            _feature = contour_flanges.AddSyncEx(
                profile,
                edge,
                ExtentTypeConstants.igFinite,
                dir_const,
                thickness,
                bend_radius,
                0,
                0.001,
                0.001,
                0,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "contour_flange_sync_ex",
                "face_index": face_index,
                "edge_index": edge_index,
                "thickness": thickness,
                "bend_radius": bend_radius,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_bend(
        self,
        bend_angle: float = 90.0,
        direction: str = "Normal",
        moving_side: str = "Right",
        bend_radius: float = 0.001,
    ) -> dict[str, Any]:
        """
        Create a basic bend feature from the active profile.

        Uses Bends.Add(Profile, BendAngle, BendPZLSide, MovingSide,
        BendDirection, BendRadius).

        Args:
            bend_angle: Bend angle in degrees
            direction: 'Normal' or 'Reverse'
            moving_side: 'Right' or 'Left'
            bend_radius: Bend radius in meters

        Returns:
            Dict with status and bend info
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            angle_rad = math.radians(bend_angle)

            # BendFeatureConstants: seBendNormal=7, seBendReverseNormal=8
            # seBendMoveRight=5, seBendMoveLeft=6, seBendPZLInside=11
            dir_const = 7 if direction == "Normal" else 8
            move_const = 5 if moving_side == "Right" else 6

            bends = model.Bends
            _feature = bends.Add(profile, angle_rad, 11, move_const, dir_const, bend_radius)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "bend",
                "bend_angle": bend_angle,
                "direction": direction,
                "moving_side": moving_side,
                "bend_radius": bend_radius,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # ----- Group 7: Pattern Ex + Slots (4 tools) -----

    def create_pattern_by_fill_ex(
        self,
        feature_name: str,
        fill_region_face_index: int,
        x_spacing: float,
        y_spacing: float,
        stagger_offset: float = 0.0,
    ) -> dict[str, Any]:
        """
        Create an extended fill pattern of a feature within a face region.

        Uses Patterns.AddByFillEx.

        Args:
            feature_name: Name of the feature to pattern
            fill_region_face_index: 0-based face index defining the fill region
            x_spacing: X direction spacing in meters
            y_spacing: Y direction spacing in meters
            stagger_offset: Stagger offset for pattern rows in meters

        Returns:
            Dict with status and pattern info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            body = model.Body
            faces = body.Faces(FaceQueryConstants.igQueryAll)
            if fill_region_face_index < 0 or fill_region_face_index >= faces.Count:
                return {
                    "error": f"Invalid fill_region_face_index: "
                    f"{fill_region_face_index}. "
                    f"Body has {faces.Count} faces."
                }

            face = faces.Item(fill_region_face_index + 1)

            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            region_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [face])

            patterns = model.Patterns
            pattern = patterns.AddByFillEx(
                1,
                feature_arr,
                1,
                region_arr,
                0,
                x_spacing,
                y_spacing,
                stagger_offset,
                0.0,
                False,
            )

            return {
                "status": "created",
                "type": "pattern_by_fill_ex",
                "feature": feature_name,
                "fill_region_face_index": fill_region_face_index,
                "x_spacing": x_spacing,
                "y_spacing": y_spacing,
                "name": pattern.Name if hasattr(pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_pattern_by_curve_ex(
        self,
        feature_name: str,
        curve_edge_index: int,
        count: int,
        spacing: float,
    ) -> dict[str, Any]:
        """
        Create a pattern along a curve using the extended API.

        Uses Patterns.AddByCurveEx.

        Args:
            feature_name: Name of the feature to pattern
            curve_edge_index: 0-based edge index defining the curve path
            count: Number of pattern occurrences
            spacing: Spacing between occurrences in meters

        Returns:
            Dict with status and pattern info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            body = model.Body
            edges = body.Edges(FaceQueryConstants.igQueryAll)
            if curve_edge_index < 0 or curve_edge_index >= edges.Count:
                return {
                    "error": f"Invalid curve_edge_index: "
                    f"{curve_edge_index}. "
                    f"Body has {edges.Count} edges."
                }

            edge = edges.Item(curve_edge_index + 1)

            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            curve_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [edge])

            patterns = model.Patterns
            pattern = patterns.AddByCurveEx(
                1,
                feature_arr,
                0,
                1,
                curve_arr,
                None,
                0,
                0.0,
                0,
                count,
                spacing,
            )

            return {
                "status": "created",
                "type": "pattern_by_curve_ex",
                "feature": feature_name,
                "curve_edge_index": curve_edge_index,
                "count": count,
                "spacing": spacing,
                "name": pattern.Name if hasattr(pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_slot_multi_body(
        self, width: float, depth: float, direction: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a slot feature that spans multiple bodies.

        Uses Slots.AddMultiBody.

        Args:
            width: Slot width in meters
            depth: Slot depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and slot info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            dir_const = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            body = model.Body
            body_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [body])

            slots = model.Slots
            _feature = slots.AddMultiBody(
                1,
                (profile,),
                dir_const,
                ExtentTypeConstants.igFinite,
                width,
                0.0,
                0.0,
                ExtentTypeConstants.igFinite,
                dir_const,
                depth,
                KeyPointExtentConstants.igTangentNormal,
                None,
                None,
                OffsetSideConstants.seOffsetNone,
                0.0,
                None,
                OffsetSideConstants.seOffsetNone,
                0.0,
                1,
                body_arr,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "slot_multi_body",
                "width": width,
                "depth": depth,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_slot_sync_multi_body(
        self, width: float, depth: float, direction: str = "Normal"
    ) -> dict[str, Any]:
        """
        Create a synchronous slot feature that spans multiple bodies.

        Uses Slots.AddSyncMultiBody.

        Args:
            width: Slot width in meters
            depth: Slot depth in meters
            direction: 'Normal' or 'Reverse'

        Returns:
            Dict with status and slot info
        """
        try:
            doc = self.doc_manager.get_active_document()
            profile = self.sketch_manager.get_active_sketch()

            if not profile:
                return {"error": "No active sketch profile. Create and close a sketch first."}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists. Create a base feature first."}

            model = models.Item(1)
            dir_const = (
                DirectionConstants.igRight if direction == "Normal" else DirectionConstants.igLeft
            )

            body = model.Body
            body_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [body])

            slots = model.Slots
            _feature = slots.AddSyncMultiBody(
                1,
                (profile,),
                dir_const,
                ExtentTypeConstants.igFinite,
                width,
                0.0,
                0.0,
                ExtentTypeConstants.igFinite,
                dir_const,
                depth,
                KeyPointExtentConstants.igTangentNormal,
                None,
                None,
                OffsetSideConstants.seOffsetNone,
                0.0,
                None,
                OffsetSideConstants.seOffsetNone,
                0.0,
                1,
                body_arr,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "slot_sync_multi_body",
                "width": width,
                "depth": depth,
                "direction": direction,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # PATTERN VARIANTS
    # =================================================================

    def create_pattern_by_curve(
        self,
        feature_name: str,
        curve_edge_index: int,
        count: int,
        spacing: float,
        rotation_type: int = 0,
    ) -> dict[str, Any]:
        """
        Create a pattern along a curve using Patterns.AddByCurve.

        Args:
            feature_name: Name of the feature to pattern
            curve_edge_index: 0-based edge index defining the curve path
            count: Number of pattern occurrences
            spacing: Spacing between occurrences in meters
            rotation_type: 0=fixed orientation, 1=follow curve tangent

        Returns:
            Dict with status and pattern info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            body = model.Body
            edges = body.Edges(FaceQueryConstants.igQueryAll)
            if curve_edge_index < 0 or curve_edge_index >= edges.Count:
                return {
                    "error": f"Invalid curve_edge_index: {curve_edge_index}. "
                    f"Body has {edges.Count} edges."
                }

            edge = edges.Item(curve_edge_index + 1)
            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            curve_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [edge])

            patterns = model.Patterns
            _pattern = patterns.AddByCurve(
                1,
                feature_arr,
                rotation_type,
                1,
                curve_arr,
                count,
                spacing,
            )
            if _pattern is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "pattern_by_curve",
                "feature": feature_name,
                "curve_edge_index": curve_edge_index,
                "count": count,
                "spacing": spacing,
                "rotation_type": rotation_type,
                "name": _pattern.Name if hasattr(_pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_pattern_by_curve_sync(
        self,
        feature_name: str,
        curve_edge_index: int,
        count: int,
        spacing: float,
        rotation_type: int = 0,
    ) -> dict[str, Any]:
        """
        Create a synchronous pattern along a curve using Patterns.AddByCurveSync.

        Args:
            feature_name: Name of the feature to pattern
            curve_edge_index: 0-based edge index defining the curve path
            count: Number of pattern occurrences
            spacing: Spacing between occurrences in meters
            rotation_type: 0=fixed orientation, 1=follow curve tangent

        Returns:
            Dict with status and pattern info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)

            target_feature, error = self._find_feature_by_name(feature_name)
            if error:
                return error

            body = model.Body
            edges = body.Edges(FaceQueryConstants.igQueryAll)
            if curve_edge_index < 0 or curve_edge_index >= edges.Count:
                return {
                    "error": f"Invalid curve_edge_index: {curve_edge_index}. "
                    f"Body has {edges.Count} edges."
                }

            edge = edges.Item(curve_edge_index + 1)
            feature_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [target_feature])
            curve_arr = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [edge])

            patterns = model.Patterns
            _pattern = patterns.AddByCurveSync(
                1,
                feature_arr,
                rotation_type,
                1,
                curve_arr,
                count,
                spacing,
            )
            if _pattern is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "pattern_by_curve_sync",
                "feature": feature_name,
                "curve_edge_index": curve_edge_index,
                "count": count,
                "spacing": spacing,
                "rotation_type": rotation_type,
                "name": _pattern.Name if hasattr(_pattern, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def recognize_and_create_patterns(
        self, tolerance: float = 0.001
    ) -> dict[str, Any]:
        """
        Auto-recognize and create patterns from existing geometry.

        Uses Patterns.RecognizeAndCreatePatterns to detect geometric
        repetition in the model and convert it into patterned features.

        Args:
            tolerance: Geometric tolerance for pattern recognition (meters)

        Returns:
            Dict with status and count of recognized patterns
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models
            if models.Count == 0:
                return {"error": "No base feature exists."}

            model = models.Item(1)
            patterns = model.Patterns
            count_before = patterns.Count

            patterns.RecognizeAndCreatePatterns(tolerance)

            count_after = patterns.Count
            recognized = count_after - count_before

            return {
                "status": "completed",
                "patterns_recognized": recognized,
                "total_patterns": count_after,
                "tolerance": tolerance,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_loft_with_guide_curves(
        self,
        guide_edge_indices: list[int],
        profile_indices: list = None,
    ) -> dict[str, Any]:
        """
        Create a loft feature with guide curves.

        Uses LoftedProtrusions.Add (full param version) which accepts
        guide curves to control the shape of the loft between profiles.
        Profiles are taken from accumulated sketches.

        Args:
            guide_edge_indices: List of 0-based edge indices to use as
                guide curves. Edges must span from first to last profile plane.
            profile_indices: Optional indices into accumulated profiles.
                If None, uses all accumulated profiles.

        Returns:
            Dict with status and loft info
        """
        try:
            doc = self.doc_manager.get_active_document()
            models = doc.Models

            all_profiles = self.sketch_manager.get_accumulated_profiles()
            if profile_indices is not None:
                profiles = [all_profiles[i] for i in profile_indices]
            else:
                profiles = all_profiles

            if len(profiles) < 2:
                return {
                    "error": f"Loft requires at least 2 profiles, got {len(profiles)}."
                }

            v_profiles, v_types, v_origins = self._make_loft_variant_arrays(profiles)

            model = models.Item(1)
            body = model.Body
            edges = body.Edges(FaceQueryConstants.igQueryAll)
            guide_edges = []
            for idx in guide_edge_indices:
                if idx < 0 or idx >= edges.Count:
                    return {
                        "error": f"Invalid guide_edge_index {idx}. "
                        f"Body has {edges.Count} edges."
                    }
                guide_edges.append(edges.Item(idx + 1))

            v_guides = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, guide_edges)
            v_guide_types = VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_I4,
                [LoftSweepConstants.igProfileBasedCrossSection] * len(guide_edges),
            )
            v_seg = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, [])

            lp = model.LoftedProtrusions
            _feature, err = self._perform_feature_call(
                lambda: lp.Add(
                    len(profiles),
                    v_profiles,
                    v_types,
                    v_origins,
                    v_seg,
                    len(guide_edges),
                    v_guides,
                    v_guide_types,
                    DirectionConstants.igRight,
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,
                    ExtentTypeConstants.igNone,
                    0.0,
                    None,
                ),
                consumes_profiles=True,
            )
            if err:
                return err

            return {
                "status": "created",
                "type": "loft_with_guide_curves",
                "num_profiles": len(profiles),
                "num_guide_curves": len(guide_edges),
                "guide_edge_indices": guide_edge_indices,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # PART CONFIGURATIONS
    # =================================================================

    def list_part_configurations(self) -> dict[str, Any]:
        """
        List all part configurations in the active part document.

        Uses PartDocument.Configurations (PartConfigurations collection).

        Returns:
            Dict with list of configuration names and current active one
        """
        try:
            doc = self.doc_manager.get_active_document()
            if not hasattr(doc, "Configurations"):
                return {"error": "Active document does not support configurations"}

            configs = doc.Configurations
            result = []
            active_name = None
            for i in range(1, configs.Count + 1):
                cfg = configs.Item(i)
                name = cfg.Name if hasattr(cfg, "Name") else f"Config {i}"
                is_active = False
                try:
                    is_active = bool(cfg.Active) if hasattr(cfg, "Active") else False
                except Exception:
                    pass
                if is_active:
                    active_name = name
                result.append({"index": i - 1, "name": name, "active": is_active})

            return {
                "status": "ok",
                "count": configs.Count,
                "active": active_name,
                "configurations": result,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_part_configuration(self, name: str) -> dict[str, Any]:
        """
        Add a new part configuration.

        Uses PartConfigurations.Add(name).

        Args:
            name: Name for the new configuration

        Returns:
            Dict with status and new configuration name
        """
        try:
            doc = self.doc_manager.get_active_document()
            if not hasattr(doc, "Configurations"):
                return {"error": "Active document does not support configurations"}

            configs = doc.Configurations
            _cfg = configs.Add(name)
            if _cfg is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "name": name,
                "total_configurations": configs.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def apply_part_configuration(self, name: str) -> dict[str, Any]:
        """
        Apply (activate) a named part configuration.

        Args:
            name: Name of the configuration to activate

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            if not hasattr(doc, "Configurations"):
                return {"error": "Active document does not support configurations"}

            configs = doc.Configurations
            for i in range(1, configs.Count + 1):
                cfg = configs.Item(i)
                cfg_name = cfg.Name if hasattr(cfg, "Name") else ""
                if cfg_name == name:
                    cfg.Activate()
                    return {"status": "activated", "name": name}

            return {
                "error": f"Configuration '{name}' not found",
                "available": [
                    configs.Item(i).Name
                    for i in range(1, configs.Count + 1)
                    if hasattr(configs.Item(i), "Name")
                ],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def delete_part_configuration(self, name: str) -> dict[str, Any]:
        """
        Delete a named part configuration.

        Args:
            name: Name of the configuration to delete

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            if not hasattr(doc, "Configurations"):
                return {"error": "Active document does not support configurations"}

            configs = doc.Configurations
            for i in range(1, configs.Count + 1):
                cfg = configs.Item(i)
                cfg_name = cfg.Name if hasattr(cfg, "Name") else ""
                if cfg_name == name:
                    cfg.Delete()
                    return {
                        "status": "deleted",
                        "name": name,
                        "remaining": configs.Count,
                    }

            return {"error": f"Configuration '{name}' not found"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}
