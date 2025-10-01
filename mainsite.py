import streamlit as st

from functions import get_query_param, set_query_param, read_in_cards, show_all_cards, read_in_versions, disable_scrolling, get_and_generate_all_guide_cards, remove_leading_and_ending_space
from pages import game_logic
from time import sleep
import random

import streamlit.components.v1 as components

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

### 🎭 Utasítás-kártyák (opcionális)

Extra kihívásért bekapcsolhatod az **utasítás-kártya rendszert**! 

- **Hogyan működik?** A beállításoknál egy csúszkával állíthatod be, hogy mekkora eséllyel kapjon a játékos véletlenszerű utasítást minden körben (0-100%).
- **Mi az utasítás?** Egy retorikai feladat, amit be kell építened az érvelésedbe. Például: *"Hivatkozz a pápára!"*, *"Hibáztatd az oroszokat!"*, *"Légy szarkasztikus Trumppal!"*
- **Miért jó?** Kiszámíthatatlanná és viccesebbé teszi a játékot, mert váratlan irányokba kell terelned az érvelésedet.
- **Pontozás:** Az utasítások nem adnak extra pontot – de ha ügyesen használod őket, meggyőzőbb lehetsz!

💡 *Tipp:* Kezdőknek 20-30% esély ajánlott, haladóknak 50-70% már komoly kihívás!


---

### 🔁 A játék menete

1. **Beállítások:**
   - Állítsátok be a játékosok neveit és nézeteit (balos vagy jobbos).
   - Döntsétek el, hány kört játszotok (1–10).
   - Állítsátok be, mennyi idő áll rendelkezésre az érvelésre (15, 30, 45, 60 másodperc)
   - Válasszátok ki, hogy minden körben a játékosok **a téma mellett vagy ellene érvelnek**. Ez végig ugyanaz marad.

2. **Körök:**
   - Minden kör elején a játék húz egy kampánykártyát.
   - Mindkét játékos érvel (mellette vagy ellene) ameddig az ideje engedi. Mindkét játékos érvel a témára.
      - Ha be van kapcsolva, véletlenszerűen kaphat a játékos egy utasítás-kártyát is.
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

- A pontozás súlyozása és a kártyák tartalma feltöltés alatt áll, és a játék folyamatosan fejlődik. Lehet, hogy a játék során találkozni fogtok hibákkal, vagy olyan kártyákkal, amelyek teljesen nem illenek a játékba. Ez van, írjatok ilyenkor.

