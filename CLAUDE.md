# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Solid Edge MCP (Model Context Protocol) server for AI-assisted CAD design. Windows-only, built on FastMCP and pywin32 COM automation. Licensed MIT.

The goal is to provide AI assistants with full access to Solid Edge CAD workflows: **connect → create → sketch → feature → query → export** with session management and undo/rollback support.

## Commands

```bash
# Install all dependencies (including dev)
uv sync --all-extras

# Run the MCP server (stdio transport)
uv run solidedge-mcp

# Run tests
uv run pytest
uv run pytest tests/unit/test_foo.py::test_bar  # single test

# Lint and format
uv run ruff check .
uv run ruff format .

# Type check
uv run mypy src/
```

## Architecture

### COM Automation Backend

Unlike KiCad (which uses file parsing), Solid Edge automation requires Windows COM through pywin32. The server communicates with a running Solid Edge instance via COM interfaces:

- **Connection layer** (`backends/connection.py`): Manages GetActiveObject/Dispatch, early/late binding
- **Document layer** (`backends/documents.py`): Create/open/save parts, assemblies, drafts
- **Sketching layer** (`backends/sketching.py`): 2D profile creation (lines, circles, arcs, rectangles, polygons)
- **Feature layer** (`backends/features.py`): 3D operations (extrude, revolve, sweep, loft, holes, fillets)
- **Assembly layer** (`backends/assembly.py`): Component placement, constraints, patterns
- **Query layer** (`backends/query.py`): Extract geometry, mass properties, feature trees
- **Export layer** (`backends/export.py`): Convert to STEP, STL, IGES, PDF, DXF

### Package Layout

```
src/solidedge_mcp/
├── server.py              # FastMCP server entry point
├── backends/              # COM automation implementations
│   ├── connection.py      # Application connection (GetActiveObject/Dispatch)
│   ├── documents.py       # Document create/open/save/close
│   ├── sketching.py       # 2D sketch profiles
│   ├── features.py        # 3D feature operations
│   ├── assembly.py        # Assembly operations
│   ├── query.py           # Model interrogation
│   ├── export.py          # Export to standard formats
│   └── constants.py       # Solid Edge API constants
├── tools/                 # MCP tool wrappers (pending)
├── resources/             # MCP Resources (read-only state) (pending)
├── prompts/               # MCP Prompt templates (pending)
└── session/               # Session/undo management (pending)
```

### Current State

**Implemented**: COM backend layer with connection, documents, sketching, features, assembly, query, and export operations. These are pure Python modules using pywin32.

**Pending**: MCP tool registration, resource providers, prompt templates, and session management. The FastMCP server exists but does not yet expose the backend operations as MCP tools.

### Three-Pillar MCP Design

Following the MCP spec, the server will expose:

- **Tools**: Actions that create/modify models (connect, create_sketch, extrude, place_component, export)
- **Resources**: Read-only model data (feature list, component tree, mass properties, document info)
- **Prompts**: Conversation templates (design review, manufacturability check, modeling guidance)

### Tool Registration Pattern

Each backend operation should be wrapped as an MCP tool. For example:

```python
@mcp.tool()
def connect_to_solidedge(start_if_needed: bool = True) -> dict:
    """Connect to Solid Edge application (start if needed)"""
    connection = SolidEdgeConnection()
    return connection.connect(start_if_needed)
```

Tools should return typed dictionaries with consistent error handling.

## Solid Edge-Specific Notes

- **Windows-only**: Solid Edge COM automation requires Windows. pywin32 does not work on Linux/macOS.
- **COM binding**: Use `gencache.EnsureDispatch()` for early binding (type hints, IntelliSense) or `Dispatch()` for late binding (more compatible but slower).
- **Active document pattern**: Most operations require an active document. The DocumentManager tracks `self.active_document`.
- **Sketch-then-feature workflow**: 3D features (extrude, revolve) require a closed 2D sketch profile. The typical flow is: `create_sketch() → draw_*() → close_sketch() → create_extrude()`.
- **COM exception handling**: COM operations can raise `pywintypes.com_error`. Always wrap in try/except with traceback for debugging.
- **Reference planes**: Solid Edge has 3 default planes (Top/XZ, Front/XY, Right/YZ). Sketches are created on these planes.
- **Units**: Solid Edge internal units are meters. Convert mm to meters by dividing by 1000.
- **Feature tree**: Features are stored in `Document.Models` collection. Each feature has properties like Name, Type, Status (normal/suppressed).

## Development Workflow

When adding new capabilities:

1. **Backend first**: Implement the raw COM operation in the appropriate `backends/` module
2. **Test manually**: Use `python -i` to import and test the backend function directly
3. **Wrap as tool**: Add `@mcp.tool()` decorator in `server.py` or `tools/` module
4. **Add tests**: Write pytest tests in `tests/unit/` or `tests/integration/`
5. **Update docs**: Add to README.md tool list if user-facing

## Testing Notes

- **Unit tests**: Mock COM objects to test logic without Solid Edge installed
- **Integration tests**: Require Solid Edge running on Windows. Mark with `@pytest.mark.integration`
- **CI limitations**: GitHub Actions runners do not have Solid Edge. Integration tests run locally only.

## Comparison to KiCad-MCP

| Aspect | KiCad-MCP | Solid Edge MCP |
|---|---|---|
| Platform | Cross-platform (Python, file I/O) | Windows-only (COM automation) |
| Read operations | S-expr parser, no KiCad needed | COM, requires Solid Edge running |
| Write operations | File mutation + kicad-cli | COM API calls |
| Session model | File-based undo/rollback | COM undo stack (pending) |
| Tool routing | 2-tier (8 direct, 67 routed) | TBD (likely simpler, fewer tools) |
| Primary use case | PCB design (board, schematic) | CAD modeling (parts, assemblies) |
