# Pokémon MCP Server

A Model Context Protocol (MCP) server that provides AI models with access to Pokémon data and battle simulation capabilities. Includes a Streamlit-based MCP Inspector for visual testing.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![MCP](https://img.shields.io/badge/Protocol-MCP-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🎮 **Interactive Battle System** - Turn-based battles with detailed logs
- 📊 **Complete Pokémon Data** - Stats, types, abilities, moves via PokeAPI
- ⚔️ **Battle Simulation** - Type effectiveness, damage calculations, status effects
- 🤖 **MCP Integration** - Resources and tools for LLM access
- 🌐 **Streamlit Inspector** - Visual interface for testing MCP functionality

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Internet connection (for PokeAPI)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pokemon-mcp-server.git
cd pokemon-mcp-server

# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

#### Option 1: Streamlit MCP Inspector (Recommended)
```bash
cd pokemon-mcp-server
streamlit run app.py
```
Opens a visual interface at `http://localhost:8501`

#### Option 2: Interactive Battle System
```bash
python interactive_battle.py
```

#### Option 3: MCP Development Mode
```bash
mcp dev main.py
```

## 📋 Project Structure

```
pokemon-mcp-server/              # Streamlit Interface
├── app.py                       # MCP Inspector UI
├── server_logic.py              # MCP resources & tools
└── requirements.txt             # Dependencies

pokemon-mcp-server-improved/     # Full MCP Server
├── src/pokemon_mcp/
│   ├── server.py               # MCP server implementation
│   ├── pokemon_data.py         # PokeAPI integration
│   ├── battle_mechanics.py     # Battle simulation engine
│   └── models.py               # Pydantic data models
├── main.py                     # Server entry point
├── interactive_battle.py       # Interactive battle CLI
├── test_server.py              # Basic tests
└── test_assignment_requirements.py  # Compliance tests
```

## 🔧 MCP Resources & Tools

### Resources
| Resource URI | Description |
|--------------|-------------|
| `pokemon://{name}` | Get comprehensive Pokémon data |
| `pokemon://search/{query}` | Search Pokémon by name |
| `pokemon://types/{type}` | Get type effectiveness info |

### Tools
| Tool | Description |
|------|-------------|
| `simulate_battle(pokemon1, pokemon2)` | Simulate a battle between two Pokémon |
| `get_evolution_chain(pokemon)` | Get evolution information |

## ⚔️ Battle Mechanics

- **Type Effectiveness**: Complete 18-type matrix (2x, 0.5x, 0x multipliers)
- **Damage Formula**: Based on attack/defense stats and move power
- **Turn Order**: Determined by Speed stat
- **Status Effects**: Paralysis, Burn, Poison, Sleep, Freeze

## 🧪 Testing

```bash
# Basic functionality test
python test_server.py

# Assignment requirements compliance
python test_assignment_requirements.py

# Quick demo
python quick_demo.py
```

## 🌐 Streamlit Cloud Deployment

1. Push the `pokemon-mcp-server/` folder to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New App** → Select repository → Deploy

## 🔌 Claude Desktop Integration

Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "pokemon": {
      "command": "python",
      "args": ["path/to/main.py"]
    }
  }
}
```

## 📖 Example Usage

### LLM Resource Query
```
Resource: pokemon://pikachu

Returns:
- Base stats (HP, Attack, Defense, Sp.Atk, Sp.Def, Speed)
- Types, abilities, moves
- Evolution information
```

### Battle Simulation
```json
{
  "tool": "simulate_battle",
  "arguments": {
    "pokemon1_name": "charizard",
    "pokemon2_name": "blastoise"
  }
}
```

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| PokeAPI errors | Check internet connection |
| Server hangs | Normal - MCP waits for stdin. Use test scripts instead |

## 📝 License

MIT License - feel free to use and modify.

---

**Ready to battle?** Start with `python interactive_battle.py` or `streamlit run app.py` 🏆


## 👨‍💻 Author

<table>
<tr>
<td align="center">
<strong>Arya Yadav</strong><br>
Bennett University<br>
<a href="mailto:aryayadav5012@gmail.com">📧 Email</a> |
<a href="https://github.com/yourusername">🐙 GitHub</a>
</td>
</tr>
</table>

---
