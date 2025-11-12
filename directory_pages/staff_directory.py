"""
File: staff_directory.py
Function: Streamlit page for JCPAO directory (INTERNAL view for JCPAO employees)
Author: Joseph Cho, ujcho@jacksongov.org
Date: April 12, 2025
Updated: November 10, 2025
"""

import streamlit as st
from pathlib import Path 
import pandas as pd

from connect_data import STAFF_DIRECTORY # Load data
from photo import load_photo

# st.title("Staff Directory")
# TODO - directory pagination? 

# # --- Configure Streamlit page settings --- 
# jcpao_logo = Path("assets/logo/jcpao_logo_500x500.png")

# # --- JCPAO Streamlit page logo --- 
# st.logo(jcpao_logo, size="large", link="https://www.jacksoncountyprosecutor.com")


# --- Initialize session state --- 

if "staffview_selected_position" not in st.session_state:
    st.session_state["staffview_selected_position"] = "All"

if "staffview_selected_unit" not in st.session_state:
    st.session_state["staffview_selected_unit"] = "All"

if "staffview_selected_location" not in st.session_state:
    st.session_state["staffview_selected_location"] = "All"

if "staffview_selected_month" not in st.session_state:
    st.session_state["staffview_selected_month"] = "All"

if "staffview_searched_text" not in st.session_state:
    st.session_state["staffview_searched_text"] = ""


# --- Define callback functions --- 

# Define update_df() function
def update_df():

    filtered_df = STAFF_DIRECTORY.copy()

    if st.session_state["staffview_selected_position"] != 'All':
        filtered_df = filtered_df[filtered_df['Position']==st.session_state["staffview_selected_position"]].reset_index(drop=True)
    if st.session_state["staffview_selected_unit"] != 'All':
        filtered_df = filtered_df[filtered_df['Assigned Unit'].apply(lambda x: st.session_state["staffview_selected_unit"] in x)].reset_index(drop=True)
    if st.session_state["staffview_selected_location"] != 'All': 
        filtered_df = filtered_df[filtered_df['Office Location']==st.session_state["staffview_selected_location"]].reset_index(drop=True)
    if st.session_state["staffview_selected_month"] != 'All':
        filtered_df = filtered_df[filtered_df['DOB Month']==int(st.session_state["staffview_selected_month"])].reset_index(drop=True)
    if st.session_state["staffview_searched_text"]: # Added searched_text to main clickback action 
        searched_text = st.session_state["staffview_searched_text"].strip().lower()
        search_cols = ["Full Name", "First Name", "Middle Name", "Last Name", "Suffix", "Preferred Name"]
        filtered_df = filtered_df[
            filtered_df[search_cols].apply(lambda row: any(searched_text in str(value).lower() for value in row), axis=1)
        ].reset_index(drop=True)

    st.session_state["staffview_filtered_df"] = filtered_df.reset_index(drop=True)

# Reset filters button
def reset_filters():
    st.session_state["staffview_selected_position"] = "All"
    st.session_state["staffview_selected_unit"] = "All"
    st.session_state["staffview_selected_location"] = "All"
    st.session_state["staffview_selected_month"] = "All"
    st.session_state["staffview_searched_text"] = ""
    # filtered_df = STAFF_DIRECTORY.copy()
    # st.session_state["staffview_filtered_df"] = filtered_df
    st.session_state["staffview_filtered_df"] = STAFF_DIRECTORY


# --- Sidebar Filter functions ---

