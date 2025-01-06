import datetime as dtime
import time
import json
from Supports import *

st.set_page_config(page_title="AI Collegues", page_icon="🤴", layout="wide", initial_sidebar_state="expanded", menu_items=None)#设置页面标题、图标、布局、初始侧边栏状态、菜单项

# 初始化session_state
if "API_KEY" not in st.session_state:
    st.session_state.API_KEY = None # 存储Deepseek API Key
if "Agents" not in st.session_state:
    st.session_state.Agents = {} # 存储Agent配置
if "Tasks" not in st.session_state:
    st.session_state.Tasks = [] # 存储Task配置
if "add_agent" not in st.session_state:
    st.session_state.add_agent = 0 # 0: 初始状态面版, 1: 添加Agent的面版 2: 编辑Agent的面版
if "add_task" not in st.session_state:
    st.session_state.add_task = 0 # 0: 初始状态面版, 1: 添加Task的面版 2: 编辑Task的面版

@st.cache_data
def try_apikey(API_KEY):
    try:
        get_deepseek_response(API_KEY, "",[{"role":"user","content":"请回复1"}],0.7,10)
        return 1
    except:
        return 0

#输入APIKEY
API_KEY = st.sidebar.text_input("API Key",type="password",value=st.session_state.API_KEY,help="为使用全部功能, 请在此输入一个可用的Deepseek API Key")
if API_KEY:
    st.session_state.API_KEY = API_KEY
    if try_apikey(API_KEY) == 0:
        st.sidebar.error("API Key无效, 请检查后重新输入")
        st.session_state.API_KEY = None
    else:
        st.session_state.API_KEY = API_KEY

agents_or_tasks = st.sidebar.selectbox("Edify Mode",["AI Agents","Tasks"], help="选择你想要操作的对象组")

st.sidebar.markdown("---")

maincol = st.columns(2)
with maincol[0]:
    st.subheader("AI Agents")
    st.json(st.session_state.Agents) #测试用, 展示session_state中的Agents

with maincol[1]:
    st.subheader("Tasks")
    st.write(st.session_state.Tasks) #测试用, 展示session_state中的Tasks

if st.session_state.API_KEY == None:
    st.warning("请先输入API Key")

