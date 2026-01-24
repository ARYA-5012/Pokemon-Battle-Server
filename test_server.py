#!/usr/bin/env python3
"""
Test script for the Pokémon MCP Server.

This script tests the basic functionality of the server.
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pokemon_mcp.pokemon_data import pokemon_service
from pokemon_mcp.battle_mechanics import battle_simulator


async def test_pokemon_data():
    """Test Pokémon data fetching."""
    print("Testing Pokémon data fetching...")
    
    try:
        # Test getting Pikachu
        pikachu = await pokemon_service.get_pokemon("pikachu")
        print(f"Successfully fetched {pikachu.name} (ID: {pikachu.id})")
        print(f"   Types: {[t.name for t in pikachu.types]}")
        print(f"   HP: {pikachu.stats.hp}")
        
        # Test getting Charizard
        charizard = await pokemon_service.get_pokemon("charizard")
        print(f"Successfully fetched {charizard.name} (ID: {charizard.id})")
        print(f"   Types: {[t.name for t in charizard.types]}")
        print(f"   HP: {charizard.stats.hp}")
        
        # Test search
        search_results = await pokemon_service.search_pokemon("pika", limit=5)
        print(f"Search for 'pika' found {len(search_results)} results")
        for result in search_results:
            print(f"   - {result['name']}")
        
        return pikachu, charizard
        
    except Exception as e:
        print(f"Error testing Pokémon data: {e}")
        return None, None


async def test_battle_simulation(pikachu, charizard):
    """Test battle simulation."""
    print("\nTesting battle simulation...")
    
    try:
        if pikachu and charizard:
            result = battle_simulator.simulate_battle(pikachu, charizard)
            print(f"Battle completed!")
            print(f"   Winner: {result.winner}")
            print(f"   Loser: {result.loser}")
            print(f"   Total turns: {result.total_turns}")
            print(f"   Total actions: {len(result.actions)}")
            
            # Show first few actions
            print("\n   First 5 actions:")
            for i, action in enumerate(result.actions[:5]):
                print(f"   {i+1}. {action.message}")
            
            if len(result.actions) > 5:
                print(f"   ... and {len(result.actions) - 5} more actions")
        else:
            print("Cannot test battle - Pokémon data not available")
            
    except Exception as e:
        print(f"Error testing battle simulation: {e}")


async def test_type_effectiveness():
    """Test type effectiveness calculations."""
    print("\nTesting type effectiveness...")
    
    try:
        # Test Water vs Fire
        effectiveness = await pokemon_service.get_type_effectiveness("water", "fire")
        print(f"Water vs Fire: {effectiveness.effectiveness}x damage")
        
        # Test Fire vs Water
        effectiveness = await pokemon_service.get_type_effectiveness("fire", "water")
        print(f"Fire vs Water: {effectiveness.effectiveness}x damage")
        
        # Test Electric vs Ground
        effectiveness = await pokemon_service.get_type_effectiveness("electric", "ground")
        print(f"Electric vs Ground: {effectiveness.effectiveness}x damage")
        
    except Exception as e:
        print(f"Error testing type effectiveness: {e}")


async def main():
    """Run all tests."""
    print("Starting Pokemon MCP Server Tests\n")
    
    # Test Pokémon data
    pikachu, charizard = await test_pokemon_data()
    
    # Test battle simulation
    await test_battle_simulation(pikachu, charizard)
    
    # Test type effectiveness
    await test_type_effectiveness()
    
    # Cleanup
    await pokemon_service.close()
    
    print("\nTests completed!")


if __name__ == "__main__":
    asyncio.run(main())
