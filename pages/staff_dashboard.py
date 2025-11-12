import streamlit as st

from connect_data import STAFF_VIEW, PETS, STAFF_DIRECTORY
from photo import load_photo

st.title("Staff Dashboard")

# st.header("Staff")
# st.write(STAFF_VIEW)

# st.header("Pets")
# st.write(PETS)

st.header("Staff Directory")
st.write(STAFF_DIRECTORY)

st.image(load_photo("JCPAO_headshots/pet.dtarantino")) # evanzutphen

# st.image("https://res.cloudinary.com/jcpao-csu/image/upload/v1749495728/pet.dtarantino")