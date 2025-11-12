import streamlit as st
from pathlib import Path


# --- Sidebar Filter functions --- 

with st.sidebar:

    # Select options: position / unit / location / birthday month 
    st.title("Jackson County Prosecuting Attorney's Office")
    st.write("***Frequently Asked Questions***")
    st.divider()
    st.write("If you have any questions that aren't answered here, please reach out to [Joseph Cho](mailto:ujcho@jacksongov.org).")
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

st.markdown("<h1 style='text-align: center; color: black;'>Frequently Asked Questions</h1>", unsafe_allow_html=True)
st.divider()

with st.expander("What user information is collected for the directory?"):
    user_data = Path("assets/text/help/user_data.txt")
    st.markdown(user_data.read_text(encoding="utf-8"), unsafe_allow_html=True)

with st.expander("How do I update my information in the directory?"):
    user_management = Path("assets/text/help/user_management.txt")
    st.markdown(user_management.read_text(encoding="utf-8"))

with st.expander("Am I allowed to use my headshot photo for personal use?"):
    photo_use = Path("assets/text/help/photo_use.txt")
    st.markdown(photo_use.read_text(encoding="utf-8"))

with st.expander("Will my personal information be shared publicly?"):
    data_sharing = Path("assets/text/help/data_sharing.txt")
    st.markdown(data_sharing.read_text(encoding="utf-8"))

with st.expander("What happens if I depart from the Office?"):
    delete_user = Path("assets/text/help/delete_user.txt")
    st.markdown(delete_user.read_text(encoding="utf-8"))

with st.expander("Technical Notes:"):
    about = Path("assets/text/help/about.txt")
    st.markdown(about.read_text(encoding="utf-8"))
