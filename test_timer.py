import streamlit as st
import time

st.set_page_config()


def clock_timer(SECONDS):
    ph = st.empty()
    for secs in range(SECONDS ,0,-1):
        mm, ss = secs//60, secs%60
        ph.metric("Visszaszámlálás", f"{mm:02d}:{ss:02d}")
        time.sleep(1)

    ph.metric("Visszaszámlálás", "00:00")

    return True

clock_timer(10)

st.info("Time's up!")