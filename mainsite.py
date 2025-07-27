import streamlit as st

from functions import get_query_param, set_query_param, read_in_cards, show_all_cards

szabaly = """
# Szabályok
A játék célja, hogy a játékosok minél jobban tudjanak egy-egy téma mellett érvelni, jobbos vagy balos politikus nézetet képviselve. A játék során a játékosok kártyákat húznak, amelyek különböző politikai témákat és álláspontokat tartalmaznak. A játékosoknak meg kell próbálniuk meggyőzni a népet az általuk képviselt nézet helyességéről.

A kártyákra olya módon kell reagálni, hogy pártálástól függően mindig mellette vagy ellenne kell érvelni. Például ha egy játékos baloldali nézeteket képvisel, és egy jobboldal számra kedves kártyát húz, majd érvelésével szavazatokat nyer, akkor rendzserint bizonyos szorzóval kap pontot.

A játék indítása:
- Döntsétek el, hogy minden körben mindenki mellette vagy ellene érvel az adott témának. Az összes körben ezt kell tartani.
- Döntsétek el hány kört szeretnétek játszani.
- Minden körben húztok egy kártyát.
- Mindkét játékosnak el kell mondania az érvet, lehetőleg pár mondatban. 
- A játékosok szavaznak, hogy kinek volt jobb érve.
- Írjátok be, melyik játékos hány szavazatot kapott. Aki a 'nép' pozícióban van, az írja be a szavazatokat, és egy körben csak egyet lehet szavazni
- Az győz, aki a legtöbb szavazatot kapta az adott játékban.
"""

@st.fragment
def game_logic():

    if "current_card" not in st.session_state:
        st.session_state.current_card = st.session_state.cards.sample().iloc[0]

    card = st.session_state.current_card
    # st.table(card)
    side = get_query_param('side')

    if card["Típus - HUN"] == "Kampány":
        mode = "erveles"
    else:
        mode = "reagalas"

    if side == "Mellette" and mode == "erveles":
        jobbos_bonus = card['Jobbos bonus']
        balos_bonus = card['Balos Bonus']
        hogyan = "mellette"
    elif side == "Ellene" and mode == "erveles":
        jobbos_bonus = card['Balos Bonus']
        balos_bonus = card['Jobbos bonus']
        hogyan = "ellene"
    elif mode == "reagalas":
        # TODO 
        jobbos_bonus = card['Jobbos bonus']
        balos_bonus = card['Balos Bonus']
        # hogyan = "reagáljatok a kártyára"


    # choose a random card from the cards dataframe

    st.session_state.rounds = int(get_query_param("rounds"))

    st.markdown(f"## Kör {st.session_state.rounds_current} / {st.session_state.rounds}")

    st.markdown(f"## **Téma:** *{card['Kártya leírás HUN']}*")
    st.markdown(f"## **Típus:** *{card['Típus - HUN']}*")
    
    st.divider()

    if mode == "erveles":
        st.markdown(f" ## Érveljetek  {hogyan}! ")
    else:
        st.markdown(f" ## Reagáljatok! ")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"## **Balos szavazati bonus:** \n\n ## {balos_bonus} x")
    with c2:
        st.markdown(f"## **Jobbos szavazati bonus:** \n\n ## {jobbos_bonus} x")

    st.divider()


    c1, c2 = st.columns(2)


    if st.session_state.player_1_view == "Balos":
        with c1:
            szavazatok_player_1 = st.number_input(
                f"## {st.session_state.player_1_name} szavazatai",
                min_value=0,
                max_value=5,
                value=0,
                key="player_1_votes"
            )
        with c2:
            szavazatok_player_2 = st.number_input(
                f"## {st.session_state.player_2_name} szavazatai",
                min_value=0,
                max_value=5,
                value=0,
                key="player_2_votes"
            )
    else:
        with c1:
            szavazatok_player_2 = st.number_input(
                f"## {st.session_state.player_2_name} szavazatai",
                min_value=0,
                max_value=5,
                value=0,
                key="player_2_votes"
            )
        with c2:
            szavazatok_player_1 = st.number_input(
                f"## {st.session_state.player_1_name} szavazatai",
                min_value=0,
                max_value=5,
                value=0,
                key="player_1_votes"
            )


    st.divider()

    st.markdown("## **Játékosok pontjai**")

    pontok_container = st.container()

    with pontok_container:
        c1, c2 = st.columns(2)
        if st.session_state.player_1_view == "Balos":
            with c1:
                _player_1_name = get_query_param("player_1_name")
                _player_1_points = get_query_param("player_1_points")
                st.markdown(f"### **{_player_1_name}** ({st.session_state.player_1_view}): {_player_1_points} pont")

            with c2:
                _player_2_name = get_query_param("player_2_name")
                _player_2_points = get_query_param("player_2_points")
                st.markdown(f"### **{_player_2_name}** ({st.session_state.player_2_view}): {_player_2_points} pont")

        else:
            with c1:
                _player_2_name = get_query_param("player_2_name")
                _player_2_points = get_query_param("player_2_points")
                st.markdown(f"### **{_player_2_name}** ({st.session_state.player_2_view}): {_player_2_points} pont")

            with c2:
                _player_1_name = get_query_param("player_1_name")
                _player_1_points = get_query_param("player_1_points")
                st.markdown(f"### **{_player_1_name}** ({st.session_state.player_1_view}): {_player_1_points} pont")

    # st.balloons()

    if st.button("Szavazatok rögzítése"):
        _temp_pont_1 = szavazatok_player_1 * jobbos_bonus
        _temp_pont_2 = szavazatok_player_2 * balos_bonus
        _current_player_1_points = get_query_param("player_1_points")
        _current_player_2_points = get_query_param("player_2_points")
        set_query_param("player_1_points", int(_current_player_1_points) + int(_temp_pont_1))
        set_query_param("player_2_points", int(_current_player_2_points) + int(_temp_pont_2))
        del st.session_state.current_card
        # st.info("Még nem vagyunk itt")
        # st.info(st.session_state.rounds_current)
        # st.info(st.session_state.rounds)
        # st.info(int(st.session_state.rounds_current) == int(st.session_state.rounds))
        if st.session_state.rounds_current == st.session_state.rounds:
            # st.info("Na itt vagyunk e")
            # get winner
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
            st.markdown(f"### **{st.session_state.player_1_name}** ({st.session_state.player_1_view}): {_player_1_points} pont")
            st.markdown(f"### **{st.session_state.player_2_name}** ({st.session_state.player_2_view}): {_player_2_points} pont")
            
            import time
            time.sleep(10)
            # st.stop()

        else:
            st.session_state.rounds_current += 1
            set_query_param("rounds_current", st.session_state.rounds_current)
            set_query_param("page", "game")

        st.rerun()





