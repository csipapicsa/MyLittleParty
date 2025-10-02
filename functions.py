import streamlit as st
import pandas as pd
import time
import random
from itertools import product
from functions_ai import generate_prompt, get_answer


def remove_leading_and_ending_space(text: str):
    try:
        return text.strip()
    except Exception:
        return text

def disable_scrolling():
    """
    Disable scrolling on mobile device. Tested on Android. 
    """
    #st.info("Scrolling behavior is disabled. Use the scroll wheel or arrow keys to scroll the page. If you want to use the touchpad, please use two fingers to scroll.")


    # this guy doesnt work from 2025-09-10, fuck knwos why
    # st.markdown("""
    #     <style>
    #     body {
    #         overscroll-behavior: none;
    #     }
    #     </style>
    # """, unsafe_allow_html=True)

    # st.markdown("""
    #     <style>
    #     html, body, [data-testid="stAppViewContainer"] {
    #         overscroll-behavior: none !important;
    #         scroll-behavior: auto;
    #     }
    #     </style>
    # """, unsafe_allow_html=True)

    # this one is slighlt better probably, more resiliint for further releases. The previos one works for sure 


    # 2025-09-10
    # st.markdown("""
    #     <style>
    #     html, body, 
    #     [data-testid="stAppViewContainer"],
    #     .main,
    #     .stApp {
    #         overscroll-behavior: none !important;
    #         scroll-behavior: auto;
    #     }
    #     </style>
    # """, unsafe_allow_html=True)
    st.markdown("""
    <style>
        html, body {
            overscroll-behavior: none !important;
            scroll-behavior: auto !important;
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Prevent overscroll on all elements
            document.body.style.overscrollBehavior = 'none';
            document.documentElement.style.overscrollBehavior = 'none';
            
            // Find and update Streamlit containers
            const containers = document.querySelectorAll('[data-testid="stAppViewContainer"], .main, .stApp');
            containers.forEach(container => {
                container.style.overscrollBehavior = 'none';
            });
            
            // Prevent touchmove events that cause bounce
            document.addEventListener('touchmove', function(e) {
                if (e.target.closest('.main') || e.target.closest('[data-testid="stAppViewContainer"]')) {
                    // Allow scrolling within content but prevent overscroll
                    const element = e.target.closest('.main') || e.target.closest('[data-testid="stAppViewContainer"]');
                    const { scrollTop, scrollHeight, clientHeight } = element;
                    
                    if ((scrollTop === 0 && e.touches[0].clientY > e.touches[0].clientY) ||
                        (scrollTop + clientHeight >= scrollHeight && e.touches[0].clientY < e.touches[0].clientY)) {
                        e.preventDefault();
                    }
                }
            }, { passive: false });
        });
    </script>
    """, unsafe_allow_html=True)


def get_a_card(debug=False, print_info=False):
    """Véletlenszerű kártya kiválasztása a kártyák közül"""
    if "cards" not in st.session_state:
        st.session_state.cards = read_in_cards()

    # Csak egyszer vágjuk le a 10-es szeletet debug módban
    if debug and "debug_filtered" not in st.session_state:
        st.session_state.cards = st.session_state.cards.iloc[10:20].copy()
        st.session_state.debug_filtered = True  # Ne vágjuk újra minden híváskor

    if len(st.session_state.cards) == 0:
        st.warning("Elfogytak a kártyák!")
        return None

    # get a random card, and remove it from the deck
    card = st.session_state.cards.sample(1).iloc[0]
    # print(f"Kiválasztott kártya: {card['Kártya leírás HUN']}")
    st.session_state.cards = st.session_state.cards.drop(card.name)

    if debug:
        st.info("----")
        st.info(f"**Kiválasztott kártya:** `{card['Kártya leírás HUN']}`")
        st.info(f"**Maradék kártyák száma:** {len(st.session_state.cards)}")
        st.info(f"Maradék kártyák: {', '.join(st.session_state.cards['Kártya leírás HUN'].tolist())}")
        st.info("----")

    if print_info:
        st.info(f"Maradék kártyák száma: {len(st.session_state.cards)}")

    return card


def clock_timer(SECONDS):
    ph = st.empty()
    for secs in range(SECONDS ,0,-1):
        mm, ss = secs//60, secs%60
        ph.metric("Érvelj!", f"{mm:02d}:{ss:02d}")
        time.sleep(1)

    ph.metric("Letelt", "00:00")

    return True

# 2025-10-01: Új időzítő, mert jobb
# @st.dialog("⏳ Érvelés ideje", dismissible=False, width="small")
# def run_timer(seconds: int, 
#               topic_message: str, 
#               hogyan_message: str, 
#               extra_task_message: str):
    
#     topic_ph = st.empty()   # for dynamic text
#     extra_task_ph = st.empty()
#     hogyan_ph = st.empty()
#     timer_ph = st.empty()    # for the timer

