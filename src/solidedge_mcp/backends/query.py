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

    def get_mass_properties(self, density: float = 7850) -> Dict[str, Any]:
        """
        Get mass properties of the part.

        Args:
            density: Material density in kg/m³ (default: 7850 for steel)

        Returns:
            Dict with volume, mass, center of gravity, etc.
        """
        try:
            doc = self.doc_manager.get_active_document()

            # Get models collection
            if not hasattr(doc, 'Models'):
                return {"error": "Document does not support mass properties"}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No features in document"}

            # Try to get mass properties
            # Note: Actual implementation varies by Solid Edge version
            try:
                # Some versions have PhysicalProperties
                if hasattr(doc, 'PhysicalProperties'):
                    props = doc.PhysicalProperties
                    volume = props.Volume if hasattr(props, 'Volume') else 0
                    mass = volume * density

                    cog_x = props.CenterOfGravityX if hasattr(props, 'CenterOfGravityX') else 0
                    cog_y = props.CenterOfGravityY if hasattr(props, 'CenterOfGravityY') else 0
                    cog_z = props.CenterOfGravityZ if hasattr(props, 'CenterOfGravityZ') else 0

                    return {
                        "volume": volume,
                        "mass": mass,
                        "center_of_gravity": [cog_x, cog_y, cog_z],
                        "density": density,
                        "units": {
                            "volume": "m³",
                            "mass": "kg",
                            "density": "kg/m³"
                        }
                    }
                else:
                    # Fallback - indicate manual calculation needed
                    return {
                        "note": "Mass properties require calculation via Solid Edge UI",
                        "density": density,
                        "status": "use_solidedge_ui"
                    }
            except Exception as inner_e:
                return {
                    "error": "Could not retrieve mass properties",
                    "details": str(inner_e),
                    "note": "Use Tools > Physical Properties in Solid Edge"
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

    def get_bounding_box(self) -> Dict[str, Any]:
        """Get the bounding box of the model"""
        try:
            doc = self.doc_manager.get_active_document()

            if not hasattr(doc, 'Models'):
                return {"error": "Document does not support bounding box"}

            models = doc.Models
            if models.Count == 0:
                return {"error": "No features in document"}

            # Get bounding box
            # Note: Implementation varies by Solid Edge version
            return {
                "note": "Bounding box calculation not implemented",
                "status": "use_solidedge_ui"
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

            if hasattr(doc, 'Models'):
                counts["features"] = doc.Models.Count

            if hasattr(doc, 'Occurrences'):
                counts["components"] = doc.Occurrences.Count

            if hasattr(doc, 'ProfileSets'):
                counts["sketches"] = doc.ProfileSets.Count

            return counts
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
