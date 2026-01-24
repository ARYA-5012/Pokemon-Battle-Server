"""
Pokémon MCP Inspector - Streamlit Interface

A chat-style inspection interface that simulates how an LLM would interact 
with MCP tools and resources. This validates MCP logic in a controlled 
environment without requiring direct protocol-level access.
"""

import streamlit as st
import json
from server_logic import get_pokemon_data, simulate_battle, get_random_pokemon


# ============================================================================
# PAGE CONFIGURATION & DARK THEME
# ============================================================================

st.set_page_config(
    page_title="Pokémon MCP Inspector",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and professional styling
st.markdown("""
<style>
    /* Dark theme base */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Main container styling */
    .main .block-container {
        padding: 2rem 3rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #e94560 0%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #a0a0a0;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .inspector-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .card-title {
        color: #e94560;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Status indicators */
    .status-online {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #00d26a;
        font-weight: 500;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #00d26a;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Result boxes */
    .result-box {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        border-left: 4px solid #e94560;
    }
    
    /* Battle log styling */
    .battle-log {
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(15, 52, 96, 0.8);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #e94560 0%, #ff6b6b 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(233, 69, 96, 0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 8px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    
    /* Pokémon sprite container */
    .pokemon-sprite {
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    /* Stats display */
    .stat-bar {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        height: 8px;
        overflow: hidden;
    }
    
    .stat-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# SIDEBAR - SERVER CONTEXT
# ============================================================================

with st.sidebar:
    st.markdown("## ⚡ MCP Server")
    
    # Server status
    st.markdown("""
    <div style="background: rgba(0, 210, 106, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        <div class="status-online">
            <div class="status-dot"></div>
            Server Online
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Server Info")
    st.markdown("""
    **Name:** Pokémon Battle Simulation Server  
    **Version:** 1.0.0  
    **Protocol:** MCP (Model Context Protocol)
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔧 Available Resources")
    st.code("pokemon://data/{name}", language=None)
    st.caption("Fetch comprehensive Pokémon data")
    
    st.markdown("---")
    
    st.markdown("### 🛠️ Available Tools")
    st.code("simulate_battle(pokemon1, pokemon2)", language=None)
    st.caption("Simulate a battle between two Pokémon")
    
    st.markdown("---")
    
    st.markdown("### 📊 API Status")
    st.markdown("""
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
        <span>PokeAPI</span>
        <span style="color: #00d26a;">● Connected</span>
    </div>
    <div style="display: flex; justify-content: space-between;">
        <span>MCP Protocol</span>
        <span style="color: #00d26a;">● Ready</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
st.markdown('<h1 class="main-header">⚡ Pokémon MCP Inspector</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive MCP Resource & Tool Testing Interface</p>', unsafe_allow_html=True)

# Create two columns for Resource and Tool inspectors
col1, col2 = st.columns(2, gap="large")


# ============================================================================
# RESOURCE INSPECTOR (Left Column)
# ============================================================================

with col1:
    st.markdown("### 📦 Resource Inspector")
    st.markdown("Query Pokémon data using the MCP resource endpoint")
    
    # Input for Pokémon name
    pokemon_input = st.text_input(
        "Pokémon Name",
        placeholder="Enter a Pokémon name (e.g., pikachu)",
        key="pokemon_name"
    )
    
    col1a, col1b = st.columns([3, 1])
    with col1a:
        fetch_btn = st.button("🔍 Fetch Data", key="fetch_pokemon", use_container_width=True)
    with col1b:
        random_btn = st.button("🎲", key="random_pokemon", help="Random Pokémon")
    
    if random_btn:
        pokemon_input = get_random_pokemon()
        st.session_state["pokemon_name"] = pokemon_input
        st.rerun()
    
    if fetch_btn and pokemon_input:
        with st.spinner(f"Fetching {pokemon_input}..."):
            result = get_pokemon_data(pokemon_input)
        
        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            # Display Pokémon card
            st.markdown(f"#### {result['name']} #{result['id']}")
            
            # Sprite and basic info
            if result.get("sprite"):
                st.image(result["sprite"], width=150)
            
            # Types
            type_colors = {
                "Fire": "#F08030", "Water": "#6890F0", "Grass": "#78C850",
                "Electric": "#F8D030", "Psychic": "#F85888", "Ice": "#98D8D8",
                "Dragon": "#7038F8", "Dark": "#705848", "Fairy": "#EE99AC",
                "Normal": "#A8A878", "Fighting": "#C03028", "Flying": "#A890F0",
                "Poison": "#A040A0", "Ground": "#E0C068", "Rock": "#B8A038",
                "Bug": "#A8B820", "Ghost": "#705898", "Steel": "#B8B8D0"
            }
            
            type_badges = ""
            for t in result["types"]:
                color = type_colors.get(t, "#888888")
                type_badges += f'<span style="background: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; margin-right: 0.5rem; font-size: 0.85rem;">{t}</span>'
            
            st.markdown(f"**Types:** {type_badges}", unsafe_allow_html=True)
            
            st.markdown(f"**Height:** {result['height']} m | **Weight:** {result['weight']} kg")
            
            # Stats
            st.markdown("##### 📊 Base Stats")
            stat_colors = {
                "HP": "#FF5959", "Attack": "#F5AC78", "Defense": "#FAE078",
                "Sp. Attack": "#9DB7F5", "Sp. Defense": "#A7DB8D", "Speed": "#FA92B2"
            }
            
            for stat_name, stat_value in result["stats"].items():
                col_stat, col_bar = st.columns([1, 2])
                with col_stat:
                    st.markdown(f"**{stat_name}:** {stat_value}")
                with col_bar:
                    st.progress(min(stat_value / 255, 1.0))
            
            # Abilities
            st.markdown("##### ✨ Abilities")
            for ability in result["abilities"]:
                hidden = " (Hidden)" if ability["hidden"] else ""
                st.markdown(f"• {ability['name']}{hidden}")
            
            # Moves
            st.markdown("##### 🎯 Sample Moves")
            st.markdown(", ".join(result["moves"]))
            
            # Raw JSON (expandable)
            with st.expander("📄 View Raw JSON"):
                st.json(result)


# ============================================================================
# TOOL INSPECTOR (Right Column)
# ============================================================================

with col2:
    st.markdown("### ⚔️ Tool Inspector")
    st.markdown("Execute the battle simulation MCP tool")
    
    # Input for battle
    st.markdown("**Pokémon 1** 🔴")
    pokemon1_input = st.text_input(
        "First Pokémon",
        placeholder="Enter first Pokémon (e.g., charizard)",
        key="pokemon1",
        label_visibility="collapsed"
    )
    
    st.markdown("**vs**", unsafe_allow_html=True)
    
    st.markdown("**Pokémon 2** 🔵")
    pokemon2_input = st.text_input(
        "Second Pokémon",
        placeholder="Enter second Pokémon (e.g., blastoise)",
        key="pokemon2",
        label_visibility="collapsed"
    )
    
    col2a, col2b = st.columns([3, 1])
    with col2a:
        battle_btn = st.button("⚔️ Simulate Battle", key="simulate_battle", use_container_width=True)
    with col2b:
        random_battle = st.button("🎲", key="random_battle", help="Random matchup")
    
    if random_battle:
        st.session_state["pokemon1"] = get_random_pokemon()
        st.session_state["pokemon2"] = get_random_pokemon()
        st.rerun()
    
    if battle_btn and pokemon1_input and pokemon2_input:
        with st.spinner(f"Simulating battle: {pokemon1_input} vs {pokemon2_input}..."):
            result = simulate_battle(pokemon1_input, pokemon2_input)
        
        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            # Battle result summary
            st.success(f"🏆 **{result['winner']}** wins in **{result['turns']}** turns!")
            
            # HP bars
            col_hp1, col_hp2 = st.columns(2)
            with col_hp1:
                p1 = result["pokemon1"]
                hp_pct = p1["remaining_hp"] / p1["max_hp"]
                st.markdown(f"**{p1['name']}**")
                st.progress(hp_pct)
                st.caption(f"HP: {p1['remaining_hp']}/{p1['max_hp']}")
            
            with col_hp2:
                p2 = result["pokemon2"]
                hp_pct = p2["remaining_hp"] / p2["max_hp"]
                st.markdown(f"**{p2['name']}**")
                st.progress(hp_pct)
                st.caption(f"HP: {p2['remaining_hp']}/{p2['max_hp']}")
            
            # Battle log
            st.markdown("##### 📜 Battle Log")
            with st.container(height=400):
                for line in result["battle_log"]:
                    st.markdown(line)
            
            # Raw JSON (expandable)
            with st.expander("📄 View Raw JSON"):
                # Don't include full battle_log in JSON display
                json_result = {k: v for k, v in result.items() if k != "battle_log"}
                json_result["battle_log"] = f"[{len(result['battle_log'])} lines]"
                st.json(json_result)


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    <p>🎮 Pokémon MCP Server | Built with Streamlit | Data from <a href="https://pokeapi.co" style="color: #e94560;">PokeAPI</a></p>
    <p style="font-size: 0.8rem;">This interface simulates MCP interactions without requiring direct protocol-level access.</p>
</div>
""", unsafe_allow_html=True)
