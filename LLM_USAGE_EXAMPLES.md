# LLM Usage Examples - Pokémon MCP Server

This document provides clear examples of how LLMs would query and interact with the Pokémon MCP Server resources and tools.

## 🎯 Assignment Requirement: "Examples of how an LLM would query your resource"

The following examples demonstrate how an LLM would access and use the Pokémon data resource and battle simulation tool.

---

## 📊 Pokémon Data Resource Examples

### Example 1: Basic Pokémon Information Query

**LLM Query:**
```
I need information about Pikachu for a battle analysis.
```

**Resource Access:**
```
Resource: pokemon://pikachu
```

**Expected LLM Response:**
```json
{
  "pokemon": {
    "id": 25,
    "name": "Pikachu",
    "height": 4,
    "weight": 60,
    "base_experience": 112,
    "description": "Pikachu is a Electric type Pokémon with 35 HP."
  },
  "base_stats": {
    "hp": 35,
    "attack": 55,
    "defense": 40,
    "special_attack": 50,
    "special_defense": 50,
    "speed": 90
  },
  "types": ["Electric"],
  "abilities": [
    {
      "name": "Static",
      "is_hidden": false,
      "description": "Regular ability"
    }
  ],
  "moves": [
    {
      "name": "Thunder Shock",
      "level_learned": 1,
      "learn_method": "level-up"
    },
    {
      "name": "Tail Whip",
      "level_learned": 1,
      "learn_method": "level-up"
    }
  ],
  "battle_summary": {
    "total_stats": 320,
    "primary_type": "Electric",
    "is_dual_type": false
  }
}
```

### Example 2: Pokémon Search Query

**LLM Query:**
```
I'm looking for Fire-type Pokémon that might be good for my team.
```

**Resource Access:**
```
Resource: pokemon://search/fire
```

**Expected LLM Response:**
```json
{
  "search_query": "fire",
  "results": [
    {
      "name": "Charmander",
      "url": "https://pokeapi.co/api/v2/pokemon/4/",
      "description": "Pokémon matching 'fire'"
    },
    {
      "name": "Charmeleon",
      "url": "https://pokeapi.co/api/v2/pokemon/5/",
      "description": "Pokémon matching 'fire'"
    },
    {
      "name": "Charizard",
      "url": "https://pokeapi.co/api/v2/pokemon/6/",
      "description": "Pokémon matching 'fire'"
    }
  ],
  "total_found": 15,
  "usage_note": "Use the exact name from results to access full Pokémon data via pokemon://{name}"
}
```

### Example 3: Type Effectiveness Query

**LLM Query:**
```
I need to understand how Water-type attacks perform against different types.
```

**Resource Access:**
```
Resource: pokemon://types/water
```

**Expected LLM Response:**
```json
{
  "attacking_type": "Water",
  "effectiveness_chart": {
    "normal": 1.0,
    "fire": 2.0,
    "water": 0.5,
    "grass": 0.5,
    "electric": 1.0,
    "ice": 1.0,
    "fighting": 1.0,
    "poison": 1.0,
    "ground": 2.0,
    "flying": 1.0,
    "psychic": 1.0,
    "bug": 1.0,
    "rock": 2.0,
    "ghost": 1.0,
    "dragon": 0.5,
    "dark": 1.0,
    "steel": 1.0,
    "fairy": 1.0
  },
  "summary": {
    "super_effective_against": ["fire", "ground", "rock"],
    "not_very_effective_against": ["water", "grass", "dragon"],
    "no_effect_against": [],
    "neutral_against": ["normal", "electric", "ice", "fighting", "poison", "flying", "psychic", "bug", "ghost", "dark", "steel", "fairy"]
  },
  "battle_tips": {
    "best_matchups": ["fire", "ground", "rock"],
    "worst_matchups": ["water", "grass", "dragon"],
    "avoid_against": []
  }
}
```

---

## ⚔️ Battle Simulation Tool Examples

