import streamlit as st
from pathlib import Path
from datetime import datetime


# --- Sidebar Filter functions --- 

with st.sidebar:

    # Select options: position / unit / location / birthday month 
    st.title("Jackson County Prosecuting Attorney's Office")
    st.write("***Home Page***")
    st.divider()
    st.write("Welcome to the JCPAO Portal! Please use the tabs at the top of the page to navigate through directories and other office resources. If you have a feature or request to add, please contact [Joseph Cho](mailto:ujcho@jacksongov.org).")
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

st.markdown("<h1 style='text-align: center; color: black;'>Welcome to the JCPAO Directory</h1>", unsafe_allow_html=True)
st.divider()

# Home bulletin
st.header("Home Bulletin", divider="gray")

# Init counter
counter = 0

# Get len of .txt files
file_count = sum(1 for p in Path("assets/text/updates").iterdir() if p.is_file())

for item in Path("assets/text/updates").iterdir():
    counter += 1
    if item.is_file() and item.suffix==".txt":
        dt_name = datetime.strptime(item.stem, "%Y_%m_%d")
        dt_name = dt_name.strftime("%A, %B %d, %Y")

        with st.expander(f"Bulletin Update #{counter}: {dt_name}", expanded=True if counter==file_count else False, width="stretch"):
            st.markdown(item.read_text(encoding="utf-8"))
