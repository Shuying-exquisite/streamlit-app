import streamlit as st

# 在Streamlit应用中嵌入本地视频文件
st.title('视频播放器示例')

# 提供本地视频文件路径或网络视频链接
video_path = 'path/to/your/video.mp4'

# 使用 st.video() 播放视频
st.video(video_path)

