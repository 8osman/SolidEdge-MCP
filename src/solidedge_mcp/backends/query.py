"""
Solid Edge Query and Inspection Operations

Handles querying model data, measurements, and properties.
"""

from typing import Dict, Any
import math
import traceback


class QueryManager:
    """Manages query and inspection operations"""

    def __init__(self, document_manager):
        self.doc_manager = document_manager

    def _get_first_model(self):
        """Get the first model from the active document."""
        doc = self.doc_manager.get_active_document()
        if not hasattr(doc, 'Models'):
            raise Exception("Document does not have a Models collection")
        models = doc.Models
        if models.Count == 0:
            raise Exception("No features in document")
        return doc, models.Item(1)

    def get_mass_properties(self, density: float = 7850) -> Dict[str, Any]:
        """
        Get mass properties of the part.

        Uses Model.ComputePhysicalProperties(status, density, accuracy) which
        returns a tuple: (volume, area, mass, cog_tuple, cov_tuple, moi_tuple, ...)

        Args:
            density: Material density in kg/m³ (default: 7850 for steel)

        Returns:
            Dict with volume, mass, surface area, center of gravity, moments of inertia
        """
        try:
            doc, model = self._get_first_model()

            # ComputePhysicalPropertiesWithSpecifiedDensity(Density, Accuracy)
            # Returns tuple: (volume, area, mass, cog, cov, moi, principal_moi,
            #                  principal_axes, radii_of_gyration, ?, ?)
            result = model.ComputePhysicalPropertiesWithSpecifiedDensity(
                density, 0.99
            )

            volume = result[0] if len(result) > 0 else 0
            surface_area = result[1] if len(result) > 1 else 0
            mass_val = result[2] if len(result) > 2 else 0
            cog = result[3] if len(result) > 3 else (0, 0, 0)
            cov = result[4] if len(result) > 4 else (0, 0, 0)
            moi = result[5] if len(result) > 5 else (0, 0, 0, 0, 0, 0)
            principal_moi = result[6] if len(result) > 6 else (0, 0, 0)

            return {
                "status": "computed",
                "density": density,
                "volume": volume,
                "surface_area": surface_area,
                "mass": mass_val,
                "center_of_gravity": list(cog) if cog else [0, 0, 0],
                "center_of_volume": list(cov) if cov else [0, 0, 0],
                "moments_of_inertia": {
                    "Ixx": moi[0] if len(moi) > 0 else 0,
                    "Iyy": moi[1] if len(moi) > 1 else 0,
                    "Izz": moi[2] if len(moi) > 2 else 0,
                    "Ixy": moi[3] if len(moi) > 3 else 0,
                    "Ixz": moi[4] if len(moi) > 4 else 0,
                    "Iyz": moi[5] if len(moi) > 5 else 0,
                },
                "principal_moments": list(principal_moi) if principal_moi else [0, 0, 0],
                "units": {
                    "volume": "m³",
                    "surface_area": "m²",
                    "mass": "kg",
                    "density": "kg/m³",
                    "moments_of_inertia": "kg·m²",
                    "coordinates": "meters"
                }
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def get_bounding_box(self) -> Dict[str, Any]:
        """
        Get the bounding box of the model.

        Uses Body.GetRange() which returns ((min_x, min_y, min_z), (max_x, max_y, max_z)).

        Returns:
            Dict with min/max coordinates and dimensions
        """
        try:
            doc, model = self._get_first_model()

            body = model.Body
            range_data = body.GetRange()

            min_pt = range_data[0]
            max_pt = range_data[1]

            return {
                "status": "computed",
                "min": list(min_pt),
                "max": list(max_pt),
                "dimensions": {
                    "x": max_pt[0] - min_pt[0],
                    "y": max_pt[1] - min_pt[1],
                    "z": max_pt[2] - min_pt[2]
                },
                "units": "meters"
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def list_features(self) -> Dict[str, Any]:
        """
        List all features in the active document.

        Uses Model.Features collection and DesignEdgebarFeatures for the feature tree.

        Returns:
            Dict with list of features
        """
        try:
            doc, model = self._get_first_model()

            features = []

            # Use DesignEdgebarFeatures for the full feature tree
            if hasattr(doc, 'DesignEdgebarFeatures'):
                debf = doc.DesignEdgebarFeatures
                for i in range(1, debf.Count + 1):
                    try:
                        feat = debf.Item(i)
                        feat_info = {
                            "index": i - 1,
                            "name": feat.Name if hasattr(feat, 'Name') else f"Feature_{i}",
                        }
                        features.append(feat_info)
                    except Exception:
                        features.append({"index": i - 1, "name": f"Feature_{i}"})
            else:
                # Fallback to Model.Features
                model_features = model.Features
                for i in range(1, model_features.Count + 1):
                    try:
                        feat = model_features.Item(i)
                        feat_info = {
                            "index": i - 1,
                            "name": feat.Name if hasattr(feat, 'Name') else f"Feature_{i}",
                        }
                        features.append(feat_info)
                    except Exception:
                        features.append({"index": i - 1, "name": f"Feature_{i}"})

            return {
                "features": features,
                "count": len(features)
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def measure_distance(self, x1: float, y1: float, z1: float,
                        x2: float, y2: float, z2: float) -> Dict[str, Any]:
        """
        Measure distance between two points.

        Args:
            x1, y1, z1: First point coordinates
            x2, y2, z2: Second point coordinates

        Returns:
            Dict with distance and components
        """
        try:
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1

            distance = math.sqrt(dx**2 + dy**2 + dz**2)

            return {
                "distance": distance,
                "delta": {
                    "x": dx,
                    "y": dy,
                    "z": dz
                },
                "point1": [x1, y1, z1],
                "point2": [x2, y2, z2],
                "units": "meters"
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def get_document_properties(self) -> Dict[str, Any]:
        """Get document properties and metadata"""
        try:
            doc = self.doc_manager.get_active_document()

            properties = {
                "name": doc.Name if hasattr(doc, 'Name') else "Unknown",
                "path": doc.FullName if hasattr(doc, 'FullName') else "Unsaved",
                "modified": not doc.Saved if hasattr(doc, 'Saved') else False,
                "read_only": doc.ReadOnly if hasattr(doc, 'ReadOnly') else False
            }

            # Try to get summary info
            try:
                if hasattr(doc, 'SummaryInfo'):
                    summary = doc.SummaryInfo
                    if hasattr(summary, 'Title'):
                        properties["title"] = summary.Title
                    if hasattr(summary, 'Author'):
                        properties["author"] = summary.Author
                    if hasattr(summary, 'Subject'):
                        properties["subject"] = summary.Subject
                    if hasattr(summary, 'Comments'):
                        properties["comments"] = summary.Comments
            except:
                pass

            # Add body topology info
            try:
                models = doc.Models
                if models.Count > 0:
                    body = models.Item(1).Body
                    properties["volume_m3"] = body.Volume
            except:
                pass

            return properties
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def get_feature_count(self) -> Dict[str, Any]:
        """Get count of features in the document"""
        try:
            doc = self.doc_manager.get_active_document()

            counts = {}

            if hasattr(doc, 'DesignEdgebarFeatures'):
                counts["features"] = doc.DesignEdgebarFeatures.Count

            if hasattr(doc, 'Models'):
                counts["models"] = doc.Models.Count

            if hasattr(doc, 'ProfileSets'):
                counts["sketches"] = doc.ProfileSets.Count

            if hasattr(doc, 'RefPlanes'):
                counts["ref_planes"] = doc.RefPlanes.Count

            if hasattr(doc, 'Variables'):
                counts["variables"] = doc.Variables.Count

            return counts
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    # =================================================================
    # VARIABLES
    # =================================================================

    def get_variables(self) -> Dict[str, Any]:
        """
        Get all variables from the active document.

        Queries the Variables collection using Query() to list all
        variable names, values, and formulas.

        Returns:
            Dict with list of variables
        """
        try:
            doc = self.doc_manager.get_active_document()
            variables = doc.Variables

            var_list = []
            for i in range(1, variables.Count + 1):
                try:
                    var = variables.Item(i)
                    var_info = {
                        "index": i - 1,
                        "name": var.DisplayName if hasattr(var, 'DisplayName') else f"Var_{i}",
                    }
                    try:
                        var_info["value"] = var.Value
                    except Exception:
                        pass
                    try:
                        var_info["formula"] = var.Formula
                    except Exception:
                        pass
                    try:
                        var_info["units"] = var.Units
                    except Exception:
                        pass
                    var_list.append(var_info)
                except Exception:
                    var_list.append({"index": i - 1, "name": f"Var_{i}"})

            return {
                "variables": var_list,
                "count": len(var_list)
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def get_variable(self, name: str) -> Dict[str, Any]:
        """
        Get a specific variable by name.

        Args:
            name: Variable display name (e.g., 'V1', 'Mass', 'Volume')

        Returns:
            Dict with variable value and info
        """
        try:
            doc = self.doc_manager.get_active_document()
            variables = doc.Variables

            # Search for the variable by display name
            for i in range(1, variables.Count + 1):
                try:
                    var = variables.Item(i)
                    display_name = var.DisplayName if hasattr(var, 'DisplayName') else ""
                    if display_name == name:
                        result = {"name": name, "index": i - 1}
                        try:
                            result["value"] = var.Value
                        except Exception:
                            pass
                        try:
                            result["formula"] = var.Formula
                        except Exception:
                            pass
                        try:
                            result["units"] = var.Units
                        except Exception:
                            pass
                        return result
                except Exception:
                    continue

            return {"error": f"Variable '{name}' not found"}
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def set_variable(self, name: str, value: float) -> Dict[str, Any]:
        """
        Set a variable's value by name.

        Args:
            name: Variable display name
            value: New value to set

        Returns:
            Dict with status and updated value
        """
        try:
            doc = self.doc_manager.get_active_document()
            variables = doc.Variables

            for i in range(1, variables.Count + 1):
                try:
                    var = variables.Item(i)
                    display_name = var.DisplayName if hasattr(var, 'DisplayName') else ""
                    if display_name == name:
                        old_value = var.Value
                        var.Value = value
                        return {
                            "status": "updated",
                            "name": name,
                            "old_value": old_value,
                            "new_value": value
                        }
                except Exception:
                    continue

            return {"error": f"Variable '{name}' not found"}
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    # =================================================================
    # CUSTOM PROPERTIES
    # =================================================================

    def get_custom_properties(self) -> Dict[str, Any]:
        """
        Get all custom properties from the active document.

        Accesses the PropertySets collection to retrieve custom properties.

        Returns:
            Dict with list of custom properties (name/value pairs)
        """
        try:
            doc = self.doc_manager.get_active_document()
            prop_sets = doc.Properties

            properties = {}

            # Iterate through property sets to find Custom
            for ps_idx in range(1, prop_sets.Count + 1):
                try:
                    ps = prop_sets.Item(ps_idx)
                    ps_name = ps.Name if hasattr(ps, 'Name') else f"Set_{ps_idx}"

                    props = {}
                    for p_idx in range(1, ps.Count + 1):
                        try:
                            prop = ps.Item(p_idx)
                            prop_name = prop.Name if hasattr(prop, 'Name') else f"Prop_{p_idx}"
                            try:
                                props[prop_name] = prop.Value
                            except Exception:
                                props[prop_name] = None
                        except Exception:
                            continue

                    properties[ps_name] = props
                except Exception:
                    continue

            return {
                "property_sets": properties,
                "count": len(properties)
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def set_custom_property(self, name: str, value: str) -> Dict[str, Any]:
        """
        Set or create a custom property.

        Creates the property if it doesn't exist, updates it if it does.

        Args:
            name: Property name
            value: Property value (string)

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            prop_sets = doc.Properties

            # Find "Custom" property set (typically the last one, index varies)
            custom_ps = None
            for ps_idx in range(1, prop_sets.Count + 1):
                try:
                    ps = prop_sets.Item(ps_idx)
                    if hasattr(ps, 'Name') and ps.Name == "Custom":
                        custom_ps = ps
                        break
                except Exception:
                    continue

            if custom_ps is None:
                return {"error": "Custom property set not found"}

            # Check if property exists
            for p_idx in range(1, custom_ps.Count + 1):
                try:
                    prop = custom_ps.Item(p_idx)
                    if hasattr(prop, 'Name') and prop.Name == name:
                        old_value = prop.Value
                        prop.Value = value
                        return {
                            "status": "updated",
                            "name": name,
                            "old_value": old_value,
                            "new_value": value
                        }
                except Exception:
                    continue

            # Property doesn't exist, add it
            custom_ps.Add(name, value)
            return {
                "status": "created",
                "name": name,
                "value": value
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def delete_custom_property(self, name: str) -> Dict[str, Any]:
        """
        Delete a custom property by name.

        Args:
            name: Property name to delete

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            prop_sets = doc.Properties

            # Find "Custom" property set
            for ps_idx in range(1, prop_sets.Count + 1):
                try:
                    ps = prop_sets.Item(ps_idx)
                    if hasattr(ps, 'Name') and ps.Name == "Custom":
                        for p_idx in range(1, ps.Count + 1):
                            try:
                                prop = ps.Item(p_idx)
                                if hasattr(prop, 'Name') and prop.Name == name:
                                    prop.Delete()
                                    return {
                                        "status": "deleted",
                                        "name": name
                                    }
                            except Exception:
                                continue
                        return {"error": f"Property '{name}' not found in Custom set"}
                except Exception:
                    continue

            return {"error": "Custom property set not found"}
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    # =================================================================
    # BODY TOPOLOGY QUERIES
    # =================================================================

    def get_body_faces(self) -> Dict[str, Any]:
        """
        Get all faces on the model body.

        Uses Body.Faces(igQueryAll=6) to enumerate faces with their
        type and edge count.

        Returns:
            Dict with list of faces
        """
        try:
            doc, model = self._get_first_model()
            body = model.Body

            faces = body.Faces(6)  # igQueryAll = 6
            face_list = []

            for i in range(1, faces.Count + 1):
                try:
                    face = faces.Item(i)
                    face_info = {"index": i - 1}
                    try:
                        face_info["type"] = face.Type
                    except Exception:
                        pass
                    try:
                        face_info["area"] = face.Area
                    except Exception:
                        pass
                    try:
                        edge_count = face.Edges.Count if hasattr(face.Edges, 'Count') else 0
                        face_info["edge_count"] = edge_count
                    except Exception:
                        pass
                    face_list.append(face_info)
                except Exception:
                    face_list.append({"index": i - 1})

            return {
                "faces": face_list,
                "count": len(face_list)
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def get_body_edges(self) -> Dict[str, Any]:
        """
        Get all unique edges on the model body.

        Enumerates edges via faces since Body.Edges() doesn't work
        in COM late binding. Deduplicates by collecting from all faces.

        Returns:
            Dict with edge count and face-edge mapping
        """
        try:
            doc, model = self._get_first_model()
            body = model.Body

            faces = body.Faces(6)  # igQueryAll = 6
            total_edges = 0
            face_edges = []

            for fi in range(1, faces.Count + 1):
                try:
                    face = faces.Item(fi)
                    edges = face.Edges
                    edge_count = edges.Count if hasattr(edges, 'Count') else 0
                    total_edges += edge_count
                    face_edges.append({
                        "face_index": fi - 1,
                        "edge_count": edge_count
                    })
                except Exception:
                    face_edges.append({"face_index": fi - 1, "edge_count": 0})

            return {
                "face_edges": face_edges,
                "total_face_count": faces.Count,
                "total_edge_references": total_edges,
                "note": "Edge count includes shared edges (counted once per face)"
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def get_face_info(self, face_index: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific face.

        Args:
            face_index: 0-based face index

        Returns:
            Dict with face type, area, edge count, and vertex count
        """
        try:
            doc, model = self._get_first_model()
            body = model.Body

            faces = body.Faces(6)  # igQueryAll = 6
            if face_index < 0 or face_index >= faces.Count:
                return {"error": f"Invalid face index: {face_index}. Count: {faces.Count}"}

            face = faces.Item(face_index + 1)

            info = {"index": face_index}

            try:
                info["type"] = face.Type
            except Exception:
                pass
            try:
                info["area"] = face.Area
            except Exception:
                pass
            try:
                edges = face.Edges
                info["edge_count"] = edges.Count if hasattr(edges, 'Count') else 0
            except Exception:
                pass
            try:
                vertices = face.Vertices
                info["vertex_count"] = vertices.Count if hasattr(vertices, 'Count') else 0
            except Exception:
                pass

            return info
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    # =================================================================
    # PERFORMANCE & RECOMPUTE
    # =================================================================

    def recompute(self) -> Dict[str, Any]:
        """
        Recompute the active document and model.

        Forces recalculation of all features.

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            # Try model-level recompute first
            try:
                models = doc.Models
                if models.Count > 0:
                    model = models.Item(1)
                    model.Recompute()
            except Exception:
                pass

            # Also try document-level recompute
            try:
                doc.Recompute()
            except Exception:
                pass

            return {"status": "recomputed"}
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
