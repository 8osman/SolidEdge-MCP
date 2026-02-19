"""
Solid Edge Assembly Operations

Handles assembly creation and component management.
"""

import contextlib
import inspect
import json
import math
import os
import traceback
from pathlib import Path
from typing import Any

import pythoncom
from win32com.client import VARIANT

from .constants import DirectionConstants, ExtentTypeConstants

# Persist feature names across MCP server restarts (stdio = fresh process per session).
# COM objects can't be serialised, but names let us give a useful "recreate" error
# instead of a silent "not found" after reconnect.
_FEATURE_NAMES_FILE = Path.home() / ".solidedge_mcp_feature_cache.json"


class AssemblyManager:
    """Manages assembly operations"""

    def __init__(self, document_manager, sketch_manager=None):
        self.doc_manager = document_manager
        self.sketch_manager = sketch_manager  # Optional; needed for assembly features
        # name → live COM object (same process only; validated before use)
        self._asm_feature_cache: dict[str, Any] = {}
        # names that survive process restart (loaded from disk on init)
        self._persistent_feature_names: set[str] = self._load_persistent_names()

    # ── persistence helpers ──────────────────────────────────────────────────

    @staticmethod
    def _load_persistent_names() -> set[str]:
        """Load known feature names from disk; return empty set on any error."""
        try:
            data = json.loads(_FEATURE_NAMES_FILE.read_text(encoding="utf-8"))
            return set(data.get("feature_names", []))
        except Exception:
            return set()

    def _save_persistent_names(self) -> None:
        """Flush current known names (cache + persistent) to disk."""
        try:
            all_names = self._persistent_feature_names | set(self._asm_feature_cache.keys())
            _FEATURE_NAMES_FILE.write_text(
                json.dumps({"feature_names": sorted(all_names)}, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass  # persistence is best-effort; don't break feature creation

    def add_component(
        self, file_path: str, x: float = 0, y: float = 0, z: float = 0
    ) -> dict[str, Any]:
        """
        Add a component (part) to the active assembly.

        Uses Occurrences.AddByFilename for origin placement, or
        Occurrences.AddWithMatrix for positioned placement.

        Args:
            file_path: Path to the part file (.par or .asm)
            x, y, z: Position coordinates in meters

        Returns:
            Dict with status and component info
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if x == 0 and y == 0 and z == 0:
                # Place at origin
                occurrence = occurrences.AddByFilename(file_path)
            else:
                # Place with transformation matrix (identity rotation + translation)
                matrix = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, x, y, z, 1.0]
                occurrence = occurrences.AddWithMatrix(file_path, matrix)

            # Get actual position from transform
            try:
                transform = occurrence.GetTransform()
                position = [transform[0], transform[1], transform[2]]
            except Exception:
                position = [x, y, z]

            return {
                "status": "added",
                "file_path": file_path,
                "name": (
                    occurrence.Name if hasattr(occurrence, "Name") else os.path.basename(file_path)
                ),
                "position": position,
                "index": occurrences.Count - 1,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # Alias for MCP tool compatibility
    place_component = add_component

    def list_components(self) -> dict[str, Any]:
        """
        List all components in the active assembly.

        Uses Occurrence.GetTransform() for position/rotation and
        OccurrenceFileName for file path.

        Returns:
            Dict with list of components and their properties
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            components = []

            for i in range(1, occurrences.Count + 1):
                occurrence = occurrences.Item(i)
                comp = {
                    "index": i - 1,
                    "name": occurrence.Name if hasattr(occurrence, "Name") else f"Component {i}",
                }

                # Get file path
                try:
                    comp["file_path"] = occurrence.OccurrenceFileName
                except Exception:
                    comp["file_path"] = "Unknown"

                # Get transform (originX, originY, originZ, angleX, angleY, angleZ)
                try:
                    transform = occurrence.GetTransform()
                    comp["position"] = [transform[0], transform[1], transform[2]]
                    comp["rotation"] = [transform[3], transform[4], transform[5]]
                except Exception:
                    comp["position"] = [0, 0, 0]
                    comp["rotation"] = [0, 0, 0]

                # Visibility/suppression
                try:
                    comp["visible"] = occurrence.Visible
                except Exception:
                    comp["visible"] = True

                components.append(comp)

            return {"components": components, "count": len(components)}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_mate(
        self, mate_type: str, component1_index: int, component2_index: int
    ) -> dict[str, Any]:
        """
        Create a mate/assembly relationship between components.

        Note: Actual mate creation requires face/edge selection which cannot
        be done programmatically without specific geometry references.

        Args:
            mate_type: Type of mate - 'Planar', 'Axial', 'Insert', 'Match', 'Parallel', 'Angle'
            component1_index: Index of first component
            component2_index: Index of second component

        Returns:
            Dict with status and mate info
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Relations3d"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component1_index >= occurrences.Count or component2_index >= occurrences.Count:
                return {"error": "Invalid component index"}

            # Mate creation requires face/edge selection
            return {
                "error": "Mate creation requires face/edge "
                "selection which is not available via "
                "COM automation. Use Solid Edge UI to "
                "create mates.",
                "mate_type": mate_type,
                "component1": component1_index,
                "component2": component2_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_component_info(self, component_index: int) -> dict[str, Any]:
        """
        Get detailed information about a specific component.

        Uses GetTransform for position/rotation and GetMatrix for the full 4x4 matrix.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with component details
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)

            info = {
                "index": component_index,
                "name": occurrence.Name if hasattr(occurrence, "Name") else "Unknown",
            }

            # File path
            try:
                info["file_path"] = occurrence.OccurrenceFileName
            except Exception:
                info["file_path"] = "Unknown"

            # Transform (position + rotation)
            try:
                transform = occurrence.GetTransform()
                info["position"] = [transform[0], transform[1], transform[2]]
                info["rotation_rad"] = [transform[3], transform[4], transform[5]]
            except Exception:
                pass

            # Full 4x4 matrix
            try:
                matrix = occurrence.GetMatrix()
                info["matrix"] = list(matrix)
            except Exception:
                pass

            # Visibility
            with contextlib.suppress(Exception):
                info["visible"] = occurrence.Visible

            # Occurrence document info
            try:
                occ_doc = occurrence.OccurrenceDocument
                info["document_name"] = occ_doc.Name
            except Exception:
                pass

            return info
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def update_component_position(
        self, component_index: int, x: float, y: float, z: float
    ) -> dict[str, Any]:
        """
        Update a component's position using a transformation matrix.

        Args:
            component_index: 0-based index of the component
            x, y, z: New position coordinates (meters)

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {"error": f"Invalid component index: {component_index}"}

            occurrence = occurrences.Item(component_index + 1)

            # Get current matrix to preserve rotation
            try:
                current = list(occurrence.GetMatrix())
                # Update translation (indices 12, 13, 14 in row-major 4x4)
                current[12] = x
                current[13] = y
                current[14] = z
                occurrence.SetMatrix(current)
                return {
                    "status": "position_updated",
                    "component": component_index,
                    "position": [x, y, z],
                }
            except Exception as e:
                return {
                    "error": f"Could not update position: {e}",
                    "note": "Position update may not be available for grounded components",
                }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_align_constraint(self, component1_index: int, component2_index: int) -> dict[str, Any]:
        """Add an align constraint between two components (requires UI for face selection)"""
        return {
            "error": "Constraint creation requires face/edge selection. Use Solid Edge UI.",
            "constraint_type": "align",
            "component1": component1_index,
            "component2": component2_index,
        }

    def add_angle_constraint(
        self, component1_index: int, component2_index: int, angle: float
    ) -> dict[str, Any]:
        """Add an angle constraint between two components (requires UI for face selection)"""
        return {
            "error": "Constraint creation requires face/edge selection. Use Solid Edge UI.",
            "constraint_type": "angle",
            "component1": component1_index,
            "component2": component2_index,
            "angle": angle,
        }

    def add_planar_align_constraint(
        self, component1_index: int, component2_index: int
    ) -> dict[str, Any]:
        """Add a planar align constraint (requires UI for face selection)"""
        return {
            "error": "Constraint creation requires face/edge selection. Use Solid Edge UI.",
            "constraint_type": "planar_align",
            "component1": component1_index,
            "component2": component2_index,
        }

    def add_axial_align_constraint(
        self, component1_index: int, component2_index: int
    ) -> dict[str, Any]:
        """Add an axial align constraint (requires UI for face selection)"""
        return {
            "error": "Constraint creation requires face/edge selection. Use Solid Edge UI.",
            "constraint_type": "axial_align",
            "component1": component1_index,
            "component2": component2_index,
        }

    def pattern_component(
        self, component_index: int, count: int, spacing: float, direction: str = "X"
    ) -> dict[str, Any]:
        """
        Create a linear pattern of a component by placing copies with offset.

        Args:
            component_index: 0-based index of the source component
            count: Number of total instances (including original)
            spacing: Distance between instances (meters)
            direction: Pattern direction - 'X', 'Y', or 'Z'

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {"error": f"Invalid component index: {component_index}"}

            source = occurrences.Item(component_index + 1)

            # Get the source file path
            try:
                file_path = source.OccurrenceFileName
            except Exception:
                return {"error": "Cannot determine source component file path"}

            # Get source position
            try:
                base_matrix = list(source.GetMatrix())
            except Exception:
                base_matrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

            dir_map = {"X": 12, "Y": 13, "Z": 14}
            dir_idx = dir_map.get(direction, 12)

            placed = []
            for i in range(1, count):
                matrix = list(base_matrix)
                matrix[dir_idx] = base_matrix[dir_idx] + (spacing * i)
                occ = occurrences.AddWithMatrix(file_path, matrix)
                placed.append(occ.Name if hasattr(occ, "Name") else f"copy_{i}")

            return {
                "status": "pattern_created",
                "source_component": component_index,
                "count": count,
                "spacing": spacing,
                "direction": direction,
                "placed_names": placed,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def suppress_component(self, component_index: int, suppress: bool = True) -> dict[str, Any]:
        """Suppress or unsuppress a component"""
        try:
            doc = self.doc_manager.get_active_document()
            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {"error": f"Invalid component index: {component_index}"}

            occurrence = occurrences.Item(component_index + 1)

            if hasattr(occurrence, "Suppress") and suppress:
                occurrence.Suppress()
            elif hasattr(occurrence, "Unsuppress") and not suppress:
                occurrence.Unsuppress()
            else:
                return {"error": "Suppress/Unsuppress not available on this occurrence"}

            return {"status": "updated", "component": component_index, "suppressed": suppress}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_occurrence_bounding_box(self, component_index: int) -> dict[str, Any]:
        """
        Get the bounding box of a specific component (occurrence) in the assembly.

        Uses Occurrence.GetRangeBox() which returns min/max 3D points.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with min/max coordinates
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)

            # GetRangeBox returns two arrays via out params
            import array

            min_point = array.array("d", [0.0, 0.0, 0.0])
            max_point = array.array("d", [0.0, 0.0, 0.0])

            occurrence.GetRangeBox(min_point, max_point)

            return {
                "component_index": component_index,
                "min": [min_point[0], min_point[1], min_point[2]],
                "max": [max_point[0], max_point[1], max_point[2]],
                "size": [
                    max_point[0] - min_point[0],
                    max_point[1] - min_point[1],
                    max_point[2] - min_point[2],
                ],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_bom(self) -> dict[str, Any]:
        """
        Get Bill of Materials from the active assembly.

        Recursively traverses all occurrences, deduplicates by file path,
        and returns a flat BOM with quantities.

        Returns:
            Dict with BOM items (file, name, quantity)
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            bom_counts: dict[str, dict[str, Any]] = {}

            for i in range(1, occurrences.Count + 1):
                occurrence = occurrences.Item(i)

                # Skip items excluded from BOM
                try:
                    if hasattr(occurrence, "IncludeInBom") and not occurrence.IncludeInBom:
                        continue
                except Exception:
                    pass

                # Skip pattern items (counted as part of pattern source)
                try:
                    if hasattr(occurrence, "IsPatternItem") and occurrence.IsPatternItem:
                        continue
                except Exception:
                    pass

                # Get file path as key
                try:
                    file_path = occurrence.OccurrenceFileName
                except Exception:
                    file_path = f"Unknown_{i}"

                name = (
                    occurrence.Name if hasattr(occurrence, "Name") else os.path.basename(file_path)
                )

                if file_path in bom_counts:
                    bom_counts[file_path]["quantity"] += 1
                else:
                    bom_counts[file_path] = {"name": name, "file_path": file_path, "quantity": 1}

            bom_items = list(bom_counts.values())

            return {
                "total_occurrences": occurrences.Count,
                "unique_parts": len(bom_items),
                "bom": bom_items,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_assembly_relations(self) -> dict[str, Any]:
        """
        Get all assembly relations (constraints) in the active assembly.

        Iterates the Relations3d collection to report constraint types,
        status, and connected occurrences.

        Returns:
            Dict with list of relations and their properties
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Relations3d"):
                return {"error": "Active document is not an assembly"}

            relations = doc.Relations3d
            relation_list = []

            # Relation type constants
            type_names = {
                0: "Ground",
                1: "Axial",
                2: "Planar",
                3: "Connect",
                4: "Angle",
                5: "Tangent",
                6: "Cam",
                7: "Gear",
                8: "ParallelAxis",
                9: "Center",
            }

            for i in range(1, relations.Count + 1):
                try:
                    rel = relations.Item(i)
                    rel_info = {"index": i - 1}

                    try:
                        rel_info["type"] = rel.Type
                        rel_info["type_name"] = type_names.get(rel.Type, f"Unknown({rel.Type})")
                    except Exception:
                        pass

                    with contextlib.suppress(Exception):
                        rel_info["status"] = rel.Status

                    with contextlib.suppress(Exception):
                        rel_info["suppressed"] = rel.Suppressed

                    with contextlib.suppress(Exception):
                        rel_info["name"] = rel.Name

                    relation_list.append(rel_info)
                except Exception:
                    relation_list.append({"index": i - 1})

            return {"relations": relation_list, "count": len(relation_list)}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_document_tree(self) -> dict[str, Any]:
        """
        Get the hierarchical document tree of the active assembly.

        Recursively traverses occurrences and sub-occurrences to build
        a nested tree structure showing the full assembly hierarchy.

        Returns:
            Dict with nested tree of components
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            def traverse_occurrence(occ, depth=0):
                """Recursively build tree from an occurrence."""
                node = {}

                try:
                    node["name"] = occ.Name
                except Exception:
                    node["name"] = "Unknown"

                try:
                    node["file"] = occ.OccurrenceFileName
                except Exception:
                    node["file"] = "Unknown"

                with contextlib.suppress(Exception):
                    node["visible"] = occ.Visible

                with contextlib.suppress(Exception):
                    node["suppressed"] = occ.IsSuppressed if hasattr(occ, "IsSuppressed") else False

                # Recurse into sub-occurrences
                children = []
                try:
                    sub_occs = occ.SubOccurrences
                    if sub_occs and hasattr(sub_occs, "Count"):
                        for j in range(1, sub_occs.Count + 1):
                            try:
                                child = sub_occs.Item(j)
                                children.append(traverse_occurrence(child, depth + 1))
                            except Exception:
                                children.append({"name": f"SubOcc_{j}", "error": "could not read"})
                except Exception:
                    pass

                if children:
                    node["children"] = children

                return node

            occurrences = doc.Occurrences
            tree = []

            for i in range(1, occurrences.Count + 1):
                try:
                    occ = occurrences.Item(i)
                    tree.append(traverse_occurrence(occ))
                except Exception:
                    tree.append({"name": f"Occurrence_{i}", "error": "could not read"})

            return {
                "tree": tree,
                "top_level_count": len(tree),
                "document": doc.Name if hasattr(doc, "Name") else "Unknown",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def set_component_visibility(self, component_index: int, visible: bool) -> dict[str, Any]:
        """
        Set the visibility of a component in the assembly.

        Args:
            component_index: 0-based index of the component
            visible: True to show, False to hide

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)
            occurrence.Visible = visible

            return {"status": "updated", "component_index": component_index, "visible": visible}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def is_subassembly(self, component_index: int) -> dict[str, Any]:
        """
        Check if a component is a subassembly (vs a part).

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with is_subassembly boolean
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)

            result = {"component_index": component_index}

            try:
                result["is_subassembly"] = occurrence.Subassembly
            except Exception:
                # Fallback: check if it has SubOccurrences
                try:
                    sub_occs = occurrence.SubOccurrences
                    result["is_subassembly"] = (
                        sub_occs.Count > 0 if hasattr(sub_occs, "Count") else False
                    )
                except Exception:
                    result["is_subassembly"] = False

            with contextlib.suppress(Exception):
                result["name"] = occurrence.Name

            return result
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_component_display_name(self, component_index: int) -> dict[str, Any]:
        """
        Get the display name of a component.

        The display name is the user-visible label in the assembly tree,
        which may differ from the internal Name or OccurrenceFileName.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with display_name and other name info
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)

            result = {"component_index": component_index}

            try:
                result["display_name"] = occurrence.DisplayName
            except Exception:
                result["display_name"] = None

            with contextlib.suppress(Exception):
                result["name"] = occurrence.Name

            with contextlib.suppress(Exception):
                result["file_name"] = occurrence.OccurrenceFileName

            return result
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_occurrence_document(self, component_index: int) -> dict[str, Any]:
        """
        Get document info for a component's source file.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with document name, path, and type
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)

            result = {"component_index": component_index}

            try:
                occ_doc = occurrence.OccurrenceDocument
                with contextlib.suppress(Exception):
                    result["document_name"] = occ_doc.Name
                with contextlib.suppress(Exception):
                    result["full_name"] = occ_doc.FullName
                with contextlib.suppress(Exception):
                    result["type"] = occ_doc.Type
                with contextlib.suppress(Exception):
                    result["read_only"] = occ_doc.ReadOnly
            except Exception:
                result["error_note"] = "Could not access OccurrenceDocument"

            with contextlib.suppress(Exception):
                result["file_name"] = occurrence.OccurrenceFileName

            return result
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_sub_occurrences(self, component_index: int) -> dict[str, Any]:
        """
        Get sub-occurrences (children) of a component.

        For subassemblies, this returns the list of nested components.
        For parts, this returns an empty list.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with list of sub-occurrence names and count
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)

            children = []
            try:
                sub_occs = occurrence.SubOccurrences
                if sub_occs and hasattr(sub_occs, "Count"):
                    for j in range(1, sub_occs.Count + 1):
                        try:
                            child = sub_occs.Item(j)
                            child_info = {"index": j - 1}
                            try:
                                child_info["name"] = child.Name
                            except Exception:
                                child_info["name"] = f"SubOcc_{j}"
                            with contextlib.suppress(Exception):
                                child_info["file"] = child.OccurrenceFileName
                            children.append(child_info)
                        except Exception:
                            children.append({"index": j - 1, "name": f"SubOcc_{j}"})
            except Exception:
                pass

            return {
                "component_index": component_index,
                "sub_occurrences": children,
                "count": len(children),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def delete_component(self, component_index: int) -> dict[str, Any]:
        """
        Delete/remove a component from the assembly.

        Args:
            component_index: 0-based index of the component to remove

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)
            name = (
                occurrence.Name if hasattr(occurrence, "Name") else f"Component_{component_index}"
            )
            occurrence.Delete()

            return {"status": "deleted", "component_index": component_index, "name": name}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def ground_component(self, component_index: int, ground: bool = True) -> dict[str, Any]:
        """
        Ground (fix in place) or unground a component in the assembly.

        Args:
            component_index: 0-based index of the component
            ground: True to ground, False to unground

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)

            if ground:
                # Add a ground constraint
                relations = doc.Relations3d
                _feature = relations.AddGround(occurrence)
                if _feature is None:
                    return {"error": "Feature creation failed: COM returned None"}
                return {"status": "grounded", "component_index": component_index}
            else:
                # Find and delete ground relation for this occurrence
                relations = doc.Relations3d
                for i in range(relations.Count, 0, -1):
                    try:
                        rel = relations.Item(i)
                        # Ground relations have Type = 0
                        if hasattr(rel, "Type") and rel.Type == 0:
                            rel.Delete()
                            return {"status": "ungrounded", "component_index": component_index}
                    except Exception:
                        continue

                return {"error": "No ground relation found for this component"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def check_interference(self, component_index: int | None = None) -> dict[str, Any]:
        """
        Run interference check on the active assembly.

        If component_index is provided, checks that component against all others.
        If not provided, checks all components against each other.

        Args:
            component_index: Optional 0-based index of a specific component to check

        Returns:
            Dict with interference status and details
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if occurrences.Count < 2:
                return {
                    "status": "no_interference",
                    "message": "Need at least 2 components for interference check",
                }

            import ctypes

            # Build set1 - single component or all
            if component_index is not None:
                if component_index < 0 or component_index >= occurrences.Count:
                    return {"error": f"Invalid component index: {component_index}"}
                set1 = [occurrences.Item(component_index + 1)]
            else:
                set1 = [occurrences.Item(i) for i in range(1, occurrences.Count + 1)]

            # Call CheckInterference
            # seInterferenceComparisonSet1vsAllOther = 1
            comparison_method = 1

            # Prepare out parameters
            interference_status = ctypes.c_int(0)
            num_interferences = ctypes.c_int(0)

            try:
                doc.CheckInterference(
                    NumElementsSet1=len(set1),
                    Set1=set1,
                    Status=interference_status,
                    ComparisonMethod=comparison_method,
                    NumElementsSet2=0,
                    AddInterferenceAsOccurrence=False,
                    NumInterferences=num_interferences,
                )

                return {
                    "status": "checked",
                    "interference_found": interference_status.value != 0,
                    "num_interferences": num_interferences.value,
                    "component_checked": component_index,
                }
            except Exception as e:
                # CheckInterference has complex COM signature; report what we can
                return {
                    "error": f"Interference check failed: {e}",
                    "note": "CheckInterference COM signature "
                    "is complex. Use Solid Edge UI for "
                    "reliable results.",
                    "traceback": traceback.format_exc(),
                }

        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def replace_component(self, component_index: int, new_file_path: str) -> dict[str, Any]:
        """
        Replace a component in the assembly with a different part/assembly file.

        Preserves position and attempts to maintain assembly relations.

        Args:
            component_index: 0-based index of the component to replace
            new_file_path: Path to the replacement file (.par or .asm)

        Returns:
            Dict with replacement status
        """
        try:
            import os

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            if not os.path.exists(new_file_path):
                return {"error": f"File not found: {new_file_path}"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)
            old_name = occurrence.Name

            try:
                occurrence.Replace(new_file_path)
            except Exception:
                # Try alternative method
                occurrence.OccurrenceFileName = new_file_path

            return {
                "status": "replaced",
                "component_index": component_index,
                "old_name": old_name,
                "new_file": new_file_path,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_component_transform(self, component_index: int) -> dict[str, Any]:
        """
        Get the full transformation matrix of a component.

        Returns the 4x4 homogeneous transformation matrix and
        decomposed origin + rotation.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with matrix, origin, and rotation
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)

            result = {
                "component_index": component_index,
                "name": occurrence.Name,
            }

            # Try GetTransform (origin + angles)
            try:
                transform = occurrence.GetTransform()
                result["origin"] = [transform[0], transform[1], transform[2]]
                result["rotation_angles"] = [transform[3], transform[4], transform[5]]
            except Exception:
                pass

            # Try GetMatrix (full 4x4)
            try:
                matrix = occurrence.GetMatrix()
                result["matrix"] = list(matrix)
            except Exception:
                pass

            return result
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_structured_bom(self) -> dict[str, Any]:
        """
        Get a hierarchical Bill of Materials with subassembly structure.

        Unlike get_bom() which returns a flat list, this preserves the
        parent-child hierarchy of subassemblies.

        Returns:
            Dict with structured BOM tree
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            def build_bom_item(occ, depth=0):
                item = {}
                try:
                    item["name"] = occ.Name
                except Exception:
                    item["name"] = "Unknown"

                try:
                    item["file"] = occ.OccurrenceFileName
                except Exception:
                    item["file"] = "Unknown"

                with contextlib.suppress(Exception):
                    item["visible"] = occ.Visible

                try:
                    item["suppressed"] = occ.IsSuppressed
                except Exception:
                    item["suppressed"] = False

                # Check for sub-occurrences (subassembly)
                children = []
                try:
                    sub_occs = occ.SubOccurrences
                    if sub_occs and hasattr(sub_occs, "Count") and sub_occs.Count > 0:
                        item["type"] = "assembly"
                        for j in range(1, sub_occs.Count + 1):
                            try:
                                children.append(build_bom_item(sub_occs.Item(j), depth + 1))
                            except Exception:
                                children.append({"name": f"SubItem_{j}", "error": "unreadable"})
                    else:
                        item["type"] = "part"
                except Exception:
                    item["type"] = "part"

                if children:
                    item["children"] = children
                    item["child_count"] = len(children)

                return item

            bom = []
            for i in range(1, occurrences.Count + 1):
                try:
                    bom.append(build_bom_item(occurrences.Item(i)))
                except Exception:
                    bom.append({"name": f"Component_{i}", "error": "unreadable"})

            return {
                "bom": bom,
                "top_level_count": len(bom),
                "document": doc.Name if hasattr(doc, "Name") else "Unknown",
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def set_component_color(
        self, component_index: int, red: int, green: int, blue: int
    ) -> dict[str, Any]:
        """
        Set the color of a component in the assembly.

        Args:
            component_index: 0-based index of the component
            red: Red component (0-255)
            green: Green component (0-255)
            blue: Blue component (0-255)

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)

            # OLE color: BGR format packed into integer
            ole_color = red | (green << 8) | (blue << 16)

            try:
                occurrence.SetColor(red, green, blue)
            except Exception:
                try:
                    occurrence.Color = ole_color
                except Exception:
                    # Try style-based approach
                    occurrence.UseOccurrenceColor = True
                    occurrence.OccurrenceColor = ole_color

            return {
                "status": "updated",
                "component_index": component_index,
                "color": [red, green, blue],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def occurrence_move(
        self, component_index: int, dx: float, dy: float, dz: float
    ) -> dict[str, Any]:
        """
        Move a component by a relative delta.

        Uses Occurrence.Move(DeltaX, DeltaY, DeltaZ) for relative translation.

        Args:
            component_index: 0-based index of the component
            dx: X translation in meters
            dy: Y translation in meters
            dz: Z translation in meters

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)
            occurrence.Move(dx, dy, dz)

            return {"status": "moved", "component_index": component_index, "delta": [dx, dy, dz]}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def occurrence_rotate(
        self,
        component_index: int,
        axis_x1: float,
        axis_y1: float,
        axis_z1: float,
        axis_x2: float,
        axis_y2: float,
        axis_z2: float,
        angle: float,
    ) -> dict[str, Any]:
        """
        Rotate a component around an axis.

        Uses Occurrence.Rotate(AxisX1, AxisY1, AxisZ1, AxisX2, AxisY2, AxisZ2, Angle).
        The axis is defined by two 3D points. Angle is in degrees (converted to radians internally).

        Args:
            component_index: 0-based index of the component
            axis_x1, axis_y1, axis_z1: First point of rotation axis (meters)
            axis_x2, axis_y2, axis_z2: Second point of rotation axis (meters)
            angle: Rotation angle in degrees

        Returns:
            Dict with status
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)
            angle_rad = math.radians(angle)
            occurrence.Rotate(axis_x1, axis_y1, axis_z1, axis_x2, axis_y2, axis_z2, angle_rad)

            return {
                "status": "rotated",
                "component_index": component_index,
                "axis": [[axis_x1, axis_y1, axis_z1], [axis_x2, axis_y2, axis_z2]],
                "angle_degrees": angle,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def set_component_transform(
        self,
        component_index: int,
        origin_x: float,
        origin_y: float,
        origin_z: float,
        angle_x: float,
        angle_y: float,
        angle_z: float,
    ) -> dict[str, Any]:
        """
        Set a component's full transform (position + rotation).

        Uses Occurrence.PutTransform(OriginX, OriginY, OriginZ, AngleX, AngleY, AngleZ).
        Angles are in degrees (converted to radians internally).

        Args:
            component_index: 0-based index of the component
            origin_x: X position in meters
            origin_y: Y position in meters
            origin_z: Z position in meters
            angle_x: Rotation around X axis in degrees
            angle_y: Rotation around Y axis in degrees
            angle_z: Rotation around Z axis in degrees

        Returns:
            Dict with status
        """
        try:
            import math

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)
            ax_rad = math.radians(angle_x)
            ay_rad = math.radians(angle_y)
            az_rad = math.radians(angle_z)
            occurrence.PutTransform(origin_x, origin_y, origin_z, ax_rad, ay_rad, az_rad)

            return {
                "status": "updated",
                "component_index": component_index,
                "origin": [origin_x, origin_y, origin_z],
                "angles_degrees": [angle_x, angle_y, angle_z],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def set_component_origin(
        self, component_index: int, x: float, y: float, z: float
    ) -> dict[str, Any]:
        """
        Set a component's origin (position only, no rotation change).

        Uses Occurrence.PutOrigin(OriginX, OriginY, OriginZ).

        Args:
            component_index: 0-based index of the component
            x: X position in meters
            y: Y position in meters
            z: Z position in meters

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)
            occurrence.PutOrigin(x, y, z)

            return {"status": "updated", "component_index": component_index, "origin": [x, y, z]}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def mirror_component(self, component_index: int, plane_index: int) -> dict[str, Any]:
        """
        Mirror a component across a reference plane.

        Uses Occurrence.Mirror(pPlane).

        Args:
            component_index: 0-based index of the component
            plane_index: 1-based index of the reference plane

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. "
                    f"Count: {occurrences.Count}"
                }

            ref_planes = doc.RefPlanes
            if plane_index < 1 or plane_index > ref_planes.Count:
                return {"error": f"Invalid plane_index: {plane_index}. Count: {ref_planes.Count}"}

            occurrence = occurrences.Item(component_index + 1)
            plane = ref_planes.Item(plane_index)
            occurrence.Mirror(plane)

            return {
                "status": "mirrored",
                "component_index": component_index,
                "plane_index": plane_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_component_with_transform(
        self,
        file_path: str,
        origin_x: float = 0,
        origin_y: float = 0,
        origin_z: float = 0,
        angle_x: float = 0,
        angle_y: float = 0,
        angle_z: float = 0,
    ) -> dict[str, Any]:
        """
        Add a component with position and Euler rotation angles.

        Uses Occurrences.AddWithTransform(filename, ox, oy, oz, ax, ay, az)
        where angles are in radians.

        Args:
            file_path: Path to the part or assembly file
            origin_x, origin_y, origin_z: Position in meters
            angle_x, angle_y, angle_z: Rotation angles in degrees

        Returns:
            Dict with status and component info
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            ax_rad = math.radians(angle_x)
            ay_rad = math.radians(angle_y)
            az_rad = math.radians(angle_z)

            occurrence = occurrences.AddWithTransform(
                file_path, origin_x, origin_y, origin_z, ax_rad, ay_rad, az_rad
            )

            return {
                "status": "added",
                "file_path": file_path,
                "name": occurrence.Name
                if hasattr(occurrence, "Name")
                else os.path.basename(file_path),
                "origin": [origin_x, origin_y, origin_z],
                "angles_degrees": [angle_x, angle_y, angle_z],
                "index": occurrences.Count - 1,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def delete_relation(self, relation_index: int) -> dict[str, Any]:
        """
        Delete an assembly relation (constraint) by index.

        Args:
            relation_index: 0-based index of the relation

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Relations3d"):
                return {"error": "Active document is not an assembly"}

            relations = doc.Relations3d

            if relation_index < 0 or relation_index >= relations.Count:
                return {
                    "error": f"Invalid relation index: {relation_index}. Count: {relations.Count}"
                }

            rel = relations.Item(relation_index + 1)
            name = ""
            with contextlib.suppress(Exception):
                name = rel.Name

            rel.Delete()

            return {"status": "deleted", "relation_index": relation_index, "name": name}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_relation_info(self, relation_index: int) -> dict[str, Any]:
        """
        Get detailed information about a specific assembly relation.

        Args:
            relation_index: 0-based index of the relation

        Returns:
            Dict with relation type, status, offset, and connected elements
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Relations3d"):
                return {"error": "Active document is not an assembly"}

            relations = doc.Relations3d

            if relation_index < 0 or relation_index >= relations.Count:
                return {
                    "error": f"Invalid relation index: {relation_index}. Count: {relations.Count}"
                }

            rel = relations.Item(relation_index + 1)

            type_names = {
                0: "Ground",
                1: "Axial",
                2: "Planar",
                3: "Connect",
                4: "Angle",
                5: "Tangent",
                6: "Cam",
                7: "Gear",
                8: "ParallelAxis",
                9: "Center",
            }

            info = {"relation_index": relation_index}

            with contextlib.suppress(Exception):
                info["type"] = rel.Type
                info["type_name"] = type_names.get(rel.Type, f"Unknown({rel.Type})")
            with contextlib.suppress(Exception):
                info["status"] = rel.Status
            with contextlib.suppress(Exception):
                info["name"] = rel.Name
            with contextlib.suppress(Exception):
                info["suppressed"] = rel.Suppressed
            with contextlib.suppress(Exception):
                info["offset"] = rel.Offset
            with contextlib.suppress(Exception):
                info["normals_aligned"] = rel.NormalsAligned

            return info
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_occurrence_count(self) -> dict[str, Any]:
        """
        Get the count of top-level occurrences in the assembly.

        Returns:
            Dict with occurrence count
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            return {"count": doc.Occurrences.Count}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # ========================================================================
    # ASSEMBLY RELATION TOOLS (Batch 1)
    # ========================================================================

    def _validate_occurrences(
        self, doc, occurrence1_index: int, occurrence2_index: int
    ) -> tuple[Any, Any, dict[str, Any] | None]:
        """Validate two occurrence indices and return occurrence objects.

        Returns (occ1, occ2, error_dict). If error_dict is not None, caller should return it.
        """
        if not hasattr(doc, "Relations3d"):
            return None, None, {"error": "Active document is not an assembly"}

        occurrences = doc.Occurrences

        if occurrence1_index < 0 or occurrence1_index >= occurrences.Count:
            return (
                None,
                None,
                {
                    "error": f"Invalid occurrence1 index: "
                    f"{occurrence1_index}. Count: {occurrences.Count}"
                },
            )
        if occurrence2_index < 0 or occurrence2_index >= occurrences.Count:
            return (
                None,
                None,
                {
                    "error": f"Invalid occurrence2 index: "
                    f"{occurrence2_index}. Count: {occurrences.Count}"
                },
            )

        occ1 = occurrences.Item(occurrence1_index + 1)
        occ2 = occurrences.Item(occurrence2_index + 1)
        return occ1, occ2, None

    def _validate_relation_index(
        self, doc, relation_index: int
    ) -> tuple[Any, dict[str, Any] | None]:
        """Validate a relation index and return the relation object.

        Returns (relation, error_dict). If error_dict is not None, caller should return it.
        """
        if not hasattr(doc, "Relations3d"):
            return None, {"error": "Active document is not an assembly"}

        relations = doc.Relations3d

        if relation_index < 0 or relation_index >= relations.Count:
            return None, {
                "error": f"Invalid relation index: {relation_index}. Count: {relations.Count}"
            }

        return relations.Item(relation_index + 1), None

    def add_planar_relation(
        self,
        occurrence1_index: int,
        occurrence2_index: int,
        offset: float = 0.0,
        orientation: str = "Align",
    ) -> dict[str, Any]:
        """
        Add a planar relation between two assembly components.

        Uses Relations3d.AddPlanar(Occurrence1, Occurrence2, Offset, OrientationType).

        Args:
            occurrence1_index: 0-based index of first component
            occurrence2_index: 0-based index of second component
            offset: Offset distance in meters (default 0.0)
            orientation: "Align" (1), "Antialign" (2), or "NotSpecified" (0)

        Returns:
            Dict with status and relation info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occ1, occ2, err = self._validate_occurrences(doc, occurrence1_index, occurrence2_index)
            if err:
                return err

            orient_map = {"Align": 1, "Antialign": 2, "NotSpecified": 0}
            orient_val = orient_map.get(orientation, 0)

            relations = doc.Relations3d
            _feature = relations.AddPlanar(occ1, occ2, offset, orient_val)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "relation_type": "Planar",
                "occurrence1_index": occurrence1_index,
                "occurrence2_index": occurrence2_index,
                "offset": offset,
                "orientation": orientation,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_axial_relation(
        self,
        occurrence1_index: int,
        occurrence2_index: int,
        orientation: str = "Align",
    ) -> dict[str, Any]:
        """
        Add an axial relation between two assembly components.

        Uses Relations3d.AddAxial(Occurrence1, Occurrence2, OrientationType).

        Args:
            occurrence1_index: 0-based index of first component
            occurrence2_index: 0-based index of second component
            orientation: "Align" (1), "Antialign" (2), or "NotSpecified" (0)

        Returns:
            Dict with status and relation info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occ1, occ2, err = self._validate_occurrences(doc, occurrence1_index, occurrence2_index)
            if err:
                return err

            orient_map = {"Align": 1, "Antialign": 2, "NotSpecified": 0}
            orient_val = orient_map.get(orientation, 0)

            relations = doc.Relations3d
            _feature = relations.AddAxial(occ1, occ2, orient_val)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "relation_type": "Axial",
                "occurrence1_index": occurrence1_index,
                "occurrence2_index": occurrence2_index,
                "orientation": orientation,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_angular_relation(
        self,
        occurrence1_index: int,
        occurrence2_index: int,
        angle: float = 0.0,
    ) -> dict[str, Any]:
        """
        Add an angular relation between two assembly components.

        Uses Relations3d.AddAngular(Occurrence1, Occurrence2, AngleInRadians).

        Args:
            occurrence1_index: 0-based index of first component
            occurrence2_index: 0-based index of second component
            angle: Angle in degrees (converted to radians for COM)

        Returns:
            Dict with status and relation info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occ1, occ2, err = self._validate_occurrences(doc, occurrence1_index, occurrence2_index)
            if err:
                return err

            angle_rad = math.radians(angle)

            relations = doc.Relations3d
            _feature = relations.AddAngular(occ1, occ2, angle_rad)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "relation_type": "Angular",
                "occurrence1_index": occurrence1_index,
                "occurrence2_index": occurrence2_index,
                "angle_degrees": angle,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_point_relation(
        self,
        occurrence1_index: int,
        occurrence2_index: int,
    ) -> dict[str, Any]:
        """
        Add a point (connect) relation between two assembly components.

        Uses Relations3d.AddPoint(Occurrence1, Occurrence2).

        Args:
            occurrence1_index: 0-based index of first component
            occurrence2_index: 0-based index of second component

        Returns:
            Dict with status and relation info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occ1, occ2, err = self._validate_occurrences(doc, occurrence1_index, occurrence2_index)
            if err:
                return err

            relations = doc.Relations3d
            _feature = relations.AddPoint(occ1, occ2)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "relation_type": "Point",
                "occurrence1_index": occurrence1_index,
                "occurrence2_index": occurrence2_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_tangent_relation(
        self,
        occurrence1_index: int,
        occurrence2_index: int,
    ) -> dict[str, Any]:
        """
        Add a tangent relation between two assembly components.

        Uses Relations3d.AddTangent(Occurrence1, Occurrence2).

        Args:
            occurrence1_index: 0-based index of first component
            occurrence2_index: 0-based index of second component

        Returns:
            Dict with status and relation info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occ1, occ2, err = self._validate_occurrences(doc, occurrence1_index, occurrence2_index)
            if err:
                return err

            relations = doc.Relations3d
            _feature = relations.AddTangent(occ1, occ2)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "relation_type": "Tangent",
                "occurrence1_index": occurrence1_index,
                "occurrence2_index": occurrence2_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_gear_relation(
        self,
        occurrence1_index: int,
        occurrence2_index: int,
        ratio1: float = 1.0,
        ratio2: float = 1.0,
    ) -> dict[str, Any]:
        """
        Add a gear relation between two assembly components.

        Uses Relations3d.AddGear(Occurrence1, Occurrence2, Ratio1, Ratio2).

        Args:
            occurrence1_index: 0-based index of first component
            occurrence2_index: 0-based index of second component
            ratio1: Gear ratio value for first component (default 1.0)
            ratio2: Gear ratio value for second component (default 1.0)

        Returns:
            Dict with status and relation info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occ1, occ2, err = self._validate_occurrences(doc, occurrence1_index, occurrence2_index)
            if err:
                return err

            relations = doc.Relations3d
            _feature = relations.AddGear(occ1, occ2, ratio1, ratio2)
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "relation_type": "Gear",
                "occurrence1_index": occurrence1_index,
                "occurrence2_index": occurrence2_index,
                "ratio1": ratio1,
                "ratio2": ratio2,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_relation_offset(self, relation_index: int) -> dict[str, Any]:
        """
        Get the offset value from a planar relation.

        Args:
            relation_index: 0-based index into Relations3d collection

        Returns:
            Dict with offset value (meters)
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            offset = rel.Offset

            return {
                "relation_index": relation_index,
                "offset": offset,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def set_relation_offset(self, relation_index: int, offset: float) -> dict[str, Any]:
        """
        Set the offset value on a planar relation.

        Args:
            relation_index: 0-based index into Relations3d collection
            offset: New offset value in meters

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            rel.Offset = offset

            return {
                "status": "updated",
                "relation_index": relation_index,
                "offset": offset,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_relation_angle(self, relation_index: int) -> dict[str, Any]:
        """
        Get the angle value from an angular relation.

        The COM API stores angles in radians; this returns degrees.

        Args:
            relation_index: 0-based index into Relations3d collection

        Returns:
            Dict with angle in degrees
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            angle_rad = rel.Angle
            angle_deg = math.degrees(angle_rad)

            return {
                "relation_index": relation_index,
                "angle_degrees": angle_deg,
                "angle_radians": angle_rad,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def set_relation_angle(self, relation_index: int, angle: float) -> dict[str, Any]:
        """
        Set the angle value on an angular relation.

        Args:
            relation_index: 0-based index into Relations3d collection
            angle: New angle in degrees (converted to radians for COM)

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            angle_rad = math.radians(angle)
            rel.Angle = angle_rad

            return {
                "status": "updated",
                "relation_index": relation_index,
                "angle_degrees": angle,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_normals_aligned(self, relation_index: int) -> dict[str, Any]:
        """
        Get the NormalsAligned property from a relation.

        Args:
            relation_index: 0-based index into Relations3d collection

        Returns:
            Dict with normals_aligned boolean
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            aligned = rel.NormalsAligned

            return {
                "relation_index": relation_index,
                "normals_aligned": aligned,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def set_normals_aligned(self, relation_index: int, aligned: bool) -> dict[str, Any]:
        """
        Set the NormalsAligned property on a relation.

        Args:
            relation_index: 0-based index into Relations3d collection
            aligned: True to align normals, False otherwise

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            rel.NormalsAligned = aligned

            return {
                "status": "updated",
                "relation_index": relation_index,
                "normals_aligned": aligned,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def suppress_relation(self, relation_index: int) -> dict[str, Any]:
        """
        Suppress an assembly relation.

        Args:
            relation_index: 0-based index into Relations3d collection

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            rel.Suppressed = True

            return {
                "status": "suppressed",
                "relation_index": relation_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def unsuppress_relation(self, relation_index: int) -> dict[str, Any]:
        """
        Unsuppress an assembly relation.

        Args:
            relation_index: 0-based index into Relations3d collection

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            rel.Suppressed = False

            return {
                "status": "unsuppressed",
                "relation_index": relation_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_relation_geometry(self, relation_index: int) -> dict[str, Any]:
        """
        Get geometry info from a relation (connected occurrence references).

        Attempts to read OccurrencePart1, OccurrencePart2, and other geometry
        properties from the relation. Not all properties are available on all
        relation types.

        Args:
            relation_index: 0-based index into Relations3d collection

        Returns:
            Dict with available geometry/occurrence info
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            info: dict[str, Any] = {"relation_index": relation_index}

            with contextlib.suppress(Exception):
                info["type"] = rel.Type

            with contextlib.suppress(Exception):
                info["name"] = rel.Name

            with contextlib.suppress(Exception):
                occ1 = rel.OccurrencePart1
                info["occurrence1_name"] = occ1.Name if hasattr(occ1, "Name") else str(occ1)

            with contextlib.suppress(Exception):
                occ2 = rel.OccurrencePart2
                info["occurrence2_name"] = occ2.Name if hasattr(occ2, "Name") else str(occ2)

            with contextlib.suppress(Exception):
                info["offset"] = rel.Offset

            with contextlib.suppress(Exception):
                info["normals_aligned"] = rel.NormalsAligned

            with contextlib.suppress(Exception):
                info["suppressed"] = rel.Suppressed

            return info
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_gear_ratio(self, relation_index: int) -> dict[str, Any]:
        """
        Get gear ratio values from a gear relation.

        Reads RatioValue1 and RatioValue2 from the relation.

        Args:
            relation_index: 0-based index into Relations3d collection

        Returns:
            Dict with ratio1 and ratio2 values
        """
        try:
            doc = self.doc_manager.get_active_document()
            rel, err = self._validate_relation_index(doc, relation_index)
            if err:
                return err

            info: dict[str, Any] = {"relation_index": relation_index}

            try:
                info["ratio1"] = rel.RatioValue1
            except Exception:
                info["ratio1"] = None
                info["ratio1_error"] = "RatioValue1 not available on this relation"

            try:
                info["ratio2"] = rel.RatioValue2
            except Exception:
                info["ratio2"] = None
                info["ratio2_error"] = "RatioValue2 not available on this relation"

            return info
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # ========================================================================
    # BATCH 8: ASSEMBLY OCCURRENCES & PROPERTIES
    # ========================================================================

    def _validate_occurrence_index(
        self, doc, component_index: int
    ) -> tuple[Any, Any, dict[str, Any] | None]:
        """Validate a single occurrence index and return (occurrences, occurrence, error_dict).

        If error_dict is not None, caller should return it.
        """
        if not hasattr(doc, "Occurrences"):
            return None, None, {"error": "Active document is not an assembly"}

        occurrences = doc.Occurrences

        if component_index < 0 or component_index >= occurrences.Count:
            return (
                None,
                None,
                {
                    "error": f"Invalid component index: "
                    f"{component_index}. Count: {occurrences.Count}"
                },
            )

        occurrence = occurrences.Item(component_index + 1)
        return occurrences, occurrence, None

    def add_family_member(
        self,
        file_path: str,
        family_member_name: str,
        x: float = 0,
        y: float = 0,
        z: float = 0,
    ) -> dict[str, Any]:
        """
        Add a Family of Parts member to the assembly.

        Uses Occurrences.AddFamilyByFilename to place a specific family member.

        Args:
            file_path: Path to the Family of Parts file (.par)
            family_member_name: Name of the family member to place
            x: X position in meters (unused, placement is at origin)
            y: Y position in meters (unused, placement is at origin)
            z: Z position in meters (unused, placement is at origin)

        Returns:
            Dict with status and component info
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            occ = occurrences.AddFamilyByFilename(file_path, family_member_name)

            return {
                "status": "added",
                "file_path": file_path,
                "family_member": family_member_name,
                "name": occ.Name if hasattr(occ, "Name") else "Unknown",
                "index": occurrences.Count - 1,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_family_with_transform(
        self,
        file_path: str,
        family_member_name: str,
        origin_x: float = 0,
        origin_y: float = 0,
        origin_z: float = 0,
        angle_x: float = 0,
        angle_y: float = 0,
        angle_z: float = 0,
    ) -> dict[str, Any]:
        """
        Add a Family of Parts member with position and rotation.

        Places the family member, then applies a transform via PutTransform.
        Angles are in degrees (converted to radians internally).

        Args:
            file_path: Path to the Family of Parts file (.par)
            family_member_name: Name of the family member to place
            origin_x, origin_y, origin_z: Position in meters
            angle_x, angle_y, angle_z: Rotation angles in degrees

        Returns:
            Dict with status and component info
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            occ = occurrences.AddFamilyByFilename(file_path, family_member_name)

            # Apply transform
            ax_rad = math.radians(angle_x)
            ay_rad = math.radians(angle_y)
            az_rad = math.radians(angle_z)
            occ.PutTransform(origin_x, origin_y, origin_z, ax_rad, ay_rad, az_rad)

            return {
                "status": "added",
                "file_path": file_path,
                "family_member": family_member_name,
                "name": occ.Name if hasattr(occ, "Name") else "Unknown",
                "origin": [origin_x, origin_y, origin_z],
                "angles_degrees": [angle_x, angle_y, angle_z],
                "index": occurrences.Count - 1,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_by_template(
        self,
        file_path: str,
        template_name: str,
    ) -> dict[str, Any]:
        """
        Add a component to the assembly using a template.

        Uses Occurrences.AddByTemplate(filename, templateName).

        Args:
            file_path: Path to the part or assembly file
            template_name: Name of the template to use

        Returns:
            Dict with status and component info
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            occ = occurrences.AddByTemplate(file_path, template_name)

            return {
                "status": "added",
                "file_path": file_path,
                "template_name": template_name,
                "name": occ.Name if hasattr(occ, "Name") else "Unknown",
                "index": occurrences.Count - 1,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_adjustable_part(
        self,
        file_path: str,
        x: float = 0,
        y: float = 0,
        z: float = 0,
    ) -> dict[str, Any]:
        """
        Add a part as an adjustable part to the assembly.

        Uses Occurrences.AddAsAdjustablePart(filename).

        Args:
            file_path: Path to the part file (.par)
            x: X position in meters (unused, placement is at origin)
            y: Y position in meters (unused, placement is at origin)
            z: Z position in meters (unused, placement is at origin)

        Returns:
            Dict with status and component info
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            occ = occurrences.AddAsAdjustablePart(file_path)

            return {
                "status": "added",
                "file_path": file_path,
                "adjustable": True,
                "name": occ.Name if hasattr(occ, "Name") else "Unknown",
                "index": occurrences.Count - 1,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def reorder_occurrence(
        self,
        component_index: int,
        target_index: int,
    ) -> dict[str, Any]:
        """
        Reorder an occurrence in the assembly tree.

        Uses Occurrences.ReorderOccurrence(occurrence, targetIndex).
        Both indices are 0-based (converted to 1-based for COM).

        Args:
            component_index: 0-based index of the component to move
            target_index: 0-based target position

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component_index < 0 or component_index >= occurrences.Count:
                return {
                    "error": f"Invalid component index: "
                    f"{component_index}. Count: {occurrences.Count}"
                }

            if target_index < 0 or target_index >= occurrences.Count:
                return {
                    "error": f"Invalid target index: {target_index}. Count: {occurrences.Count}"
                }

            occurrence = occurrences.Item(component_index + 1)
            occurrences.ReorderOccurrence(occurrence, target_index + 1)

            return {
                "status": "reordered",
                "component_index": component_index,
                "target_index": target_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def put_transform_euler(
        self,
        component_index: int,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
    ) -> dict[str, Any]:
        """
        Set a component's transform using Euler angles.

        Uses occurrence.PutTransform(x, y, z, rx_rad, ry_rad, rz_rad).
        Angles are in degrees (converted to radians internally).

        Args:
            component_index: 0-based index of the component
            x: X position in meters
            y: Y position in meters
            z: Z position in meters
            rx: Rotation around X axis in degrees
            ry: Rotation around Y axis in degrees
            rz: Rotation around Z axis in degrees

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences, occurrence, err = self._validate_occurrence_index(doc, component_index)
            if err:
                return err

            rx_rad = math.radians(rx)
            ry_rad = math.radians(ry)
            rz_rad = math.radians(rz)
            occurrence.PutTransform(x, y, z, rx_rad, ry_rad, rz_rad)

            return {
                "status": "updated",
                "component_index": component_index,
                "position": [x, y, z],
                "angles_degrees": [rx, ry, rz],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def put_origin(
        self,
        component_index: int,
        x: float,
        y: float,
        z: float,
    ) -> dict[str, Any]:
        """
        Set a component's origin (position only, no rotation change).

        Uses occurrence.PutOrigin(x, y, z).

        Args:
            component_index: 0-based index of the component
            x: X position in meters
            y: Y position in meters
            z: Z position in meters

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences, occurrence, err = self._validate_occurrence_index(doc, component_index)
            if err:
                return err

            occurrence.PutOrigin(x, y, z)

            return {
                "status": "updated",
                "component_index": component_index,
                "origin": [x, y, z],
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def make_writable(self, component_index: int) -> dict[str, Any]:
        """
        Make a component writable (editable) in the assembly.

        Uses occurrence.MakeWritable() to allow editing of the component.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences, occurrence, err = self._validate_occurrence_index(doc, component_index)
            if err:
                return err

            occurrence.MakeWritable()

            return {
                "status": "writable",
                "component_index": component_index,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def swap_family_member(
        self,
        component_index: int,
        new_member_name: str,
    ) -> dict[str, Any]:
        """
        Swap a Family of Parts occurrence for a different family member.

        Uses occurrence.SwapFamilyMember(newMemberName).

        Args:
            component_index: 0-based index of the component
            new_member_name: Name of the new family member

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences, occurrence, err = self._validate_occurrence_index(doc, component_index)
            if err:
                return err

            occurrence.SwapFamilyMember(new_member_name)

            return {
                "status": "swapped",
                "component_index": component_index,
                "new_member_name": new_member_name,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_occurrence_bodies(self, component_index: int) -> dict[str, Any]:
        """
        Get body information from a specific component occurrence.

        Reads occurrence.Bodies property to enumerate solid bodies.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with body count and body info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences, occurrence, err = self._validate_occurrence_index(doc, component_index)
            if err:
                return err

            bodies_info = []
            try:
                bodies = occurrence.Bodies
                body_count = bodies.Count if hasattr(bodies, "Count") else 0

                for i in range(1, body_count + 1):
                    body = bodies.Item(i)
                    body_info: dict[str, Any] = {"index": i - 1}

                    with contextlib.suppress(Exception):
                        body_info["name"] = body.Name

                    with contextlib.suppress(Exception):
                        body_info["volume"] = body.Volume

                    bodies_info.append(body_info)
            except Exception:
                body_count = 0

            return {
                "component_index": component_index,
                "body_count": len(bodies_info),
                "bodies": bodies_info,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_occurrence_style(self, component_index: int) -> dict[str, Any]:
        """
        Get the style (appearance) of a component occurrence.

        Reads occurrence.Style property.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with style info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences, occurrence, err = self._validate_occurrence_index(doc, component_index)
            if err:
                return err

            result: dict[str, Any] = {"component_index": component_index}

            try:
                style = occurrence.Style
                result["style"] = str(style) if style is not None else None
            except Exception:
                result["style"] = None
                result["style_note"] = "Style property not available on this occurrence"

            return result
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def is_tube(self, component_index: int) -> dict[str, Any]:
        """
        Check if a component occurrence is a tube.

        Reads occurrence.IsTube property.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with is_tube boolean
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences, occurrence, err = self._validate_occurrence_index(doc, component_index)
            if err:
                return err

            result: dict[str, Any] = {"component_index": component_index}

            try:
                result["is_tube"] = bool(occurrence.IsTube)
            except Exception:
                result["is_tube"] = False
                result["is_tube_note"] = "IsTube property not available on this occurrence"

            return result
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_adjustable_part(self, component_index: int) -> dict[str, Any]:
        """
        Get adjustable part info from a component occurrence.

        Reads occurrence.GetAdjustablePart() to check if the component
        is adjustable and retrieve its adjustable part object info.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with adjustable part info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences, occurrence, err = self._validate_occurrence_index(doc, component_index)
            if err:
                return err

            result: dict[str, Any] = {"component_index": component_index}

            try:
                adj_part = occurrence.GetAdjustablePart()
                result["is_adjustable"] = adj_part is not None
                if adj_part is not None:
                    with contextlib.suppress(Exception):
                        result["adjustable_name"] = adj_part.Name
            except Exception:
                result["is_adjustable"] = False
                result["adjustable_note"] = "GetAdjustablePart not available on this occurrence"

            return result
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_face_style(self, component_index: int) -> dict[str, Any]:
        """
        Get the face style of a component occurrence.

        Reads occurrence.GetFaceStyle2() for face style information.

        Args:
            component_index: 0-based index of the component

        Returns:
            Dict with face style info
        """
        try:
            doc = self.doc_manager.get_active_document()
            occurrences, occurrence, err = self._validate_occurrence_index(doc, component_index)
            if err:
                return err

            result: dict[str, Any] = {"component_index": component_index}

            try:
                face_style = occurrence.GetFaceStyle2()
                result["face_style"] = str(face_style) if face_style is not None else None
            except Exception:
                result["face_style"] = None
                result["face_style_note"] = "GetFaceStyle2 not available on this occurrence"

            return result
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_family_with_matrix(
        self,
        family_file_path: str,
        member_name: str,
        matrix: list[float],
    ) -> dict[str, Any]:
        """
        Add a Family of Parts member with a 4x4 transformation matrix.

        Uses Occurrences.AddFamilyWithMatrix(OccurrenceFileName, Matrix, MemberName)
        to place a specific family member at the position/orientation defined by the matrix.

        Args:
            family_file_path: Path to the Family of Parts file (.par)
            member_name: Name of the family member to place
            matrix: 16-element list of floats representing a 4x4 transformation matrix

        Returns:
            Dict with status and component info
        """
        try:
            if not os.path.exists(family_file_path):
                return {"error": f"File not found: {family_file_path}"}

            if len(matrix) != 16:
                return {"error": f"Matrix must have exactly 16 elements, got {len(matrix)}"}

            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            occ = occurrences.AddFamilyWithMatrix(family_file_path, matrix, member_name)

            # Extract position from transform
            position = [matrix[12], matrix[13], matrix[14]]

            return {
                "status": "added",
                "file_path": family_file_path,
                "family_member": member_name,
                "name": occ.Name if hasattr(occ, "Name") else "Unknown",
                "position": position,
                "matrix": matrix,
                "index": occurrences.Count - 1,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def get_occurrence(self, internal_id: int) -> dict[str, Any]:
        """
        Get an occurrence by its internal ID.

        Uses Occurrences.GetOccurrence(ID) to retrieve a specific occurrence
        by its internal ID (not by index). This is useful when you know the
        internal identifier assigned by Solid Edge.

        Args:
            internal_id: Internal ID of the occurrence (integer)

        Returns:
            Dict with occurrence info (name, file path, transform, etc.)
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            occurrence = occurrences.GetOccurrence(internal_id)

            if occurrence is None:
                return {"error": f"No occurrence found with ID: {internal_id}"}

            info: dict[str, Any] = {"internal_id": internal_id}

            # Name
            try:
                info["name"] = occurrence.Name
            except Exception:
                info["name"] = "Unknown"

            # File path
            try:
                info["file_path"] = occurrence.OccurrenceFileName
            except Exception:
                info["file_path"] = "Unknown"

            # Transform (position + rotation)
            try:
                transform = occurrence.GetTransform()
                info["position"] = [transform[0], transform[1], transform[2]]
                info["rotation_rad"] = [transform[3], transform[4], transform[5]]
            except Exception:
                pass

            # Full 4x4 matrix
            try:
                mat = occurrence.GetMatrix()
                info["matrix"] = list(mat)
            except Exception:
                pass

            # Visibility
            with contextlib.suppress(Exception):
                info["visible"] = occurrence.Visible

            # Occurrence document info
            try:
                occ_doc = occurrence.OccurrenceDocument
                info["document_name"] = occ_doc.Name
            except Exception:
                pass

            return info
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ASSEMBLY CONFIGURATIONS
    # =================================================================

    def list_configurations(self) -> dict[str, Any]:
        """
        List all configurations in the active assembly document.

        Uses AssemblyDocument.Configurations collection.

        Returns:
            Dict with list of configurations and the active one
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
                cfg_type = None
                try:
                    cfg_type = cfg.Type if hasattr(cfg, "Type") else None
                except Exception:
                    pass
                is_active = False
                try:
                    is_active = bool(cfg.Active) if hasattr(cfg, "Active") else False
                except Exception:
                    pass
                if is_active:
                    active_name = name
                result.append({
                    "index": i - 1,
                    "name": name,
                    "type": cfg_type,
                    "active": is_active,
                })

            return {
                "status": "ok",
                "count": configs.Count,
                "active": active_name,
                "configurations": result,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_configuration(
        self, name: str, config_type: int = 0
    ) -> dict[str, Any]:
        """
        Add a new assembly configuration.

        Uses Configurations.Add(type, name).
        Configuration types: 0=Display (default), 1=Explode.

        Args:
            name: Name for the new configuration
            config_type: 0=Display (default), 1=Explode

        Returns:
            Dict with status and name
        """
        try:
            doc = self.doc_manager.get_active_document()
            if not hasattr(doc, "Configurations"):
                return {"error": "Active document does not support configurations"}

            configs = doc.Configurations
            _cfg = configs.Add(config_type, name)
            if _cfg is None:
                return {"error": "Configuration creation failed: COM returned None"}

            return {
                "status": "created",
                "name": name,
                "config_type": config_type,
                "total_configurations": configs.Count,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def apply_configuration(self, name: str) -> dict[str, Any]:
        """
        Activate a named assembly configuration.

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

    def delete_configuration(self, name: str) -> dict[str, Any]:
        """
        Delete a named assembly configuration.

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

    def detect_under_constrained(self) -> dict[str, Any]:
        """
        Detect which assembly components are under-constrained.

        Iterates occurrences and checks grounded status and relation count
        to identify components with no positioning constraints.

        Returns:
            Dict with lists of grounded, constrained, and under-constrained components
        """
        try:
            doc = self.doc_manager.get_active_document()
            if not hasattr(doc, "Occurrences"):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            under_constrained = []
            grounded = []
            fully_constrained = []

            for i in range(1, occurrences.Count + 1):
                occ = occurrences.Item(i)
                name = occ.Name if hasattr(occ, "Name") else f"Component {i}"
                is_grounded = False
                is_suppressed = False
                try:
                    is_grounded = bool(occ.IsGrounded) if hasattr(occ, "IsGrounded") else False
                except Exception:
                    pass
                try:
                    is_suppressed = bool(occ.Suppressed) if hasattr(occ, "Suppressed") else False
                except Exception:
                    pass

                if is_suppressed:
                    continue
                if is_grounded:
                    grounded.append({"index": i - 1, "name": name})
                    continue

                relations_count = 0
                try:
                    relations = doc.Relations3d
                    for j in range(1, relations.Count + 1):
                        rel = relations.Item(j)
                        try:
                            geom1 = rel.GetGeometry1()
                            occ1 = geom1.Occurrence if hasattr(geom1, "Occurrence") else None
                            if occ1 is not None and occ1 == occ:
                                relations_count += 1
                                continue
                        except Exception:
                            pass
                        try:
                            geom2 = rel.GetGeometry2()
                            occ2 = geom2.Occurrence if hasattr(geom2, "Occurrence") else None
                            if occ2 is not None and occ2 == occ:
                                relations_count += 1
                        except Exception:
                            pass
                except Exception:
                    pass

                entry = {"index": i - 1, "name": name, "relations_count": relations_count}
                if relations_count == 0:
                    under_constrained.append(entry)
                else:
                    fully_constrained.append(entry)

            return {
                "status": "ok",
                "total_components": occurrences.Count,
                "grounded": grounded,
                "fully_constrained_count": len(fully_constrained),
                "under_constrained": under_constrained,
                "under_constrained_count": len(under_constrained),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    # =================================================================
    # ASSEMBLY-LEVEL FEATURES
    # =================================================================

    def _get_assembly_features(self, doc):
        """Get the AssemblyFeatures object from an assembly document."""
        if not hasattr(doc, "AssemblyFeatures"):
            raise AttributeError(
                "Active document does not have AssemblyFeatures. "
                "Make sure an assembly document is active."
            )
        return doc.AssemblyFeatures

    def _get_asm_profile(self):
        """Get the most recently accumulated assembly profile."""
        if self.sketch_manager is None:
            raise RuntimeError("SketchManager not available on AssemblyManager.")
        profiles = self.sketch_manager.get_accumulated_profiles()
        if not profiles:
            raise RuntimeError(
                "No closed sketch profile found. "
                "Call create_sketch(), draw geometry, and close_sketch() first."
            )
        return profiles[-1]

    def _get_scope_parts(self, doc, component_indices: list[int] | None = None) -> tuple:
        """
        Return a tuple of occurrence COM objects to use as pScopeParts.

        If component_indices is None, all occurrences in the assembly are included.
        Indices are 0-based; COM collection is 1-based.
        """
        occurrences = doc.Occurrences
        count = occurrences.Count
        if count == 0:
            raise RuntimeError("Assembly has no components (Occurrences.Count == 0).")
        if component_indices is None:
            return tuple(occurrences.Item(i + 1) for i in range(count))
        result = []
        for idx in component_indices:
            if idx < 0 or idx >= count:
                raise ValueError(
                    f"component_index {idx} out of range (assembly has {count} components)."
                )
            result.append(occurrences.Item(idx + 1))
        return tuple(result)

    def diagnose_assembly_features_api(self) -> dict[str, Any]:
        """
        Discover the AssemblyFeatures COM API on the active assembly document.

        Lists all attributes/collections available on doc.AssemblyFeatures
        and the Add methods available on each collection. Use this to verify
        the exact API before calling assembly feature creation methods.

        Returns:
            Dict with API discovery results
        """
        try:
            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)

            top_attrs = [a for a in dir(asm_features) if not a.startswith("_")]
            collections = {}
            for attr in top_attrs:
                try:
                    coll = getattr(asm_features, attr)
                    coll_type = type(coll).__name__
                    add_methods = [m for m in dir(coll) if m.startswith("Add")]
                    collections[attr] = {
                        "type": coll_type,
                        "add_methods": add_methods,
                    }
                except Exception as e:
                    collections[attr] = {"error": str(e)}

            # Also check doc-level pattern/mirror APIs
            doc_level = {}
            for candidate in ["AssemblyPatterns", "AssemblyMirrors"]:
                try:
                    coll = getattr(doc, candidate)
                    add_methods = [m for m in dir(coll) if m.startswith("Add") and not m.startswith("_")]
                    doc_level[candidate] = {"add_methods": add_methods}
                except Exception:
                    doc_level[candidate] = {"error": "not available"}

            def _dump_add_typeinfo(coll_obj):
                """Return parameter names and vt values for the Add method on a collection."""
                try:
                    ti = coll_obj._oleobj_.GetTypeInfo()
                    ta = ti.GetTypeAttr()
                    for i in range(ta.cFuncs):
                        fd = ti.GetFuncDesc(i)
                        names = ti.GetNames(fd.memid)
                        method_name = names[0] if names else f"func_{i}"
                        if method_name != "Add":
                            continue
                        args_info = []
                        for j, arg in enumerate(fd.args):
                            param_name = names[j + 1] if j + 1 < len(names) else f"p{j}"
                            arg_detail = {"name": param_name}
                            if hasattr(arg, "vt"):
                                arg_detail["vt"] = arg.vt
                                arg_detail["vt_hex"] = hex(arg.vt)
                            elif hasattr(arg, "tdesc"):
                                try:
                                    arg_detail["tdesc_vt"] = arg.tdesc.vt
                                    arg_detail["tdesc_vt_hex"] = hex(arg.tdesc.vt)
                                except Exception as e2:
                                    arg_detail["tdesc_error"] = str(e2)
                            args_info.append(arg_detail)
                        return {"param_count": len(args_info), "params": args_info}
                    return {"error": "Add method not found"}
                except Exception as e:
                    return {"error": str(e), "traceback": traceback.format_exc()}

            return {
                "status": "ok",
                "top_level_attributes": top_attrs,
                "feature_collections": collections,
                "doc_level_apis": doc_level,
                "extruded_cutouts_typeinfo": _dump_add_typeinfo(
                    asm_features.AssemblyFeaturesExtrudedCutouts
                ),
                "holes_typeinfo": _dump_add_typeinfo(
                    asm_features.AssemblyFeaturesHoles
                ),
                "patterns_typeinfo": _dump_add_typeinfo(
                    asm_features.AssemblyFeaturesPatterns
                ),
                "mirrors_typeinfo": _dump_add_typeinfo(
                    asm_features.AssemblyFeaturesMirrors
                ),
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def test_assembly_pattern(self, feature_names: list[str]) -> dict[str, Any]:
        """
        Diagnostic: probe AssemblyFeaturesPatterns.Add with all plausible arg
        combinations to determine which (if any) avoids E_ACCESSDENIED.

        Tries each attempt in isolation, undoes on success, wraps every attempt
        in try/except so a single crash doesn't abort the whole test.

        Returns a dict with:
          - patterns_dir: all public attrs on the patterns collection
          - patterns_typeinfo: re-runs GetTypeInfo for the Add method
          - doc_edit_methods: doc attrs containing 'undo'/'begin'/'edit'
          - attempts: {label: {result|error, ...}}
        """
        try:
            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)
            features = self._find_asm_features_by_name(doc, feature_names)
            feature = features[0]
            feature_tuple = tuple(features)

            patterns = asm_features.AssemblyFeaturesPatterns

            # ── collection introspection ──────────────────────────────────────
            patterns_dir = [a for a in dir(patterns) if not a.startswith("_")]

            # Reuse existing typeinfo helper
            def _dump_typeinfo(coll_obj):
                try:
                    ti = coll_obj._oleobj_.GetTypeInfo()
                    ta = ti.GetTypeAttr()
                    info = {}
                    for i in range(ta.cFuncs):
                        fd = ti.GetFuncDesc(i)
                        names = ti.GetNames(fd.memid)
                        method_name = names[0] if names else f"func_{i}"
                        params = []
                        for j, arg in enumerate(fd.args):
                            p = {"name": names[j + 1] if j + 1 < len(names) else f"p{j}"}
                            try:
                                p["vt"] = arg.vt
                                p["vt_hex"] = hex(arg.vt)
                            except Exception:
                                try:
                                    p["tdesc_vt"] = arg.tdesc.vt
                                except Exception:
                                    pass
                            params.append(p)
                        info[method_name] = {"cParams": len(params), "params": params}
                    return info
                except Exception as e:
                    return {"error": str(e)}

            patterns_typeinfo = _dump_typeinfo(patterns)

            # ── doc-level inspection ──────────────────────────────────────────
            doc_edit_methods = sorted(
                a for a in dir(doc)
                if any(kw in a.lower() for kw in ("undo", "begin", "edit", "mode"))
                and not a.startswith("_")
            )

            # ── attempt helper ────────────────────────────────────────────────
            def try_add(label, *args):
                try:
                    result = patterns.Add(*args)
                    outcome = {
                        "result": "success",
                        "returned_type": type(result).__name__,
                        "name": None,
                    }
                    try:
                        outcome["name"] = result.Name
                    except Exception:
                        pass
                    # Undo so subsequent attempts start clean
                    try:
                        doc.Undo()
                        outcome["undo"] = "ok"
                    except Exception as ue:
                        outcome["undo"] = str(ue)
                    return outcome
                except Exception as e:
                    return {"error": str(e)}

            # ── gather accumulated sketch profile if any ──────────────────────
            sketch_profile = None
            if self.sketch_manager:
                accumulated = self.sketch_manager.get_accumulated_profiles()
                if accumulated:
                    sketch_profile = accumulated[-1]

            # ── systematic attempts ───────────────────────────────────────────
            attempts: dict[str, Any] = {}

            # 1–3: PatternType 0/1/2 with Profile=None
            for pt in (0, 1, 2):
                attempts[f"pt{pt}_profile_none"] = try_add(
                    f"pt{pt}_none", len(features), feature_tuple, None, pt
                )

            # 4: use the accumulated sketch profile with PatternType=0
            if sketch_profile is not None:
                attempts["pt0_profile_sketch"] = try_add(
                    "pt0_sketch", len(features), feature_tuple, sketch_profile, 0
                )
            else:
                attempts["pt0_profile_sketch"] = {"skipped": "no accumulated sketch profile"}

            # 5: pass single COM object instead of tuple
            attempts["single_com_no_tuple"] = try_add(
                "single_no_tuple", 1, feature, None, 0
            )

            # 6: NumberOfFeatures=0, empty array — does the error change?
            attempts["num_features_0_empty"] = try_add(
                "empty", 0, (), None, 0
            )

            # 7: PatternType 0/1/2 with Points2d profile built on AsmRefPlanes
            try:
                plane = doc.AsmRefPlanes.Item(1)
                ps = doc.ProfileSets.Add()
                prof = ps.Profiles.Add(plane)
                pts = prof.Points2d
                pts.Add(0.0, 0.0)
                pts.Add(0.05, 0.0)
                prof.End(0)
                for pt in (0, 1, 2):
                    attempts[f"pt{pt}_points2d_profile"] = try_add(
                        f"pt{pt}_p2d", len(features), feature_tuple, prof, pt
                    )
                try:
                    ps.Delete()
                except Exception:
                    try:
                        doc.ProfileSets.Remove(ps)
                    except Exception:
                        pass
            except Exception as e:
                attempts["points2d_profile_build"] = {"error": str(e)}

            # ── edit-mode attempts ────────────────────────────────────────────
            # SE may require the doc to be in an explicit modeling/edit mode
            # before AssemblyFeaturesPatterns.Add is permitted.
            edit_mode_attempts: dict[str, Any] = {}

            for mode_name in ("EditAssembly", "ModelingInAssembly", "BeginCachedSolve"):
                mode_result: dict[str, Any] = {}
                # call the mode-entry method
                try:
                    getattr(doc, mode_name)()
                    mode_result["mode_call"] = "ok"
                except Exception as me:
                    mode_result["mode_call"] = str(me)

                # retry the simplest patterns.Add signature
                mode_result["add_after_mode"] = try_add(
                    f"after_{mode_name}", len(features), feature_tuple, None, 0
                )

                # try to leave the mode cleanly (best-effort)
                for exit_name in ("EndEditAssembly", "EndModelingInAssembly",
                                  "EndCachedSolve", "EndEdit"):
                    try:
                        getattr(doc, exit_name)()
                        mode_result["mode_exit"] = exit_name
                        break
                    except Exception:
                        pass
                else:
                    mode_result["mode_exit"] = "no exit method succeeded"

                edit_mode_attempts[mode_name] = mode_result

            # ── supplemental doc properties ───────────────────────────────────
            performance_mode: Any = None
            try:
                performance_mode = doc.PerformanceMode
            except Exception as e:
                performance_mode = f"error: {e}"

            # doc.AssemblyModel crashes SE — do NOT probe it.

            # ── feature type introspection ────────────────────────────────────
            feature_type_info: dict[str, Any] = {
                "python_type": type(feature).__name__,
            }
            for attr in ("Type", "FeatureType", "Category", "SubType", "Status"):
                try:
                    feature_type_info[attr] = getattr(feature, attr)
                except Exception as e:
                    feature_type_info[attr] = f"error: {e}"
            feature_type_info["dir"] = [
                a for a in dir(feature) if not a.startswith("_")
            ]

            return {
                "status": "completed",
                "feature_names_tested": feature_names,
                "feature_validated_live": self._validate_com_object(feature),
                "feature_type_info": feature_type_info,
                "patterns_dir": patterns_dir,
                "patterns_all_methods_typeinfo": patterns_typeinfo,
                "doc_edit_methods": doc_edit_methods,
                "has_accumulated_sketch_profile": sketch_profile is not None,
                "attempts": attempts,
                "edit_mode_attempts": edit_mode_attempts,
                "doc_performance_mode": performance_mode,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_assembly_extruded_cutout(
        self,
        depth: float,
        direction: str = "Normal",
        through_all: bool = False,
        component_indices: list[int] | None = None,
    ) -> dict[str, Any]:
        """
        Create an assembly-level extruded cutout that cuts across multiple components.

        Requires a closed sketch profile already created with create_sketch() /
        draw_*() / close_sketch() on the assembly document.

        Real COM signature:
        AssemblyFeaturesExtrudedCutouts.Add(
            nNumScopeParts, pScopeParts,
            nNumProfiles, pProfiles,
            ExtentType, pExtentSide, profileSide, pdDistance,
            pKeyPoint, pKeyPointFlags, pFromSurfOrPlane, pToSurfOrPlane)

        Args:
            depth: Cut depth in meters (ignored when through_all=True)
            direction: 'Normal' (default) or 'Reverse'
            through_all: If True, cut through all components
            component_indices: 0-based indices of components to cut through.
                               None (default) cuts through all components.

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)
            profile = self._get_asm_profile()
            scope_parts = self._get_scope_parts(doc, component_indices)

            dir_const = DirectionConstants.igRight
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            extent = ExtentTypeConstants.igThroughAll if through_all else ExtentTypeConstants.igFinite

            cutouts = asm_features.AssemblyFeaturesExtrudedCutouts
            _feature = cutouts.Add(
                len(scope_parts),   # nNumScopeParts
                scope_parts,        # pScopeParts
                1,                  # nNumProfiles
                (profile,),         # pProfiles
                extent,             # ExtentType
                dir_const,          # pExtentSide
                dir_const,          # profileSide
                depth,              # pdDistance
                None,               # pKeyPoint
                None,               # pKeyPointFlags
                None,               # pFromSurfOrPlane
                None,               # pToSurfOrPlane
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            _fname = getattr(_feature, "Name", None)
            if _fname:
                self._asm_feature_cache[_fname] = _feature
                self._persistent_feature_names.add(_fname)
                self._save_persistent_names()

            return {
                "status": "created",
                "type": "assembly_extruded_cutout",
                "depth": depth,
                "direction": direction,
                "through_all": through_all,
                "scope_parts_count": len(scope_parts),
                "name": _feature.Name if hasattr(_feature, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_assembly_extruded_protrusion(
        self,
        depth: float,
        direction: str = "Normal",
    ) -> dict[str, Any]:
        """
        Create an assembly-level extruded protrusion (adds material across assembly).

        Requires a closed sketch profile already on the assembly document.

        Uses doc.AssemblyFeatures.ExtrudedProtrusions.Add(nProfiles, profiles,
        extentSide, extentType, depth).  [ExtrudedProtrusions is unprefixed in SE 2026]

        Args:
            depth: Protrusion depth in meters
            direction: 'Normal' (default) or 'Reverse'

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)
            profile = self._get_asm_profile()

            dir_const = DirectionConstants.igRight
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            protrusions = asm_features.ExtrudedProtrusions
            _feature = protrusions.Add(
                1,
                (profile,),
                dir_const,
                ExtentTypeConstants.igFinite,
                depth,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "assembly_extruded_protrusion",
                "depth": depth,
                "direction": direction,
                "name": _feature.Name if hasattr(_feature, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_assembly_hole(
        self,
        depth: float,
        direction: str = "Normal",
        through_all: bool = False,
        component_indices: list[int] | None = None,
    ) -> dict[str, Any]:
        """
        Create an assembly-level hole through multiple components.

        Requires a closed circular sketch profile on the assembly document.

        Real COM signature:
        AssemblyFeaturesHoles.Add(
            nNumScopeParts, pScopeParts,
            nNumProfiles, pProfiles,
            ExtentType, pExtentSide, profileSide, pdDistance,
            pKeyPoint, pKeyPointFlags, pFromSurfOrPlane, pToSurfOrPlane)

        Args:
            depth: Hole depth in meters (ignored when through_all=True)
            direction: 'Normal' (default) or 'Reverse'
            through_all: If True, drill through all components
            component_indices: 0-based indices of components to drill through.
                               None (default) drills through all components.

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)
            profile = self._get_asm_profile()
            scope_parts = self._get_scope_parts(doc, component_indices)

            dir_const = DirectionConstants.igRight
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            extent = ExtentTypeConstants.igThroughAll if through_all else ExtentTypeConstants.igFinite

            holes = asm_features.AssemblyFeaturesHoles
            # Real signature (12 params, differs from ExtrudedCutouts):
            # Add(nNumScopeParts, pScopeParts, nNumProfiles, pProfiles,
            #     pExtentSide, pHoledata, ExtentType, pHoleDepth,
            #     pFromSurfOrPlane, pToSurfOrPlane, pKeyPoint, pKeyPointFlags)
            # pHoledata is a hole definition object; passing None to test
            # whether SE accepts a plain circular profile via pProfiles alone.
            _feature = holes.Add(
                len(scope_parts),   # nNumScopeParts
                scope_parts,        # pScopeParts
                1,                  # nNumProfiles
                (profile,),         # pProfiles
                dir_const,          # pExtentSide
                None,               # pHoledata (None = rely on pProfiles)
                extent,             # ExtentType
                depth,              # pHoleDepth
                None,               # pFromSurfOrPlane
                None,               # pToSurfOrPlane
                None,               # pKeyPoint
                None,               # pKeyPointFlags
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            _fname = getattr(_feature, "Name", None)
            if _fname:
                self._asm_feature_cache[_fname] = _feature
                self._persistent_feature_names.add(_fname)
                self._save_persistent_names()

            return {
                "status": "created",
                "type": "assembly_hole",
                "depth": depth,
                "direction": direction,
                "through_all": through_all,
                "scope_parts_count": len(scope_parts),
                "name": _feature.Name if hasattr(_feature, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_assembly_revolved_cutout(
        self,
        angle: float = 360.0,
        direction: str = "Normal",
        component_indices: list[int] | None = None,
    ) -> dict[str, Any]:
        """
        Create an assembly-level revolved cutout across multiple components.

        Requires a closed sketch profile with a revolution axis set
        (via set_axis_of_revolution) on the assembly document.

        Real COM signature (assumed same prefix pattern as extruded):
        AssemblyFeaturesRevolvedCutouts.Add(
            nNumScopeParts, pScopeParts,
            nNumProfiles, pProfiles,
            ExtentType, pExtentSide, profileSide, pdAngle,
            pKeyPoint, pKeyPointFlags, pFromSurfOrPlane, pToSurfOrPlane)

        Args:
            angle: Revolution angle in degrees (default 360)
            direction: 'Normal' (default) or 'Reverse'
            component_indices: 0-based indices of components to cut through.
                               None (default) cuts through all components.

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)
            profile = self._get_asm_profile()
            scope_parts = self._get_scope_parts(doc, component_indices)

            dir_const = DirectionConstants.igRight
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            angle_rad = math.radians(angle)

            cutouts = asm_features.AssemblyFeaturesRevolvedCutouts
            _feature = cutouts.Add(
                len(scope_parts),           # nNumScopeParts
                scope_parts,                # pScopeParts
                1,                          # nNumProfiles
                (profile,),                 # pProfiles
                ExtentTypeConstants.igFinite,  # ExtentType
                dir_const,                  # pExtentSide
                dir_const,                  # profileSide
                angle_rad,                  # pdAngle
                None,                       # pKeyPoint
                None,                       # pKeyPointFlags
                None,                       # pFromSurfOrPlane
                None,                       # pToSurfOrPlane
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            _fname = getattr(_feature, "Name", None)
            if _fname:
                self._asm_feature_cache[_fname] = _feature
                self._persistent_feature_names.add(_fname)
                self._save_persistent_names()

            return {
                "status": "created",
                "type": "assembly_revolved_cutout",
                "angle": angle,
                "direction": direction,
                "scope_parts_count": len(scope_parts),
                "name": _feature.Name if hasattr(_feature, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_assembly_revolved_protrusion(
        self,
        angle: float = 360.0,
        direction: str = "Normal",
    ) -> dict[str, Any]:
        """
        Create an assembly-level revolved protrusion.

        Requires a closed sketch profile with a revolution axis on the assembly doc.

        Uses doc.AssemblyFeatures.RevolvedProtrusions.Add(nProfiles, profiles,
        extentSide, extentType, angle).  [RevolvedProtrusions is unprefixed in SE 2026]

        Args:
            angle: Revolution angle in degrees (default 360)
            direction: 'Normal' (default) or 'Reverse'

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)
            profile = self._get_asm_profile()

            dir_const = DirectionConstants.igRight
            if direction == "Reverse":
                dir_const = DirectionConstants.igLeft

            angle_rad = math.radians(angle)

            protrusions = asm_features.RevolvedProtrusions
            _feature = protrusions.Add(
                1,
                (profile,),
                dir_const,
                ExtentTypeConstants.igFinite,
                angle_rad,
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            self.sketch_manager.clear_accumulated_profiles()

            return {
                "status": "created",
                "type": "assembly_revolved_protrusion",
                "angle": angle,
                "direction": direction,
                "name": _feature.Name if hasattr(_feature, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    @staticmethod
    def _validate_com_object(obj) -> bool:
        """Return True if the COM object is still alive (not stale)."""
        try:
            _ = obj.Name
            return True
        except Exception:
            return False

    def _find_asm_features_by_name(self, doc, feature_names: list[str]) -> list:
        """
        Look up assembly feature COM objects by name.

        Strategy:
        1. Check self._asm_feature_cache first.  Validate each hit — if the COM
           object is stale (server restarted, RPC gone), prune it from cache and
           fall through to collection search.
        2. Search all AssemblyFeatures sub-collections for any still-missing names.
           Update cache with fresh references discovered here.
        3. Build ordered result.  For names that are cached-but-stale and also not
           in any collection, raise a clear "stale reference" error so the user
           knows to recreate the feature rather than getting a cryptic COM error.

        Returns list of COM feature objects in the same order as feature_names.
        Raises RuntimeError if any name is not found or only has a stale reference.
        """
        found: dict[str, Any] = {}
        stale: set[str] = set()

        # --- 1. cache lookup with liveness validation ---
        for name in feature_names:
            if name in self._asm_feature_cache:
                obj = self._asm_feature_cache[name]
                if self._validate_com_object(obj):
                    found[name] = obj
                else:
                    # Dead reference — prune and force collection search
                    del self._asm_feature_cache[name]
                    stale.add(name)

        still_missing = [n for n in feature_names if n not in found]

        # --- 2. collection search for anything not yet resolved ---
        name_map: dict[str, Any] = {}
        if still_missing:
            asm_features = self._get_assembly_features(doc)
            collections_to_search = [
                "AssemblyFeaturesExtrudedCutouts",
                "AssemblyFeaturesHoles",
                "AssemblyFeaturesRevolvedCutouts",
                "ExtrudedProtrusions",
                "RevolvedProtrusions",
                "AssemblyFeaturesSweptProtrusions",
                "AssemblyFeaturesMirrors",
                "AssemblyFeaturesPatterns",
            ]
            for coll_name in collections_to_search:
                try:
                    coll = getattr(asm_features, coll_name)
                    for i in range(coll.Count):
                        item = coll.Item(i + 1)
                        try:
                            name_map[item.Name] = item
                        except Exception:
                            pass
                except Exception:
                    pass
            # Refresh cache with live collection objects
            self._asm_feature_cache.update(name_map)
            found.update({n: name_map[n] for n in still_missing if n in name_map})

        # --- 3. build result / surface clear errors ---
        result = []
        not_found = []
        for name in feature_names:
            if name in found:
                result.append(found[name])
            else:
                not_found.append(name)

        if not_found:
            # Three failure modes, each with a distinct action message:
            # 1. stale: was in cache this session but COM proxy died
            # 2. persistent: known from a previous server session, not yet live
            # 3. never_found: name has never been seen
            truly_stale = [n for n in not_found if n in stale]
            from_prev_session = [
                n for n in not_found
                if n not in stale and n in self._persistent_feature_names
            ]
            never_found = [
                n for n in not_found
                if n not in stale and n not in self._persistent_feature_names
            ]
            available = sorted(found.keys() | name_map.keys())
            parts = []
            if truly_stale:
                parts.append(
                    f"Feature(s) {truly_stale} COM reference is stale — "
                    "recreate the feature in this session before patterning/mirroring."
                )
            if from_prev_session:
                parts.append(
                    f"Feature(s) {from_prev_session} were created in a previous server "
                    "session. The name is persisted on disk but the COM reference is gone "
                    "after the process restarted. Recreate the feature to get a fresh "
                    "COM reference."
                )
            if never_found:
                parts.append(
                    f"Feature(s) {never_found} not found. Available: {available}"
                )
            raise RuntimeError("  ".join(parts))

        return result

    def create_assembly_mirror(
        self,
        feature_names: list[str],
        plane_index: int,
        mirror_type: int = 0,
    ) -> dict[str, Any]:
        """
        Create an assembly-level mirror of one or more assembly features.

        Real COM signature:
        AssemblyFeaturesMirrors.Add(NumberOfFeatures, ppFeaturesArray,
                                    pMirrorPlane, MirrorType)

        ppFeaturesArray contains existing assembly features (cutouts, holes,
        protrusions) — NOT component occurrences.

        Args:
            feature_names: Names of existing assembly features to mirror
                           (e.g. ["Cutout 1"])
            plane_index: 1-based AsmRefPlanes index to mirror across
            mirror_type: MirrorType enum value (default 0)

        Returns:
            Dict with status
        """
        try:
            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)

            features = self._find_asm_features_by_name(doc, feature_names)

            # Assembly docs use AsmRefPlanes (try first), fall back to RefPlanes
            try:
                ref_planes = doc.AsmRefPlanes
                _ = ref_planes.Count
            except Exception:
                ref_planes = doc.RefPlanes

            if plane_index < 1 or plane_index > ref_planes.Count:
                return {
                    "error": f"Invalid plane_index {plane_index}. "
                    f"Assembly has {ref_planes.Count} reference planes."
                }

            mirror_plane = ref_planes.Item(plane_index)
            mirrors = asm_features.AssemblyFeaturesMirrors
            _feature = mirrors.Add(
                len(features),      # NumberOfFeatures
                tuple(features),    # ppFeaturesArray
                mirror_plane,       # pMirrorPlane
                mirror_type,        # MirrorType
            )
            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "assembly_mirror",
                "feature_names": feature_names,
                "plane_index": plane_index,
                "name": _feature.Name if hasattr(_feature, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def _build_points_profile(self, doc, plane_index: int, points: list[tuple[float, float]]):
        """
        Build a temporary Points2d sketch profile on the given AsmRefPlane.

        Creates a new ProfileSet, adds a Profile on the plane, inserts one
        Point2d per (x, y) tuple, and closes the profile with End(0).

        Returns the profile COM object.  The caller owns the ProfileSet and
        should delete it after the feature Add() call completes.
        """
        try:
            plane = doc.AsmRefPlanes.Item(plane_index)
        except Exception:
            plane = doc.RefPlanes.Item(plane_index)

        profile_set = doc.ProfileSets.Add()
        profile = profile_set.Profiles.Add(plane)
        pts = profile.Points2d
        for x, y in points:
            pts.Add(x, y)
        profile.End(0)
        return profile_set, profile

    def create_assembly_pattern_rectangular(
        self,
        feature_names: list[str],
        x_count: int,
        x_spacing: float,
        y_count: int = 1,
        y_spacing: float = 0.0,
    ) -> dict[str, Any]:
        """
        Create a rectangular pattern of assembly features using a Points2d sketch.

        Real COM signature:
        AssemblyFeaturesPatterns.Add(NumberOfFeatures, ppFeaturesArray,
                                     Profile, PatternType)

        Builds a temporary ProfileSet on AsmRefPlanes.Item(1) containing one
        Point2d per grid cell (x_count × y_count), then passes it as Profile.

        Args:
            feature_names: Names of existing assembly features to pattern
            x_count: Number of instances in X (must be >= 1)
            x_spacing: Spacing between X instances in meters
            y_count: Number of instances in Y (default 1)
            y_spacing: Spacing between Y instances in meters (default 0.0)

        Returns:
            Dict with status
        """
        try:
            if x_count < 1:
                return {"error": "x_count must be >= 1"}
            if y_count < 1:
                return {"error": "y_count must be >= 1"}

            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)
            features = self._find_asm_features_by_name(doc, feature_names)

            # Build grid of Points2d on the Top/XY plane (index 1)
            grid_points = [
                (xi * x_spacing, yi * y_spacing)
                for yi in range(y_count)
                for xi in range(x_count)
            ]
            profile_set, profile = self._build_points_profile(doc, 1, grid_points)

            try:
                patterns = asm_features.AssemblyFeaturesPatterns
                _feature = patterns.Add(
                    len(features),      # NumberOfFeatures
                    tuple(features),    # ppFeaturesArray
                    profile,            # Profile (Points2d grid)
                    0,                  # PatternType: rectangular
                )
            finally:
                # Clean up temporary profile set
                try:
                    profile_set.Delete()
                except Exception:
                    try:
                        doc.ProfileSets.Remove(profile_set)
                    except Exception:
                        pass

            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "assembly_pattern_rectangular",
                "feature_names": feature_names,
                "x_count": x_count,
                "x_spacing": x_spacing,
                "y_count": y_count,
                "y_spacing": y_spacing,
                "name": _feature.Name if hasattr(_feature, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def create_assembly_pattern_circular(
        self,
        feature_names: list[str],
        count: int,
        angle: float = 360.0,
        axis_plane_index: int = 1,
        radius: float = 0.05,
    ) -> dict[str, Any]:
        """
        Create a circular pattern of assembly features using a Points2d sketch.

        Real COM signature:
        AssemblyFeaturesPatterns.Add(NumberOfFeatures, ppFeaturesArray,
                                     Profile, PatternType)

        Builds a temporary ProfileSet on AsmRefPlanes.Item(axis_plane_index)
        with Points2d arranged on a circle of the given radius, then passes it
        as Profile.

        Args:
            feature_names: Names of existing assembly features to pattern
            count: Total number of instances (including original)
            angle: Total arc angle in degrees (360 = full circle)
            axis_plane_index: 1-based AsmRefPlanes index whose normal is the
                              rotation axis (default 1 = Top/XY)
            radius: Radius of the circular pattern in meters (default 0.05)

        Returns:
            Dict with status
        """
        try:
            if count < 1:
                return {"error": "count must be >= 1"}

            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)
            features = self._find_asm_features_by_name(doc, feature_names)

            # Build circle of Points2d; step angle = total_angle / count
            total_rad = math.radians(angle)
            step = total_rad / count
            circle_points = [
                (radius * math.cos(step * i), radius * math.sin(step * i))
                for i in range(count)
            ]
            profile_set, profile = self._build_points_profile(
                doc, axis_plane_index, circle_points
            )

            try:
                patterns = asm_features.AssemblyFeaturesPatterns
                _feature = patterns.Add(
                    len(features),      # NumberOfFeatures
                    tuple(features),    # ppFeaturesArray
                    profile,            # Profile (Points2d circle)
                    1,                  # PatternType: circular
                )
            finally:
                try:
                    profile_set.Delete()
                except Exception:
                    try:
                        doc.ProfileSets.Remove(profile_set)
                    except Exception:
                        pass

            if _feature is None:
                return {"error": "Feature creation failed: COM returned None"}

            return {
                "status": "created",
                "type": "assembly_pattern_circular",
                "feature_names": feature_names,
                "count": count,
                "angle": angle,
                "axis_plane_index": axis_plane_index,
                "radius": radius,
                "name": _feature.Name if hasattr(_feature, "Name") else None,
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def list_assembly_features(self) -> dict[str, Any]:
        """
        List all assembly features grouped by collection name.

        Searches all known AssemblyFeatures sub-collections and returns a dict
        mapping collection name → list of feature names.  Only non-empty
        collections are included.  Features that were created this session but
        are not enumerable via collections (Count stays 0) appear under the
        special key '_cached'.

        Returns:
            Dict with status and features mapping
        """
        try:
            doc = self.doc_manager.get_active_document()
            asm_features = self._get_assembly_features(doc)

            collections_to_search = [
                "AssemblyFeaturesExtrudedCutouts",
                "AssemblyFeaturesHoles",
                "AssemblyFeaturesRevolvedCutouts",
                "ExtrudedProtrusions",
                "RevolvedProtrusions",
                "AssemblyFeaturesSweptProtrusions",
                "AssemblyFeaturesMirrors",
                "AssemblyFeaturesPatterns",
            ]
            result: dict[str, list[str]] = {}
            listed_names: set[str] = set()
            for coll_name in collections_to_search:
                try:
                    coll = getattr(asm_features, coll_name)
                    count = coll.Count
                    if count == 0:
                        continue
                    names = []
                    for i in range(count):
                        try:
                            item = coll.Item(i + 1)
                            try:
                                n = item.Name
                                names.append(n)
                                listed_names.add(n)
                                # Keep cache in sync
                                self._asm_feature_cache[n] = item
                            except Exception:
                                names.append(f"Item{i + 1}")
                        except Exception:
                            names.append(f"Item{i + 1}")
                    result[coll_name] = names
                except Exception:
                    pass

            # Prune stale cache entries before building _cached.
            stale_keys = [
                n for n, obj in self._asm_feature_cache.items()
                if not self._validate_com_object(obj)
            ]
            for k in stale_keys:
                del self._asm_feature_cache[k]

            # Features created this session but not enumerable via collections.
            unlisted = sorted(
                n for n in self._asm_feature_cache if n not in listed_names
            )
            if unlisted:
                result["_cached"] = unlisted

            # Features known from a previous server session (name persisted on
            # disk) but for which we have no live COM reference right now.
            prev_session = sorted(
                n for n in self._persistent_feature_names
                if n not in listed_names and n not in self._asm_feature_cache
            )
            if prev_session:
                result["_persistent_stale"] = prev_session

            return {"status": "success", "features": result}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}
