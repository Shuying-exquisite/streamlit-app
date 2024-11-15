import streamlit as st
import re
import os

folder_path = "/mount/src/streamlit-app/刷步数"  # 指定文件夹路径

# 获取文件夹下的所有文件和子目录
files = os.listdir(folder_path)

# 打印文件和子目录列表
for file in files:
    st.write(file)

# 读取 Markdown 文件
with open("Operationdocument.md", "r", encoding="utf-8") as file:
    markdown_text = file.read()

# 在 Streamlit 应用中显示 Markdown 内容，同时处理图片
def render_markdown_with_images(markdown_text):
    # 匹配 Markdown 图片语法 ![alt text](image_url)
    pattern = re.compile(r'!\[.*?\]\((.*?)\)')

    # 记录上一个位置
    last_pos = 0

    # 查找所有匹配项
    for match in pattern.finditer(markdown_text):
        # 显示上一个位置到匹配位置之间的文本
        st.markdown(markdown_text[last_pos:match.start()], unsafe_allow_html=True)

        # 显示图片
        img_url = match.group(1)
        st.image(img_url)

        # 更新上一个位置
        last_pos = match.end()

    # 显示剩余的文本
    st.markdown(markdown_text[last_pos:], unsafe_allow_html=True)

# 调用函数显示内容
render_markdown_with_images(markdown_text)
