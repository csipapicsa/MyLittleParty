import streamlit as st
from time import sleep

with st.spinner("**BIG SPINNER**"):
    sleep(3)
    st.success("Done!")

with st.spinner("# fucking big spinner"):
    sleep(3)
    st.success("Done!")

with st.spinner("### Gondolkodok nagyon, kb 10 másodperc..."):
    sleep(3)
    st.success("Done!")