###### Ötleted vagy visszajelzésed van?  
Írd meg a [GitHub-oldalon](https://github.com/csipapicsa/MyLittleParty/discussions), a [Discord szerveren](https://discord.gg/AtnQJ6YcYA), vagy küldd el e-mailben: **gergo pont gyori pont project[kukac]gmail.com**

---
"""

st.set_page_config(
    page_title="Az én kicsi pártom",
    page_icon="🗳️",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://www.facebook.com/mounitarsasjatek",
        "Report a bug": "https://discord.gg/AtnQJ6YcYA",
        "About": """
### 🎲 Az én kicsi pártom

Egy szatirikus politikai társasjáték, ahol kampánytémák mentén kell érvelned – akár a saját nézeteiddel szembemenve is.

###### Ötleted vagy visszajelzésed van?  
Írd meg a [GitHub-oldalon](https://github.com/csipapicsa/MyLittleParty/discussions),  
a [Discord szerveren](https://discord.gg/AtnQJ6YcYA),  
vagy küldd el e-mailben: **gergo.pont.gyori.pont.project[kukac]gmail.com**
        """
    }
)





def init_variables():
    if "init_variables" not in st.session_state:
        st.session_state.init_variables = True
        st.session_state.new_game = True
        st.session_state.times_up = False
        st.session_state.rounds_current = 1
        st.session_state.player_1_points = 0
        st.session_state.player_2_points = 0
        st.session_state._init_game = False
        st.session_state.player_dictionary = {  "player_1": {"name": "Player 1", "points": 0, "view": "Balos"},
                                                "player_2": {"name": "Player 2", "points": 0, "view": "Jobbos"}}
        st.session_state.guide_lapok = get_and_generate_all_guide_cards()
        st.session_state.get_random_text = False
        st.session_state.get_random_text_chance = 100
        st.session_state.jatek_gep_ellen = False
        try:
            del st.session_state["ai_answer_generated"]
        except Exception:
            pass


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

def on_player1_view_change():
    st.session_state.player_1_view_state = st.session_state.player_1_view_selectbox
    set_query_param('player_1_view', st.session_state.player_1_view_state)
    ellen_state = "Jobbos" if st.session_state.player_1_view_state == "Balos" else "Balos"
    set_query_param('player_2_view', ellen_state)

@st.fragment
def main():
    st.markdown("<div id='top'></div>", unsafe_allow_html=True)
    st.markdown("#### Az én kicsi pártom kártyajáték - teszt oldal")
    
    tab_names = ["Szabályok", "Beállítások", "Játék", "Kártya ötletek"]
    tab_keys = ["szabaly", "settings", "game", "card_ideas"]

    init_variables()
    disable_scrolling()

    font_size = 12
    st._config.set_option(f'theme.baseFontSize', font_size) # type: ignore

    # Get page from query, default to "szabaly"
    page = get_query_param("page")
    if page not in tab_keys:
        page = "szabaly"

    selected_index = tab_keys.index(page)
    current_site = tab_names[selected_index]

    # st.markdown("""
    # <style>
    #     div[data-testid="stSegmentedControl"] {
    #         display: flex;
    #         justify-content: center;
    #     }
    #     div[data-testid="stSegmentedControl"] > div {
    #         margin: 0 auto;
    #     }
    # </style>
    # """, unsafe_allow_html=True)

    # selected_tab = st.segmented_control(
    #     label="Válassz lapot:",
    #     options=tab_names,
    #     default=current_site,
    #     selection_mode="single",
    #     label_visibility="collapsed",
    # )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_tab = st.segmented_control(
            label="Válassz lapot:",
            options=tab_names,
            default=current_site,
            selection_mode="single",
            label_visibility="collapsed",
        )

        # Update query param when user changes tab
    if selected_tab is not None and selected_tab in tab_names:
        new_page = tab_keys[tab_names.index(selected_tab)]
        if new_page != page:
            set_query_param("page", new_page)
            st.rerun()
    else:
        new_page = page  # Keep current page if selection is invalid

    
    # Content logic
    if new_page == "szabaly":
        read_in_versions()
        st.markdown(szabaly)
    elif new_page == "settings":
        st.markdown("#### Beállítások")
        options = ["Balos", "Jobbos"]

        cm1, cm2 = st.columns(2)
        
        with cm1:
            játékos_1_neve = st.text_input("Játékos 1 neve", value=get_query_param("player_1_name"))
            játékos_1_neve = remove_leading_and_ending_space(játékos_1_neve)
            
            # Initialize session state only once
            if "player_1_view_state" not in st.session_state:
                _jatékos_1_politikai_nézete = get_query_param("player_1_view")
                if _jatékos_1_politikai_nézete == "_":
                    _jatékos_1_politikai_nézete = "Balos"
                st.session_state.player_1_view_state = _jatékos_1_politikai_nézete

            játékos_1_politikai_nézete = st.selectbox(
                "Játékos 1 politikai nézete", 
                options, 
                index=options.index(st.session_state.player_1_view_state),
                key="player_1_view_selectbox",
                on_change=on_player1_view_change
            )

        # st.warning("Még nem megy az ai mód")
        jatek_gep_ellen = st.toggle("Játék az AI ellen", 
                            value=get_query_param("gep_ellen", return_type="bool"),
                            help="Ha ezt választod, akkor a játékos 2 szerepét az AI fogja betölteni (amíg van ingyenes token).",
                            key="gep_ellen")
        
        if jatek_gep_ellen and get_query_param("player_2_name") == "":
            nevek = ["Józsi", "Pisti", "Béci", "Renátó", "Lajoska", "Kati", "Erzsike"]
            # choose a random name
            játékos_2_neve = random.choice(nevek)
            set_query_param("player_2_name", f"AI {játékos_2_neve}")

        if jatek_gep_ellen != st.session_state.jatek_gep_ellen:
            st.session_state.jatek_gep_ellen = jatek_gep_ellen
            set_query_param("gep_ellen", "true" if jatek_gep_ellen else "false")
            # st.rerun()

        with cm2:
            játékos_2_neve = st.text_input("Játékos 2 neve", value=get_query_param("player_2_name"))
            játékos_2_neve = remove_leading_and_ending_space(játékos_2_neve)
            ellen_index = 1 - options.index(st.session_state.player_1_view_state)
            key2 = f"player_2_view_selectbox_{ellen_index}"
            játékos_2_politikai_nézete = st.selectbox(
                "Játékos 2 politikai nézete",
                options,
                index=ellen_index,
                disabled=True,
                key=key2
            )
        
        current_rounds = get_query_param("rounds")
        if current_rounds == "_":
            current_rounds = 1
        else:
            current_rounds = int(current_rounds)

        if "rounds" not in st.session_state:
            st.session_state.rounds = 5  # default
        if "rounds_committed" not in st.session_state:
            st.session_state.rounds_committed = st.session_state.rounds

        # UI
        new_value = st.number_input("Körök száma", min_value=1, max_value=10, value=st.session_state.rounds_committed)

        if new_value != st.session_state.rounds_committed:
            st.session_state.rounds_committed = new_value
            st.session_state.rounds = new_value
            set_query_param("rounds", new_value)
            st.rerun()  # <- required for immediate effect


        st.session_state.erveles_time = st.select_slider(label="Hány másodpercig akartok érvelni?",
                                                         options=[15, 30, 45, 60])
        
        set_query_param("erveles_time", st.session_state.erveles_time)

        # Detect change


        st.session_state.rounds_current = 1

        # Initial default (only once)
        if "side" not in st.session_state:
            st.session_state.side = get_query_param("side") or "Mellette"

        # Show radio
        new_side = st.radio(
            "Minden körben mellette vagy ellene érveltek?",
            ("Mellette", "Ellene"),
            index=0 if st.session_state.side == "Mellette" else 1
        )

        st.divider()
        st.write("##### Véletlen utasítások játékmód:")
        st.write("A csúszka beállítja, hogy **mekkora eséllyel kapsz véletlenszerű utasítást** minden körben. Ha 0-ra van állítva, nem kapsz utasítást. Minél magasabb az érték, annál nagyobb az esély, hogy kapj egyet. Az utasítást bele kell szőnöd az érvelésedbe.")
        esely_a_random_textre = st.slider(label="Véletlen utasítások utasítások esesélye (%)", 
                                          min_value=0, 
                                          max_value=100, 
                                          step=1,
                                          value=get_query_param("get_random_text_chance", return_type="int"))
        

        if esely_a_random_textre > 0:
            st.session_state.get_random_text = True
            # st.session_state.get_random_text_chance = esely_a_random_textre


        if esely_a_random_textre != st.session_state.get_random_text_chance:
            # st.info("esely_a_random_textre")
            # st.info(esely_a_random_textre)
            # sleep(5)
            st.session_state.get_random_text_chance = esely_a_random_textre
            set_query_param("get_random_text_chance", esely_a_random_textre)
            st.rerun()  # <- required for immediate effect
        
        st.divider()

        # Detect change and rerun
        if new_side != st.session_state.side:
            st.session_state.side = new_side
            set_query_param("side", new_side)
            st.rerun()


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
        set_query_param("side", st.session_state.side)
        st.session_state.side = st.session_state.side
        set_query_param("player_1_points", 0)
        st.session_state.player_1_points = 0
        set_query_param("player_2_points", 0)
        st.session_state.player_2_points = 0

        if st.button("Játék indítása"):
            st.session_state.new_game = False
            set_query_param("page", "game")
            st.session_state._init_game = True
            try:
                del st.session_state.current_card
            except Exception:
                pass
            st.rerun()

    elif new_page == "game":
        # st.info('no?')
        if st.session_state.get("_init_game", False):
            # set_query_param("rounds_current", 0)
            st.session_state.cards = read_in_cards()
            st.session_state._init_game = False

        if "cards" not in st.session_state:
            st.warning("Először állítsd be a játékot a Beállítások fülön!")
            st.stop()
        else:
            game_logic()

    elif new_page == "card_ideas":
        show_all_cards()

disable_scrolling()
main()