else:   

    if agents_or_tasks == "AI Agents":

        if st.session_state.add_agent == 0:
            
            subcol = st.sidebar.columns(2)

            add_agent = subcol[0].button("添加Agent",help="添加或自定义一个AI Agent",)
            if add_agent:
                st.session_state.add_agent = 1
                st.rerun()

            edit_agent = subcol[1].button("修改Agent",help="编辑已添加的AI Agent")
            if edit_agent:
                st.session_state.add_agent = 2
                st.rerun()
            st.sidebar.markdown("---")

            upload_agent_config = st.sidebar.file_uploader(
                label="Upload Agent Config",
                type=["json"],
                accept_multiple_files=False,
                help="上传Agent配置"
            )

            apply_agent_config = st.sidebar.button("Apply Agent Config",help="应用Agent配置")
            if apply_agent_config and upload_agent_config != None:

                uploaded_agent_config = upload_agent_config.read()
                try:
                    # 解析 JSON 数据
                    st.session_state.Agents = json.loads(uploaded_agent_config)
                    st.rerun()
                except Exception as e:
                    st.error(f"{e}\nInvalid JSON file. Please upload a valid JSON file.")
                    
            st.sidebar.markdown("---")
            
            download_agent_config = st.sidebar.download_button(
                label="Donwload Agent Config",
                file_name=f"agent_config{dtime.datetime.now().strftime('%Y%m%d%H%M%S')}.json",
                data = json.dumps(st.session_state.Agents, indent=4),
                mime="text/json",
                help="下载当前Agent配置"
            )
            st.sidebar.markdown("---")

        elif st.session_state.add_agent == 1:

            with open("Agent_paradigms.json", "r", encoding="utf-8") as f:
                agent_paradigms = json.load(f)

            agent_type = st.sidebar.selectbox("Agent模板",["自定义","(Chinese)Prompt Improver", "(Chinese)Formater", "(Chinese)Summary Assistant", "(Chinese)Developer", "(Chinese)Tester", "(Chinese)Project Manager", "(Chinese)Data Scientist", "(Chinese)UX Designer", "(Chinese)Content Writer", "(Chinese)Security Analyst", "(Chinese)Marketing Specialist", "(Chinese)Customer Support Agent", "(Chinese)Financial Analyst", "(Chinese)Human Resources Manager", "(Chinese)Research Scientist", "Prompt Improver", "Formater", "Summary Assistant", "Developer", "Tester", "Project Manager", "Data Scientist", "UX Designer", "Content Writer", "Security Analyst", "Marketing Specialist", "Customer Support Agent", "Financial Analyst", "Human Resources Manager", "Research Scientist"])

            if agent_type == "自定义":

                agent_name = st.sidebar.text_input("Agent名称",help="请输入Agent名称, 不能重复")
                agent_role = st.sidebar.text_input("Agent Role",help="请输入Agent的身份")
                agent_background = st.sidebar.text_area("Agent Background",help="请输入Agent的背景, 这会在很大程度上决定Agent的职能")
                agent_goal = st.sidebar.text_area("Agent Goal",help="请输入Agent的目标")
                agent_temp = st.sidebar.slider("Agent Temperature",min_value=0.5,max_value=1.5,value=1.0,step=0.1,help="设置Agent的温度, 温度越高, 回复不确定性越大; 越低则反是")
            
            else:

                agent_name = st.sidebar.text_input("Agent名称",help="请输入Agent名称, 不能重复",value=agent_paradigms[agent_type]["role"])
                agent_role = st.sidebar.text_input("Agent Role",help="请输入Agent的身份",value=agent_paradigms[agent_type]["role"])
                agent_background = st.sidebar.text_area("Agent Background",help="请输入Agent的背景, 这会在很大程度上决定Agent的职能",value=agent_paradigms[agent_type]["background"])
                agent_goal = st.sidebar.text_area("Agent Goal",help="请输入Agent的目标",value=agent_paradigms[agent_type]["goal"])
                agent_temp = st.sidebar.slider("Agent Temperature",min_value=0.5,max_value=1.5,value=agent_paradigms[agent_type]["temp"],step=0.1)
            
            col = st.sidebar.columns(2)
            
            confirm_add = col[0].button("确认添加",help="确认添加Agent")
            if confirm_add:
                if agent_name in st.session_state.Agents:
                    st.sidebar.error("Agent名称重复, 请重新输入")
                elif agent_name == "":
                    st.sidebar.error("Agent名称不能为空, 请重新输入")
                else:
                    st.session_state.Agents[agent_name] = {"role":agent_role,"background":agent_background,"goal":agent_goal,"temp":agent_temp}
                    
                    st.sidebar.success("添加成功")
                    time.sleep(0.3)
                    st.rerun()

            back = col[1].button("返回",help="返回")
            if back:
                st.session_state.add_agent = 0
                st.rerun()

        elif st.session_state.add_agent == 2:

            if st.session_state.Agents == {}:
                st.sidebar.write("无Agent捏")

                back = st.sidebar.button("返回",help="返回")
                if back:
                    st.session_state.add_agent = 0
                    st.rerun()
            else:
                agent_name = st.sidebar.selectbox("Agent名称",list(st.session_state.Agents.keys()))

                edited_agent_name = st.sidebar.text_input("Agent名称",value=agent_name,help="请输入Agent名称")
                edited_agent_role = st.sidebar.text_input("Agent Role",value=st.session_state.Agents[agent_name]["role"],help="请输入Agent的身份")
                edited_agent_background = st.sidebar.text_area("Agent Background",value=st.session_state.Agents[agent_name]["background"],help="请输入Agent的背景")
                edited_agent_goal = st.sidebar.text_area("Agent Goal",value=st.session_state.Agents[agent_name]["goal"],help="请输入Agent的目标")
                edited_agent_temp = st.sidebar.slider("Agent Temperature",min_value=0.5,max_value=1.5,value=st.session_state.Agents[agent_name]["temp"],step=0.1,help="请输入Agent的温度")

                col = st.sidebar.columns(3)
                
                confirm_edit = col[0].button("修改",help="确认修改Agent")
                if confirm_edit:
                    if agent_name == "":
                        st.sidebar.error("Agent名称不能为空, 请重新输入")
                    elif edited_agent_name in st.session_state.Agents and edited_agent_name != agent_name:
                        st.sidebar.error("Agent名称重复, 请重新输入")
                    else:

                        if agent_name != edited_agent_name:
                            for task in st.session_state.Tasks:
                                if agent_name == task["agent"]:
                                    task["agent"] = edited_agent_name

                        del st.session_state.Agents[agent_name]
                        st.session_state.Agents[edited_agent_name] = {}
                        st.session_state.Agents[edited_agent_name]["role"] = edited_agent_role
                        st.session_state.Agents[edited_agent_name]["background"] = edited_agent_background
                        st.session_state.Agents[edited_agent_name]["goal"] = edited_agent_goal
                        st.session_state.Agents[edited_agent_name]["temp"] = edited_agent_temp
                        
                        st.sidebar.success("修改成功")
                        time.sleep(0.3)
                        st.rerun()
                
                delete_agent = col[1].button("删除",help="删除Agent")
                if delete_agent:
                    del st.session_state.Agents[agent_name]

                    for task in st.session_state.Tasks:
                        if agent_name == task["agent"]:
                            task["agent"] = None
                    
                    st.sidebar.success("删除成功")
                    time.sleep(0.3)
                    st.rerun()

                back = col[2].button("返回",help="返回")
                if back:
                    st.session_state.add_agent = 0
                    st.rerun()

    elif agents_or_tasks == "Tasks":

        if st.session_state.add_task == 0:

            subcol = st.sidebar.columns(2)

            add_task = subcol[0].button("添加Task",help="添加或自定义一个Task")
            if add_task:
                st.session_state.add_task = 1
                st.rerun()

            edit_task = subcol[1].button("修改Task",help="编辑已添加的Task")
            if edit_task:
                st.session_state.add_task = 2
                st.rerun()
            st.sidebar.markdown("---")

            upload_task_config = st.sidebar.file_uploader(
                label="Upload Task Config",
                type=["json"],
                accept_multiple_files=False,
                help="上传Task配置"
            )

            apply_task_config = st.sidebar.button("Apply Task Config(NOT IMPLEMENTED YET)",help="应用Task配置")

            if apply_task_config and upload_task_config != None:
                uploaded_task_config = upload_task_config.read()
                try:
                    # 解析 JSON 数据
                    st.session_state.Tasks = json.loads(uploaded_task_config)
                    st.rerun()
                except Exception as e:
                    st.error(f"{e}\nInvalid JSON file. Please upload a valid JSON file.")
            
            download_task_config = st.sidebar.download_button(
                label="Donwload Task Config",
                file_name=f"task_config{dtime.datetime.now().strftime('%Y%m%d%H%M%S')}.json",
                data = json.dumps(st.session_state.Tasks, indent=4),
                mime="text/json",
                help="下载当前Task配置"
            )
            st.sidebar.markdown("---")


        if st.session_state.add_task == 1:

            add_task_name = st.sidebar.text_input("Task名称",help="请输入Task名称")
            add_task_priority = st.sidebar.number_input("Task优先级",min_value=0,max_value=10,value=len(st.session_state.Tasks),help="在指定位置(0-10)插入task")
            assigned_agent = st.sidebar.selectbox("分配给该Task的Agent",list(st.session_state.Agents.keys()),help="选择Agent")
            add_task_description = st.sidebar.text_area("Task描述",help="请输入Task内容")
            add_task_background = st.sidebar.multiselect("Task前置任务",st.session_state.Tasks[:add_task_priority],help="选择后, 前置任务的输出会提供给对应Agent")

            col = st.sidebar.columns(2)
            
            confirm_add = col[0].button("确认添加",help="确认添加Task")
            if confirm_add:
                err = 0
                for task in st.session_state.Tasks:
                    if task["name"] == add_task_name:
                        st.sidebar.error("Task名称重复, 请重新输入")
                        err = 1
                        break
                
                if err == 0:
                    if add_task_priority == len(st.session_state.Tasks):
                        st.session_state.Tasks.append({"name":add_task_name,"agent":assigned_agent,"description":add_task_description,"background":add_task_background})
                    else:
                        st.session_state.Tasks.insert(add_task_priority,{"name":add_task_name,"agent":assigned_agent,"description":add_task_description,"background":add_task_background})
                
                    st.sidebar.success("添加成功")
                    time.sleep(0.3)
                    st.rerun()
            
            back = col[1].button("返回",help="返回")
            if back:
                st.session_state.add_task = 0
                st.rerun()


        if st.session_state.add_task == 2:
            if st.session_state.Tasks == []:
                st.sidebar.write("无Task捏")

                back = st.sidebar.button("返回",help="返回")
                if back:
                    st.session_state.add_task = 0
                    st.rerun()
            else:
                chosen_task = st.sidebar.selectbox("选择Task",st.session_state.Tasks)
                chosen_task_index = st.session_state.Tasks.index(chosen_task)

                edited_task_name = st.sidebar.text_input("Task名称",value=chosen_task["name"],help="请输入Task名称")

                edited_assigned_agent = st.sidebar.selectbox("分配给该Task的Agent",list(st.session_state.Agents.keys()),help="选择Agent")

                edited_task_description = st.sidebar.text_area("Task描述",value=chosen_task["description"],help="请输入Task内容")
                
                edited_task_background = st.sidebar.multiselect("Task前置任务",st.session_state.Tasks[:chosen_task_index],help="选择后, 前置任务的输出会提供给对应Agent")

                col = st.sidebar.columns(3)
                
                confirm_edit = col[0].button("修改",help="确认修改Task")
                if confirm_edit:
                    if edited_task_name == "":
                        st.sidebar.error("Task名称不能为空, 请重新输入")
                    else:
                        err = 0
                        for task in st.session_state.Tasks:
                            if task["name"] == edited_task_name and task != chosen_task:
                                st.sidebar.error("Task名称重复, 请重新输入")
                                err = 1
                                break
                        if err == 0:
                            edit_index = st.session_state.Tasks.index(chosen_task)
                            st.session_state.Tasks[edit_index]["name"] = edited_task_name
                            st.session_state.Tasks[edit_index]["agent"] = edited_assigned_agent
                            st.session_state.Tasks[edit_index]["description"] = edited_task_description
                            st.session_state.Tasks[edit_index]["background"] = edited_task_background

                            st.sidebar.success("修改成功")
                            time.sleep(0.3)
                            st.rerun()
                
                delete_task = col[1].button("删除",help="删除Task")
                if delete_task:
                    edit_index = st.session_state.Tasks.index(chosen_task)
                    del st.session_state.Tasks[edit_index]

                    st.sidebar.success("删除成功")
                    time.sleep(0.3)
                    st.rerun()

                back = col[2].button("返回",help="返回")
                if back:
                    st.session_state.add_task = 0
                    st.rerun()

