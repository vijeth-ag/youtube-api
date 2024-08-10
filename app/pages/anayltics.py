import streamlit as st
import pandas as pd

from db.tables import get_vidoos_and_channel, most_videos, top_10, comments_video_names, \
    highest_likes, total_likes, total_views_channel_names, \
    videos_2022, avg_duration, highest_comments_channel_name

st.set_page_config(page_title="YouTube Channel Data Analysis", layout="wide")

st.write("Analytics")
res =  get_vidoos_and_channel()
df = pd.DataFrame(res)
st.dataframe(df)

st.write("Most Videos")

res = most_videos()
df = pd.DataFrame(res)
st.dataframe(df)

st.write("top_10")
res = top_10()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("Comments")

res = comments_video_names()
df = pd.DataFrame(res)
st.dataframe(df)

st.write("Highest Likes")

res = highest_likes()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("Total Likes")
res = total_likes()
df = pd.DataFrame(res)
st.dataframe(df)

st.write("Total Views for channels")
res = total_views_channel_names()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("Videos in 2022")
res = videos_2022()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("Average Duration")
res = avg_duration()
df = pd.DataFrame(res)
st.dataframe(df)


st.write("Highest Comments")
res = highest_comments_channel_name()
df = pd.DataFrame(res)
st.dataframe(df)
