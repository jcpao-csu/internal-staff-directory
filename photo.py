import streamlit as st
import cloudinary
from cloudinary import CloudinaryImage

config = cloudinary.config(
    cloud_name = st.secrets["cloudinary"]["CLOUD_NAME"], 
    api_key = st.secrets["cloudinary"]["API_KEY"],
    api_secret = st.secrets["cloudinary"]["API_SECRET"],
    secure = True
)

import cloudinary.uploader
import cloudinary.api
import time
from pathlib import Path 


# Define load_photo() 
def load_photo(public_id):
    """Loads photo from Cloudinary with the provided public ID; returns img src URL that can be read into st.image()/st.markdown()"""
    return CloudinaryImage(public_id).build_url(version=None)

# TODO - update upload_photo() function and add to special admin function page
# Define upload_photo()
def upload_photo():
    cloudinary.uploader.upload(
        "path/to/photo.jpg",
        public_id="pet.dtarantino",
        overwrite=True,
        invalidate=True  # invalidates cached version so new image is served
    )
    return True