with st.sidebar:
    # Select options: position / unit / location / birthday month 
    st.title("Jackson County Prosecuting Attorney's Office")
    st.write("***Internal Staff Directory***")
    st.divider()
    st.write("Please use the directory to view information on all attorneys and support staff actively employed in the Jackson County Prosecuting Attorney's Office.")
    st.divider()
    
    # Filter by job position (position_enum): 
    positions_dict = { 
        'All': 'All Job Positions', 
        'Exec': 'Executive Staff', 
        'CTA': 'Chief Trial Attorneys', 
        'TTL': 'Trial Team Leaders', 
        'APA': 'Assistant Prosecuting Attorneys',
        'I': 'Investigators',
        'VA': 'Victim Advocates',
        'LA': 'Legal Assistants',
        'SS': 'Support Staff',
        'INTERN': 'Interns',
        'PET': 'Paw-secuting Attorneys 🐾'
    }
    position_options = st.selectbox(
        label= ":green-badge[**Filter by Position:**]", # "Filter by Position:",
        options=positions_dict.keys(), # ('All', 'Exec', 'CTA', 'TTL', 'APA', 'I', 'VA', 'LA', 'SS')
        index=0, # All
        format_func=lambda x: positions_dict[x],
        key='staffview_selected_position',
        placeholder="Select job position",
        on_change=update_df,
    )

    # Filter by assigned unit (unit_enum): 
    units_dict = { 
        'All': 'All Office Units',
        'Exec': 'Executive Staff',
        'GCU': 'General Crimes Unit (GCU)',
        'SVU': 'Special Victims Unit (SVU)',
        'VCU': 'Violent Crimes Unit (VCU)',
        'CSU': 'Crime Strategies Unit (CSU)',
        'COMBAT': 'COMBAT',
        'Drug': 'Drug Court',
        'FSD': 'Family Support Division',
        'WARRANT': 'Warrant Desk'
    }
    unit_options = st.selectbox(
        label=":blue-badge[**Filter by Assigned Unit:**]", # "Filter by Assigned Unit:",
        options=units_dict.keys(), # ('Exec', 'GCU', 'SVU', 'VCU', 'CSU', 'COMBAT', 'Drug', 'FSD')
        index=0, # All
        format_func=lambda x: units_dict[x],
        key='staffview_selected_unit',
        placeholder="Select unit",
        on_change=update_df,
    )

    # Filter by office location (location_enum): 
    locations_dict = {
        'All': 'All Office Locations',
        'Dt-11': 'Downtown Courthouse, 11th floor',
        'Dt-10': 'Downtown Courthouse, 10th floor',
        'Dt-9': 'Downtown Courthouse, 9th floor (COMBAT)',
        'Dt-7M': 'Downtown Courthouse, 7M',
        'Indy': 'Eastern Jackson Courthouse, Independence',
        'FSD': 'Family Support Division'
    }
    location_options = st.selectbox(
        label=":orange-badge[**Filter by Office Location:**]", # "Filter by Office Location:",
        options=locations_dict.keys(), # ('Dt-11', 'Dt-10', 'Dt-9', 'Dt-7M', 'Indy', 'FSD')
        index=0, # All
        format_func=lambda x: locations_dict[x],
        key='staffview_selected_location',
        placeholder="Select office location",
        on_change=update_df,
    )

    # Filter by birthday month:
    months_dict = {
        'All': 'All Months',
        '1': 'Jan',
        '2': 'Feb',
        '3': 'Mar',
        '4': 'Apr',
        '5': 'May',
        '6': 'Jun',
        '7': 'Jul',
        '8': 'Aug',
        '9': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }
    month_options = st.selectbox(
        label=":violet-badge[**Filter by Birthday Month:**]", # "Filter by Birthday Month:",
        options=months_dict.keys(),
        index=0, # All
        format_func=lambda x: months_dict[x],
        key='staffview_selected_month',
        placeholder="Select birthday month",
        on_change=update_df,
    )

    # Reset filters 
    refresh = st.button(
        label="Reset Filters",
        key="staffview_filter_reset",
        on_click=reset_filters,
        type="secondary",
        icon="🔄",
    )

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

# --- Internal Directory HELPER funcs --- 

def reformat_phone_num(phone_num):
    # Handle NaN values or non-string types 
    if not isinstance(phone_num, str) or pd.isna(phone_num):
        return phone_num
    
    # Check length is 10-digits, then reformat 
    if len(phone_num) == 10:
        return f"{phone_num[:3]}-{phone_num[3:6]}-{phone_num[6:]}"
    else:
        return phone_num

