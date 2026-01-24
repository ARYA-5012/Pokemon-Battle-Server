# Pokémon MCP Server - Project Structure

This document outlines the complete project structure and file organization.

## 📁 Directory Structure

```
pokemon-mcp-server/
├── src/
│   └── pokemon_mcp/
│       ├── __init__.py              # Package initialization
│       ├── models.py                # Pydantic data models
│       ├── pokemon_data.py          # PokeAPI data fetching service
│       ├── battle_mechanics.py      # Battle simulation logic
│       └── server.py                # Main MCP server implementation
├── main.py                          # Entry point script
├── test_server.py                   # Test script
├── example_usage.py                 # Usage examples
├── setup.py                         # Setup and installation script
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project configuration
├── config.json                      # Server configuration
├── README.md                        # Main documentation
└── PROJECT_STRUCTURE.md             # This file
```

## 📋 File Descriptions

### Core Implementation Files

#### `src/pokemon_mcp/models.py`
- **Purpose**: Data models using Pydantic
- **Key Classes**:
  - `Pokemon`: Complete Pokémon data structure
  - `PokemonStats`: Base stats (HP, Attack, Defense, etc.)
  - `BattlePokemon`: Pokémon in battle state
  - `BattleResult`: Complete battle simulation result
  - `TypeEffectiveness`: Type matchup data
  - `StatusEffect`: Status effect definitions

#### `src/pokemon_mcp/pokemon_data.py`
- **Purpose**: Data fetching from PokeAPI
- **Key Features**:
  - Async HTTP client with httpx
  - Data caching for performance
  - Error handling and validation
  - Search functionality
  - Type effectiveness calculations

#### `src/pokemon_mcp/battle_mechanics.py`
- **Purpose**: Battle simulation engine
- **Key Features**:
  - Turn-based combat system
  - Type effectiveness calculations
  - Status effect processing
  - Damage calculation formulas
  - Speed-based turn order

#### `src/pokemon_mcp/server.py`
- **Purpose**: MCP server implementation
- **Key Features**:
  - FastMCP server setup
  - Resource definitions
  - Tool implementations
  - Prompt templates
  - Lifecycle management

### Entry Points and Scripts

#### `main.py`
- **Purpose**: Main entry point
- **Usage**: `python main.py` or `mcp dev main.py`
- **Features**: Server startup and configuration

#### `test_server.py`
- **Purpose**: Test script for verification
- **Usage**: `python test_server.py`
- **Features**: Tests all major functionality

#### `example_usage.py`
- **Purpose**: Usage examples and demonstrations
- **Usage**: `python example_usage.py`
- **Features**: Shows how to use the server

#### `setup.py`
- **Purpose**: Automated setup and installation
- **Usage**: `python setup.py`
- **Features**: Dependency installation and verification

### Configuration Files

#### `requirements.txt`
- **Purpose**: Python package dependencies
- **Contents**: MCP, httpx, pydantic, typing-extensions

#### `pyproject.toml`
- **Purpose**: Project metadata and build configuration
- **Contents**: Project info, dependencies, build settings

#### `config.json`
- **Purpose**: Server configuration
- **Contents**: API settings, battle parameters, logging config

### Documentation

#### `README.md`
- **Purpose**: Main documentation
- **Contents**: Installation, usage, API reference, examples

#### `PROJECT_STRUCTURE.md`
- **Purpose**: Project organization guide
- **Contents**: File descriptions, architecture overview

## 🏗️ Architecture Overview

### Data Flow
1. **Client Request** → MCP Server
2. **Server** → PokemonDataService
3. **DataService** → PokeAPI
4. **Response** → Caching → Client

### Battle Simulation Flow
1. **Battle Request** → BattleSimulator
2. **Pokemon Data** → BattlePokemon objects
3. **Turn Processing** → Status effects, moves, damage
4. **Result Generation** → BattleResult with actions

### MCP Integration
1. **Resources**: Data access (pokemon://, search://, types://)
2. **Tools**: Actions (simulate_battle, get_pokemon_info, etc.)
3. **Prompts**: Templates (battle_analysis, team_builder)

## 🔧 Key Dependencies

### Core Dependencies
- **mcp**: Model Context Protocol SDK
- **httpx**: Async HTTP client for API calls
- **pydantic**: Data validation and serialization
- **typing-extensions**: Enhanced type hints

### Development Dependencies
- **pytest**: Testing framework
- **ruff**: Code linting and formatting

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Tests**:
   ```bash
   python test_server.py
   ```

3. **Start Server**:
   ```bash
   python main.py
   # or
   mcp dev main.py
   ```

4. **View Examples**:
   ```bash
   python example_usage.py
   ```

## 📊 Performance Considerations

### Caching Strategy
- Pokémon data cached in memory
- Type effectiveness cached
- Move data cached
- Configurable cache size

### API Rate Limiting
- Respects PokeAPI rate limits
- Async operations for efficiency
- Error handling for timeouts

### Memory Management
- Efficient data structures
- Lazy loading where possible
- Cleanup on server shutdown

## 🧪 Testing Strategy

### Unit Tests
- Individual component testing
- Mock external API calls
- Data validation testing

### Integration Tests
- End-to-end functionality
- Real API integration
- Error handling verification

### Performance Tests
- Load testing
- Memory usage monitoring
- Response time measurement

## 🔒 Security Considerations

### Input Validation
- Pydantic model validation
- Sanitized user inputs
- Type checking

### API Security
- HTTPS only for external calls
- Timeout configurations
- Error message sanitization

### Data Privacy
- No user data storage
- Stateless operations
- Secure configuration

## 📈 Scalability

### Horizontal Scaling
- Stateless server design
- External API dependency
- Load balancer compatible

### Vertical Scaling
- Memory-efficient caching
- Async operations
- Configurable limits

### Monitoring
- Comprehensive logging
- Error tracking
- Performance metrics

---

This structure provides a solid foundation for the Pokémon MCP Server with clear separation of concerns, comprehensive testing, and excellent documentation.
