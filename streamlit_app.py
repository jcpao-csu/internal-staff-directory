import streamlit as st
from pathlib import Path
import time

from connect_data import log_user

# --- Configure Streamlit page settings --- 

jcpao_logo = Path("assets/logo/jcpao_logo_500x500.png")

st.set_page_config(
    page_title="JCPAO Directory", # court-view only
    page_icon=jcpao_logo, # cloudinary.CloudinaryImage('jcpao_logo_200x200').build_url()
    layout="wide", # "centered" or "wide"
    initial_sidebar_state="collapsed", # "expanded" / "auto" / "collapsed"
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "mailto:ujcho@jacksongov.org", # To report a bug, please email
        'About': "The JCPAO Portal was built by Joseph Cho and the Crime Strategies Unit (CSU) of the Jackson County Prosecuting Attorney's Office."
    }
)

# --- JCPAO Streamlit page logo --- 
st.logo(jcpao_logo, size="large", link="https://www.jacksoncountyprosecutor.com")

# --- Connect to database --- 

# --- Initialize st.session_state --- 
if "verified" not in st.session_state:
    st.session_state["verified"] = False

# st.write(st.session_state)

# --- Initialize callback functions --- 

def verify_attempt():
    """Verify form submission"""

    # Variables
    email = st.session_state["verified_email"]
    code = st.session_state["security_code"]
    security_code = st.secrets["security_codes"]["court"]

    # Check verification
    # TODO - add security of checking if the @jacksongov.org email actually exists/is active in the database prior to verification
    # if (email.endswith("@courts.mo.gov") or email.endswith("@jacksongov.org")) and code == security_code:
    if email.endswith("@jacksongov.org") and code == security_code:
        log_user(email, "LOGIN") # also track ip address? [st.context.ip_address]
        success_message = st.success(f"Verification successful: *{st.session_state['verified_email']}*")
        time.sleep(2)
        success_message.empty()
        st.session_state["verified"] = True # Unlocks directory
    else:
        fail_message = st.error("Failed to verify user. Please try again with an authorized email and security code.")
        time.sleep(2)
        fail_message.empty()

# --- Enter security code --- 

def display_portal():
    """Display access portal"""

    # Custom vertical space (CSS)
    st.markdown(
        """
        <style>
        .space { margin-top: 300px; }
        </style>
        <div class="space"></div>
        """,
        unsafe_allow_html=True
    )

    # Display form
    cols = st.columns(
        3, 
        gap=None,
        vertical_alignment="center",
        border=False,
        width="stretch"
    )

    with cols[1]:
        
        # Form to verify user 
        with st.form(
            "verify_user",
            clear_on_submit=False,
            enter_to_submit=False,
            border=True,
            width="stretch",
            height="content"
        ):
            st.markdown(":small[*Please verify the following information to access the directory*]") # :material/gavel:

            # Email
            verified_email = st.text_input(
                label="Enter email",
                placeholder=None,
                help=None,
                key="verified_email",
                disabled=st.session_state["verified"],
            )

            # Security code
            security_code = st.text_input(
                label="Enter authorized security code",
                placeholder=None,
                help=None,
                key="security_code",
                disabled=st.session_state["verified"],
                type="password",
            )

            # Submit 
            verify_button = st.form_submit_button(
                label="Verify", # :material/keyboard_return: 
                icon=":material/keyboard_return:",
                disabled=st.session_state["verified"],
                on_click=verify_attempt,
                type="primary",
                width="stretch"
            )

# --- Run STREAMLIT APP via st.navigation --- 


# --- RUN STREAMLIT APP --- 

if not st.session_state["verified"]:
    display_portal() # Display verification portal

else: # st.session_state["verified"] == TRUE

    # Preserve st.session_state?
    # st.session_state["verified_email"] = st.session_state["verified_email"]

    # Display APA Directory 
    directory_pages = {
        "Home": [
            st.Page("pages/welcome_page.py", title="JCPAO Portal", icon=":material/home:"), # 🏡 
        ],
        "Directories": [
            st.Page("pages/staff_directory.py", title="Staff Directory", icon=":material/contacts:"), # ☎️
            st.Page("pages/staff_birthdays.py", title="Staff Birthdays", icon=":material/cake:"), # 🎂
            st.Page("pages/court_directory.py", title="Court-view Directory", icon=":material/account_balance:"), # 🏛️
        ],
        "Resources": [
            # st.Page("court_view.py", title="JCPAO Attorney Directory", icon=":material/contact_page:"),
            st.Page("pages/staff_dashboard.py", title="Staff Dashboard", icon=":material/monitoring:"),
            st.Page("pages/faq.py", title="Frequently Asked Questions", icon=":material/question_mark:"),
            st.Page("pages/resources.py", title="Office Resources", icon=":material/support_agent:"),
        ], 
    }

    court_pg = st.navigation(directory_pages, position="top")
    court_pg.run() 