"""
File: staff_birthdays.py
Function: View JCPAO staff by birthday month
Author: Joseph Cho, ujcho@jacksongov.org
Date: June 6, 2025
"""

import streamlit as st
from datetime import datetime
from pathlib import Path
import pandas as pd

from connect_data import display_personal_name, ordinal, parse_month #, init_bdays
from connect_data import STAFF_DIRECTORY # , get_interns
from photo import load_photo

# --- Configure Streamlit page settings --- 
jcpao_logo = Path("assets/logo/jcpao_logo_500x500.png")

# # --- JCPAO Streamlit page logo --- 
# st.logo(jcpao_logo, size="large", link="https://www.jacksoncountyprosecutor.com")


# --- Load data --- 
emp_view = STAFF_DIRECTORY # "emp_view"
today = datetime.today()
today_date = today.strftime("%A, %B %d, %Y")

# --- Initialize session state ---

# init_bdays(parse_month("index", date.today().month))
# if "selected_staff_bdays_month" not in st.session_state:
#     st.session_state["selected_staff_bdays_month"] = parse_month("index", str(today.month)) # None

if "filtered_staff_bdays_df" not in st.session_state:
    current_month = today.month
    filtered_df = emp_view[emp_view['DOB Month']==current_month].sort_values(by=["DOB Month", "DOB Day", "Last Name"], ascending=[True, True, True]).reset_index(drop=True).copy()
    st.session_state["filtered_staff_bdays_df"] = filtered_df

# --- Callback functions ---

# Define update_df() function
def update_df():

    current_month = int(st.session_state["selected_staff_bdays_month"])
    filtered_df = emp_view.copy()
    filtered_df = filtered_df[filtered_df['DOB Month']==current_month].sort_values(by=["DOB Month", "DOB Day", "Last Name"], ascending=[True, True, True]).reset_index(drop=True).copy()
    st.session_state["filtered_staff_bdays_df"] = filtered_df

# --- Sidebar Filter functions --- 

with st.sidebar:

    st.title("Jackson County Prosecuting Attorney's Office")
    st.write("***JCPAO Staff Birthdays***")
    st.divider()
    st.write(
        f"View upcoming staff birthdays!\n"
        f"Today is {today_date}."
    ) # Today's date is {today}.
    st.divider()

    # Filter by birthday month:
    month_options = st.selectbox(
        label=":violet-badge[**Filter by Birthday Month:**]", # "Filter by Birthday Month:",
        options=parse_month("options"),
        index=parse_month("index", str(today.month)), # All
        format_func=parse_month("format_func"),
        key='selected_staff_bdays_month',
        placeholder="Select birthday month to filter",
        on_change=update_df,
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


# --- display_employee() function --- 

def display_employee(row):

    col1, col2, col3 = st.columns([1.5, 1, 1.5], gap="large",vertical_alignment="center")

    with col2:
        # Headshot Photo (if None, JCPAO logo)
        if row['PhotoID'] is None:
            st.image(
                jcpao_logo, 
                caption=(
                    f"{display_personal_name(row)}\n"
                    f":violet-badge[🎉**{row['DOB'].strftime('%b')} {ordinal(row['DOB'].day)}**]"
                ),
                width=250)
        else:
            headshot_path = "JCPAO_headshots/"+row['PhotoID']
            attorney_headshot = load_photo(headshot_path)
            st.image(
                attorney_headshot, 
                caption=(
                    f"{display_personal_name(row)}\n"
                    f":violet-badge[🎉**{row['DOB'].strftime('%b')} {ordinal(row['DOB'].day)}**]"
                ), # f":violet-badge[🎉 **{dob_month}/{dob_day}**]"
                width=250
            )

    # with col3:

    #     # Employee Name
    #     if row['Preferred Name']:
    #         st.header(f"{row['Preferred Name'].strip()} {row['Last Name'].strip()}")
    #     else:
    #         st.header(f"{row['First Name'].strip()} {row['Last Name'].strip()}")
        
    #     # DOB Month / DOB Day BADGE 
    #     birthday = f""
    #     dob_badge = st.subheader(f"**{birthday}**")
        
    # st.divider()

# --- Display Page --- 
st.title("JCPAO Staff Birthdays")
st.divider()

# --- Display birthdays --- 

df = st.session_state["filtered_staff_bdays_df"].copy()

if df.empty:
    st.info("No upcoming birthdays this month. Make sure that a birthday month is selected in the sidebar!", icon="🥳")
    # st.write("No upcoming birthdays this month. Make sure that a birthday month is selected in the sidebar!")

else:
    st.balloons()
    for i, row in df.iterrows():
        display_employee(row)



# By Zodiac Sign 

# st.markdown(
#     """
#     Aries  March 21 - April 19 ♈️
#     Taurus  April 20 - May 20 ♉️
#     Gemini  May 21 - June 21 ♊️
#     Cancer  June 22 - July 22 ♋️
#     Leo  July 23 - Aug 22 ♌️
#     Virgo  Aug 23 - Sept 22 ♍️
#     Libra  Sept 23 - Oct 22 ♎️
#     Scorpio  Oct 23 - Nov 21 ♏️
#     Sagittarius  Nov 22 - Dec 21 ♐️
#     Capricorn  Dec 22 - Jan 19 ♑️
#     Aquarius  Jan 20 - Feb 18 ♒️
#     Pisces  Feb 19 - Mar 20 ♓️
#     """
# )


# Aries  March 21 - April 19 ♈️
# Taurus  April 20 - May 20 ♉️
# Gemini  May 21 - June 21 ♊️
# Cancer  June 22 - July 22 ♋️
# Leo  July 23 - Aug 22 ♌️
# Virgo  Aug 23 - Sept 22 ♍️
# Libra  Sept 23 - Oct 22 ♎️
# Scorpio  Oct 23 - Nov 21 ♏️
# Sagittarius  Nov 22 - Dec 21 ♐️
# Capricorn  Dec 22 - Jan 19 ♑️
# Aquarius  Jan 20 - Feb 18 ♒️
# Pisces  Feb 19 - Mar 20 ♓️
