#!/usr/bin/env python
"""Test the fixed set_view method"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from solidedge_mcp.backends.connection import SolidEdgeConnection
from solidedge_mcp.backends.documents import DocumentManager
from solidedge_mcp.backends.export import ViewModel
import time

connection = SolidEdgeConnection()
doc_manager = DocumentManager(connection)
view_manager = ViewModel(doc_manager)

connection.connect(start_if_needed=True)
doc_manager.create_part()

# Create simple geometry
doc = doc_manager.get_active_document()
ref_planes = doc.RefPlanes
profile_sets = doc.ProfileSets
profile_set = profile_sets.Add()
profiles = profile_set.Profiles
profile = profiles.Add(ref_planes.Item(1))

lines = profile.Lines2d
lines.AddBy2Points(-0.05, -0.05, 0.05, -0.05)
lines.AddBy2Points(0.05, -0.05, 0.05, 0.05)
lines.AddBy2Points(0.05, 0.05, -0.05, 0.05)
lines.AddBy2Points(-0.05, 0.05, -0.05, -0.05)
profile.End(0)

# Extrude
models = doc.Models
try:
    models.AddFiniteExtrudedProtrusion(
        NumberOfProfiles=1,
        ProfileArray=(profile,),
        ProfilePlaneSide=1,
        ExtrusionDistance=0.03
    )
except:
    pass

print("Testing fixed set_view method...")
print("="*60)

for view_name in ["Iso", "Top", "Front", "Right"]:
    print(f"\nSetting view to: {view_name}")
    result = view_manager.set_view(view_name)
    print(f"Result: {result}")
    time.sleep(1)

print("\n" + "="*60)
print("View setting works!")

doc_manager.close_document(save=False)
