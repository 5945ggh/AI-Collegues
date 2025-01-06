import datetime as dtime

import streamlit as st
from openai import OpenAI


def get_deepseek_response(api_keys = None, sys_message:str = "", message:list = [], temp:float = 1 ,max_tokens:int = None) -> str:
    
    #message标准示例: [{"role":"user","content":"You are an assistant"},{"role":"user","content":"str"}]
    if max_tokens == None:

        client = OpenAI(api_key=api_keys, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(

            model="deepseek-chat",
            messages=[{"role": "system", "content": sys_message}] + message,
            temperature=temp,
            stream=False
        )
    else:
        
        client = OpenAI(api_key=api_keys, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(

            model="deepseek-chat",
            messages=[{"role": "system", "content": sys_message}] + message,
            temperature=temp,
            max_tokens=max_tokens,
            stream=False
        )

    return(response.choices[0].message.content)



def get_txt(file_path)->str:

    try:
        with open(file_path, 'r',encoding='utf-8') as f:
            lines = []

            line = f.readline()
            while line != '':
                lines.append(line)
                line = f.readline()
            return(lines)
        
    except:
        print('文件读取错误.')
        return []