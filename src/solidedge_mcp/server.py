"""Solid Edge MCP Server"""

from fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("Solid Edge MCP Server")


def main():
    """Entry point for the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
