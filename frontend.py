import streamlit as st
import requests

BACKEND_URL='http://localhost:8000/ask'

st.set_page_config(page_title='AI Mental Health Assistant',page_icon=':robot_face:',layout='wide')
st.title('AI Mental Health Assistant')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
user_input=st.chat_input("what's on your mind?")
if user_input:
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
    response=requests.post(BACKEND_URL, json={'message':user_input})
    
   
    st.session_state.chat_history.append({'role':'assistant','content':f"{response.json()['response']} TOOL CALLED [{response.json()['tool_called']}]" })
    
    
for msg in st.session_state.chat_history:
    with st.chat_message(msg['role']):
        st.write(msg['content'])