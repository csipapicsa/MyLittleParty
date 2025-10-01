from google import genai
# import google.generativeai as genai

import streamlit as st

def get_answer(prompt):
    try:
        with st.spinner("# Gondolkodok nagyon, kb 10 másodperc..."):
            client = genai.Client(api_key=st.secrets["API_FREE_KEY_GEMINI"])

            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
        return response.text
    except Exception as e:
        st.error(f" Valami baj van, egész pontosan ez? \n\n {e}")
        return "Hát erre most nem tudok mit mondani. Elfogytak a szavak more."

def generate_prompt(tema, utasitas, erveles_iranya, politikai_oldal, ido, debug=False):
    # Szószám kalkuláció (átlag 2.5 szó/másodperc beszédnél)
    szo_per_masodperc = 2.5
    target_szo_szam = int(ido * szo_per_masodperc)
    szo_tartomany_min = int(target_szo_szam * 0.9)  # -10%
    szo_tartomany_max = int(target_szo_szam * 1.1)  # +10%

    # Prompt összeállítása
    prompt = f"""Te egy **{politikai_oldal.lower()} politikus** vagy egy vitajátékban.

    **A játék célja:** Meggyőző érvelés a megadott témában, hogy szavazatokat szerezz.

    **Fontos szabályok:**
    - Rövid, tömör érvelés (max {ido} másodperc felolvasási idő, kb. {szo_tartomany_min}-{szo_tartomany_max} szó)
    - Kampány-stílusú beszéd (emotív, meggyőző, néha szatirikus)
    - A politikai oldaladat ({politikai_oldal}) képviseld, de kreatívan
    - Az utasítást kötelező beépíteni az érvelésbe

    ---

    **TÉMA:** {tema}

    **ÉRVELJ:** {erveles_iranya.upper()}

    **UTASÍTÁS:** {utasitas}

    ---

    **Feladatod:**
    Írj egy {ido} másodperces kampánybeszédet, amely:
    1. Érvel a téma {erveles_iranya}
    2. {politikai_oldal} nézőpontból közelít
    3. Beépíti az utasítást: "{utasitas}"
    4. Meggyőző, kampányszerű, esetleg humoros/szatirikus

    **Fontos:** Ne magyarázd el mit csinálsz, csak add meg a beszédet! Ne írj meta-kommenteket!

    Beszéd:"""

    if debug:
        st.info("generate_prompt() debug")
        st.info(f"Prompt: {prompt}")


    return prompt
