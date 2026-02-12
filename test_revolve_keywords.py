#!/usr/bin/env python
"""Test revolve with keyword arguments like extrude uses"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from solidedge_mcp.backends.connection import SolidEdgeConnection
from solidedge_mcp.backends.documents import DocumentManager
import math

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

print("Testing AddRevolvedProtrusion with keyword arguments (like extrude)...")

# Try like extrude does it - keyword arguments with tuple
try:
    model = models.AddRevolvedProtrusion(
        NumberOfProfiles=1,
        ProfileArray=(profile,),
        FiniteAngle1=angle_rad
    )
    print("SUCCESS with keyword arguments!")
except Exception as e:
    print(f"Failed with keywords: {e}")

doc_manager.close_document(save=False)
