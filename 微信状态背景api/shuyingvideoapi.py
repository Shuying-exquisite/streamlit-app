import streamlit as st
import random
import requests

# GitHub API URL
repo_url = "https://api.github.com/repos/Shuying-exquisite/streamlit-app/contents/微信状态背景api/video"

# 获取GitHub目录下的视频文件
response = requests.get(repo_url)
data = response.json()

# 提取视频文件的原始链接（过滤出以.mp4结尾的文件）
video_urls = [file['download_url'] for file in data if file['name'].endswith('.mp4')]

# 随机选择一个视频链接
if video_urls:
    selected_video = random.choice(video_urls)
    st.title('随机播放视频')
    st.video(selected_video)
else:
    st.write('没有找到视频文件。')
