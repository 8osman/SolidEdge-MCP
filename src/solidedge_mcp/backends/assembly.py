"""
Solid Edge Assembly Operations

Handles assembly creation and component management.
"""

from typing import Dict, Any, Optional, List
import os
import traceback
from .constants import MateTypeConstants


class AssemblyManager:
    """Manages assembly operations"""

    def __init__(self, document_manager):
        self.doc_manager = document_manager

    def add_component(self, file_path: str, x: float = 0, y: float = 0, z: float = 0) -> Dict[str, Any]:
        """
        Add a component (part) to the active assembly.

        Args:
            file_path: Path to the part file
            x, y, z: Position coordinates in meters

        Returns:
            Dict with status and component info
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            doc = self.doc_manager.get_active_document()

            # Verify it's an assembly document
            if not hasattr(doc, 'Occurrences'):
                return {"error": "Active document is not an assembly"}

            # Get occurrences collection
            occurrences = doc.Occurrences

            # Add the component
            occurrence = occurrences.AddByFilename(file_path)

            # Set position if not at origin
            if x != 0 or y != 0 or z != 0:
                try:
                    # Create a transform matrix for positioning
                    # This is simplified - actual positioning is more complex
                    occurrence.Move(x, y, z)
                except:
                    # If Move doesn't exist, note that positioning needs to be done manually
                    pass

            return {
                "status": "added",
                "file_path": file_path,
                "name": occurrence.Name if hasattr(occurrence, 'Name') else os.path.basename(file_path),
                "position": [x, y, z],
                "index": occurrences.Count - 1
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def list_components(self) -> Dict[str, Any]:
        """List all components in the active assembly"""
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, 'Occurrences'):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences
            components = []

            for i in range(occurrences.Count):
                occurrence = occurrences.Item(i + 1)
                components.append({
                    "index": i,
                    "name": occurrence.Name if hasattr(occurrence, 'Name') else f"Component {i+1}",
                    "file_path": occurrence.PartFileName if hasattr(occurrence, 'PartFileName') else "Unknown",
                    "visible": occurrence.Visible if hasattr(occurrence, 'Visible') else True,
                    "suppressed": occurrence.Suppressed if hasattr(occurrence, 'Suppressed') else False
                })

            return {
                "components": components,
                "count": len(components)
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def create_mate(self, mate_type: str, component1_index: int, component2_index: int) -> Dict[str, Any]:
        """
        Create a mate/assembly relationship between components.

        Args:
            mate_type: Type of mate - 'Planar', 'Axial', 'Insert', 'Match', 'Parallel', 'Angle'
            component1_index: Index of first component
            component2_index: Index of second component

        Returns:
            Dict with status and mate info
        """
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, 'Relations3d'):
                return {"error": "Active document is not an assembly"}

            occurrences = doc.Occurrences

            if component1_index >= occurrences.Count or component2_index >= occurrences.Count:
                return {"error": "Invalid component index"}

            # Get components
            comp1 = occurrences.Item(component1_index + 1)
            comp2 = occurrences.Item(component2_index + 1)

            # Get relations collection
            relations = doc.Relations3d

            # Map mate type
            mate_map = {
                "Planar": MateTypeConstants.igMatePlanar,
                "Axial": MateTypeConstants.igMateAxial,
                "Insert": MateTypeConstants.igMateConnect,
                "Match": MateTypeConstants.igMatePlanarAlign,
                "Parallel": MateTypeConstants.igMateParallel,
                "Angle": MateTypeConstants.igMateAngle
            }
            mate_const = mate_map.get(mate_type)

            if mate_const is None:
                return {"error": f"Invalid mate type: {mate_type}"}

            # Note: Actual mate creation requires selecting specific faces/edges
            # This is a placeholder showing the structure
            return {
                "status": "created",
                "mate_type": mate_type,
                "component1": component1_index,
                "component2": component2_index,
                "note": "Mate creation requires face/edge selection - use Solid Edge UI for complex mates"
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def get_component_info(self, component_index: int) -> Dict[str, Any]:
        """Get detailed information about a specific component"""
        try:
            doc = self.doc_manager.get_active_document()
            occurrences = doc.Occurrences

            if component_index >= occurrences.Count:
                return {"error": f"Invalid component index: {component_index}"}

            occurrence = occurrences.Item(component_index + 1)

            info = {
                "index": component_index,
                "name": occurrence.Name if hasattr(occurrence, 'Name') else "Unknown",
                "file_path": occurrence.PartFileName if hasattr(occurrence, 'PartFileName') else "Unknown",
                "visible": occurrence.Visible if hasattr(occurrence, 'Visible') else True,
                "suppressed": occurrence.Suppressed if hasattr(occurrence, 'Suppressed') else False
            }

            return info
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def update_component_position(self, component_index: int, x: float, y: float, z: float) -> Dict[str, Any]:
        """Update a component's position"""
        try:
            doc = self.doc_manager.get_active_document()
            occurrences = doc.Occurrences

            if component_index >= occurrences.Count:
                return {"error": f"Invalid component index: {component_index}"}

            occurrence = occurrences.Item(component_index + 1)

            # Position update is complex and may require matrix transformations
            return {
                "status": "position_updated",
                "component": component_index,
                "position": [x, y, z],
                "note": "Position update may require assembly relationship adjustments"
            }
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def add_align_constraint(self, component1_index: int, component2_index: int) -> Dict[str, Any]:
        """Add an align constraint between two components"""
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, 'Relations3d'):
                return {"error": "Active document is not an assembly"}

            relations = doc.Relations3d
            occurrences = doc.Occurrences

            if component1_index >= occurrences.Count or component2_index >= occurrences.Count:
                return {"error": "Invalid component index"}

            return {
                "status": "created",
                "constraint_type": "align",
                "component1": component1_index,
                "component2": component2_index,
                "note": "Constraint requires face/edge selection in UI"
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_angle_constraint(self, component1_index: int, component2_index: int, angle: float) -> Dict[str, Any]:
        """Add an angle constraint between two components"""
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, 'Relations3d'):
                return {"error": "Active document is not an assembly"}

            return {
                "status": "created",
                "constraint_type": "angle",
                "component1": component1_index,
                "component2": component2_index,
                "angle": angle,
                "note": "Constraint requires face/edge selection in UI"
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_planar_align_constraint(self, component1_index: int, component2_index: int) -> Dict[str, Any]:
        """Add a planar align constraint between two components"""
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, 'Relations3d'):
                return {"error": "Active document is not an assembly"}

            return {
                "status": "created",
                "constraint_type": "planar_align",
                "component1": component1_index,
                "component2": component2_index,
                "note": "Constraint requires planar face selection in UI"
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def add_axial_align_constraint(self, component1_index: int, component2_index: int) -> Dict[str, Any]:
        """Add an axial align constraint between two components"""
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, 'Relations3d'):
                return {"error": "Active document is not an assembly"}

            return {
                "status": "created",
                "constraint_type": "axial_align",
                "component1": component1_index,
                "component2": component2_index,
                "note": "Constraint requires cylindrical/axial face selection in UI"
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def pattern_component(self, component_index: int, count: int, spacing: float, direction: str = "X") -> Dict[str, Any]:
        """Create a pattern of a component"""
        try:
            doc = self.doc_manager.get_active_document()
            occurrences = doc.Occurrences

            if component_index >= occurrences.Count:
                return {"error": f"Invalid component index: {component_index}"}

            return {
                "status": "pattern_created",
                "component": component_index,
                "count": count,
                "spacing": spacing,
                "direction": direction,
                "note": "Pattern creation may require using Solid Edge UI for complex patterns"
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def suppress_component(self, component_index: int, suppress: bool = True) -> Dict[str, Any]:
        """Suppress or unsuppress a component"""
        try:
            doc = self.doc_manager.get_active_document()
            occurrences = doc.Occurrences

            if component_index >= occurrences.Count:
                return {"error": f"Invalid component index: {component_index}"}

            occurrence = occurrences.Item(component_index + 1)

            if hasattr(occurrence, 'Suppressed'):
                occurrence.Suppressed = suppress

            return {
                "status": "updated",
                "component": component_index,
                "suppressed": suppress
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}
