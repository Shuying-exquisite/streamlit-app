import streamlit as st

# 图片 URL
image_url = "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/3.jpg"

# 隐藏所有页面元素
st.set_page_config(page_title="图片展示", layout="centered")

# 仅显示图片
st.image(image_url, caption="头像图片", use_column_width=True)