def display_employee(row):

    with st.container():

        col1, col2 = st.columns([1,1.25], gap="small", vertical_alignment="center")

        with col1:
            
            # Headshot Photo (if None, JCPAO logo)
            jcpao_logo = Path("assets/logo/jcpao_logo_500x500.png")
            if row['PhotoID'] is None:
                st.image(jcpao_logo, width=400)
            else:
                headshot_path = "JCPAO_headshots/"+row['PhotoID'].strip()
                staff_headshot = load_photo(headshot_path)
                st.image(staff_headshot, width=400)
            
        with col2:

            # Employee Name
            if row['Preferred Name']: # If preferred name exists
                st.header(f"{row['Preferred Name'].strip()} {row['Last Name'].strip()}")
            else:
                st.header(f"{row['First Name'].strip()} {row['Last Name'].strip()}")

            # Job Title
            st.subheader(f"{row['Job Title']}")

            # Position BADGE
            positions_badge = {
                'Exec': 'Exec Staff', 
                'CTA': 'CTA', 
                'TTL': 'TTL', 
                'APA': 'APA',
                'I': 'Investigator',
                'VA': 'Victim Advocate',
                'LA': 'Legal Assistant',
                'SS': 'Support Staff',
                'INTERN': 'Intern',
                'PET': 'Paw-secuting Attorney 🐾'
            }
            # position_badge = st.badge(f"**Position:** {positions_badge.get(row['Position'], row['Position'])}", icon=None, color="green")

            # Assigned Unit (unit_enum[]) BADGE
            units_badge = {
                'Exec': 'Exec Staff',
                'GCU': 'GCU',
                'SVU': 'SVU',
                'VCU': 'VCU',
                'CSU': 'CSU',
                'COMBAT': 'COMBAT',
                'Drug': 'Drug Court',
                'FSD': 'Family Support',
                'WARRANT': 'Warrant Desk'
            } # units_badge.get(row['Assigned Unit'], row['Assigned Unit'])
            # unit_badge = st.badge(f"**{' / '.join(units_badge.get(item, item) for item in row['Assigned Unit'])}**", icon=None, color="blue")

            # Office Location BADGE
            locations_badge = {
                'Dt-11': 'Downtown, 11th',
                'Dt-10': 'Downtown, 10th',
                'Dt-9': 'Downtown, 9th',
                'Dt-7M': 'Downtown, 7M',
                'Indy': 'Eastern Jack, Indy',
                'FSD': 'Downtown, FSD'
            }
            # location_badge = st.badge(f"**Office Location:** {locations_badge.get(row['Office Location'], row['Office Location'])}", icon="🏢", color="orange")

            # DOB Month / DOB Day BADGE 
            if not pd.isna(row['DOB Month']):
                dob_month = int(row['DOB Month'])
            else:
                dob_month = " "
            if not pd.isna(row['DOB Day']):
                dob_day = int(row['DOB Day'])
            else:
                dob_day = " "
            # dob_badge = st.badge(f"**Birthday:** {row['DOB Month']}/{row['DOB Day']}", icon="🎉", color="violet")

            # Display BADGE thread 
            st.markdown( # position_badge, unit_badge, location_badge, dob_badge
                f":green-badge[**{positions_badge.get(row['Position'], row['Position'])}**]"
                f":blue-badge[**{' / '.join(units_badge.get(item, item) for item in row['Assigned Unit'])}**]"
                f":orange-badge[🏢 **{locations_badge.get(row['Office Location'], row['Office Location'])}**]"
                f":violet-badge[🎉 **{dob_month}/{dob_day}**]"
            )

            # Work Phone Number
            work_phone = reformat_phone_num(row['Work Phone #'])
            if str(row['Work Phone #']).startswith("816881"):
                st.write(f"**Work Phone:** {work_phone} (ext. {str(row['Work Phone #'])[-4:]})")
            else:
                st.write(f"**Work Phone:** {work_phone}")
            
            # Work Email Address
            st.write(f"**Work Email:** {row['Work Email Address']}")

            # Personal Phone Number
            personal_phone = reformat_phone_num(row['Personal Phone #'])
            st.write(f"**Personal Phone:** {personal_phone}")

            # Personal Email Address - exclude, for now 
            # st.write(f"**Personal Email:** {row['Personal Email Address']}")
            
        st.divider()

# --- Display INTERNAL Directory ---

# filtered_df = emp_view.copy()
# filtered_df.reset_index(drop=True, inplace=True)

df = st.session_state.get("staffview_filtered_df", STAFF_DIRECTORY)

# Internal Directory title 
st.markdown("<h1 style='text-align: center; color: black;'>Internal Staff Directory</h1>", unsafe_allow_html=True)
st.divider()

# Text Search feature 
searched_text = st.text_input(
    "Search employee name:",
    key="staffview_searched_text"
)

text_search = st.button(
    "Search",
    icon="🔎",
    on_click=update_df,
    key="staffview_text_search",
)

st.divider()

if df.empty:
    st.info("No active JCPAO staff found given the selected category filters.", icon="⚠️")
else:
    for i, row in df.iterrows():
        display_employee(row)

