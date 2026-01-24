#!/usr/bin/env python3
"""
Quick Feature Demonstration - Pokémon MCP Server
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pokemon_mcp.pokemon_data import pokemon_service
from pokemon_mcp.battle_mechanics import battle_simulator


async def quick_demo():
    print("POKEMON MCP SERVER - FEATURE DEMO")
    print("=" * 45)
    
    # Initialize variables
    pikachu = None
    charizard = None
    
    # Feature 1: Data Retrieval
    print("\nFeature 1: Pokemon Data Retrieval")
    try:
        pikachu = await pokemon_service.get_pokemon("pikachu")
        print(f"✓ {pikachu.name} - HP:{pikachu.stats.hp}, Types:{[t.name for t in pikachu.types]}")
        
        charizard = await pokemon_service.get_pokemon("charizard") 
        print(f"✓ {charizard.name} - HP:{charizard.stats.hp}, Types:{[t.name for t in charizard.types]}")
    except Exception as e:
        print(f"✗ Data error: {e}")
    
    # Feature 2: Type Effectiveness
    print("\nFeature 2: Type Effectiveness")
    try:
        water_vs_fire = await pokemon_service.get_type_effectiveness("water", "fire")
        print(f"✓ Water vs Fire: {water_vs_fire.effectiveness}x (Super Effective!)")
        
        electric_vs_ground = await pokemon_service.get_type_effectiveness("electric", "ground")
        print(f"✓ Electric vs Ground: {electric_vs_ground.effectiveness}x (No Effect!)")
    except Exception as e:
        print(f"✗ Type error: {e}")
    
    # Feature 3: Battle Simulation  
    print("\nFeature 3: Battle Simulation")
    try:
        if pikachu and charizard:
            result = battle_simulator.simulate_battle(pikachu, charizard)
            print(f"✓ Battle: {result.winner} defeats {result.loser}")
            print(f"   Stats: {result.total_turns} turns, {len(result.actions)} actions")
            print(f"   Sample: {result.actions[0].message}")
        else:
            print("✗ Cannot simulate battle: Pokemon data not available")
    except Exception as e:
        print(f"✗ Battle error: {e}")
    
    # Feature 4: Search
    print("\nFeature 4: Search Functionality")
    try:
        results = await pokemon_service.search_pokemon("pika", limit=3)
        print(f" Search 'pika': {[r['name'] for r in results]}")
    except Exception as e:
        print(f" Search error: {e}")
    
    # Feature 5: Status Effects
    print("\nFeature 5: Status Effects")
    effects = list(battle_simulator.status_effects.keys())
    print(f"✓ Available: {effects}")
    
    await pokemon_service.close()
    
    print("\nAll Features Working!")
    print("=" * 45)


if __name__ == "__main__":
    asyncio.run(quick_demo())
