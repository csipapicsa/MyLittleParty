import streamlit as st

from functions import get_query_param, set_query_param, read_in_cards, show_all_cards

szabaly = """
### 🎲 Az én kicsi pártom – Játékszabályok

**Leírás**  
Ez egy minimum három fővel játszható, tervezés alatt álló kártyajáték online verziója, amely a politikai nézetek és érvek játékos ütköztetésére épül. A játék során egy képzeletbeli jobbos vagy balos párt politikusának bőrébe bújva kampánytémákat húztok, és azok mellett vagy ellen kell érvelnetek – néha még a saját vagy választott politikai meggyőződésetekkel szembemenve is.

**Cél**  
Gyűjtsd a legtöbb szavazatot érveid meggyőző erejével! Aki a legtöbb pontot szerzi a játék végére, megnyeri a választásokat.

---

### 👥 Játékosok

- A játékhoz minimum három játékos szükséges.
- Az egyik játékos **baloldali**, a másik **jobboldali** nézetet képvisel. A többiek a szavazók szerepét töltik be. - 💡 *Tipp:* Akkor a legszórakoztatóbb, ha a saját meggyőződéseddel **ellentétes** oldalt választasz.


---

### 🃏 A kártyák

- Minden kártya egy politikai kampánytémát tartalmaz.
- A kártyákhoz pontszorzók is tartoznak, attól függően, hogy melyik oldal számára előnyös a téma, illetve hogy a játékos épp mellette vagy ellene érvel.  
  Például: egy baloldali nézőpontú játékos számára egy balos téma melletti érvelés nem jár szorzóval, de ha ugyanezen a téma mellett egy jobboldali játékos érvel meggyőzően, bónuszszorzót kap. Ugyanez fordítva is igaz: jobboldali nézőpontból egy jobbos téma ellen érvelve is szorzót kaphatsz, ha így is képes vagy szavazatokat szerezni.

---

### 🔁 A játék menete

1. **Beállítások:**
   - Állítsátok be a játékosok neveit és nézeteit (balos vagy jobbos).
   - Döntsétek el, hány kört játszotok (1–10).
   - Válasszátok ki, hogy minden körben a játékosok **a téma mellett vagy ellene érvelnek**. Ez végig ugyanaz marad.

2. **Körök:**
   - Minden kör elején a játék húz egy kampánykártyát.
   - Mindkét játékos röviden érvel szóban a játék beállítása szerint (mellette vagy ellene).
   - A választók szavaznak: mindenki 1 szavazatot adhat le.
   - A szavazatokból pontok keletkeznek az adott kártyán szereplő szorzók alapján.

3. **Pontozás:**
   - A játék automatikusan kiszámolja a pontokat.
   - A pontok körönként összeadódnak.

---

### 🏆 A játék vége

- Az utolsó kör után a játék automatikusan kiírja a nyertest.
- A győztes az, aki a legtöbb pontot szerezte.


### A szerő üzenete

- A pontozás súlyozása és a kártyák tartalma feltöltés alatt áll, és a játék folyamatosan fejlődik. Szóval szinte biztos, hogy a játék során találkozni fogtok hibákkal, vagy olyan kártyákkal, amelyek teljesen nem illenek a jétákba. 

###### Ötleted vagy visszajelzésed van?  
Írd meg a [GitHub-oldalon](https://github.com/csipapicsa/MyLittleParty/discussions), a [Discord szerveren](https://discord.gg/AtnQJ6YcYA), vagy küldd el e-mailben: **gergo pont gyori[kukac]gmail.com**

---
"""




import streamlit.components.v1 as components
def scroll_to_top():
    """Függvény az oldal tetejére való ugráshoz"""
    components.html("""
        <script>
            window.parent.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        </script>
    """, height=0)

