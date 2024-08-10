import streamlit as st
import pandas as pd

from db.tables import get_vidoos_and_channel, most_videos, top_10, comments_video_names, \
    highest_likes, total_likes, total_views_channel_names, \
    videos_2022, avg_duration, highest_comments_channel_name

st.set_page_config(page_title="YouTube Channel Data Analysis", layout="wide")

st.write("What are the names of all the videos and their corresponding channels?")
res =  get_vidoos_and_channel()
df = pd.DataFrame(res)
st.dataframe(df)

st.write("Which channels have the most number of videos, and how many videos do they have?")

res = most_videos()
df = pd.DataFrame(res)
st.dataframe(df)

st.write("What are the top 10 most viewed videos and their respective channels?")
res = top_10()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("How many comments were made on each video, and what are their corresponding video names?")

res = comments_video_names()
df = pd.DataFrame(res)
st.dataframe(df)

st.write("Which videos have the highest number of likes, and what are their corresponding channel names?")

res = highest_likes()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("What is the total number of likes and dislikes for each video, and what are their corresponding video names?")
res = total_likes()
df = pd.DataFrame(res)
st.dataframe(df)

st.write("What is the total number of views for each channel, and what are their corresponding channel names?")
res = total_views_channel_names()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("What are the names of all the channels that have published videos in the year 2022?")
res = videos_2022()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("What is the average duration of all videos in each channel, and what are their corresponding channel names?")
res = avg_duration()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("Which videos have the highest number of comments, and what are their corresponding channel names?")
res = highest_comments_channel_name()
df = pd.DataFrame(res)
st.dataframe(df)
