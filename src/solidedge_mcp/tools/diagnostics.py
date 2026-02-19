"""Diagnostic tools for Solid Edge MCP."""

from solidedge_mcp.backends.diagnostics import diagnose_se_ai as _diagnose_se_ai
from solidedge_mcp.managers import connection, diagnose_document, doc_manager


def diagnose_api() -> dict:
    """Run diagnostic checks on the Solid Edge API connection and active document."""
    # Assuming diagnose_document takes the active document object
    doc = doc_manager.get_active_document()
    return diagnose_document(doc)


def diagnose_se_ai() -> dict:
    """
    Probe Solid Edge 2026's Application object for any COM-accessible AI
    assistant interface.

    Checks for AI-related attributes (ai, assistant, copilot, nlp, chat,
    prompt, ask, gpt, llm) on the Application, probes specific candidate
    entry-point names (AIAssistant, SEAssistant, CopilotPane, AskSolidEdge,
    etc.), and inspects CommandBarManager / DockableWindows for AI pane
    listings.

    If any AI object is found, its dir() and string-accepting methods are
    returned so we can see whether it exposes a natural-language command
    interface.

    Returns a dict with app_ai_keyword_attrs, candidate_probes,
    bar_manager_probes, and start_command_note.
    """
    try:
        app = connection.get_application()
        return _diagnose_se_ai(app)
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


def register(mcp):
    """Register diagnostic tools with the MCP server."""
    mcp.tool()(diagnose_api)
    mcp.tool()(diagnose_se_ai)
