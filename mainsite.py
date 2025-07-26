import streamlit as st

from functions import get_query_param, set_query_param, read_in_cards

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
    st.markdown("Most kezdődik a játék!")
    # choose a random card from the cards dataframe
    card = st.session_state.cards.sample().iloc[0]
    st.markdown(f"**Kártya leírás:** {card['Kártya leírás HUN']}")
    st.markdown(f"**Típus:** {card['Típus - HUN']}")
    st.markdown(f"**Jobbos bonus:** {card['Jobbos bonus']}")    

def main():
    st.title("Az én kicsi pártom kártyajáték - teszt oldal")

    tab_names = ["Szabályok", "Beállítások", "Játék"]
    tab_keys = ["szabaly", "settings", "game"]

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
            játékos_1_politikai_nézete = st.selectbox("Játékos 1 politikai nézete", options, index=options.index(get_query_param("player_1_view")))

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
        korok = get_query_param("rounds")
        if korok == "_":
            korok = 2
        else:
            korok = int(korok)
        korok_szama = st.number_input("Körök száma", min_value=1, max_value=100, value=korok)

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
        set_query_param("player_1_view", játékos_1_politikai_nézete)
        set_query_param("player_2_name", játékos_2_neve)
        set_query_param("player_2_view", játékos_2_politikai_nézete)
        set_query_param("rounds", korok_szama)
        set_query_param("side", mellette_vagy_ellene)

        if st.button("Játék indítása"):
            set_query_param("page", "game")
            st.session_state._init_game = True
            st.rerun()

    elif new_page == "game":
        st.markdown("## Játék indítása")
        if st.session_state._init_game:
            st.session_state.cards = read_in_cards()
            st.session_state._init_game = False
        game_logic()

main()



