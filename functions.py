import streamlit as st
import pandas as pd
import time


def clock_timer(SECONDS):
    ph = st.empty()
    for secs in range(SECONDS ,0,-1):
        mm, ss = secs//60, secs%60
        ph.metric("Visszaszámlálás", f"{mm:02d}:{ss:02d}")
        time.sleep(1)

    ph.metric("Visszaszámlálás", "00:00")

    return True

def read_in_versions():
    # readin versions.txt content line by line and write it
    with open("versions.txt", "r", encoding="utf-8") as file:
        versions = file.readlines()
    versions = [line.strip() for line in versions if line.strip()]
    
    # Assuming 'st.write' is a function available in your environment (e.g., Streamlit)
    # If not, you can replace it with 'print()' for console output.
    for line in versions:
        st.write(line) 

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