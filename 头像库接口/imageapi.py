import streamlit as st
import random

# 定义图片链接列表
image_urls = [
    "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/1.jpg",
    "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/2.jpg",
    "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/3.jpg",
    # 其他图片链接...
]

# 随机选择一个链接
random_image_url = random.choice(image_urls)

# 使用JavaScript打开新标签页
st.markdown(f"""
    <script type="text/javascript">
        window.open("{random_image_url}", "_blank");
    </script>
""", unsafe_allow_html=True)

# 提示用户操作
st.write("正在跳转到随机链接...")
