#!/usr/bin/env python
"""Test revolve with proper 14-parameter signature"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from solidedge_mcp.backends.connection import SolidEdgeConnection
from solidedge_mcp.backends.documents import DocumentManager
import math
import pythoncom

connection = SolidEdgeConnection()
connection.connect(start_if_needed=True)
doc_manager = DocumentManager(connection)
doc_manager.create_part()
doc = doc_manager.get_active_document()

# Create sketch for revolve
ref_planes = doc.RefPlanes
ref_plane = ref_planes.Item(2)  # Front plane
profile_sets = doc.ProfileSets
profile_set = profile_sets.Add()
profiles = profile_set.Profiles
profile = profiles.Add(ref_plane)

# Draw a simple L-shape
lines = profile.Lines2d
lines.AddBy2Points(0, 0, 0.02, 0)
lines.AddBy2Points(0.02, 0, 0.02, 0.04)
lines.AddBy2Points(0.02, 0.04, 0, 0.04)
lines.AddBy2Points(0, 0.04, 0, 0)

profile.End(0)

models = doc.Models
angle_rad = math.radians(360)

print("Testing AddRevolvedProtrusion with proper 14 parameters...")
print("Signature: (NumberOfProfiles, ProfileArray, RefAxis, ProfileSide, ExtentType1, ExtentSide1, FiniteAngle1, KeyPointOrTangentFace1, KeyPointFlags1, ExtentType2, ExtentSide2, FiniteAngle2, KeyPointOrTangentFace2, KeyPointFlags2)")

try:
    # For a simple full revolve, try using defaults (pythoncom.Empty) for most params
    model = models.AddRevolvedProtrusion(
        1,  # NumberOfProfiles
        [profile],  # ProfileArray as list
        pythoncom.Empty,  # RefAxis (use default)
        pythoncom.Empty,  # ProfileSide
        pythoncom.Empty,  # ExtentType1
        pythoncom.Empty,  # ExtentSide1
        angle_rad,  # FiniteAngle1
        pythoncom.Empty,  # KeyPointOrTangentFace1
        pythoncom.Empty,  # KeyPointFlags1
        pythoncom.Empty,  # ExtentType2
        pythoncom.Empty,  # ExtentSide2
        pythoncom.Empty,  # FiniteAngle2
        pythoncom.Empty,  # KeyPointOrTangentFace2
        pythoncom.Empty   # KeyPointFlags2
    )
    print("SUCCESS!")
except Exception as e:
    print(f"Failed: {e}")

doc_manager.close_document(save=False)
