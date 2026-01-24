"""
MCP Server Logic for Pokémon Data and Battle Simulation

This module contains:
1. Pokémon Data Resource - Fetches real-time Pokémon data from PokeAPI
2. Battle Simulation Tool - Simulates turn-based battles between two Pokémon
"""

import requests
import random
from typing import Dict, List, Any, Optional


# ============================================================================
# POKÉMON DATA RESOURCE (pokemon://data)
# ============================================================================

def get_pokemon_data(name: str) -> Dict[str, Any]:
    """
    Fetch comprehensive Pokémon data from PokeAPI.
    
    This function simulates an MCP Resource (pokemon://data).
    
    Args:
        name: Pokémon name (case-insensitive)
    
    Returns:
        dict: Structured Pokémon information including:
            - Base statistics (HP, Attack, Defense, Sp.Atk, Sp.Def, Speed)
            - Types (Fire, Water, Grass, etc.)
            - Abilities
            - Limited move set (first 5 moves)
    """
    try:
        # Normalize input
        pokemon_name = name.lower().strip()
        
        # Fetch from PokeAPI
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return {"error": f"Pokémon '{name}' not found"}
        
        response.raise_for_status()
        data = response.json()
        
        # Extract base stats
        stats = {}
        stat_mapping = {
            "hp": "HP",
            "attack": "Attack",
            "defense": "Defense",
            "special-attack": "Sp. Attack",
            "special-defense": "Sp. Defense",
            "speed": "Speed"
        }
        for stat in data["stats"]:
            stat_name = stat["stat"]["name"]
            if stat_name in stat_mapping:
                stats[stat_mapping[stat_name]] = stat["base_stat"]
        
        # Extract types
        types = [t["type"]["name"].capitalize() for t in data["types"]]
        
        # Extract abilities
        abilities = [
            {
                "name": a["ability"]["name"].replace("-", " ").title(),
                "hidden": a["is_hidden"]
            }
            for a in data["abilities"]
        ]
        
        # Extract limited move set (first 5)
        moves = [
            m["move"]["name"].replace("-", " ").title()
            for m in data["moves"][:5]
        ]
        
        # Build structured response
        return {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "types": types,
            "stats": stats,
            "abilities": abilities,
            "moves": moves,
            "height": data["height"] / 10,  # Convert to meters
            "weight": data["weight"] / 10,  # Convert to kg
            "sprite": data["sprites"]["front_default"]
        }
        
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch data: {str(e)}"}


# ============================================================================
# BATTLE SIMULATION TOOL
# ============================================================================

