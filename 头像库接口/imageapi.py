import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# 设置页面配置：不显示任何 UI 元素
st.set_page_config(page_title="每日一图", layout="centered", initial_sidebar_state="collapsed")

# 隐藏所有 Streamlit 默认元素（菜单、页脚、头部）
hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# 图片 URL（可以是静态图像或动态生成的每日一图链接）
image_url = "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/3.jpg"

# 从 URL 加载图像
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

# 返回图片（不显示其他内容）
st.image(img, use_column_width=True)

# 自动下载功能
# 将图像保存为临时文件并提供下载
img_path = '/tmp/temp_image.jpg'
img.save(img_path)

# 提供下载按钮
with open(img_path, "rb") as file:
    btn = st.download_button(
        label="下载图片",
        data=file,
        file_name="每日一图.jpg",
        mime="image/jpeg"
    )
