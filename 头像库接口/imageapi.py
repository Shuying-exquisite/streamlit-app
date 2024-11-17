import streamlit as st

# 设置页面配置，隐藏所有默认的 Streamlit UI 元素
st.set_page_config(page_title="每日一图", layout="centered", initial_sidebar_state="collapsed")

# 隐藏菜单、页脚和头部
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

# 仅显示图片
st.image(image_url, use_column_width=True)
