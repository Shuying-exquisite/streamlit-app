import streamlit as st
import random
import requests

# GitHub API URL
repo_url = "https://api.github.com/repos/Shuying-exquisite/streamlit-app/contents/头像库接口/image"

# 获取GitHub目录下的图像文件
response = requests.get(repo_url)
data = response.json()

# 提取图像文件的原始链接（过滤出常见图片格式的文件）
image_urls = [file['download_url'] for file in data if file['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# 随机选择一张图像链接
if image_urls:
    selected_image = random.choice(image_urls)
    st.title('随机显示图像')
    st.image(selected_image, use_column_width=True)
else:
    st.write('没有找到图像文件。')