### Example 1: Basic Battle Simulation

**LLM Query:**
```
Simulate a battle between Pikachu and Charizard to see who would win.
```

**Tool Call:**
```json
{
  "tool": "simulate_battle",
  "parameters": {
    "pokemon1_name": "pikachu",
    "pokemon2_name": "charizard"
  }
}
```

**Expected LLM Response:**
```json
{
  "winner": "Charizard",
  "loser": "Pikachu",
  "total_turns": 8,
  "actions": [
    {
      "pokemon_name": "Charizard",
      "action_type": "attack",
      "move_name": "Flamethrower",
      "damage_dealt": 45,
      "effectiveness": "It's super effective!",
      "message": "Charizard used Flamethrower! It's super effective! It dealt 45 damage!"
    },
    {
      "pokemon_name": "Pikachu",
      "action_type": "attack",
      "move_name": "Thunder Shock",
      "damage_dealt": 32,
      "effectiveness": "",
      "message": "Pikachu used Thunder Shock! It dealt 32 damage!"
    },
    {
      "pokemon_name": "Pikachu",
      "action_type": "faint",
      "message": "Pikachu fainted!"
    }
  ],
  "battle_summary": "🏆 BATTLE SUMMARY 🏆\n\nWinner: Charizard\nLoser: Pikachu\nTotal Turns: 8\n\nKey Moments:\nTurn 1: Charizard used Flamethrower! It's super effective! It dealt 45 damage!\nTurn 2: Pikachu used Thunder Shock! It dealt 32 damage!\nTurn 3: Pikachu fainted!"
}
```

### Example 2: Battle with Status Effects

**LLM Query:**
```
I want to see how status effects affect a battle between two strong Pokémon.
```

**Tool Call:**
```json
{
  "tool": "simulate_battle",
  "parameters": {
    "pokemon1_name": "blastoise",
    "pokemon2_name": "venusaur"
  }
}
```

**Expected LLM Response:**
```json
{
  "winner": "Blastoise",
  "loser": "Venusaur",
  "total_turns": 12,
  "actions": [
    {
      "pokemon_name": "Blastoise",
      "action_type": "attack",
      "move_name": "Hydro Pump",
      "damage_dealt": 38,
      "effectiveness": "It's super effective!",
      "message": "Blastoise used Hydro Pump! It's super effective! It dealt 38 damage!"
    },
    {
      "pokemon_name": "Venusaur",
      "action_type": "status",
      "message": "Venusaur is hurt by Poison and takes 6 damage!"
    },
    {
      "pokemon_name": "Venusaur",
      "action_type": "attack",
      "move_name": "Solar Beam",
      "damage_dealt": 28,
      "effectiveness": "",
      "message": "Venusaur used Solar Beam! It dealt 28 damage!"
    }
  ],
  "battle_summary": "🏆 BATTLE SUMMARY 🏆\n\nWinner: Blastoise\nLoser: Venusaur\nTotal Turns: 12\n\nKey Moments:\nTurn 1: Blastoise used Hydro Pump! It's super effective! It dealt 38 damage!\nTurn 2: Venusaur is hurt by Poison and takes 6 damage!\nTurn 3: Venusaur used Solar Beam! It dealt 28 damage!"
}
```

---

## 🤖 LLM Integration Patterns

### Pattern 1: Data-Driven Analysis

**LLM Workflow:**
1. Query Pokémon data: `pokemon://pikachu`
2. Query type effectiveness: `pokemon://types/electric`
3. Analyze strengths and weaknesses
4. Provide strategic recommendations

**Example LLM Response:**
```
Based on the data, Pikachu is an Electric-type Pokémon with high Speed (90) but low HP (35). 
Electric-type attacks are super effective against Water and Flying types, making Pikachu 
excellent against Water-type Pokémon like Blastoise. However, its low HP makes it vulnerable 
to strong attacks, so it should focus on speed and hit-and-run tactics.
```

