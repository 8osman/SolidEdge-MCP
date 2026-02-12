#!/usr/bin/env python
"""Test different revolve signatures"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from solidedge_mcp.backends.connection import SolidEdgeConnection
from solidedge_mcp.backends.documents import DocumentManager
import math
import win32com.client
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

print("Testing AddRevolvedProtrusion with different signatures...")

# Create COM VARIANT array for profiles
profile_array = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [profile])

try:
    # Try with count, VARIANT array, angle (3 params)
    model = models.AddRevolvedProtrusion(1, profile_array, angle_rad)
    print("SUCCESS with 3 params using VARIANT array!")
except Exception as e:
    print(f"Failed with VARIANT array (3 params): {e}")
    try:
        # Try with count, array, None, angle (4 params with axis=None)
        model = models.AddRevolvedProtrusion(1, profile_array, None, angle_rad)
        print("SUCCESS with 4 params (count, array, None, angle)!")
    except Exception as e2:
        print(f"Failed with 4 params: {e2}")

doc_manager.close_document(save=False)
