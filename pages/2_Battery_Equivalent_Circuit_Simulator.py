
from urllib.error import URLError

import pandas as pd
import pydeck as pdk

import streamlit as st
from streamlit.hello.utils import show_code


def run_calc() -> None:

    # Interactive Streamlit elements, like these sliders, return their value.
    # This gives you an extremely simple interaction model.

    st.write("")
    # Non-interactive elements return a placeholder to their location
    # in the app. Here we're storing progress_bar to update it later.
    # progress_bar = st.sidebar.progress(0)

    # These two elements will be filled in later, so we create a placeholder
    # for them using st.empty()
    #frame_text = st.sidebar.empty()
    #image = st.empty()



st.set_page_config(page_title="Battery Equivalent Circuit Simulator", page_icon="🔋")
st.markdown("# This is an equivalent circuit simulator")
st.sidebar.header("Model parameters")
st.write('The influence of the open circuit voltage change due to the state-of-charge change because of the current pulse is currently not depicted.')


import numpy as np
import matplotlib.pyplot as plt

R0 = st.sidebar.slider("R0 in (mOhm)", 0.0, 1.0, 0.030, 0.001)
#Rc = st.sidebar.slider("R1 in (mOhm)", 0.0, 0.1, 0.005,0.001)
#C = st.sidebar.slider("C1 in (F)", 0, 10000, 500,10)

t_pulse=st.number_input('pulse duration (s):',0,100,20,key='t_pulse')
t_relax=st.number_input('relaxation duration (s):',0,3600,500,key='t_relax')
n_rc=st.number_input('number of rc elements:',0,10,1,key='n_rc')+1

if n_rc>1:
    Rn = np.zeros(n_rc)
    Cn = np.zeros(n_rc)
    Rn[1]=0.05
    Cn[1]=500
    for i in range(1, n_rc):
        if i==1:
            Rn[1]=0.05
            Cn[1]=500
        Rn[i] = st.sidebar.slider("R"+str(i)+" in (mOhm)", 0.0, 0.5, float(Rn[i-1]*1.25),0.001,key='R'+str(i))
        Cn[i] = st.sidebar.slider("C"+str(i)+" in (F)", 0.0, 10000.0, float(Cn[i-1]*1.25),10.0,key='C'+str(i))    

# Parameters (you can adjust these values)
OCV = 3.7  # Open-circuit voltage (V)

# Time settings
dt = 0.1  # Time step (seconds)
t_end = t_relax+10+t_pulse  # End time (seconds)
time = np.arange(0, t_end, dt)

# Create the current profile
current = np.zeros(len(time))
idx = np.where(np.logical_and(time >= 10, time <= 10+t_pulse))
current[idx] = 1.0  # 10 seconds of 1A current

# Initialize voltage and state variables
voltage = np.zeros(len(time))
voltage[0] = OCV

# Simulate the Thevenin model
urc = np.zeros([len(time),n_rc])
for i in range(1, len(time)):
    if n_rc>0:
        for j in range(1,n_rc):
            urc[i,j] = np.exp(-dt / (Rn[j] * Cn[j])) * urc[i - 1,j] + Rn[j] * (1-np.exp(-dt / (Rn[j] * Cn[j]))) * current[i]
        voltage[i] = OCV + current[i] * R0 + np.sum(urc[i,:])
    else:
        voltage[i] = OCV + current[i] * R0


# Plot the voltage response
fig =plt.figure()
fig.patch.set_facecolor('#0E1117')
ax = fig.add_subplot(111)
if n_rc>0:
    for j in range(1,n_rc):
        ax.plot(time, urc[:,j]+OCV, label="RC"+str(j)+", tau="+str(round(Rn[j]*Cn[j],1))+"s")
ax.plot(time, OCV + current * R0,'k--', label="R0")
ax.plot(time, voltage, 'k:',label="Battery Voltage")
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
