# Solid Edge MCP Server Structure Review
Date: 2026-02-13

## 1. Analysis of Current State

### Project Organization
- **Root**: Standard Python project structure (`pyproject.toml`, `src`, `tests`).
- **Source (`src/solidedge_mcp`)**:
    - `server.py`: **Critical Issue**. This file is a monolith of ~4300 lines. It contains:
        - `FastMCP` initialization.
        - Global backend manager instantiation.
        - **All** tool definitions (decorated with `@mcp.tool`).
    - `tools/`: Currently empty.
    - `backends/`: Good modularity. Contains the actual logic (`connection.py`, `documents.py`, `features.py`, etc.).
    - `server.py` acts as a massive wrapper layer around `backends/`.

### Context Consumption
- The monolithic `server.py` is a significant context sink for LLMs.
- Reading the "entry point" loads 4000+ lines of code, most of which is repetitive wrapper definitions.
- Docstrings in `server.py` are verbose and redundant given the backend implementations.

### Framework Capabilities
- Usage of `FastMCP` from `fastmcp` library.
- Verified capabilities via introspection script:
    - `mcp.tool` decorator exists (currently used).
    - `mcp.add_tool` method **exists**. This is key for refactoring. It allows programmatically registering functions as tools without decorating them at definition time, enabling better separation of concerns.

## 2. Refactoring Plan

### Goal
Restructure the server to improve maintainability and reduce context usage for AI assistants.

### Strategy
1.  **Modularize Tool Definitions**:
    - Move tool wrapper functions from `server.py` to dedicated modules in `src/solidedge_mcp/tools/`.
    - Group by function: `connection.py`, `documents.py`, `sketching.py`, etc.
    - These functions will be plain Python functions, importing the necessary backend managers.

2.  **Dynamic Registration**:
    - Create `src/solidedge_mcp/tools/__init__.py`.
    - Implement a `register_tools(mcp)` function that imports the tool modules and calls `mcp.add_tool(func)` for each tool.
    - Update `server.py` to simply initialize `FastMCP` and call `register_tools`.

3.  **Context Optimization**:
    - Simplify docstrings in the new tool wrappers.
    - Rely on concise, descriptive function names and type hints.
    - Remove redundant "Args" and "Returns" sections where they don't add value over the signature.

### Proposed File Structure
```
src/solidedge_mcp/
├── server.py              <-- Thin entry point (< 100 lines)
├── users.py               <-- (Optional/Future)
├── tools/                 <-- NEW: Modular tool definitions
│   ├── __init__.py        <-- Registration logic
│   ├── connection.py
│   ├── documents.py
│   ├── sketching.py
│   ├── features.py
│   ├── assembly.py
│   ├── query.py
│   ├── export.py
│   └── diagnostics.py
└── backends/              <-- EXISTING: Core logic (unchanged)
```

### Verification
- **Unit Tests**: Existing tests in `tests/unit/` verify `backends` logic and should pass without modification.
- **Tool Check**: A script will be needed to verify that all tools are correctly registered on the `FastMCP` server instance after refactoring.