if st.sidebar.button("Kickout",help="开始运行AI Collegues!"):

    if st.session_state.Agents == {}:
        st.error("请先添加Agent")

    elif st.session_state.Tasks == []:
        st.error("请先添加Task")

    else:
        err = 0
        for task in st.session_state.Tasks:
            if task["agent"] == None:
                st.error("请先为所有任务指派Agent")
                err = 1
                break
        if err == 0:

            for task in st.session_state.Tasks: #开始按顺序遍历每一个任务

                prompt =  f"任务名称: {task['name']}\n任务描述: {task['description']}\n"

                sys_message = f"""Role: 在我们的开发团队中, 你是"{st.session_state.Agents[task['agent']]['role']}"这一关键角色。\nBackground: \n{st.session_state.Agents[task['agent']]['background']}"""
            
                if task["background"] != []: #如果该任务有前置任务
                    prompt += f"""\n以下是已经做过的任务: \n"""

                    for background_task in task["background"]:
                        
                        background_task_name = background_task["name"]
                        background_task_description = background_task["description"]
                        background_task_agent = background_task["agent"]
                        for find_task in st.session_state.Tasks:
                            if find_task["name"] == background_task_name:
                                background_task_output = find_task["output"]
                                background_task_index = st.session_state.Tasks.index(find_task)
                                break
                        
                        prompt += f"""\n\t任务名称:{background_task_name}\t完成者:{background_task_agent}\n\t任务描述: {background_task_description}\n\t"{background_task_agent}"任务成果:\n\t{background_task_output}\n"""
                
                working_condition = st.empty()
                task_index = st.session_state.Tasks.index(task)
                with working_condition:
                    st.write(f"starting task[{task_index}]...")

                ####test
                # with open(f"prompt{task_index}","w",encoding="utf-8") as f:
                #     f.write(sys_message)
                #     f.write(prompt)
                
                output = get_deepseek_response(st.session_state.API_KEY,sys_message,[{"role":"user","content":prompt}],st.session_state.Agents[task['agent']]['temp'])

                st.session_state.Tasks[task_index]["output"] = output #将输出存入task中

                with working_condition:
                    st.write(f"task[{task_index}] finished.")
        
            ans = ""
            for task in st.session_state.Tasks:
                ans += f"Task{st.session_state.Tasks.index(task)}: {task['name']}\t\tAgent: {task['agent']}\nOutput: {task['output']}\n\n\n"
            
            download_answers = st.sidebar.download_button(
                label="Download Answers",
                file_name=f"answers{dtime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                data=ans,
                mime="text/plain",
                help="下载所有Task的输出"
            )


                    

                            
                            
                            
                      
                            

                    