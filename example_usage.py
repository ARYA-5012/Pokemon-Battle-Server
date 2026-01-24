#!/usr/bin/env python3
"""
Example usage of the Pokémon MCP Server.

This script demonstrates how to use the server's capabilities.
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pokemon_mcp.pokemon_data import pokemon_service
from pokemon_mcp.battle_mechanics import battle_simulator


async def example_pokemon_data():
    """Example of fetching Pokémon data."""
    print(" Example: Fetching Pokémon Data")
    print("=" * 50)
    
    try:
        # Get Pikachu's data
        pikachu = await pokemon_service.get_pokemon("pikachu")
        print(f"Name: {pikachu.name}")
        print(f"ID: {pikachu.id}")
        print(f"Height: {pikachu.height} dm")
        print(f"Weight: {pikachu.weight} hg")
        print(f"Types: {[t.name for t in pikachu.types]}")
        print(f"Stats: HP={pikachu.stats.hp}, Attack={pikachu.stats.attack}, Defense={pikachu.stats.defense}")
        print(f"Abilities: {[a.name for a in pikachu.abilities]}")
        print(f"Sample moves: {[m.name for m in pikachu.moves[:5]]}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")


async def example_battle_simulation():
    """Example of battle simulation."""
    print(" Example: Battle Simulation")
    print("=" * 50)
    
    try:
        # Get two Pokémon
        pikachu = await pokemon_service.get_pokemon("pikachu")
        charizard = await pokemon_service.get_pokemon("charizard")
        
        print(f"Battle: {pikachu.name} vs {charizard.name}")
        print(f"{pikachu.name} - HP: {pikachu.stats.hp}, Speed: {pikachu.stats.speed}")
        print(f"{charizard.name} - HP: {charizard.stats.hp}, Speed: {charizard.stats.speed}")
        print()
        
        # Simulate battle
        result = battle_simulator.simulate_battle(pikachu, charizard)
        
        print(f" Winner: {result.winner}")
        print(f" Loser: {result.loser}")
        print(f" Total turns: {result.total_turns}")
        print()
        
        print("Battle log (first 10 actions):")
        for i, action in enumerate(result.actions[:10]):
            print(f"  {i+1}. {action.message}")
        
        if len(result.actions) > 10:
            print(f"  ... and {len(result.actions) - 10} more actions")
        print()
        
    except Exception as e:
        print(f"Error: {e}")


async def example_type_effectiveness():
    """Example of type effectiveness."""
    print(" Example: Type Effectiveness")
    print("=" * 50)
    
    try:
        # Test different type matchups
        matchups = [
            ("water", "fire"),
            ("fire", "grass"),
            ("electric", "water"),
            ("electric", "ground"),
            ("fighting", "normal"),
            ("ghost", "normal")
        ]
        
        for attacking, defending in matchups:
            effectiveness = await pokemon_service.get_type_effectiveness(attacking, defending)
            multiplier = effectiveness.effectiveness
            
            if multiplier >= 2.0:
                result_text = "Super effective!"
            elif multiplier <= 0.5:
                result_text = "Not very effective..."
            elif multiplier == 0.0:
                result_text = "No effect!"
            else:
                result_text = "Normal effectiveness"
            
            print(f"{attacking.title()} vs {defending.title()}: {multiplier}x damage - {result_text}")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}")


async def example_search():
    """Example of Pokémon search."""
    print(" Example: Pokémon Search")
    print("=" * 50)
    
    try:
        # Search for Pokémon with "char" in the name
        results = await pokemon_service.search_pokemon("char", limit=5)
        print(f"Search results for 'char':")
        for result in results:
            print(f"  - {result['name']}")
        print()
        
        # Search for Pokémon with "pika" in the name
        results = await pokemon_service.search_pokemon("pika", limit=3)
        print(f"Search results for 'pika':")
        for result in results:
            print(f"  - {result['name']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")


async def main():
    """Run all examples."""
    print(" Pokémon MCP Server - Example Usage")
    print("=" * 60)
    print()
    
    # Run examples
    await example_pokemon_data()
    await example_battle_simulation()
    await example_type_effectiveness()
    await example_search()
    
    # Cleanup
    await pokemon_service.close()
    
    print(" Examples completed!")
    print("\nTo use the MCP server with AI models:")
    print("1. Run: python main.py")
    print("2. Or: mcp dev main.py")
    print("3. Connect your AI model to the server")


if __name__ == "__main__":
    asyncio.run(main())