@st.fragment
def game_logic():

    if "current_card" not in st.session_state:
        st.session_state.current_card = st.session_state.cards.sample().iloc[0]
        scroll_to_top()
        st.components.v1.html("""
            <script>
                window.parent.scrollTo(0, 0);
            </script>
        """, height=0)

    card = st.session_state.current_card
    # st.table(card)
    side = get_query_param('side')

    # if card["Típus - HUN"] == "Kampány":
    #     mode = "erveles"
    # else:
    #     mode = "reagalas"

    if side == "Mellette":
        jobbos_bonus = card['Jobbos bonus']
        balos_bonus = card['Balos Bonus']
        hogyan = "mellette"
    elif side == "Ellene":
        jobbos_bonus = card['Balos Bonus']
        balos_bonus = card['Jobbos bonus']
        hogyan = "ellene"
    # elif mode == "reagalas":
    #     # TODO 
    #     jobbos_bonus = card['Jobbos bonus']
    #     balos_bonus = card['Balos Bonus']
        # hogyan = "reagáljatok a kártyára"


    # choose a random card from the cards dataframe

    st.session_state.rounds = int(get_query_param("rounds"))

    st.markdown(f"#### Kör {st.session_state.rounds_current} / {st.session_state.rounds}")

    st.markdown(f"#### **Téma:** *{card['Kártya leírás HUN']}*")
    st.markdown(f"#### **Típus:** *{card['Típus - HUN']}*")
    
    st.divider()

    # if mode == "erveles":
    #     st.markdown(f" ### Érveljetek  {hogyan}! ")
    # else:
    #     st.markdown(f" ### Reagáljatok! ")

    st.markdown(f" #### Érveljetek  {hogyan}! ")    
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"#### **Balos szavazati bonus:** \n\n ### {balos_bonus} x")
    with c2:
        st.markdown(f"#### **Jobbos szavazati bonus:** \n\n ### {jobbos_bonus} x")

    st.divider()


    c1, c2 = st.columns(2)

    round_key_suffix = f"_round_{st.session_state.rounds_current}"
    if st.session_state.player_1_view == "Balos":
        with c1:
            szavazatok_player_1 = st.number_input(
                f"#### {st.session_state.player_1_name} szavazatai",
                min_value=0,
                max_value=5,
                value=0,
                key=f"player_1_votes{round_key_suffix}"
            )
        with c2:
            szavazatok_player_2 = st.number_input(
                f"#### {st.session_state.player_2_name} szavazatai",
                min_value=0,
                max_value=5,
                value=0,
                key=f"player_2_votes{round_key_suffix}"
            )
    else:
        with c1:
            szavazatok_player_2 = st.number_input(
                f"#### {st.session_state.player_2_name} szavazatai",
                min_value=0,
                max_value=5,
                value=0,
                key=f"player_2_votes{round_key_suffix}"
            )
        with c2:
            szavazatok_player_1 = st.number_input(
                f"#### {st.session_state.player_1_name} szavazatai",
                min_value=0,
                max_value=5,
                value=0,
                key=f"player_1_votes{round_key_suffix}"
            )


    st.divider()

    st.markdown("#### **Játékosok pontjai**")

    pontok_container = st.container()

    with pontok_container:
        c1, c2 = st.columns(2)
        if st.session_state.player_1_view == "Balos":
            with c1:
                _player_1_name = get_query_param("player_1_name")
                _player_1_points = get_query_param("player_1_points")
                st.markdown(f"#### **{_player_1_name}** ({st.session_state.player_1_view}): {_player_1_points} pont")

            with c2:
                _player_2_name = get_query_param("player_2_name")
                _player_2_points = get_query_param("player_2_points")
                st.markdown(f"#### **{_player_2_name}** ({st.session_state.player_2_view}): {_player_2_points} pont")

        else:
            with c1:
                _player_2_name = get_query_param("player_2_name")
                _player_2_points = get_query_param("player_2_points")
                st.markdown(f"#### **{_player_2_name}** ({st.session_state.player_2_view}): {_player_2_points} pont")

            with c2:
                _player_1_name = get_query_param("player_1_name")
                _player_1_points = get_query_param("player_1_points")
                st.markdown(f"#### **{_player_1_name}** ({st.session_state.player_1_view}): {_player_1_points} pont")

    # st.balloons()

    if st.button("Szavazatok rögzítése"):
        _temp_pont_1 = szavazatok_player_1 * jobbos_bonus
        _temp_pont_2 = szavazatok_player_2 * balos_bonus
        _current_player_1_points = get_query_param("player_1_points")
        _current_player_2_points = get_query_param("player_2_points")
        set_query_param("player_1_points", int(_current_player_1_points) + int(_temp_pont_1))
        set_query_param("player_2_points", int(_current_player_2_points) + int(_temp_pont_2))
        del st.session_state.current_card
        
        vote_keys_to_delete = [key for key in st.session_state.keys() if key.startswith(('player_1_votes', 'player_2_votes'))]
        for key in vote_keys_to_delete:
            del st.session_state[key]
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
            st.markdown(f"## **{st.session_state.player_1_name}** ({st.session_state.player_1_view}): {_player_1_points} pont")
            st.markdown(f"## **{st.session_state.player_2_name}** ({st.session_state.player_2_view}): {_player_2_points} pont")
            
            import time
            time.sleep(10)
            # st.stop()

        else:
            st.session_state.rounds_current += 1
            set_query_param("rounds_current", st.session_state.rounds_current)
            set_query_param("page", "game")

        st.rerun()





def main():
    st.markdown("#### Az én kicsi pártom kártyajáték - teszt oldal")

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
        st.markdown("#### Beállítások")
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
        
        current_rounds = get_query_param("rounds")
        if current_rounds == "_":
            current_rounds = 1
        else:
            current_rounds = int(current_rounds)
            
        st.session_state.rounds = st.number_input("Körök száma", min_value=1, max_value=10, step=1, value=current_rounds)
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
            try:
                del st.session_state.current_card
            except:
                pass
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



