import streamlit as st
from functions import get_query_param, set_query_param, disable_scrolling, get_a_card, clock_timer, run_timer_human, get_a_random_guide_card, get_next_speaker, has_everyone_argued_this_round, run_timer_ai
import time
import random

@st.fragment
def game_logic():
    st.markdown("<div id='top'></div>", unsafe_allow_html=True)
    end_of_game = False

    disable_scrolling()

    if "current_card" not in st.session_state:


        st.session_state.current_card = get_a_card(debug=False, print_info=False)

    # get a new one every time. Super dumb, but fuck cares. There is a lot anyways    
    # st.session_state.current_guide_card = get_a_random_guide_card()

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
    st.markdown(f"###### **Kampánytéma:** {st.session_state.current_card['Kártya leírás HUN']}") # type: ignore
    st.markdown(f"###### Érveljetek  {hogyan}! ")
    theme_message = f"*Kampánytéma:* {st.session_state.current_card['Kártya leírás HUN']} "
    hogyan_message = f"*Érvelj {hogyan}*! "

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
    # Default timer setup
    if "times_up" not in st.session_state:
        st.session_state.times_up = False

    cbal, cjobb = st.columns(2)

    SECONDS = st.session_state.get("erveles_time", 15)

    if random.randint(0, 100) <= st.session_state.get_random_text_chance:
        st.session_state.get_random_text_chance

    with cbal:
        
        disable_button = has_everyone_argued_this_round()
        if st.button(f"Érvelés tájmer ({SECONDS} mp) indítása", disabled=disable_button):
            st.session_state.times_up = False  # Reset timer flag
            ki_ervel = get_next_speaker()
            if ki_ervel == "player_1":
                ki_ervel_nev = f"**{st.session_state.player_1_name}**, _{st.session_state.player_1_view}_"
                politika_oldal = st.session_state.player_1_view
                second_player_ai = False
            else:
                ki_ervel_nev = f"**{st.session_state.player_2_name}**, _{st.session_state.player_2_view}_"
                politika_oldal = st.session_state.player_2_view
                second_player_ai = True if get_query_param("gep_ellen", return_type="bool") else False
            

            if random.randint(1, 100) <= st.session_state.get_random_text_chance:
                extra_task_text = get_a_random_guide_card()
                extra_task_text = f"*Retorikai feladat:* {extra_task_text}"
            else:
                extra_task_text = ""

            if not second_player_ai:
                run_timer_human(seconds=SECONDS, 
                        topic_message=theme_message, 
                        hogyan_message=hogyan_message, 
                        extra_task_message=extra_task_text,
                        ki_ervel_nev=ki_ervel_nev,
                        second_player_ai=second_player_ai,
                        politikai_oldal=politika_oldal)      # Open the dialog
            else:
                run_timer_ai(seconds=SECONDS, 
                        topic_message=theme_message, 
                        hogyan_message=hogyan_message, 
                        retorikai_feladat=extra_task_text,
                        ki_ervel_nev=ki_ervel_nev,
                        politikai_oldal=politika_oldal,
                        debug=False)      # Open the dialog


    with cjobb:
        disable_button = not has_everyone_argued_this_round()
        if st.button("Szavazatok rögzítése", key=f"commit_votes{round_key_suffix}", disabled = disable_button):

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
            st.session_state.speakers_this_round = []
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

