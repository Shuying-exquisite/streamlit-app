import streamlit as st

# 设置页面配置
st.set_page_config(page_title="图片展示", layout="centered", initial_sidebar_state="collapsed")

# 隐藏所有的默认元素（如：标题、边框等）
hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# 图片 URL
image_url = "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/3.jpg"

# 显示图片
st.image(image_url, caption="头像图片", use_column_width=True)
