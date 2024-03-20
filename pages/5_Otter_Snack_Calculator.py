
from urllib.error import URLError

import pandas as pd
import pydeck as pdk

import streamlit as st
from streamlit.hello.utils import show_code


def run_calc() -> None:

    # Interactive Streamlit elements, like these sliders, return their value.
    # This gives you an extremely simple interaction model.
    a = st.sidebar.slider("number of otters?", 0, 20, 1, 1)
    b = st.sidebar.slider("snacks per otter and day", 0, 10, 3)
    st.write("You need to provide ",str(a+b)," otter snacks today!")
    # Non-interactive elements return a placeholder to their location
    # in the app. Here we're storing progress_bar to update it later.
    # progress_bar = st.sidebar.progress(0)

    # These two elements will be filled in later, so we create a placeholder
    # for them using st.empty()
    #frame_text = st.sidebar.empty()
    #image = st.empty()



st.set_page_config(page_title="Animation Demo (st.set_page_config.page_title)", page_icon="📹")
st.markdown("# Otter Snack Amount Calculation")
st.sidebar.header("Otter Snack Calculator")
st.write(
    "Here you can find the amount of necessary otter snacks:"
)

run_calc()

show_code(run_calc)
