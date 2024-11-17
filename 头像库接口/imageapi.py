import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64

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

# 图片 URL（你可以设置每日图像的动态链接）
image_url = "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/3.jpg"

# 从 URL 加载图像
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

# 保存图像到临时文件
img_path = '/tmp/temp_image.jpg'
img.save(img_path)

# 将文件转换为 base64 编码（用于自动下载）
with open(img_path, "rb") as file:
    img_data = file.read()
    img_base64 = base64.b64encode(img_data).decode()

# 自动下载图片（通过 <a> 标签触发下载）
download_link = f'<a href="data:image/jpeg;base64,{img_base64}" download="每日一图.jpg">自动下载图片</a>'

# 显示下载链接
st.markdown(download_link, unsafe_allow_html=True)

# 仅显示图片
st.image(img, use_column_width=True)

