"""
Unit tests for SketchManager backend methods.

Uses unittest.mock to simulate COM objects so tests run without Solid Edge.
"""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def sketch_mgr():
    """Create SketchManager with mocked dependencies."""
    from solidedge_mcp.backends.sketching import SketchManager
    dm = MagicMock()
    doc = MagicMock()
    dm.get_active_document.return_value = doc
    sm = SketchManager(dm)
    return sm, doc


# ============================================================================
# PROJECT REF PLANE
# ============================================================================

class TestProjectRefPlane:
    def test_success(self, sketch_mgr):
        sm, doc = sketch_mgr
        profile = MagicMock()
        sm.active_profile = profile

        ref_plane = MagicMock()
        ref_planes = MagicMock()
        ref_planes.Count = 3
        ref_planes.Item.return_value = ref_plane
        doc.RefPlanes = ref_planes

        projected = MagicMock()
        profile.ProjectRefPlane.return_value = projected

        result = sm.project_ref_plane(1)
        assert result["status"] == "projected"
        assert result["plane_index"] == 1
        profile.ProjectRefPlane.assert_called_once_with(ref_plane)

    def test_no_active_sketch(self, sketch_mgr):
        sm, doc = sketch_mgr
        sm.active_profile = None

        result = sm.project_ref_plane(1)
        assert "error" in result
        assert "No active sketch" in result["error"]

    def test_invalid_plane_index(self, sketch_mgr):
        sm, doc = sketch_mgr
        profile = MagicMock()
        sm.active_profile = profile

        ref_planes = MagicMock()
        ref_planes.Count = 3
        doc.RefPlanes = ref_planes

        result = sm.project_ref_plane(10)
        assert "error" in result
        assert "plane_index" in result["error"]

    def test_plane_index_zero(self, sketch_mgr):
        sm, doc = sketch_mgr
        profile = MagicMock()
        sm.active_profile = profile

        ref_planes = MagicMock()
        ref_planes.Count = 3
        doc.RefPlanes = ref_planes

        result = sm.project_ref_plane(0)
        assert "error" in result


# ============================================================================
# OFFSET SKETCH 2D
# ============================================================================

class TestOffsetSketch2d:
    def test_success(self, sketch_mgr):
        sm, doc = sketch_mgr
        profile = MagicMock()
        sm.active_profile = profile

        result = sm.offset_sketch_2d(1.0, 0.0, 0.005)
        assert result["status"] == "offset"
        assert result["offset_side_x"] == 1.0
        assert result["offset_side_y"] == 0.0
        assert result["offset_distance"] == 0.005
        profile.Offset2d.assert_called_once_with(1.0, 0.0, 0.005)

    def test_no_active_sketch(self, sketch_mgr):
        sm, doc = sketch_mgr
        sm.active_profile = None

        result = sm.offset_sketch_2d(1.0, 0.0, 0.005)
        assert "error" in result
        assert "No active sketch" in result["error"]

    def test_negative_values(self, sketch_mgr):
        sm, doc = sketch_mgr
        profile = MagicMock()
        sm.active_profile = profile

        result = sm.offset_sketch_2d(-1.0, -1.0, 0.01)
        assert result["status"] == "offset"
        profile.Offset2d.assert_called_once_with(-1.0, -1.0, 0.01)
