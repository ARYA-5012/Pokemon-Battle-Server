#!/usr/bin/env python3
"""
Quick Battle Tournament Demonstration
"""

import asyncio
import sys
import os
import time

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pokemon_mcp.pokemon_data import pokemon_service
from pokemon_mcp.battle_mechanics import battle_simulator


async def tournament_demo():
    """Run a quick tournament between popular Pokémon."""
    print("POKEMON BATTLE TOURNAMENT")
    print("=" * 50)
    
    contestants = ["pikachu", "charizard", "blastoise", "venusaur"]
    results = []
    
    print("Tournament Bracket:")
    for i in range(0, len(contestants), 2):
        pokemon1_name = contestants[i]
        pokemon2_name = contestants[i+1] if i+1 < len(contestants) else contestants[0]
        
        try:
            print(f"\nMATCH: {pokemon1_name.title()} vs {pokemon2_name.title()}")
            
            # Get Pokémon
            pokemon1 = await pokemon_service.get_pokemon(pokemon1_name)
            pokemon2 = await pokemon_service.get_pokemon(pokemon2_name)
            
            # Quick battle
            start_time = time.time()
            result = battle_simulator.simulate_battle(pokemon1, pokemon2)
            battle_time = time.time() - start_time
            
            print(f"Winner: {result.winner}")
            print(f"Battle time: {battle_time:.3f}s")
            print(f"Actions: {len(result.actions)} in {result.total_turns} turns")
            
            results.append({
                'winner': result.winner,
                'loser': result.loser,
                'turns': result.total_turns,
                'time': battle_time
            })
            
        except Exception as e:
            print(f"Match error: {e}")
    
    print(f"\nTournament Results:")
    for i, result in enumerate(results, 1):
        print(f"   Match {i}: {result['winner']} defeated {result['loser']} ({result['turns']} turns)")
    
    await pokemon_service.close()
    print("\nTournament complete!")


if __name__ == "__main__":
    asyncio.run(tournament_demo())