#     if st.button("Indíccs", key="start_button", disabled=False):
#         for secs in range(seconds, 0, -1):
#             mm, ss = secs // 60, secs % 60
#             topic_ph.write(topic_message)
#             if extra_task_message != "":
#                 extra_task_ph.write(f'## {extra_task_message}')
#             hogyan_ph.write(hogyan_message)
#             timer_ph.metric(label="idő", value=f"{mm:02d}:{ss:02d}", label_visibility="hidden")
#             time.sleep(1)

#         timer_ph.metric(label="⏰ Letelt", value="00:00")
#         st.session_state.times_up = True
#         st.rerun()


@st.dialog("⏳ Érvelés ideje és részletei", dismissible=False, width="small")
def run_timer_human(seconds: int, 
              topic_message: str, 
              hogyan_message: str, 
              extra_task_message: str,
              ki_ervel_nev: str,
              second_player_ai: bool,
              politikai_oldal: str):
    
    
    ki_ervel = st.empty()
    topic_ph = st.empty()   # for dynamic text
    extra_task_ph = st.empty()
    hogyan_ph = st.empty()
    timer_ph = st.empty()    # for the timer

    ki_ervel.write(f'# *Aki érvel:* {ki_ervel_nev}')
    topic_ph.write(f'# {topic_message}')
    if extra_task_message != "":
        extra_task_ph.write(f'# {extra_task_message}')

    hogyan_ph.write(f'# {hogyan_message}')
    
    if st.button("Indulhat a kampánybeszéd", key="start_button", disabled=False):
        for secs in range(seconds, 0, -1):
            mm, ss = secs // 60, secs % 60
            timer_ph.metric(label="idő", value=f"{mm:02d}:{ss:02d}", label_visibility="hidden")
            time.sleep(1)

        timer_ph.metric(label="⏰ Letelt", value="00:00")
        st.session_state.times_up = True
        st.rerun()

# @st.dialog("⏳ Érvelés ideje és részletei", dismissible=False, width="small")
# def run_timer_ai(seconds: int, 
#               topic_message: str, 
#               hogyan_message: str, 
#               extra_task_message: str,
#               ki_ervel_nev: str,
#               second_player_ai: bool,
#               politikai_oldal: str):
    
#     # get current time, print inof
    
#     ki_ervel = st.empty()
#     topic_ph = st.empty()   # for dynamic text
#     extra_task_ph = st.empty()
#     hogyan_ph = st.empty()
#     timer_ph = st.empty()    # for the timer

#     ki_ervel.write(f'# Aki érvel: {ki_ervel_nev}')
#     topic_ph.write(topic_message)
#     if extra_task_message != "":
#         extra_task_ph.write(f'## {extra_task_message}')

#     hogyan_ph.write(hogyan_message)
#     prompt = generate_prompt(tema = topic_message, 
#                                 utasitas = extra_task_message,
#                                 erveles_iranya = hogyan_message,
#                                 politikai_oldal = politikai_oldal,
#                                 ido = seconds,
#                                 debug=False)
    
#     if not st.session_state.times_up:
#         from datetime import datetime
#         st.info("Times up?")
#         st.info(st.session_state.times_up)
        
#         st.info(f"Idő: {datetime.now().strftime('%H:%M:%S')}")
#         st.info("Getting the answer")
#         time.sleep(3)
#         answer = "this is it"
#         # answer = get_answer(prompt)
#     # time.sleep(5)
#     # answer = "Demo válasz"
#     st.markdown(f"**{answer}**")
    
#     if st.button("Elolvastuk", key="start_button", disabled=False):
#         st.session_state.times_up = True
#         st.rerun()


@st.dialog("⏳ AI Érvelése", dismissible=False, width="small")
def run_timer_ai(seconds: int, 
              topic_message: str, 
              hogyan_message: str, 
              retorikai_feladat: str,
              ki_ervel_nev: str,
              politikai_oldal: str,
              debug=False):
    
    st.write(f'# *Aki érvel:* {ki_ervel_nev}')
    st.write(f'# {topic_message}')
    if retorikai_feladat != "":
        st.write(f'# {retorikai_feladat}')
    st.write(f'# {hogyan_message}')
    
    # Generálás csak egyszer
    if "ai_answer_generated" not in st.session_state:
        prompt = generate_prompt(
            tema=topic_message, 
            retorikai_feladat=retorikai_feladat,
            erveles_iranya=hogyan_message,
            politikai_oldal=politikai_oldal,
            ido=seconds,
            debug=debug
        )

        # answer = "This is the answer"
        if debug:
            answer = "This is the answer"
        else:
            answer = get_answer(prompt)
        
        st.session_state.ai_answer = answer
        st.session_state.ai_answer_generated = True
            # NE LEGYEN ITT st.rerun()!
    
    # Válasz megjelenítése (már van session_state-ben)
    lines = st.session_state.ai_answer.split('\n')
    formatted_lines = ['# ' + line if line.strip() else '' for line in lines]
    answer_with_hashes = '\n'.join(formatted_lines)
    st.markdown(f"# A beszéd: \n\n {answer_with_hashes}")
    
    # Gomb ami bezárja
    if st.button("Elolvastuk", key="ai_done"):
        # Cleanup
        del st.session_state.ai_answer
        del st.session_state.ai_answer_generated
        st.session_state.times_up = True
        st.rerun()  # Most már OK a rerun, mert bezárjuk

