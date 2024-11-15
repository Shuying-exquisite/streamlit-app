import streamlit as st

# 提供GitHub上的视频文件URL
video_url = 'https://github.com/Shuying-exquisite/streamlit-app/blob/main/微信状态背景api/video/明明就.mp4?raw=true'

# 使用 st.video() 播放视频
st.title('播放视频示例')
st.video(video_url)
