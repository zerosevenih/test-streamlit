
from urllib.error import URLError

import pandas as pd
import pydeck as pdk
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Nimbus Sans"]

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

    st.write("")
    # Non-interactive elements return a placeholder to their location
    # in the app. Here we're storing progress_bar to update it later.
    # progress_bar = st.sidebar.progress(0)

    # These two elements will be filled in later, so we create a placeholder
    # for them using st.empty()
    #frame_text = st.sidebar.empty()
    #image = st.empty()



st.set_page_config(page_title="Capacity estimation error calculator", page_icon="")
st.markdown("# Capacity estimation error calculator")
st.write("This calculator can be used to estimate the expected error on the estimated capacity. The error can be caused by different effects.")
st.write("Please choose SOC range for the estimation as well as errors to consider in the sidbar")
col1, col2 = st.sidebar.columns(2)
soc_max = col1.number_input("Upper SOC (%):", value=90, placeholder="Type a number...",key="soc_max")
soc_min = col2.number_input("Lower SOC (%):", value=10, placeholder="Type a number...",key="soc_min")

col1a, col2a = st.sidebar.columns(2)
err_max = col1a.number_input("Voltage error (mV):", value=10, placeholder="Type a number...",key="err_max")
err_min = col2a.number_input("Voltage error (mV):", value=10, placeholder="Type a number...",key="err_min")

state_hysteresis = st.sidebar.toggle("hysteresis error")

col1b, col2b = st.sidebar.columns(2)
state_tcv = col1b.toggle("temperature dependency OCV")
if state_tcv==True:
    val_tcv = col2b.number_input("Voltage error (mV):", value=10, placeholder="Type a number...",key="val_tcv")
else:
    val_tcv=0

col1b, col2b = st.sidebar.columns(2)
state_relaxation = col1b.toggle("relaxation behaviour")
if state_relaxation==True:
    val_relax = col2b.number_input("Voltage error (mV):", value=10, placeholder="Type a number...",key="val_relax")
else:
    val_relax=0


ocv_max=np.interp(soc_max,soc,ocvmean)
ocv_min=np.interp(soc_min,soc,ocvmean)
if state_hysteresis:
    err_hys_max_up=soc_max-np.interp(ocv_max,ocvcha,soc)
    err_hys_max_lo=soc_max-np.interp(ocv_max,ocvdis,soc)
    err_hys_min_up=soc_min-np.interp(ocv_min,ocvcha,soc)
    err_hys_min_lo=soc_min-np.interp(ocv_min,ocvdis,soc)
else:
    err_hys_max_up, err_hys_max_lo,err_hys_min_up, err_hys_min_lo =0,0,0,0

#st.write(str(err_hys_min_lo))

err_max=err_max+val_tcv+val_relax
err_min=-err_min-val_tcv-val_relax

soc_max_err1=np.interp(ocv_max+err_max/1000,ocvmean,soc)-err_hys_max_lo
soc_max_err2=np.interp(ocv_max-err_max/1000,ocvmean,soc)-err_hys_max_up

soc_min_err1=np.interp(ocv_min+err_min/1000,ocvmean,soc)-err_hys_min_lo
soc_min_err2=np.interp(ocv_min-err_min/1000,ocvmean,soc)-err_hys_min_up

#st.write(str(err_hys_min_up))


st.write("## Output:")
output1a, output1b = st.columns(2)
output1a.latex("\Delta SOC_{true}="+str(round(soc_max-soc_min,2))+"\,\%")
output1a.latex("\Delta SOC_{max}="+str(-round(np.min([soc_min_err1,soc_min_err2])-np.max([soc_max_err1,soc_max_err2]),2))+"\,\%")
output1a.latex("\Delta SOC_{min}="+str(-round(np.max([soc_min_err1,soc_min_err2])-np.min([soc_max_err1,soc_max_err2]),2))+"\,\%")
c=(soc_max-soc_min)/(soc_max-soc_min)
output1b.latex("C_{true}="+str(round(c,2))+"\,Ah")
c_max=abs((np.min([soc_min_err1,soc_min_err2])-np.max([soc_max_err1,soc_max_err2]))/(soc_max-soc_min))
output1b.latex("C_{max}="+str(round(c_max,2))+"\,Ah")
c_min=abs((np.max([soc_min_err1,soc_min_err2])-np.min([soc_max_err1,soc_max_err2]))/(soc_max-soc_min))
output1b.latex("C_{min}="+str(round(c_min,2))+"\,Ah")
output1b.latex("\Delta C=±"+str(round((abs(c-c_min)/c)*100,2))+"\,\%")
if (abs(c-c_min)/c)*100>5:
    st.write("⚠️Warning: The error in the capacity estimaten exceeds 5%. This can be problematic, since the ageing related capacity degree has a value range from 20-30% (SOH=70-80%)",color='r')

st.write("## Visualisation:")

fig =plt.figure()
fig.patch.set_facecolor('#0E1117')
ax = fig.add_subplot(111)
ax.plot(soc,ocvmean,color='black')
if state_hysteresis:
    ax.plot(soc,ocvdis,color='r')
    ax.plot(soc,ocvcha,color='g')
ax.scatter(soc_max,ocv_max,marker='x', color='red')
ax.scatter(soc_min,ocv_min,marker='x', color='red')
ax.axvline(x=soc_min_err1,color='r',linestyle='--')
ax.axvline(x=soc_min_err2,color='r',linestyle='--')
ax.axvline(x=soc_max_err1,color='r',linestyle='--')
ax.axvline(x=soc_max_err2,color='r',linestyle='--')

ax.set_xlabel('SOC in (%)')
ax.set_ylabel('U in (V)')
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.grid(which='both', color='grey', linewidth=0.4)
#ax.minorticks_on()
ax.set_facecolor('#EBEBEB')
st.pyplot(fig)

run_calc()

#show_code(run_calc)
