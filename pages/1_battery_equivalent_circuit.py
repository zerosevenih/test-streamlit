
from urllib.error import URLError

import pandas as pd
import pydeck as pdk

import streamlit as st
from streamlit.hello.utils import show_code


def run_calc() -> None:

    # Interactive Streamlit elements, like these sliders, return their value.
    # This gives you an extremely simple interaction model.

    st.write("Calculate...")
    # Non-interactive elements return a placeholder to their location
    # in the app. Here we're storing progress_bar to update it later.
    # progress_bar = st.sidebar.progress(0)

    # These two elements will be filled in later, so we create a placeholder
    # for them using st.empty()
    #frame_text = st.sidebar.empty()
    #image = st.empty()



st.set_page_config(page_title="Battery (st.set_page_config.page_title)", page_icon="📹")
st.markdown("# This is a equivalent circuit simulator")
st.sidebar.header("Simulate for current response")
st.write(
    "result"
)

import numpy as np
import matplotlib.pyplot as plt

R0 = st.sidebar.slider("value of R0", 0.0, 1.0, 0.001, 0.03)
Rc = st.sidebar.slider("value of R1", 0.0, 0.1, 0.001,0.005)
C = st.sidebar.slider("value of C1", 0, 10000, 10,1000)


# Parameters (you can adjust these values)
OCV = 3.7  # Open-circuit voltage (V)

# Time settings
dt = 0.1  # Time step (seconds)
t_end = 50  # End time (seconds)
time = np.arange(0, t_end, dt)

# Create the current profile
current = np.zeros(len(time))
idx = np.where(np.logical_and(time >= 10, time <= 30))
current[idx] = 1.0  # 10 seconds of 1A current

# Initialize voltage and state variables
voltage = np.zeros(len(time))
voltage[0] = OCV

# Simulate the Thevenin model
urc = np.zeros(len(time))
for i in range(1, len(time)):
    urc[i] = np.exp(-dt / (Rc * C)) * urc[i - 1] + Rc * np.exp(-dt / (Rc * C)) * current[i]
    voltage[i] = OCV + current[i] * R0 + urc[i]

# Plot the voltage response
fig =plt.figure()
fig.patch.set_facecolor('#0E1117')
ax = fig.add_subplot(111)
ax.plot(time, voltage, label="Battery Voltage",color='k')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.grid(which='both', color='grey', linewidth=0.4)
#ax.minorticks_on()
ax.set_facecolor('#EBEBEB')
ax.legend()
st.pyplot(fig)

# Plot the current response
fig =plt.figure()
fig.patch.set_facecolor('#0E1117')
ax = fig.add_subplot(111)
ax.plot(time, current, label="Battery Voltage",color='k')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.grid(which='both', color='grey', linewidth=0.4)
#ax.minorticks_on()
ax.set_facecolor('#EBEBEB')
ax.legend()
st.pyplot(fig)


run_calc()

#show_code(run_calc)