# Type effectiveness chart (simplified)
TYPE_EFFECTIVENESS = {
    "Fire": {"Grass": 2.0, "Water": 0.5, "Fire": 0.5, "Ice": 2.0, "Bug": 2.0, "Steel": 2.0},
    "Water": {"Fire": 2.0, "Grass": 0.5, "Water": 0.5, "Ground": 2.0, "Rock": 2.0},
    "Grass": {"Water": 2.0, "Fire": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0},
    "Electric": {"Water": 2.0, "Grass": 0.5, "Electric": 0.5, "Flying": 2.0, "Ground": 0.0},
    "Ground": {"Fire": 2.0, "Electric": 2.0, "Grass": 0.5, "Flying": 0.0, "Rock": 2.0, "Steel": 2.0},
    "Rock": {"Fire": 2.0, "Ice": 2.0, "Flying": 2.0, "Bug": 2.0, "Grass": 0.5, "Fighting": 0.5},
    "Flying": {"Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Electric": 0.5, "Rock": 0.5},
    "Psychic": {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0},
    "Ice": {"Grass": 2.0, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Fire": 0.5, "Water": 0.5},
    "Dragon": {"Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0},
    "Normal": {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
    "Fighting": {"Normal": 2.0, "Ice": 2.0, "Rock": 2.0, "Dark": 2.0, "Steel": 2.0, "Flying": 0.5, "Psychic": 0.5, "Ghost": 0.0},
    "Poison": {"Grass": 2.0, "Fairy": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0},
    "Bug": {"Grass": 2.0, "Psychic": 2.0, "Dark": 2.0, "Fire": 0.5, "Fighting": 0.5, "Flying": 0.5, "Ghost": 0.5},
    "Ghost": {"Psychic": 2.0, "Ghost": 2.0, "Normal": 0.0, "Dark": 0.5},
    "Steel": {"Ice": 2.0, "Rock": 2.0, "Fairy": 2.0, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5},
    "Fairy": {"Fighting": 2.0, "Dragon": 2.0, "Dark": 2.0, "Fire": 0.5, "Poison": 0.5, "Steel": 0.5},
    "Dark": {"Psychic": 2.0, "Ghost": 2.0, "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5}
}


def get_type_effectiveness(attacker_type: str, defender_types: List[str]) -> float:
    """Calculate type effectiveness multiplier."""
    multiplier = 1.0
    
    if attacker_type in TYPE_EFFECTIVENESS:
        for def_type in defender_types:
            if def_type in TYPE_EFFECTIVENESS[attacker_type]:
                multiplier *= TYPE_EFFECTIVENESS[attacker_type][def_type]
    
    return multiplier


def calculate_damage(attacker_stats: Dict, defender_stats: Dict, 
                     attacker_type: str, defender_types: List[str]) -> tuple:
    """
    Calculate damage dealt in a battle turn.
    
    Uses a simplified Pokémon damage formula:
    Damage = ((2 * Level / 5 + 2) * Power * (Attack / Defense) / 50 + 2) * Modifier
    """
    level = 50  # Assume level 50
    power = random.randint(60, 100)  # Random move power
    
    attack = attacker_stats.get("Attack", 100)
    defense = defender_stats.get("Defense", 100)
    
    # Base damage calculation
    base_damage = ((2 * level / 5 + 2) * power * (attack / defense) / 50 + 2)
    
    # Type effectiveness
    effectiveness = get_type_effectiveness(attacker_type, defender_types)
    
    # Random modifier (0.85 to 1.0)
    random_mod = random.uniform(0.85, 1.0)
    
    # Critical hit chance (6.25%)
    critical = 2.0 if random.random() < 0.0625 else 1.0
    
    final_damage = int(base_damage * effectiveness * random_mod * critical)
    
    return final_damage, effectiveness, critical > 1


def simulate_battle(pokemon1_name: str, pokemon2_name: str) -> Dict[str, Any]:
    """
    Simulate a turn-based battle between two Pokémon.
    
    This function represents an MCP Tool that executes backend logic
    and returns a formatted battle log.
    
    Args:
        pokemon1_name: Name of the first Pokémon
        pokemon2_name: Name of the second Pokémon
    
    Returns:
        dict: Battle result including:
            - winner: Name of the winning Pokémon
            - loser: Name of the losing Pokémon
            - turns: Number of turns in the battle
            - battle_log: Step-by-step battle narrative
    """
    # Fetch Pokémon data
    pokemon1 = get_pokemon_data(pokemon1_name)
    pokemon2 = get_pokemon_data(pokemon2_name)
    
    # Check for errors
    if "error" in pokemon1:
        return {"error": pokemon1["error"]}
    if "error" in pokemon2:
        return {"error": pokemon2["error"]}
    
    # Initialize battle state
    hp1 = pokemon1["stats"]["HP"] * 2  # Scale HP for battle
    hp2 = pokemon2["stats"]["HP"] * 2
    max_hp1 = hp1
    max_hp2 = hp2
    
    battle_log = []
    battle_log.append(f"⚔️ **BATTLE START!**")
    battle_log.append(f"🔴 **{pokemon1['name']}** ({'/'.join(pokemon1['types'])}) - HP: {hp1}")
    battle_log.append(f"🔵 **{pokemon2['name']}** ({'/'.join(pokemon2['types'])}) - HP: {hp2}")
    battle_log.append("")
    
    # Determine turn order based on Speed
    speed1 = pokemon1["stats"]["Speed"]
    speed2 = pokemon2["stats"]["Speed"]
    
    if speed1 >= speed2:
        first, second = (pokemon1, pokemon2), (pokemon2, pokemon1)
        hp_order = [("hp1", "hp2"), ("hp2", "hp1")]
    else:
        first, second = (pokemon2, pokemon1), (pokemon1, pokemon2)
        hp_order = [("hp2", "hp1"), ("hp1", "hp2")]
    
    turn = 0
    max_turns = 30
    
    # Battle loop
    while hp1 > 0 and hp2 > 0 and turn < max_turns:
        turn += 1
        battle_log.append(f"### Turn {turn}")
        
        # Both Pokémon attack in order
        for idx, (attacker, defender) in enumerate([(first[0], first[1]), (second[0], second[1])]):
            if hp1 <= 0 or hp2 <= 0:
                break
            
            attacker_type = attacker["types"][0]
            
            damage, effectiveness, is_crit = calculate_damage(
                attacker["stats"], 
                defender["stats"],
                attacker_type,
                defender["types"]
            )
            
            # Apply damage
            if attacker["name"] == pokemon1["name"]:
                hp2 -= damage
                hp2 = max(0, hp2)
                remaining_hp = hp2
            else:
                hp1 -= damage
                hp1 = max(0, hp1)
                remaining_hp = hp1
            
            # Build action description
            action = f"**{attacker['name']}** attacks **{defender['name']}**!"
            
            if effectiveness > 1:
                action += " 💥 *It's super effective!*"
            elif effectiveness < 1 and effectiveness > 0:
                action += " 🛡️ *It's not very effective...*"
            elif effectiveness == 0:
                action += " ❌ *It has no effect!*"
            
            if is_crit:
                action += " ⭐ *Critical hit!*"
            
            action += f" (-{damage} HP)"
            battle_log.append(action)
            battle_log.append(f"   └─ {defender['name']}'s HP: {remaining_hp}")
            
            if remaining_hp <= 0:
                break
        
        battle_log.append("")
    
    # Determine winner
    if hp1 > 0:
        winner = pokemon1["name"]
        loser = pokemon2["name"]
    else:
        winner = pokemon2["name"]
        loser = pokemon1["name"]
    
    battle_log.append(f"## 🏆 **{winner} WINS!**")
    battle_log.append(f"{loser} has fainted!")
    
    return {
        "winner": winner,
        "loser": loser,
        "turns": turn,
        "pokemon1": {
            "name": pokemon1["name"],
            "remaining_hp": max(0, hp1),
            "max_hp": max_hp1
        },
        "pokemon2": {
            "name": pokemon2["name"],
            "remaining_hp": max(0, hp2),
            "max_hp": max_hp2
        },
        "battle_log": battle_log
    }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_random_pokemon() -> str:
    """Get a random Pokémon name from the first 151."""
    popular_pokemon = [
        "bulbasaur", "charmander", "squirtle", "pikachu", "jigglypuff",
        "meowth", "psyduck", "growlithe", "abra", "machop",
        "geodude", "magnemite", "gastly", "onix", "drowzee",
        "krabby", "voltorb", "cubone", "hitmonlee", "lickitung",
        "koffing", "rhyhorn", "tangela", "kangaskhan", "horsea",
        "goldeen", "staryu", "scyther", "jynx", "electabuzz",
        "magmar", "pinsir", "tauros", "magikarp", "lapras",
        "ditto", "eevee", "porygon", "omanyte", "kabuto",
        "aerodactyl", "snorlax", "articuno", "zapdos", "moltres",
        "dratini", "mewtwo", "mew", "charizard", "blastoise",
        "venusaur", "gengar", "alakazam", "dragonite", "gyarados"
    ]
    return random.choice(popular_pokemon)
