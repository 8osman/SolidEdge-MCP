"""
Unit tests for ExportManager backend methods.

Tests draft sheet management and assembly drawing views.
Uses unittest.mock to simulate COM objects.
"""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def export_mgr():
    """Create ExportManager with mocked dependencies."""
    from solidedge_mcp.backends.export import ExportManager
    dm = MagicMock()
    doc = MagicMock()
    dm.get_active_document.return_value = doc
    return ExportManager(dm), doc


# ============================================================================
# DRAFT SHEET MANAGEMENT
# ============================================================================

class TestAddDraftSheet:
    def test_success(self, export_mgr):
        em, doc = export_mgr
        sheet = MagicMock()
        sheet.Name = "Sheet 2"

        sheets = MagicMock()
        sheets.Count = 2
        sheets.AddSheet.return_value = sheet
        doc.Sheets = sheets

        result = em.add_draft_sheet()
        assert result["status"] == "added"
        assert result["total_sheets"] == 2
        sheets.AddSheet.assert_called_once()
        sheet.Activate.assert_called_once()

    def test_not_draft(self, export_mgr):
        em, doc = export_mgr
        del doc.Sheets

        result = em.add_draft_sheet()
        assert "error" in result


# ============================================================================
# ASSEMBLY DRAWING VIEW
# ============================================================================

class TestAddAssemblyDrawingView:
    def test_success(self, export_mgr):
        em, doc = export_mgr

        model_link = MagicMock()
        model_links = MagicMock()
        model_links.Count = 1
        model_links.Item.return_value = model_link
        doc.ModelLinks = model_links

        sheet = MagicMock()
        dvs = MagicMock()
        sheet.DrawingViews = dvs
        doc.ActiveSheet = sheet
        doc.Sheets = MagicMock()

        result = em.add_assembly_drawing_view(0.15, 0.15, "Front", 1.0)
        assert result["status"] == "added"
        assert result["orientation"] == "Front"

    def test_not_draft(self, export_mgr):
        em, doc = export_mgr
        del doc.Sheets

        result = em.add_assembly_drawing_view()
        assert "error" in result

    def test_no_model_link(self, export_mgr):
        em, doc = export_mgr
        doc.Sheets = MagicMock()

        model_links = MagicMock()
        model_links.Count = 0
        doc.ModelLinks = model_links

        result = em.add_assembly_drawing_view()
        assert "error" in result

    def test_invalid_orientation(self, export_mgr):
        em, doc = export_mgr
        doc.Sheets = MagicMock()

        model_links = MagicMock()
        model_links.Count = 1
        doc.ModelLinks = model_links

        result = em.add_assembly_drawing_view(orientation="InvalidView")
        assert "error" in result


# ============================================================================
# FLAT DXF EXPORT
# ============================================================================

class TestExportFlatDxf:
    def test_success(self, export_mgr):
        em, doc = export_mgr
        flat_models = MagicMock()
        doc.FlatPatternModels = flat_models

        result = em.export_flat_dxf("C:/output/flat.dxf")
        assert result["status"] == "exported"
        assert result["format"] == "Flat DXF"
        flat_models.SaveAsFlatDXFEx.assert_called_once()

    def test_not_sheet_metal(self, export_mgr):
        em, doc = export_mgr
        del doc.FlatPatternModels

        result = em.export_flat_dxf("C:/output/flat.dxf")
        assert "error" in result

    def test_adds_extension(self, export_mgr):
        em, doc = export_mgr
        flat_models = MagicMock()
        doc.FlatPatternModels = flat_models

        result = em.export_flat_dxf("C:/output/flat")
        assert result["path"] == "C:/output/flat.dxf"


# ============================================================================
# DOCUMENT MANAGEMENT (activate, undo, redo)
# ============================================================================

@pytest.fixture
def doc_mgr():
    """Create DocumentManager with mocked connection."""
    from solidedge_mcp.backends.documents import DocumentManager
    conn = MagicMock()
    app = MagicMock()
    conn.get_application.return_value = app
    dm = DocumentManager(conn)
    return dm, app


class TestActivateDocument:
    def test_by_index(self, doc_mgr):
        dm, app = doc_mgr
        doc = MagicMock()
        doc.Name = "Part1.par"
        doc.FullName = "C:/parts/Part1.par"
        doc.Type = 1

        docs = MagicMock()
        docs.Count = 2
        docs.Item.return_value = doc
        app.Documents = docs

        result = dm.activate_document(0)
        assert result["status"] == "activated"
        assert result["name"] == "Part1.par"
        doc.Activate.assert_called_once()

    def test_by_name(self, doc_mgr):
        dm, app = doc_mgr
        doc1 = MagicMock()
        doc1.Name = "Part1.par"
        doc1.FullName = "C:/Part1.par"
        doc1.Type = 1

        doc2 = MagicMock()
        doc2.Name = "Part2.par"
        doc2.FullName = "C:/Part2.par"
        doc2.Type = 1

        docs = MagicMock()
        docs.Count = 2
        docs.Item.side_effect = lambda i: [None, doc1, doc2][i]
        app.Documents = docs

        result = dm.activate_document("Part2.par")
        assert result["status"] == "activated"
        doc2.Activate.assert_called_once()

    def test_not_found(self, doc_mgr):
        dm, app = doc_mgr
        doc1 = MagicMock()
        doc1.Name = "Part1.par"

        docs = MagicMock()
        docs.Count = 1
        docs.Item.return_value = doc1
        app.Documents = docs

        result = dm.activate_document("Nonexistent.par")
        assert "error" in result

    def test_invalid_index(self, doc_mgr):
        dm, app = doc_mgr
        docs = MagicMock()
        docs.Count = 1
        app.Documents = docs

        result = dm.activate_document(5)
        assert "error" in result


class TestUndo:
    def test_success(self, doc_mgr):
        dm, app = doc_mgr
        doc = MagicMock()
        dm.active_document = doc

        result = dm.undo()
        assert result["status"] == "undone"
        doc.Undo.assert_called_once()


class TestRedo:
    def test_success(self, doc_mgr):
        dm, app = doc_mgr
        doc = MagicMock()
        dm.active_document = doc

        result = dm.redo()
        assert result["status"] == "redone"
        doc.Redo.assert_called_once()