def read_in_versions():
    # readin versions.txt content line by line and write it
    with open("versions.txt", "r", encoding="utf-8") as file:
        versions = file.readlines()
    versions = [line.strip() for line in versions if line.strip()]
    
    # Assuming 'st.write' is a function available in your environment (e.g., Streamlit)
    # If not, you can replace it with 'print()' for console output.
    for line in versions:
        st.write(line) 

def get_query_param(key, return_type="str"):
    try:
        value = st.query_params[key]

        if return_type == "str":
            return value
        elif return_type == "bool":
            return str(value).lower() in ["1", "true", "yes"]
        elif return_type == "int":
            return int(value)
        else:
            return value
    except KeyError:
        if return_type == "str":
            return ""
        elif return_type == "bool":
            return False
        else:
            return None
    
def set_query_param(key, value):
    if isinstance(value, bool):
        st.query_params[key] = "1" if value else "0"
    else:
        st.query_params[key] = str(value)

def read_in_cards():
    cards = pd.read_csv("Az én kicsi pártom - Kártyák.csv", skiprows=1)

    cards = cards[cards["online"] == "x"]
    cards = cards[["online", "Kártya leírás HUN", "Típus - HUN", "Jobbos bonus", "Balos Bonus"]]
    cards["Jobbos bonus"] = cards["Jobbos bonus"].astype(int)
    cards["Balos Bonus"] = cards["Balos Bonus"].astype(int)
    # Típus hun == kampány
    cards = cards[cards["Típus - HUN"] == "Kampány"]
    # st.table(cards)
    return cards

def show_all_cards():
    cards = pd.read_csv("Az én kicsi pártom - Kártyák.csv", skiprows=1)
    cards = cards[["Kártya leírás HUN", "Típus - HUN", "Jobbos bonus", "Balos Bonus"]]
    cards = cards[
    cards["Kártya leírás HUN"].notna() &
    (cards["Kártya leírás HUN"].str.strip() != "")
    ]
    
    cards["Jobbos bonus"] = cards["Jobbos bonus"].astype(int, errors='ignore')
    cards["Balos Bonus"] = cards["Balos Bonus"].astype(int, errors='ignore')
    st.markdown("### **Kártyák**")
    st.markdown("Csak úgy mutiba, hogy lásd, milyen kártyák vannak/lesznek a játékban.")
    st.dataframe(cards)


def extra_task_generator(chance=0.5):
    if random.random() < chance:
        extra_task = "Fogd a pápára"
        return extra_task
    else:
        return ""


def get_and_generate_all_guide_cards():
    cards = pd.read_csv("Az én kicsi pártom - Guide lapok.csv")
    cards = cards[["Guide", "Tárgya"]]
    guides = cards["Guide"].dropna().unique()
    targets = cards["Tárgya"].dropna().unique()
    combinations = [f"{g} {t}" for g, t in product(guides, targets)]
    guide_lapok = pd.DataFrame(combinations, columns=["Guide x Tárgya kombináció"])
    # guide_lapok = guide_lapok["Guide x Tárgya kombináció"].to_list()

    return guide_lapok

def get_a_random_guide_card():
        # get a random card, and remove it from the deck
    card = st.session_state.guide_lapok.sample(1).iloc[0]
    # print(f"Kiválasztott kártya: {card['Kártya leírás HUN']}")
    st.session_state.guide_lapok = st.session_state.guide_lapok.drop(card.name)

    return card.values[0]

def get_next_speaker():
    if "speakers_this_round" not in st.session_state:
        st.session_state.speakers_this_round = []

    already_spoken = st.session_state.speakers_this_round

    if len(already_spoken) == 0:
        next_speaker = random.choice(["player_1", "player_2"])
    elif len(already_spoken) == 1:
        next_speaker = "player_2" if already_spoken[0] == "player_1" else "player_1"
    else:
        return None  # mindketten beszéltek

    st.session_state.speakers_this_round.append(next_speaker)
    return next_speaker


def has_everyone_argued_this_round():
    """
    True, ha ebben a körben már ketten beszéltek.
    """
    return len(st.session_state.get("speakers_this_round", [])) >= 2


