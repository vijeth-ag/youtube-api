import json
import streamlit as st
import time
from utils.utils import is_valid_youtube_channel_url, get_channelid_from_url
from styles.custom import get_custom_css
from api.api import get_channel_details
from db.tables import insert_channel_details, insert_playlists_data, insert_videos_data, insert_comments_data, delete_all_tables

# Set the page configuration
st.set_page_config(
    page_title="YouTube Channel Data Analysis",
    layout="wide"
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize the session state for the channels list
if 'channels' not in st.session_state:
    st.session_state.channels = ['']

# Function to add a new input box
def add_channel():    
    entered_url = st.session_state.channels[len(st.session_state.channels)-1]
    if "https://www." in entered_url:
        entered_url = entered_url.replace("https://www.","")

    if is_valid_youtube_channel_url(entered_url):
        if len(st.session_state.channels) < 10:            
            st.session_state.channels[len(st.session_state.channels)-1] = entered_url

            st.session_state.channels.append("")
    else:
        st.toast("Please enter a valid Youtube channel url", icon="❌")
        time.sleep(3)


# Function to remove an input box
def remove_channel(index):
    st.session_state.channels.pop(index)

# Function to process the channels
def process_channels():
    for channel in st.session_state.channels:
        channel_id = get_channelid_from_url(channel)
        st.write(channel_id)
        channel_all_data = get_channel_details(channel_id)

        insert_channel_details(channel_all_data["channel_details"])
        insert_playlists_data(channel_all_data["playlists_data"])
        insert_videos_data(channel_all_data["videos"])
        insert_comments_data(channel_all_data["comment_data"])




# Display the input boxes for channels
for i, channel in enumerate(st.session_state.channels):
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.session_state.channels[i] = st.text_input(f"Channel {i + 1}", value=channel, key=f"channel_{i}")
    with col2:
        if len(st.session_state.channels) > 1:
            st.button("Remove", key=f"remove_{i}", on_click=remove_channel, args=(i,)) 

# Add button to add more channels
if len(st.session_state.channels) < 10:
    st.button("Add Another Channel", on_click=add_channel)

# Process button at the bottom
st.button("Process channels", on_click=process_channels)
# st.button("DROP_ALL", on_click=delete_all_tables)
