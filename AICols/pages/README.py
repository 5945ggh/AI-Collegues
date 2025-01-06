import streamlit as st

st.set_page_config(page_title="AI Collegues", page_icon="❓", layout="wide", initial_sidebar_state="expanded", menu_items=None)#设置页面标题、图标、布局、初始侧边栏状态、菜单项

st.title("AI Collegues")

st.markdown("""AI Collegues（AI打工人），是一个基于Streamlit的Web应用程序，用于模拟AI团队协作效果，灵感来源于Python库“CrewAI”\n
            使用说明：\n
            1.在https://platform.deepseek.com/usage 页面注册账号
            2.申请一个新的API密钥
            3.选择Edify mode为AI Agents, 创建Agents
            4.选择Edify mode为Tasks, 按顺序创建Tasks, 并为每一个Task指定一个对应Agent
            5.点击页面左下方的Kickoff按钮, 开始按顺序执行任务, 以此实现初步的AI协作效果
            6.下载结果文件
\n\n

TIPs:\n
1.如对安全性有所疑虑，可在每次使用时都临时申请一个Deepseek密钥，并在试用结束后及时在Deepseek API面版删除密钥。\n
2.每次上传密钥时，为确保密钥有效，程序会调用DeepseekAPI进行验证，过程所消耗的token可以忽略不计。\n
3.目前仅支持按顺序、一对一的任务树结构，后续（等我把异步再搞明白点（））或许将支持更复杂的任务结构。\n
            """)