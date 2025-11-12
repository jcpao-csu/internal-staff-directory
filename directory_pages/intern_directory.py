"""
File: intern_directory.py
Function: Streamlit page for active JCPAO interns
Author: Joseph Cho, ujcho@jacksongov.org
Date: June 9, 2025
"""

import streamlit as st
from pathlib import Path

# --- Configure Streamlit page settings --- 
jcpao_logo = Path("assets/logo/jcpao_logo_500x500.png")

# --- JCPAO Streamlit page logo --- 
st.logo(jcpao_logo, size="large", link="https://www.jacksoncountyprosecutor.com")


st.title("Intern Directory")

st.markdown("🚧 **Intern Directory is still under construction. Thank you for your patience!**")