import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px

from staff_dashboard_metrics import summary_metrics, position_metrics, unit_metrics, office_metrics, service_years_metrics, service_days_metrics, race_unique_metrics, race_total_metrics, gender_metrics


# # --- Configure Streamlit page settings --- 
# jcpao_logo = Path("assets/logo/jcpao_logo_500x500.png")

# # --- JCPAO Streamlit page logo --- 
# st.logo(jcpao_logo, size="large", link="https://www.jacksoncountyprosecutor.com")

# --- Sidebar Filter functions --- 

with st.sidebar:
    st.title("Jackson County Prosecuting Attorney's Office")
    st.write("***Staff Dashboard***")
    st.divider()
    # st.write("Please use navigate the JCPAO Staff Dashboard to view personnel information all active JCPAO staff.")
    st.write("Navigate the JCPAO Staff Dashboard to learn more about the composition of the Office!")
    st.divider()
    st.write("To securely exit portal, logout or just exit page:")
    # Logout 
    logout = st.button(
        label="Logout",
        key="logout",
        on_click=lambda: st.session_state.clear(), # Clear session state
        type="secondary",
        icon=":material/logout:"
    )

# --- Run page --- 
st.title("Staff Dashboard")

summary_metrics()

tabs = st.tabs(["Job Position", "Assigned Unit", "Office Location", "Service Duration", "Race/Ethnicity", "Gender"])

with tabs[0]:
    position_metrics()

with tabs[1]:
    unit_metrics()

with tabs[2]:
    office_metrics()

with tabs[3]:

    # ----- UI Title -----
    st.subheader("📈 JCPAO Staff by Service Duration")
    unit = st.radio("Select unit of measurement:", ["Years", "Days"], horizontal=True)
    st.divider()
    if unit == "Years":
        service_years_metrics() # st.session_state["login_email"]
    elif unit == "Days":
        service_days_metrics() # st.session_state["login_email"]

with tabs[4]:

    # ----- Title -----
    st.subheader("🌍 JCPAO Staff by Race/Ethnicity")

    race_metrics = st.columns(2)
    with race_metrics[0]:
        race_unique_metrics()
    with race_metrics[1]:
        race_total_metrics()

with tabs[5]:
    gender_metrics()