import streamlit as st
from functions import get_query_param, set_query_param, disable_scrolling, get_a_card, clock_timer
import time

@st.fragment
def game_logic():
    st.markdown("<div id='top'></div>", unsafe_allow_html=True)
    end_of_game = False

    disable_scrolling()

    if "current_card" not in st.session_state:
        # st.session_state.current_card = st.session_state.cards.sample().iloc[0]
        #scroll_to_top()

        st.session_state.current_card = get_a_card(debug=False, print_info=False)
    # st.table(card)
    side = get_query_param('side')

    if side == "Mellette":
        jobbos_bonus = st.session_state.current_card['Jobbos bonus'] # type: ignore
        balos_bonus = st.session_state.current_card['Balos Bonus']  # type: ignore
        hogyan = "mellette"
    elif side == "Ellene":
        jobbos_bonus = st.session_state.current_card['Balos Bonus'] # type: ignore
        balos_bonus = st.session_state.current_card['Jobbos bonus'] # type: ignore
        hogyan = "ellene"

    if st.session_state.player_1_view == "Balos" and side == "Mellette":
        st.session_state.player_1_bonus = balos_bonus
        st.session_state.player_2_bonus = jobbos_bonus
    else:
        st.session_state.player_1_bonus = jobbos_bonus
        st.session_state.player_2_bonus = balos_bonus

    st.session_state.rounds = int(get_query_param("rounds"))
    st.markdown(f"###### Kör {st.session_state.rounds_current} / {st.session_state.rounds}")
    st.markdown(f"###### **Téma:** *{st.session_state.current_card['Kártya leírás HUN']}*") # type: ignore
    st.markdown(f"###### Érveljetek  {hogyan}! ")

    c1, c2 = st.columns(2)

    round_key_suffix = f"_round_{st.session_state.rounds_current}"
    with c1:
        szavazatok_player_1 = st.number_input(
            f"###### {st.session_state.player_1_name} ({st.session_state.player_1_view}) szavazatai. Szorzó: {st.session_state.player_1_bonus} X",
            min_value=0,
            max_value=5,
            value=0,
            key=f"player_1_votes{round_key_suffix}"
        )
    with c2:
        szavazatok_player_2 = st.number_input(
            f"###### {st.session_state.player_2_name} ({st.session_state.player_2_view}) szavazatai. Szorzó: {st.session_state.player_2_bonus} X",
            min_value=0,
            max_value=5,
            value=0,
            key=f"player_2_votes{round_key_suffix}"
        )

    st.markdown("###### **Játékosok pontjai**")


    c1, c2 = st.columns(2)
    with c1:
        _player_1_name = get_query_param("player_1_name")
        _player_1_points = get_query_param("player_1_points")
        pass
        # st.markdown(f"**{_player_1_name}** ({st.session_state.player_1_view}): {_player_1_points} pont")

    with c2:
        _player_2_name = get_query_param("player_2_name")
        _player_2_points = get_query_param("player_2_points")
        pass
        # st.markdown(f"**{_player_2_name}** ({st.session_state.player_2_view}): {_player_2_points} pont")

    st.markdown(f"**{_player_1_name}** ({st.session_state.player_1_view}): {_player_1_points} pont / **{_player_2_name}** ({st.session_state.player_2_view}): {_player_2_points} pont")

    # st.balloons()

    cbal, cjobb = st.columns(2)

    SECONDS = st.session_state.get("erveles_time", 30)

    with cbal:

        # timer_info = st.empty()

        if st.button(f"Érvelés tájmer ({SECONDS} mp) indítása"):
            # from functions import clock_timer
            # timer_info.info("Időzítő fut...")
            st.session_state.times_up = clock_timer(SECONDS)

        if st.session_state.times_up:
            # st.success("Lejárt az idő. Rögzítsétek a szavazatokat!")
            st.session_state.times_up = False
            st.session_state.allow_record_votes = True
            # timer_info.info("Lejárt az idő. Rögzítsétek a szavazatokat!")

        else:
            pass
            # st.session_state.allow_record_votes = False    
            # timer_info.info("Indítsd el az időzítőt, ha szeretnétek időre érvelni!")

    with cjobb:

        if st.button("Szavazatok rögzítése", key=f"commit_votes{round_key_suffix}", disabled = False):

            _temp_pont_1 = szavazatok_player_1 * jobbos_bonus
            _temp_pont_2 = szavazatok_player_2 * balos_bonus
            _current_player_1_points = get_query_param("player_1_points")
            _current_player_2_points = get_query_param("player_2_points")
            set_query_param("player_1_points", int(_current_player_1_points) + int(_temp_pont_1))
            set_query_param("player_2_points", int(_current_player_2_points) + int(_temp_pont_2))
            del st.session_state.current_card
            
            vote_keys_to_delete = [key for key in st.session_state.keys() if key.startswith(('player_1_votes', 'player_2_votes'))] # type: ignore
            for key in vote_keys_to_delete:
                del st.session_state[key]
            st.session_state.rounds_current += 1
            set_query_param("rounds_current", st.session_state.rounds_current)
            if st.session_state.rounds_current-1 < st.session_state.rounds:
                end_of_game = False
                st.rerun()
            else:
                end_of_game = True
    
    if end_of_game:
        _player_1_points = get_query_param("player_1_points")
        _player_2_points = get_query_param("player_2_points")
        if int(_player_1_points) > int(_player_2_points):
            st.success(f"{st.session_state.player_1_name} nyert {int(_player_1_points)} ponttal!")
        elif int(_player_1_points) < int(_player_2_points):
            st.success(f"{st.session_state.player_2_name} nyert {int(_player_2_points)} ponttal!")
        else:
            st.success("Döntetlen!")
        st.balloons()
        # végső pontok kiírása
        st.markdown(f"## **{st.session_state.player_1_name}** ({st.session_state.player_1_view}): {_player_1_points} pont")
        st.markdown(f"## **{st.session_state.player_2_name}** ({st.session_state.player_2_view}): {_player_2_points} pont")
        st.session_state.new_game = True
        st.success("Kattints a Beállítások gombra az új játékhoz!")
        time.sleep(5)

    # if st.session_state.rounds_current == st.session_state.rounds:
        # st.info("Na itt vagyunk e")
        # get winner

