import streamlit as st
import random
import requests

# GitHub API URL
repo_url = "https://api.github.com/repos/Shuying-exquisite/streamlit-app/contents/头像库接口/image"

# 获取GitHub目录下的文件
response = requests.get(repo_url)

# 检查响应状态
if response.status_code == 200:
    data = response.json()
    # 提取图像文件的原始链接
    if isinstance(data, list):
        image_urls = [
            file['download_url']
            for file in data
            if file.get('name', '').lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]
    else:
        st.error("API 返回的数据不是预期的列表。")
        image_urls = []
else:
    st.error(f"无法访问 API: {response.status_code}")
    st.write("响应内容:", response.text)
    image_urls = []

# 随机选择并返回图片链接
if image_urls:
    selected_image = random.choice(image_urls)
    st.write("随机图片链接：")
    st.write(selected_image)

    # 返回 HTML 格式的图片链接
    st.markdown(f"![随机图片]({selected_image})")
else:
    st.write('没有找到图像文件。')

