import streamlit as st
import psycopg
from psycopg_pool import ConnectionPool
import pandas as pd
import time

# --- Local .env file ---
# from dotenv import load_dotenv
# import os
# load_dotenv(override=True)
# conn_string = os.getenv("DATABASE_URL")


# --- Initialize database connection pool ---

# Define get_database_session() 
@st.cache_resource
def get_database_session(database_url: str):
    try: 
        # Create a database session object that points to the URL.
        pool = ConnectionPool(
            conninfo=database_url, 
            min_size=1, 
            max_size=10,
            max_lifetime=300, # recycle connections every 300 seconds
            max_idle=60, # close idle connections after 60 seconds
            timeout=10 # wait 10 seconds to connect
        ) # Initialize connection pool
        return pool
    except psycopg.OperationalError as e:
        st.error(
            f"Network is blocking connection to the database server.\n"
            f"Please try again on a different network/internet connection, or reach out to admin at ujcho@jacksongov.org.\n{e}"
        )
        return None

# Establish NEON database connection (via psycopg3)
database_url = st.secrets["neonDB"]["database_url"]

# Attempt connection
db_connection = get_database_session(database_url)


# --- Define helper functions ---

# Define parse_enum()
def parse_enum(array):
    """Return enum array dtypes in a workable format"""
    if pd.isna(array):
        return []
    array = array.strip('{}')
    return array.split(',') if array else []

# Define display_personal_name()
# def display_personal_name(pref_name, first_name):
#     if not pref_name:
#         return first_name
#     else:
#         return pref_name

def display_personal_name(row):
    if row['Preferred Name']:
        return f"{row['Preferred Name'].strip()} {row['Last Name'].strip()}"
    else:
        return f"{row['First Name'].strip()} {row['Last Name'].strip()}"

# Define ordinal() 
def ordinal(n):
    if 10 <= n % 100 <= 20: # Covers unique cases, like 11th, 12th, 13th
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

# Define display_service()
def display_service(service_days, service_percentile):
    if service_days and service_percentile:
        st.write(f"**Fun fact:** You have been with the JCPAO for {service_days} days, and are in the ***:blue[{ordinal(service_percentile)} percentile]*** among all active JCPAO employees! Thank you for your service to the JCPAO!")

# Birthday Month (not enum)

