import streamlit as st

st.set_page_config(page_title="Deepseek", page_icon="🐋", layout="wide", initial_sidebar_state="expanded", menu_items=None)

sidebar_selection = st.sidebar.selectbox("Functions",["API面版","对话"])

if sidebar_selection == "API面版":

    st.header("API面版")
    st.markdown("***")
    st.components.v1.iframe("https://platform.deepseek.com/usage",width = 1080, height = 720)

elif sidebar_selection == "对话":
    st.markdown("***")
    st.components.v1.iframe("https://chat.deepseek.com/",width = 1080, height = 720)


