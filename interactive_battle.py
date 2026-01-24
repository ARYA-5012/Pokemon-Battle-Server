#!/usr/bin/env python3
"""
Interactive Pokémon Battle System

This script allows users to interactively choose two Pokémon and watch a detailed battle simulation.
It provides comprehensive battle logs showing each action and outcome.
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pokemon_mcp.pokemon_data import pokemon_service
from pokemon_mcp.battle_mechanics import battle_simulator


def get_user_input(prompt: str) -> str:
    """Get user input with error handling."""
    try:
        return input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n\nExiting battle system...")
        sys.exit(0)


async def get_pokemon_with_retry(pokemon_name: str, max_retries: int = 3):
    """Get Pokemon data with retry logic for invalid names."""
    for attempt in range(max_retries):
        try:
            pokemon = await pokemon_service.get_pokemon(pokemon_name)
            return pokemon
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Could not find '{pokemon_name}'. Error: {e}")
                
                # Suggest similar Pokemon if possible
                try:
                    search_results = await pokemon_service.search_pokemon(pokemon_name[:4], limit=5)
                    if search_results:
                        print("Did you mean one of these?")
                        for result in search_results:
                            print(f"   - {result['name']}")
                except:
                    pass
                
                pokemon_name = get_user_input(f"Please enter a valid Pokémon name (attempt {attempt + 2}/{max_retries}): ")
            else:
                raise Exception(f"Could not find Pokemon '{pokemon_name}' after {max_retries} attempts")
    
    return None


def print_pokemon_info(pokemon):
    """Print detailed Pokemon information."""
    print(f"\n{pokemon.name.upper()} (#{pokemon.id})")
    print(f"   Types: {', '.join([t.name for t in pokemon.types])}")
    print(f"   Base Stats:")
    print(f"      HP: {pokemon.stats.hp}")
    print(f"      Attack: {pokemon.stats.attack}")
    print(f"      Defense: {pokemon.stats.defense}")
    print(f"      Special Attack: {pokemon.stats.special_attack}")
    print(f"      Special Defense: {pokemon.stats.special_defense}")
    print(f"      Speed: {pokemon.stats.speed}")
    total_stats = sum([pokemon.stats.hp, pokemon.stats.attack, pokemon.stats.defense, 
                      pokemon.stats.special_attack, pokemon.stats.special_defense, pokemon.stats.speed])
    print(f"   Total Base Stats: {total_stats}")
    print(f"   Abilities: {', '.join([a.name for a in pokemon.abilities[:2]])}")


def print_detailed_battle_log(battle_result):
    """Print comprehensive battle log with detailed formatting."""
    print("\n" + "=" * 80)
    print("DETAILED BATTLE RESULTS")
    print("=" * 80)
    
    print(f"\nWINNER: {battle_result.winner}")
    print(f"LOSER: {battle_result.loser}")
    print(f"TOTAL TURNS: {battle_result.total_turns}")
    print(f"TOTAL ACTIONS: {len(battle_result.actions)}")
    
    print("\n" + "=" * 80)
    print("ACTION-BY-ACTION BATTLE LOG")
    print("=" * 80)
    
    for i, action in enumerate(battle_result.actions):
        print(f"\nTurn {action.turn}: {action.message}")
        
        if action.damage and action.damage > 0:
            print(f"   Damage dealt: {action.damage} HP")
        
        if action.status_applied:
            print(f"   Status effect applied: {action.status_applied}")
        
        if "fainted" in action.message.lower():
            print(f"   {action.actor} has been defeated!")
            break
    
    print(f"\n{battle_result.battle_summary}")
    print("=" * 80)


async def run_type_analysis(pokemon1, pokemon2):
    """Analyze type effectiveness between the two Pokemon."""
    print("\nTYPE EFFECTIVENESS ANALYSIS")
    print("-" * 50)
    
    try:
        # Get primary types
        type1 = pokemon1.types[0].name.lower() if pokemon1.types else "normal"
        type2 = pokemon2.types[0].name.lower() if pokemon2.types else "normal"
        
        # Check type effectiveness both ways
        effectiveness_1_vs_2 = await pokemon_service.get_type_effectiveness(type1, type2)
        effectiveness_2_vs_1 = await pokemon_service.get_type_effectiveness(type2, type1)
        
        print(f"{pokemon1.name}'s {type1.title()} vs {pokemon2.name}'s {type2.title()}: {effectiveness_1_vs_2.effectiveness}x")
        if effectiveness_1_vs_2.effectiveness > 1.0:
            print(f"   {pokemon1.name} has type advantage!")
        elif effectiveness_1_vs_2.effectiveness < 1.0:
            print(f"   {pokemon2.name} resists {pokemon1.name}'s attacks!")
        
        print(f"{pokemon2.name}'s {type2.title()} vs {pokemon1.name}'s {type1.title()}: {effectiveness_2_vs_1.effectiveness}x")
        if effectiveness_2_vs_1.effectiveness > 1.0:
            print(f"   {pokemon2.name} has type advantage!")
        elif effectiveness_2_vs_1.effectiveness < 1.0:
            print(f"   {pokemon1.name} resists {pokemon2.name}'s attacks!")
            
    except Exception as e:
        print(f"Could not analyze type effectiveness: {e}")


async def main():
    """Main interactive battle system."""
    print("INTERACTIVE POKEMON BATTLE SYSTEM")
    print("=" * 60)
    print("Welcome to the Pokemon Battle Arena!")
    print("Choose two Pokemon to battle and watch the detailed combat unfold.")
    print("=" * 60)
    
    try:
        # Get first Pokemon
        print("\nChoose your first Pokemon:")
        pokemon1_name = get_user_input("Enter first Pokemon name: ")
        print(f"Searching for {pokemon1_name}...")
        
        pokemon1 = await get_pokemon_with_retry(pokemon1_name)
        if not pokemon1:
            print("Could not retrieve first Pokemon. Exiting.")
            return
            
        print_pokemon_info(pokemon1)
        
        # Get second Pokemon
        print("\nChoose your second Pokemon:")
        pokemon2_name = get_user_input("Enter second Pokemon name: ")
        print(f"Searching for {pokemon2_name}...")
        
        pokemon2 = await get_pokemon_with_retry(pokemon2_name)
        if not pokemon2:
            print("Could not retrieve second Pokemon. Exiting.")
            return
            
        print_pokemon_info(pokemon2)
        
        # Run type analysis
        await run_type_analysis(pokemon1, pokemon2)
        
        # Confirm battle
        print(f"\nBATTLE PREVIEW: {pokemon1.name.upper()} vs {pokemon2.name.upper()}")
        confirm = get_user_input("Start the battle? (y/n): ")
        
        if confirm.lower() not in ['y', 'yes']:
            print("Battle cancelled.")
            return
        
        # Start battle simulation
        print(f"\nBATTLE BEGINS!")
        print(f"{pokemon1.name} (HP: {pokemon1.stats.hp}) vs {pokemon2.name} (HP: {pokemon2.stats.hp})")
        print("Simulating battle...")
        
        # Simulate the battle
        battle_result = battle_simulator.simulate_battle(pokemon1, pokemon2)
        
        # Display detailed results
        print_detailed_battle_log(battle_result)
        
        # Ask if user wants another battle
        print("\nWant to battle again?")
        again = get_user_input("Start another battle? (y/n): ")
        
        if again.lower() in ['y', 'yes']:
            await main()  # Recursive call for another battle
        else:
            print("\nThank you for using the Pokemon Battle System!")
            print("May the best trainer win!")
        
    except KeyboardInterrupt:
        print("\n\nBattle interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred during battle: {e}")
    finally:
        # Cleanup
        await pokemon_service.close()


if __name__ == "__main__":
    asyncio.run(main())