# Filter by birthday month:
months_dict = {
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

def parse_month(type: str, value: str = None):
    month_list = list(months_dict.keys())

    if type == "options":
        return month_list
    elif type == "index":
        try:
            return month_list.index(value)
        except ValueError: # Value isn't in the list 
            return None
    elif type == "format_func":
        return lambda x: months_dict[x]

# --- Define function to read tables from Neon DB ---

@st.cache_data
def query_table(sql_query: str, _connection: ConnectionPool = db_connection) -> pd.DataFrame:
    if _connection is None:
        return pd.DataFrame()
    
    try:
        if isinstance(_connection, ConnectionPool):
            with _connection.connection() as conn:
                df = pd.read_sql(sql_query, conn)

        else:
            df = pd.read_sql(sql_query, _connection)

        return df
    
    except psycopg.OperationalError as e:
        st.error(f"Database query failed: {e}")
        return pd.DataFrame()

# --- Query tables ---

# Get main STAFF_VIEW table
staff_view = query_table("SELECT * FROM employee_info_view")

if staff_view.empty:
    staff_view = pd.DataFrame()
else:
    staff_view["Assigned Unit"] = staff_view["Assigned Unit"].apply(parse_enum)
    staff_view["Race"] = staff_view["Race"].apply(parse_enum)

STAFF_VIEW = staff_view.copy()

# Get office PETS table 
pets = query_table("SELECT * FROM active_pets")
if pets.empty:
    pets = pd.DataFrame()
else:
    pets["Assigned Unit"] = pets["Assigned Unit"].apply(parse_enum)

PETS = pets.copy()

# Merge STAFF_VIEW and PETS table for staff directory

def directory_df_merge(
    pet_df: pd.DataFrame = pets.copy(), 
    staff_df: pd.DataFrame = staff_view.copy()
) -> pd.DataFrame:
    """
    Merge pet df and staff df together to display internal staff directory
    """

    pet_df.rename(
        columns={
            "Pet Full Name": "Full Name", 
            # "old_col2": "First Name", --no col
            # "Middle Name" --no col
            "Pet Last Name": "Last Name",
            # "Suffix", --no col
            "Pet Pref Name": "Preferred Name",
            # "Karpel ID", --no col
            # "Work Phone #", --no col
            # "Personal Phone #", --no col
            # "Work Email Address", --already matching
            # "Personal Email Address", --no col
            "Pet Job Title": "Job Title",
            # "Position", --no col
            # "Assigned Unit", --already matching
            # "Office Location", --already matching
            # "Hire Start Date", --no col
            # "Service (days)", --no col
            # "Service (percentile)", --no col
            "Pet DOB": "DOB",
            "Pet DOB Month": "DOB Month",
            "Pet DOB Day": "DOB Day",
            # "Race", --no col
            # "Sex", --no col
            "Pet PhotoID": "PhotoID"
        }, inplace=True)

    pet_df["First Name"] = pet_df["Preferred Name"]
    pet_df["Position"] = "PET" # custom addition to job position (position_enum)

    new_cols = ["Middle Name", "Suffix", "Karpel ID", "Hire Start Date", "Service (days)", "Service (percentile)", "Race", "Sex"]
    for col in new_cols:
        pet_df[col] = None

    pet_df = pet_df.merge(staff_df[["Work Email Address", "Work Phone #", "Personal Phone #", "Personal Email Address"]].copy(), how="left", on="Work Email Address")

    # Rearrange pet_df cols in staff_df col order 
    pet_df = pet_df[[
        "Full Name", 
        "First Name",
        "Middle Name",
        "Last Name",
        "Suffix",
        "Preferred Name",
        "Karpel ID",
        "Work Phone #",
        "Personal Phone #",
        "Work Email Address",
        "Personal Email Address",
        "Job Title",
        "Position",
        "Assigned Unit",
        "Office Location",
        "Hire Start Date",
        "Service (days)",
        "Service (percentile)",
        "DOB",
        "DOB Month",
        "DOB Day",
        "Race",
        "Sex",
        "PhotoID"
    ]]

    merge_df = pd.concat([staff_df, pet_df], ignore_index=True)
    merge_df.sort_values(by=["Last Name", "First Name"], ascending=[True, True], inplace=True, ignore_index=True)

    return merge_df

STAFF_DIRECTORY = directory_df_merge()

# --- Log activity --- 

def log_user(
    email_address: str, 
    activity_type: str, 
    _connection: ConnectionPool = db_connection
):
    """
    Log user activity in the user_activity table.
    Possible values in user_activity_enum:
        'SIGN UP' / 'LOGIN' / 'UPDATE PROFILE' / 'REMOVE PROFILE' / 'ANNOUNCEMENT' / 'ADMIN-AUTHORIZE' / 'ADMIN-REMOVE PROFILE' / 'POST-TRIAL SURVEY' / 'RESET PASSWORD' / 'UPDATE PHOTO' / 'UPDATE NAME' / 'UPDATE JOB' / 'UPDATE OFFICE' / 'UPDATE DEMOGRAPHIC' / 'UPDATE INTERN'
    Logs user login (to track who is using the directory).
    See technical notes: https://www.psycopg.org/psycopg3/docs/basic/params.html
    """

    try:
        # Always grab a fresh connection from the pool
        with _connection.connection() as conn:
            if conn.closed:
                # Replace with a fresh connection if the previous one was bad or stale
                conn = _connection.connection()

            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO user_activity (work_email, activity) VALUES (%s, %s)",
                    (email_address, activity_type),
                )
                conn.commit()

    except psycopg.OperationalError as e:
        # This catches stale/SSL-closed connections and reattempts once
        try:
            # st.warning("Reconnecting to database...")
            with _connection.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO user_activity (work_email, activity) VALUES (%s, %s)",
                        (email_address, activity_type),
                    )
                    conn.commit()
        except Exception as e2:
            error_msg1 = st.error(f"Database reconnect failed: {e2}")
            time.sleep(2)
            error_msg1.empty()

    except Exception as e:
        error_msg2 = st.error(f"Error logging activity: {e}")
        time.sleep(2)
        error_msg2.empty()


# Define refresh_app() function
def refresh_app():
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()