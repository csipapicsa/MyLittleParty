import streamlit as st
from functions import set_query_param, get_query_param  


# def main():
#     st.write("# Forgós játék")
#     st.session_state.player_names = []
#     st.session_state.side = []

#     jatekosok_szama = st.number_input(
#         "Hány játékos játszik?", min_value=3, max_value=10, value=3)
    

#     for i in range(jatekosok_szama):
#         c1, c2 = st.columns(2)
#         with c1:
#             player_name = st.text_input(f"Játékos {i + 1} neve:", key=f"player_{i}")
#             st.session_state.player_names.append(player_name)

#         with c2:
#             side = st.selectbox(
#                 f"{player_name} oldala:",
#                 ["Balos", "Jobbos"],
#             key=f"side_{i}"
#         )
#         st.session_state.side.append(side)

#     st.info(st.session_state.player_names)
#     set_query_param("forgo_player_names", [st.session_state.player_names])
#     st.info(st.session_state.side)
#     set_query_param("forgo_sides", [st.session_state.side])

#     # get query parameters, print them line by line 
#     st.markdown("### **Játékosok**")
#     names = get_query_param("forgo_player_names")
#     sides = get_query_param("forgo_sides")

#     for name, side in zip(names, sides):
#         st.markdown(f"- {name} ({side})")

# main()


import streamlit as st
import json
import urllib.parse

def main():
    st.write("# Forgós játék")
    
    # Initialize session state
    if 'player_names' not in st.session_state:
        st.session_state.player_names = []
    if 'sides' not in st.session_state:
        st.session_state.sides = []
    
    jatekosok_szama = st.number_input(
        "Hány játékos játszik?", min_value=3, max_value=10, value=3)
    
    # Collect player data
    players_data = []
    
    for i in range(jatekosok_szama):
        c1, c2 = st.columns(2)
        with c1:
            player_name = st.text_input(f"Játékos {i + 1} neve:", key=f"player_{i}")
        
        with c2:
            side = st.selectbox(
                f"Játékos {i + 1} oldala:",
                ["Balos", "Jobbos"],
                key=f"side_{i}"
            )
        
        if player_name:  # Only add if name is provided
            players_data.append({"name": player_name, "side": side})
    
    # Method 1: JSON format (RECOMMENDED)
    if players_data:
        json_data = json.dumps(players_data, ensure_ascii=False)
        encoded_json = urllib.parse.quote(json_data)
        st.query_params["players_json"] = encoded_json
        
        st.success("✅ JSON formátum (ajánlott):")
        st.code(json_data, language='json')
    
    # Method 2: Pipe separated format
    if players_data:
        pipe_format = "|".join([f"{p['name']}:{p['side']}" for p in players_data])
        st.query_params["players_pipe"] = pipe_format
        
        st.info("📋 Pipe formátum:")
        st.code(pipe_format)
    
    # Method 3: Base64 encoded JSON (for special characters)
    if players_data:
        import base64
        json_bytes = json.dumps(players_data, ensure_ascii=False).encode('utf-8')
        base64_data = base64.b64encode(json_bytes).decode('utf-8')
        st.query_params["players_b64"] = base64_data
        
        st.info("🔐 Base64 kódolt JSON:")
        st.code(base64_data[:50] + "..." if len(base64_data) > 50 else base64_data)

    # Reading back the data
    st.markdown("---")
    st.markdown("### **Adatok visszaolvasása**")
    
    # Read JSON format
    if "players_json" in st.query_params:
        try:
            decoded_json = urllib.parse.unquote(st.query_params["players_json"])
            players_from_json = json.loads(decoded_json)
            
            st.markdown("**JSON-ból visszaolvasott játékosok:**")
            for player in players_from_json:
                st.markdown(f"- {player['name']} ({player['side']})")
        except:
            st.error("Hiba a JSON visszaolvasásakor")
    
    # Read pipe format
    if "players_pipe" in st.query_params:
        try:
            pipe_data = st.query_params["players_pipe"]
            players_from_pipe = []
            for item in pipe_data.split("|"):
                if ":" in item:
                    name, side = item.split(":", 1)
                    players_from_pipe.append({"name": name, "side": side})
            
            st.markdown("**Pipe formátumból visszaolvasott játékosok:**")
            for player in players_from_pipe:
                st.markdown(f"- {player['name']} ({player['side']})")
        except:
            st.error("Hiba a pipe formátum visszaolvasásakor")
    
    # Read Base64 format
    if "players_b64" in st.query_params:
        try:
            import base64
            base64_data = st.query_params["players_b64"]
            json_bytes = base64.b64decode(base64_data.encode('utf-8'))
            json_str = json_bytes.decode('utf-8')
            players_from_b64 = json.loads(json_str)
            
            st.markdown("**Base64-ből visszaolvasott játékosok:**")
            for player in players_from_b64:
                st.markdown(f"- {player['name']} ({player['side']})")
        except:
            st.error("Hiba a Base64 visszaolvasásakor")

# Helper functions for easier usage
def save_players_to_query(players_data, method="json"):
    """
    Save players data to query parameters
    
    Args:
        players_data: List of dicts with 'name' and 'side' keys
        method: 'json', 'pipe', or 'base64'
    """
    if method == "json":
        json_data = json.dumps(players_data, ensure_ascii=False)
        encoded_json = urllib.parse.quote(json_data)
        st.query_params["players"] = encoded_json
    
    elif method == "pipe":
        pipe_format = "|".join([f"{p['name']}:{p['side']}" for p in players_data])
        st.query_params["players"] = pipe_format
    
    elif method == "base64":
        import base64
        json_bytes = json.dumps(players_data, ensure_ascii=False).encode('utf-8')
        base64_data = base64.b64encode(json_bytes).decode('utf-8')
        st.query_params["players"] = base64_data

def load_players_from_query(method="json"):
    """
    Load players data from query parameters
    
    Args:
        method: 'json', 'pipe', or 'base64'
    
    Returns:
        List of dicts with 'name' and 'side' keys
    """
    if "players" not in st.query_params:
        return []
    
    try:
        if method == "json":
            decoded_json = urllib.parse.unquote(st.query_params["players"])
            return json.loads(decoded_json)
        
        elif method == "pipe":
            pipe_data = st.query_params["players"]
            players = []
            for item in pipe_data.split("|"):
                if ":" in item:
                    name, side = item.split(":", 1)
                    players.append({"name": name, "side": side})
            return players
        
        elif method == "base64":
            import base64
            base64_data = st.query_params["players"]
            json_bytes = base64.b64decode(base64_data.encode('utf-8'))
            json_str = json_bytes.decode('utf-8')
            return json.loads(json_str)
    
    except Exception as e:
        st.error(f"Hiba az adatok betöltésekor: {e}")
        return []

if __name__ == "__main__":
    main()