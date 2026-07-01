import streamlit as st
from pathlib import Path
import time
import base64

from connect_data import log_user, STAFF_EMAILS

# --- Configure Streamlit page settings --- 

jcpao_logo = Path("assets/logo/jcpao_logo_500x500.png")

st.set_page_config(
    page_title="JCPAO Directory", # court-view only
    page_icon=jcpao_logo, # cloudinary.CloudinaryImage('jcpao_logo_200x200').build_url()
    layout="wide", # "centered" or "wide"
    initial_sidebar_state="auto", # "expanded" / "auto" / "collapsed"
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "mailto:ujcho@jacksongov.org", # To report a bug, please email
        'About': "The JCPAO Portal was built by Joseph Cho and the Crime Strategies Unit (CSU) of the Jackson County Prosecuting Attorney's Office."
    }
)

# --- JCPAO Streamlit page logo ---
st.logo(jcpao_logo, size="large", link="https://www.jacksoncountyprosecutor.com")

@st.cache_data
def get_logo_base64(path: Path) -> str:
    """Base64-encode the logo so it can be centered via custom HTML."""
    return base64.b64encode(path.read_bytes()).decode()

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
    if email in STAFF_EMAILS and code == security_code:
        log_user(email, "LOGIN") # also track ip address? [st.context.ip_address]
        success_message = st.success(f"Verification successful: *{st.session_state['verified_email']}*")
        time.sleep(2)
        success_message.empty()
        st.session_state["verified"] = True # Unlocks directory
    else:
        fail_message = st.error("Failed to verify user. Please try again with an authorized email and security code.")
        time.sleep(2)
        fail_message.empty()

# --- New user dialog ---

@st.dialog("New to the JCPAO Directory?", width="small")
def new_user_dialog():
    st.markdown(
        """
        The **JCPAO Staff Directory** is *only* available to current JCPAO staff
        with an active **@jacksongov.org** email.

        If you're a new hire and haven't been added to the directory yet, please
        complete the [**Personnel Intake Survey**](https://form.jotform.com/261024019483047) below. Once submitted, your
        information will be reviewed and you will receive an email confirming you
        have been successfully added.
        """
    )
    st.write(" ")
    st.page_link(
        "https://form.jotform.com/261024019483047",
        label="Personnel Intake Survey",
        icon=":material/open_in_new:",
    )

# --- Enter security code ---

def display_portal():
    """Display access portal"""

    # Custom vertical space (CSS)
    st.markdown(
        """
        <style>
        .space { margin-top: 100px; }
        </style>
        <div class="space"></div>
        """,
        unsafe_allow_html=True
    )

    # Display form
    cols = st.columns(
        3,
        gap=None,
        vertical_alignment="top",
        border=False,
        width="stretch"
    )

    with cols[1]:

        # Centered JCPAO logo
        st.markdown(
            f"""
            <div style='text-align: center; margin-bottom: 36px;'>
                <img src='data:image/png;base64,{get_logo_base64(jcpao_logo)}' width='200'>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Form to verify user
        with st.form(
            "verify_user",
            clear_on_submit=False,
            enter_to_submit=False,
            border=True,
            width="stretch",
            height="content"
        ):
            # st.markdown("<h1 style='text-align: center; color: black;'>Court-View Directory</h1>", unsafe_allow_html=True)
            # st.markdown(":small[*Please verify the following information to access the directory*]", unsafe_allow_html=True) # :material/gavel:
            st.markdown("<div style='text-align: center; font-size: 1.75rem; font-weight: bold; color: #000000;'>JCPAO Directory</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: small; color: #000000; margin-bottom: 20px;'>Please verify the following information to access the directory</div>", unsafe_allow_html=True)

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

        # New user dialog trigger
        if st.button(
            "New user? Click here",
            key="new_user_btn",
            icon=":material/person_add:",
            type="tertiary",
            use_container_width=True,
        ):
            new_user_dialog()

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
            st.Page("directory_pages/welcome_page.py", title="JCPAO Portal", icon=":material/home:"), # 🏡 
        ],
        "Directories": [
            st.Page("directory_pages/staff_directory.py", title="Staff Directory", icon=":material/contacts:"), # ☎️
            st.Page("directory_pages/staff_birthdays.py", title="Staff Birthdays", icon=":material/cake:"), # 🎂
            st.Page("directory_pages/court_directory.py", title="Court-view Directory", icon=":material/account_balance:"), # 🏛️
        ],
        "Resources": [
            # st.Page("court_view.py", title="JCPAO Attorney Directory", icon=":material/contact_page:"),
            st.Page("directory_pages/staff_dashboard.py", title="Staff Dashboard", icon=":material/monitoring:"),
            st.Page("directory_pages/faq.py", title="Frequently Asked Questions", icon=":material/question_mark:"),
            st.Page("directory_pages/resources.py", title="Office Resources", icon=":material/support_agent:"),
        ], 
    }

    court_pg = st.navigation(directory_pages, position="top")
    court_pg.run() 