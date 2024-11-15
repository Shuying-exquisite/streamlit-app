import streamlit as st

# 提供GitHub上的视频文件URL
video_url = 'https://github.com/Shuying-exquisite/streamlit-app/blob/main/%E5%BE%AE%E4%BF%A1%E7%8A%B6%E6%80%81%E8%83%8C%E6%99%AFapi/video/%E5%92%8F%E6%98%A5%E5%8F%B6%E9%97%AE.mp4?raw=true'

# 使用 st.video() 播放视频
st.title('播放视频示例')
st.video(video_url)
