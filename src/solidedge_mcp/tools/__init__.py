from . import (
    assembly,
    connection,
    diagnostics,
    documents,
    export,
    features,
    query,
    sheet_metal,
    sketching,
)


def register_tools(mcp):
    """Register all tools with the MCP server instance."""
    connection.register(mcp)
    documents.register(mcp)
    sketching.register(mcp)
    features.register(mcp)
    assembly.register(mcp)
    sheet_metal.register(mcp)
    query.register(mcp)
    export.register(mcp)
    diagnostics.register(mcp)
