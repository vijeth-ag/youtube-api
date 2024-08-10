import streamlit as st
from db.db import init_db


init_db()

# Set up the page configuration
st.set_page_config(
    page_title="Youtube channel analysis",
    layout="wide"
)

st.title("Youtube Analytics")

st.write("\n")
st.write("\n")
st.write("\n")

st.write("Select \"Add Urls\" option to add youtube channels")
st.write("Select \"Analysys\" option to view results")