def main():
    st.title("Az én kicsi pártom kártyajáték - teszt oldal")

    tab_names = ["Szabályok", "Beállítások", "Játék", "Kártya ötletek"]
    tab_keys = ["szabaly", "settings", "game", "card_ideas"]

    # Get page from query, default to "szabaly"
    page = get_query_param("page")
    if page not in tab_keys:
        page = "szabaly"

    selected_index = tab_keys.index(page)

    # Use radio to simulate tabs
    selected_tab = st.radio(
        "Válassz lapot:",
        tab_names,
        index=selected_index,
        horizontal=True,
        label_visibility="collapsed"
    )

    # Update query param when user changes tab
    new_page = tab_keys[tab_names.index(selected_tab)]
    if new_page != page:
        set_query_param("page", new_page)
        st.rerun()

    # Content logic
    if new_page == "szabaly":
        st.markdown(szabaly)
    elif new_page == "settings":
        st.markdown("## Beállítások")
        options = ["Balos", "Jobbos"]

        cm1, cm2 = st.columns(2)
        with cm1:
            játékos_1_neve = st.text_input("Játékos 1 neve", value=get_query_param("player_1_name"))
            _jatékos_1_politikai_nézete = get_query_param("player_1_view")
            if _jatékos_1_politikai_nézete == "_":
                _jatékos_1_politikai_nézete = "Balos"
            játékos_1_politikai_nézete = st.selectbox("Játékos 1 politikai nézete", options, index=options.index(_jatékos_1_politikai_nézete))

        with cm2:
            játékos_2_neve = st.text_input("Játékos 2 neve", value=get_query_param("player_2_name"))
            ellen_index = 1 - options.index(játékos_1_politikai_nézete)
            játékos_2_politikai_nézete = st.selectbox(
                "Játékos 2 politikai nézete",
                options,
                index=ellen_index,
                disabled=True
            )

        st.divider()
        # Módosított kód:
            
        st.session_state.rounds = st.number_input("Körök száma", min_value=1, max_value=10, step=1)
        st.session_state.rounds_current = 1

        mellette_vagy_ellene = get_query_param("side")
        if mellette_vagy_ellene == "_":
            mellette_vagy_ellene = "Mellette"
            
        mellette_vagy_ellene = st.radio(
            "Minden körben mellette vagy ellene érveltek?",
            ("Mellette", "Ellene"),
            index=0 if mellette_vagy_ellene == "Mellette" else 1
        )

        # Set query parameters for state sharing / bookmarking
        set_query_param("player_1_name", játékos_1_neve)
        st.session_state.player_1_name = játékos_1_neve
        set_query_param("player_1_view", játékos_1_politikai_nézete)
        st.session_state.player_1_view = játékos_1_politikai_nézete
        set_query_param("player_2_name", játékos_2_neve)
        st.session_state.player_2_name = játékos_2_neve
        set_query_param("player_2_view", játékos_2_politikai_nézete)
        st.session_state.player_2_view = játékos_2_politikai_nézete
        set_query_param("rounds", st.session_state.rounds)
        # st.session_state.rounds = korok_szama
        set_query_param("side", mellette_vagy_ellene)
        st.session_state.side = mellette_vagy_ellene
        set_query_param("player_1_points", 0)
        st.session_state.player_1_points = 0
        set_query_param("player_2_points", 0)
        st.session_state.player_2_points = 0

        if st.button("Játék indítása"):
            set_query_param("page", "game")
            st.session_state._init_game = True
            st.rerun()

    elif new_page == "game":
        if st.session_state.get("_init_game", False):
            st.session_state.cards = read_in_cards()
            st.session_state._init_game = False

        if "cards" not in st.session_state:
            st.warning("Először állítsd be a játékot a Beállítások fülön!")
            st.stop()
        else:
            game_logic()

    elif new_page == "card_ideas":
        show_all_cards()

main()



