import streamlit as st

@st.fragment
def test():
    options = ["Balos", "Jobbos"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        player_1_name = st.text_input("Player 1 name")
        
        # Try with on_change callback
        def on_player1_change():
            st.session_state.player_1_view = st.session_state.player_1_selectbox
        
        if "player_1_view" not in st.session_state:
            st.session_state.player_1_view = "Balos"
        
        st.selectbox(
            "Player 1 political view", 
            options, 
            index=options.index(st.session_state.player_1_view),
            key="player_1_selectbox",
            on_change=on_player1_change
        )

    with col2:
        player_2_name = st.text_input("Player 2 name")
        
        # Use the callback-updated value
        player_1_selection = st.session_state.get("player_1_view", "Balos")
        opposite_index = 1 - options.index(player_1_selection)
        
        st.selectbox(
            "Player 2 political view",
            options,
            index=opposite_index,
            disabled=True,
            key="player_2_selectbox"
        )

test()