#!/usr/bin/env python
"""Test AddFiniteRevolvedProtrusion (simpler 7-parameter revolve)"""

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

print("=" * 70)
print("Testing AddFiniteRevolvedProtrusion (7 parameters)")
print("=" * 70)
print(f"\nSignature:")
print("  (NumberOfProfiles, ProfileArray, ReferenceAxis, ProfilePlaneSide,")
print("   AngleofRevolution, KeyPointOrTangentFace, KeyPointFlags)")

# Test 1: Try with keyword arguments, mimicking extrude pattern
print("\n[Test 1] Keyword args, minimal params (first 2 + angle)")
try:
    model = models.AddFiniteRevolvedProtrusion(
        NumberOfProfiles=1,
        ProfileArray=(profile,),
        AngleofRevolution=angle_rad
    )
    print("SUCCESS!")
    doc_manager.close_document(save=False)
    sys.exit(0)
except Exception as e:
    print(f"Failed: {e}")

# Test 2: Try with ReferenceAxis=None
print("\n[Test 2] With ReferenceAxis=None")
try:
    model = models.AddFiniteRevolvedProtrusion(
        NumberOfProfiles=1,
        ProfileArray=(profile,),
        ReferenceAxis=None,
        AngleofRevolution=angle_rad
    )
    print("SUCCESS!")
    doc_manager.close_document(save=False)
    sys.exit(0)
except Exception as e:
    print(f"Failed: {e}")

# Test 3: Try with pythoncom.Empty
print("\n[Test 3] With ReferenceAxis=pythoncom.Empty")
try:
    model = models.AddFiniteRevolvedProtrusion(
        NumberOfProfiles=1,
        ProfileArray=(profile,),
        ReferenceAxis=pythoncom.Empty,
        AngleofRevolution=angle_rad
    )
    print("SUCCESS!")
    doc_manager.close_document(save=False)
    sys.exit(0)
except Exception as e:
    print(f"Failed: {e}")

# Test 4: Try with ReferenceAxis as one of the sketch lines (Y-axis)
print("\n[Test 4] With ReferenceAxis as Y-axis line from sketch")
try:
    # Use the left edge of the L-shape as axis (x=0 line)
    axis_line = lines.Item(4)  # Last line we drew (0,0.04 to 0,0)
    model = models.AddFiniteRevolvedProtrusion(
        NumberOfProfiles=1,
        ProfileArray=(profile,),
        ReferenceAxis=axis_line,
        AngleofRevolution=angle_rad
    )
    print("SUCCESS!")
    doc_manager.close_document(save=False)
    sys.exit(0)
except Exception as e:
    print(f"Failed: {e}")

# Test 5: Try positional arguments
print("\n[Test 5] Positional args (1, tuple, None, None, angle, None, None)")
try:
    model = models.AddFiniteRevolvedProtrusion(
        1,
        (profile,),
        None,
        None,
        angle_rad,
        None,
        None
    )
    print("SUCCESS!")
    doc_manager.close_document(save=False)
    sys.exit(0)
except Exception as e:
    print(f"Failed: {e}")

# Test 6: Try with all Empty
print("\n[Test 6] All optional params as pythoncom.Empty")
try:
    model = models.AddFiniteRevolvedProtrusion(
        1,
        (profile,),
        pythoncom.Empty,
        pythoncom.Empty,
        angle_rad,
        pythoncom.Empty,
        pythoncom.Empty
    )
    print("SUCCESS!")
    doc_manager.close_document(save=False)
    sys.exit(0)
except Exception as e:
    print(f"Failed: {e}")

print("\n" + "=" * 70)
print("All tests failed. Need SDK documentation for ReferenceAxis parameter.")
print("=" * 70)

doc_manager.close_document(save=False)
