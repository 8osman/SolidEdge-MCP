# Solid Edge MCP Server

AI-assisted CAD design through the [Model Context Protocol](https://modelcontextprotocol.io). Create, analyze, modify, and export Solid Edge models — all from your AI assistant.

## What It Does

This MCP server gives AI assistants (Claude, etc.) access to Solid Edge CAD workflows:

- **Connect to Solid Edge** application via COM automation
- **Create and manage** parts and assemblies
- **Sketch 2D geometry** - lines, circles, arcs, rectangles, polygons
- **Create 3D features** - extrude, revolve, sweep, loft
- **Query and analyze** models - dimensions, mass properties, feature trees
- **Export** models to various formats (STEP, STL, IGES, PDF, DXF)
- **View control** - set viewpoints, zoom, fit

## Quick Start

### Install

```bash
# Requires Python 3.11+ and Windows (Solid Edge is Windows-only)
uv sync --all-extras
```

### Configure Your AI Client

Add to your MCP client configuration (e.g. Claude Desktop `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "solidedge-mcp": {
      "command": "uv",
      "args": ["--directory", "C:/path/to/SolidEdge_MCP", "run", "solidedge-mcp"]
    }
  }
}
```

### Run Standalone

```bash
uv run solidedge-mcp
```

## Architecture

### COM Automation Backend

The server communicates with Solid Edge through Windows COM automation (pywin32):

- **Connection management** - Connect to running instance or start new one
- **Document handling** - Create, open, save, close parts and assemblies
- **Sketching** - 2D profile creation on reference planes
- **Features** - 3D modeling operations (extrude, revolve, etc.)
- **Query** - Extract geometry, dimensions, properties
- **Export** - Convert models to standard CAD formats

### Package Layout

```
src/solidedge_mcp/
├── server.py           # FastMCP server entry point
├── backends/           # COM automation implementations
│   ├── connection.py   # Application connection management
│   ├── documents.py    # Document operations
│   ├── sketching.py    # 2D sketch creation
│   ├── features.py     # 3D feature operations
│   ├── assembly.py     # Assembly operations
│   ├── query.py        # Model interrogation
│   └── export.py       # Export operations
├── tools/              # MCP tools (pending implementation)
├── resources/          # MCP resources (pending implementation)
├── prompts/            # MCP prompt templates (pending implementation)
└── session/            # Session/undo management (pending implementation)
```

### Three-Pillar MCP Design

Following the MCP specification, the server will expose:

- **Tools**: Actions that create/modify models (create sketch, extrude, place component)
- **Resources**: Read-only model data (feature list, component tree, mass properties)
- **Prompts**: Conversation templates (design review, manufacturability check)

## Requirements

- **Python 3.11+**
- **Windows** (Solid Edge is Windows-only)
- **Solid Edge** installed and licensed
- **pywin32** for COM automation

## Development

```bash
# Install with dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Lint and format
uv run ruff check .
uv run ruff format .

# Type check
uv run mypy src/
```

## License

MIT
