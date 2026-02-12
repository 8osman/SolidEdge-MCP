#!/usr/bin/env python
"""Test ApplyNamedView method for setting view orientation"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from solidedge_mcp.backends.connection import SolidEdgeConnection
from solidedge_mcp.backends.documents import DocumentManager
import time

connection = SolidEdgeConnection()
connection.connect(start_if_needed=True)
doc_manager = DocumentManager(connection)

# Create a simple part so we have something to view
doc_manager.create_part()
doc = doc_manager.get_active_document()

# Create a simple box sketch
ref_planes = doc.RefPlanes
ref_plane = ref_planes.Item(1)  # Top plane
profile_sets = doc.ProfileSets
profile_set = profile_sets.Add()
profiles = profile_set.Profiles
profile = profiles.Add(ref_plane)

lines = profile.Lines2d
lines.AddBy2Points(-0.05, -0.05, 0.05, -0.05)
lines.AddBy2Points(0.05, -0.05, 0.05, 0.05)
lines.AddBy2Points(0.05, 0.05, -0.05, 0.05)
lines.AddBy2Points(-0.05, 0.05, -0.05, -0.05)

profile.End(0)

# Extrude it
models = doc.Models
try:
    model = models.AddFiniteExtrudedProtrusion(
        NumberOfProfiles=1,
        ProfileArray=(profile,),
        ProfilePlaneSide=1,  # igRight
        ExtrusionDistance=0.03
    )
    print("Created test geometry")
except Exception as e:
    print(f"Note: Extrude failed but continuing with view tests: {e}")

# Get view object
app = connection.application
window = app.ActiveWindow
view = window.View

print("=" * 70)
print("Testing ApplyNamedView(Name)")
print("=" * 70)
print("Signature: ApplyNamedView(Name)")

# Import constants
try:
    from win32com.client import constants
    has_constants = True
except:
    has_constants = False

# Test 1: String names
view_names = ["Iso", "Top", "Front", "Right", "Bottom", "Back", "Left"]

for view_name in view_names:
    print(f"\n[Test] ApplyNamedView('{view_name}')")
    try:
        result = view.ApplyNamedView(view_name)
        print(f"SUCCESS! Result: {result}")
        time.sleep(0.5)  # Pause to see the view change
    except Exception as e:
        print(f"Failed: {e}")

# Test 2: Try with constants if available
if has_constants:
    print("\n" + "-" * 70)
    print("Testing with constants")
    print("-" * 70)

    constant_views = [
        ("seIsoView", "Iso"),
        ("seTopView", "Top"),
        ("seFrontView", "Front"),
    ]

    for const_name, desc in constant_views:
        print(f"\n[Test] ApplyNamedView(ViewOrientationConstants.{const_name})")
        try:
            const_value = getattr(constants, f"ViewOrientationConstants.{const_name}", None)
            if const_value is None:
                # Try without the prefix
                const_value = getattr(constants, const_name, None)

            if const_value is not None:
                result = view.ApplyNamedView(const_value)
                print(f"SUCCESS! Result: {result}")
                time.sleep(0.5)
            else:
                print(f"Constant not found: {const_name}")
        except Exception as e:
            print(f"Failed: {e}")

# Test 3: Try numeric values (constants are typically integers)
print("\n" + "-" * 70)
print("Testing with numeric values")
print("-" * 70)

for i in range(1, 8):
    print(f"\n[Test] ApplyNamedView({i})")
    try:
        result = view.ApplyNamedView(i)
        print(f"SUCCESS! Value {i} worked. Result: {result}")
        time.sleep(0.5)
    except Exception as e:
        print(f"Failed: {e}")

print("\n" + "=" * 70)
print("Testing complete")
print("=" * 70)

doc_manager.close_document(save=False)
