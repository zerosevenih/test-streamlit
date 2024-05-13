
from urllib.error import URLError

import pandas as pd
import pydeck as pdk
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
import matplotlib.pyplot as plt

arr = np.loadtxt("ocv.csv", delimiter=",")
soc=arr[:,0]
ocvdis=arr[:,1]
ocvmean=arr[:,2]
ocvcha=arr[:,3]

def run_calc() -> None:

    # Interactive Streamlit elements, like these sliders, return their value.
    # This gives you an extremely simple interaction model.
    #a = st.sidebar.slider("value of R0", 0, 10, 1, 1)
    #b = st.sidebar.slider("value of R1", 0, 10, 3)
    #c = st.sidebar.slider("value of C1", 0, 10, 3)

    st.write("Calculate...")
    # Non-interactive elements return a placeholder to their location
    # in the app. Here we're storing progress_bar to update it later.
    # progress_bar = st.sidebar.progress(0)

    # These two elements will be filled in later, so we create a placeholder
    # for them using st.empty()
    #frame_text = st.sidebar.empty()
    #image = st.empty()



st.set_page_config(page_title="Battery (st.set_page_config.page_title)", page_icon="📹")
st.markdown("# SOH Estimation Error Calculator")
st.write(
    "result"
)

fig =plt.figure()
plt.plot(soc,ocvmean)
st.pyplot(fig)

run_calc()

#show_code(run_calc)
