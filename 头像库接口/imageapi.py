import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64

# 设置页面配置
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

# 将图片转换为 base64 编码
with open(img_path, "rb") as file:
    img_data = file.read()
    img_base64 = base64.b64encode(img_data).decode()

# 使用 JavaScript 自动触发文件下载
html_code = f"""
    <html>
        <body>
            <script>
                // 创建下载链接并自动触发点击
                var link = document.createElement('a');
                link.href = 'data:image/jpeg;base64,{img_base64}';
                link.download = '每日一图.jpg';
                link.click();
            </script>
        </body>
    </html>
"""

# 嵌入自定义 HTML 和 JavaScript 触发下载
st.components.v1.html(html_code)

# 显示图片
st.image(img, use_column_width=True)

