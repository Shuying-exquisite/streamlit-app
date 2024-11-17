import streamlit as st
import random
import time

# 定义图片链接列表
image_urls = [
    "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/1.jpg",
    "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/2.jpg",
    "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/3.jpg",
    # 其他图片链接...
]

# 随机选择一个链接
random_image_url = random.choice(image_urls)

# 延时跳转
time.sleep(2)  # 延时2秒后跳转
st.experimental_set_query_params(url=random_image_url)

# 执行页面跳转
st.markdown(f"<meta http-equiv='refresh' content='0; url={random_image_url}'>", unsafe_allow_html=True)
