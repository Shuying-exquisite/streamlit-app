import streamlit as st

# 设置页面配置
st.set_page_config(page_title="每日一图", layout="wide", initial_sidebar_state="collapsed")

# 隐藏所有 Streamlit 默认元素
hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# 图片 URL（你可以动态获取每日一图链接，或者直接使用固定链接）
image_url = "https://raw.githubusercontent.com/Shuying-exquisite/streamlit-app/main/头像库接口/image/3.jpg"

# 显示图片
st.image(image_url, caption="每日一图", use_column_width=True)
