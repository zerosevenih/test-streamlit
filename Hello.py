# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import matplotlib.pyplot as plt
import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Overview",
        page_icon=" 🔋",
    )

    st.write("# This is a battery web application for explaining battery behaviour with interactive tools.")

    st.sidebar.success("Please select tool from above")

    st.markdown(
        """
        👈 Please try a tool from the sidebar

        
    """
    )

    st.markdown('### Capacity Estimation Error Calculator')
    st.write('This tool can simulate the expected error in capacity estimation using  the OCV method. With the provided OCV-SOC curve and a given error (for  example, in the voltage measurement), the impact of this error on the  capacity estimation can be visualised.')

    st.markdown('### Battery Equivalent Circuit Simulator')
    st.write('This tool enables the simulation of the voltage response to a current pulse with an equivalent circuit model based on RC elements. The number of RC elements, their parameters, and pulse and relaxation duration can be chosen and altered.')



if __name__ == "__main__":
    run()
