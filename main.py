#!/usr/bin/env python3
"""
Pokémon Battle Simulation MCP Server

This is the main entry point for the Pokémon MCP server.
It provides comprehensive Pokémon data and battle simulation capabilities.

Usage:
    python main.py
    uv run main.py
    mcp dev main.py
"""

from src.pokemon_mcp.server import mcp

if __name__ == "__main__":
    mcp.run()
