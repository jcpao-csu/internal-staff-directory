import streamlit as st
from psycopg_pool import ConnectionPool
import psycopg
import pandas as pd

# --- Local .env file ---
# from dotenv import load_dotenv
# import os
# load_dotenv(override=True)
# conn_string = os.getenv("DATABASE_URL")


# --- Initialize database connection pool ---

# Define get_database_session() 
@st.cache_resource
def get_database_session(database_url):
    try: 
        # Create a database session object that points to the URL.
        pool = ConnectionPool(
            database_url, 
            min_size=1, 
            max_size=10
        ) # Initialize connection pool
        return pool
    except psycopg.OperationalError as e:
        st.error(f"Network is blocking connection to the database server.\nPlease try again on a different network/internet connection, or reach out to admin at ujcho@jacksongov.org.\n{e}")
        return None

# Establish NEON database connection (via psycopg3)
database_url = st.secrets["neonDB"]["database_url"]

# Attempt connection
try:
    db_connection = get_database_session(database_url)
except Exception as e:
    print(f"{e}")
    st.stop()

# --- Define helper functions ---

# Define parse_enum()
def parse_enum(array):
    """Return enum array dtypes in a workable format"""
    if pd.isna(array):
        return []
    array = array.strip('{}')
    return array.split(',') if array else []


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

# --- Log activity --- 

def log_user(
    # insert_table: str, # preset table in query 
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
        if isinstance(_connection, ConnectionPool):
            with _connection.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO user_activity (work_email, activity) VALUES (%s, %s)",
                        (email_address, activity_type),
                    )
                conn.commit()

    except Exception as e:
        st.error(f"Error logging activity: {e}")



# # Define jcpao_log_activity()
# def jcpao_log_activity(work_email, activity_type, _connection_pool=db_connection):
#     """Log user activity in the user_activity table"""
#     # activity_type = 'SIGN UP' / 'LOGIN' / 'UPDATE PROFILE' / 'REMOVE PROFILE' / 'ANNOUNCEMENT' / 'ADMIN-AUTHORIZE' / 'ADMIN-REMOVE PROFILE' / 'POST-TRIAL SURVEY' / 'RESET PASSWORD' / 
#                     # 'UPDATE PHOTO' / 'UPDATE NAME' / 'UPDATE JOB' / 'UPDATE OFFICE' / 'UPDATE DEMOGRAPHIC' / 'UPDATE INTERN'

#     conn = _connection_pool.getconn()
#     try:
#         with conn.cursor() as cur:
#             try: 
#                 query = sql.SQL("INSERT INTO user_activity (work_email, activity) VALUES (%s, %s);")
#                 cur.execute(query, (work_email, activity_type))
#             except psycopg2.Error as e:
#                 st.error(f"An error has occurred. Failed to log activity.")
#             else:
#                 conn.commit()

#     finally:
#         _connection_pool.putconn(conn)

# # Define external_log_activity()
# def external_log_activity(_connection_pool, db_table_name, user_email, user_ip): # police_log, courts_log 

#     with _connection_pool.getconn() as conn:

#         with conn.cursor() as cur:
#             try: 
#                 query = sql.SQL("INSERT INTO {table_name} (user_email, user_ip) VALUES (%s, %s)").format(
#                     table_name=sql.Identifier(db_table_name)
#                 )
#                 cur.execute(query, (user_email, user_ip))
#             except psycopg2.Error as e:
#                 st.error(f"An error has occurred.")
#             else:
#                 conn.commit()
#         cur.close()
#     conn.close()