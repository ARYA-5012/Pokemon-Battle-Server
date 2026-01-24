#!/usr/bin/env python3
"""
Automated test of the interactive battle system without user input.
"""

import asyncio
import sys
import os

# Add the src directory to the path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pokemon_mcp.pokemon_data import pokemon_service
from pokemon_mcp.battle_mechanics import battle_simulator


async def automated_interactive_demo():
    """Automated demonstration of the interactive battle functionality."""
    print("AUTOMATED INTERACTIVE BATTLE DEMO")
    print("============================================================")
    print("Demonstrating what happens when users choose: Pikachu vs Charizard")
    print("============================================================")
    
    try:
        # Simulate user choosing Pikachu and Charizard
        pokemon1_name = "pikachu"
        pokemon2_name = "charizard"
        
        print(f"\nUser chose first Pokemon: {pokemon1_name.title()}")
        print(f"Searching for {pokemon1_name}...")
        
        pokemon1 = await pokemon_service.get_pokemon(pokemon1_name)
        print(f"Found {pokemon1.name}!")
        print(f"   Stats: HP={pokemon1.stats.hp}, ATK={pokemon1.stats.attack}, DEF={pokemon1.stats.defense}")
        print(f"   Types: {[t.name for t in pokemon1.types]}")
        print(f"   Abilities: {[a.name for a in pokemon1.abilities]}")
        
        print(f"\nUser chose second Pokemon: {pokemon2_name.title()}")
        print(f"Searching for {pokemon2_name}...")
        
        pokemon2 = await pokemon_service.get_pokemon(pokemon2_name)
        print(f"Found {pokemon2.name}!")
        print(f"   Stats: HP={pokemon2.stats.hp}, ATK={pokemon2.stats.attack}, DEF={pokemon2.stats.defense}")
        print(f"   Types: {[t.name for t in pokemon2.types]}")
        print(f"   Abilities: {[a.name for a in pokemon2.abilities]}")
        
        # Pre-battle analysis
        print(f"\n PRE-BATTLE ANALYSIS")
        print("=" * 60)
        
        type1 = pokemon1.types[0].name.lower()
        type2 = pokemon2.types[0].name.lower()
        
        effectiveness1vs2 = battle_simulator.get_type_effectiveness(type1, [type2])
        effectiveness2vs1 = battle_simulator.get_type_effectiveness(type2, [type1])
        
        print(f"Type Matchup:")
        print(f"   {pokemon1.name} ({type1.title()}) vs {pokemon2.name} ({type2.title()})")
        print(f"   {pokemon1.name}'s attacks: {effectiveness1vs2}x effectiveness")
        print(f"   {pokemon2.name}'s attacks: {effectiveness2vs1}x effectiveness")
        
        speed_advantage = "Tied" if pokemon1.stats.speed == pokemon2.stats.speed else \
                         pokemon1.name if pokemon1.stats.speed > pokemon2.stats.speed else pokemon2.name
        print(f"Speed Advantage: {speed_advantage}")
        
        # Battle simulation
        print(f"\nBATTLE BEGINS!")
        print("=" * 60)
        
        result = battle_simulator.simulate_battle(pokemon1, pokemon2)
        
        print(f"WINNER: {result.winner}")
        print(f"Loser: {result.loser}")
        print(f"Total Turns: {result.total_turns}")
        print(f"Total Actions: {len(result.actions)}")
        
        print(f"\n DETAILED BATTLE LOG:")
        print("=" * 60)
        
        for action in result.actions:
            turn_indicator = f"[Turn {action.turn}]" if hasattr(action, 'turn') else "[---]"
            print(f"{turn_indicator} {action.message}")
        
        print(f"\nBATTLE SUMMARY:")
        print("=" * 60)
        if result.battle_summary:
            print(result.battle_summary)
        
        print(f"\n Interactive battle system demonstration complete!")
        
    except Exception as e:
        print(f" Demo error: {e}")
    
    finally:
        await pokemon_service.close()


if __name__ == "__main__":
    asyncio.run(automated_interactive_demo())
