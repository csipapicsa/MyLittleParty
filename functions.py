import streamlit as st
import pandas as pd

def teszt_gorgo():
    import streamlit as st

    # Próbáld meg telepíteni: pip install streamlit-scroll-to-top
    try:
        from streamlit_scroll_to_top import scroll_to_here
        SCROLL_PACKAGE_AVAILABLE = True
        st.success("✅ streamlit-scroll-to-top package elérhető!")
    except ImportError:
        SCROLL_PACKAGE_AVAILABLE = False
        st.error("❌ streamlit-scroll-to-top package nem elérhető!")
        st.info("Telepítsd: `pip install streamlit-scroll-to-top`")

    st.title("🔝 Streamlit Scroll Test")

    # Package elérhetőség check
    if SCROLL_PACKAGE_AVAILABLE:
        st.markdown("### Package működés teszt")
        
        # Step 1: Initialize scroll state in session_state
        if 'scroll_to_top' not in st.session_state:
            st.session_state.scroll_to_top = False
            
        if 'scroll_to_header' not in st.session_state:
            st.session_state.scroll_to_header = False
        
        # Step 2: Handle the scroll-to-top action
        if st.session_state.scroll_to_top:
            scroll_to_here(0, key='top')  # Scroll to the top instantly
            st.session_state.scroll_to_top = False  # Reset the state after scrolling
        
        # Step 3: Define scroll functions
        def scroll():
            st.session_state.scroll_to_top = True
            
        def scrollheader():
            st.session_state.scroll_to_header = True
        
        # Scroll gombok a tetején is
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("🔝 Scroll to Top (tetén)", on_click=scroll, key="top_button_1")
        with col2:
            if st.button("🔝 Scroll to Top 2 (tetén)", key="top_button_2"):
                st.session_state.scroll_to_top = True
                st.rerun()
        with col3:
            st.button("📍 Scroll to Header (tetén)", on_click=scrollheader, key="header_button_1")

    st.markdown("---")

    # Generate long content to test scrolling
    st.markdown("### 📄 Hosszú tartalom teszt")
    st.info("Görgess le, majd használd a scroll gombokat!")

    for i in range(100):
        if i == 25:
            if SCROLL_PACKAGE_AVAILABLE and st.session_state.scroll_to_header:
                scroll_to_here(0, key='header')  # Scroll to header
                st.session_state.scroll_to_header = False
            st.header("🎯 Header - ide is lehet scrollozni")
            st.markdown("**Ez a középső header, ide is tudsz scrollozni!**")
            
            # Header scroll gombok
            col1, col2 = st.columns(2)
            with col1:
                if SCROLL_PACKAGE_AVAILABLE:
                    st.button("🔝 Scroll to Top (közepe)", on_click=scroll, key="mid_top")
            with col2:
                if SCROLL_PACKAGE_AVAILABLE:
                    st.button("📍 Scroll to Header (közepe)", on_click=scrollheader, key="mid_header")
        
        elif i == 50:
            st.subheader("🏁 Félúton")
            st.info(f"Ez a {i+1}. sor - félúton vagyunk!")
            
        elif i == 75:
            st.subheader("🎮 Játék szimulálás")
            st.markdown("**Szimuláljuk a te játékodat:**")
            
            # Simulate game round
            with st.container():
                st.markdown("#### Kör 3/5")
                st.markdown("**Téma:** *Klímaváltozás elleni küzdelem*")
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                with col1:
                    votes1 = st.number_input("Játékos 1 szavazatai", 0, 5, 0, key=f"votes1_{i}")
                with col2:
                    votes2 = st.number_input("Játékos 2 szavazatai", 0, 5, 0, key=f"votes2_{i}")
                
                # Simulate vote submission
                if st.button("Szavazatok rögzítése", key=f"submit_{i}"):
                    if SCROLL_PACKAGE_AVAILABLE:
                        st.session_state.scroll_to_top = True
                        st.success("Szavazatok rögzítve! Scrollozunk a tetejére...")
                        st.rerun()
                    else:
                        st.warning("Scroll package nem elérhető - csak üzenet jelenik meg")
        
        else:
            st.text(f"📝 {i + 1}. sor: Ez egy hosszú teszt tartalom a scrollozáshoz...")

    # Bottom buttons
    st.markdown("---")
    st.markdown("### 🔚 Oldal vége")

    if SCROLL_PACKAGE_AVAILABLE:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("🔝 Scroll to Top (alul)", on_click=scroll, key="bottom_top")
        with col2:
            if st.button("🔝 Scroll to Top 2 (alul)", key="bottom_top_2"):
                st.session_state.scroll_to_top = True
                st.rerun()
        with col3:
            st.button("📍 Scroll to Header (alul)", on_click=scrollheader, key="bottom_header")

    # Debug info
    st.markdown("---")
    st.markdown("### 🐛 Debug Info")
    st.json({
        "scroll_package_available": SCROLL_PACKAGE_AVAILABLE,
        "scroll_to_top": st.session_state.get('scroll_to_top', False),
        "scroll_to_header": st.session_state.get('scroll_to_header', False),
        "session_state_keys": list(st.session_state.keys())
    })

    # Instructions
    st.markdown("---")
    st.markdown("""
    ### 📋 Használati útmutató

    **Ha a package elérhető:**
    1. Görgess le az oldalon
    2. Nyomd meg valamelyik "Scroll to Top" gombot
    3. Az oldal automatikusan a tetejére ugrik

    **Ha nem elérhető:**
    1. Telepítsd: `pip install streamlit-scroll-to-top`
    2. Indítsd újra a Streamlit alkalmazást
    3. Próbáld újra

    **A te játékodban:**
    ```python
    # A szavazatok rögzítése gombban:
    if st.button("Szavazatok rögzítése"):
        # ... a szavazási logika ...
        st.session_state.scroll_to_top = True
        st.rerun()
    ```
    """)

    # Installation command
    st.code("pip install streamlit-scroll-to-top", language="bash")

def get_query_param(key):
    try:
        return st.query_params[key]
    except KeyError:
        return "_"
    
def set_query_param(key, value):
    st.query_params[key] = value


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