#!/usr/bin/env python3
"""
Setup script for Pokémon MCP Server.

This script helps set up the environment and install dependencies.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    if sys.version_info < (3, 10):
        print("[ERROR] Python 3.10 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"[SUCCESS] Python {sys.version.split()[0]} is compatible")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    # Try pip first
    if run_command("pip install -r requirements.txt", "Installing with pip"):
        return True
    
    # Try pip3 if pip failed
    if run_command("pip3 install -r requirements.txt", "Installing with pip3"):
        return True
    
    # Try uv if available
    if run_command("uv pip install -r requirements.txt", "Installing with uv"):
        return True
    
    print("[ERROR] Failed to install dependencies with any method")
    print("   Please install manually: pip install -r requirements.txt")
    return False


def test_installation():
    """Test if the installation works."""
    print("Testing installation...")
    
    try:
        # Test imports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from pokemon_mcp.models import Pokemon
        from pokemon_mcp.pokemon_data import pokemon_service
        from pokemon_mcp.battle_mechanics import battle_simulator
        print("[SUCCESS] All imports successful")
        return True
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False


def main():
    """Main setup function."""
    print("Setting up Pokemon MCP Server\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nDependencies installation failed, but you can try running the server anyway")
    
    # Test installation
    if test_installation():
        print("\n[SUCCESS] Setup completed successfully!")
        print("\nYou can now run the server with:")
        print("   python main.py")
        print("   or")
        print("   mcp dev main.py")
    else:
        print("\n[ERROR] Setup completed with errors")
        print("   Please check the error messages above")


if __name__ == "__main__":
    main()
