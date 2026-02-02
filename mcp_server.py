from fastmcp import FastMCP
import sqlite3

# MCP Sever instance 
mcp = FastMCP("Tienda de Peliculas")

# Start point
if __name__ == "__main__":
    mcp.run()