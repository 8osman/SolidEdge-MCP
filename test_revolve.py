#!/usr/bin/env python
"""Quick test for revolve fix"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from solidedge_mcp.backends.connection import SolidEdgeConnection
from solidedge_mcp.backends.documents import DocumentManager
from solidedge_mcp.backends.sketching import SketchManager
from solidedge_mcp.backends.features import FeatureManager

connection = SolidEdgeConnection()
connection.connect(start_if_needed=True)
doc_manager = DocumentManager(connection)
sketch_manager = SketchManager(doc_manager)
feature_manager = FeatureManager(doc_manager, sketch_manager)

# Create part
doc_manager.create_part()

# Create sketch for revolve
sketch_manager.create_sketch("Front")
sketch_manager.draw_line(0, 0, 0.02, 0)
sketch_manager.draw_line(0.02, 0, 0.02, 0.04)
sketch_manager.draw_line(0.02, 0.04, 0, 0.04)
sketch_manager.draw_line(0, 0.04, 0, 0)
sketch_manager.close_sketch()

# Test revolve
print("Testing revolve...")
result = feature_manager.create_revolve(360, "Add")
if "error" in result:
    print(f"FAILED: {result['error']}")
else:
    print(f"SUCCESS: {result}")

# Clean up
doc_manager.close_document(save=False)