### Pattern 2: Battle Prediction

**LLM Workflow:**
1. Query both Pokémon: `pokemon://charizard` and `pokemon://blastoise`
2. Query type effectiveness: `pokemon://types/fire` and `pokemon://types/water`
3. Run battle simulation: `simulate_battle("charizard", "blastoise")`
4. Analyze results and provide insights

**Example LLM Response:**
```
The battle simulation shows that Blastoise wins against Charizard due to type advantage. 
Water-type attacks are super effective against Fire-types, dealing 2x damage. While Charizard 
has higher Attack stats, Blastoise's type advantage and higher HP (79 vs 78) give it the edge. 
The simulation confirms that type effectiveness is crucial in Pokémon battles.
```

### Pattern 3: Team Building

**LLM Workflow:**
1. Search for Pokémon by type: `pokemon://search/fire`
2. Query individual Pokémon data
3. Analyze type coverage and team balance
4. Suggest optimal team composition

**Example LLM Response:**
```
For a balanced team, I recommend:
1. Charizard (Fire/Flying) - Strong attacker with good type coverage
2. Blastoise (Water) - Counters Fire and Rock types
3. Venusaur (Grass/Poison) - Covers Water and Ground weaknesses
4. Pikachu (Electric) - Fast attacker for Flying and Water types
5. Snorlax (Normal) - Tank with high HP for defense
6. Alakazam (Psychic) - Special attacker with high Special Attack

This team provides good type coverage and balances physical and special attackers.
```

---

## 🔧 Technical Integration

### MCP Client Integration

```python
# Example of how an LLM client would integrate
async def analyze_pokemon_battle(pokemon1, pokemon2):
    # Access Pokémon data resource
    pokemon1_data = await client.read_resource(f"pokemon://{pokemon1}")
    pokemon2_data = await client.read_resource(f"pokemon://{pokemon2}")
    
    # Get type effectiveness
    type1 = pokemon1_data["types"][0]
    type2 = pokemon2_data["types"][0]
    effectiveness = await client.read_resource(f"pokemon://types/{type1}")
    
    # Simulate battle
    battle_result = await client.call_tool("simulate_battle", {
        "pokemon1_name": pokemon1,
        "pokemon2_name": pokemon2
    })
    
    return {
        "pokemon1": pokemon1_data,
        "pokemon2": pokemon2_data,
        "type_effectiveness": effectiveness,
        "battle_result": battle_result
    }
```

### Resource URL Patterns

```
pokemon://pikachu              # Get Pikachu data
pokemon://25                   # Get Pokémon with ID 25
pokemon://search/fire          # Search for Fire-type Pokémon
pokemon://types/water          # Get Water type effectiveness
pokemon://types/electric       # Get Electric type effectiveness
```

### Tool Call Patterns

```json
{
  "tool": "simulate_battle",
  "parameters": {
    "pokemon1_name": "pikachu",
    "pokemon2_name": "charizard"
  }
}
```

```json
{
  "tool": "get_evolution_chain",
  "parameters": {
    "pokemon_name": "charmander"
  }
}
```

---

## 📈 Expected LLM Behaviors

### 1. Data Retrieval
- LLMs will query resources to get Pokémon information
- They'll use search functionality to discover Pokémon
- They'll access type effectiveness for battle analysis

### 2. Battle Simulation
- LLMs will use the battle tool to simulate matches
- They'll analyze battle results for strategic insights
- They'll compare different Pokémon matchups

### 3. Strategic Analysis
- LLMs will combine data from multiple resources
- They'll provide recommendations based on type advantages
- They'll suggest optimal team compositions

### 4. Educational Content
- LLMs will explain Pokémon mechanics using the data
- They'll create battle scenarios and predictions
- They'll teach users about type effectiveness

---

This comprehensive resource enables LLMs to become true Pokémon experts, providing accurate data, realistic battle simulations, and strategic insights that enhance the user experience in the Pokémon world.
