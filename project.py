import streamlit as st
from streamlit_chat import message
import openai

openai.api_key = st.secrets["API_KEY"]
st.title("chatBot : Streamlit + openAI")

if "chathistory" not in st.session_state:
    st.session_state.chathistory = [{"role": "system", "content": "You a helpuful assistant."}]

def respond(prompt):
    st.session_state.chathistory.append({"role": "user", "content": prompt})
    ans = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.chathistory,
    )
    st.session_state.chathistory.append({"role": "assistant", "content": ans['choices'][0]['message']['content']})
    return ans['choices'][0]['message']['content']

user_input = st.text_input("You: ",placeholder='ask anything', key="input")
message(len(st.session_state.chathistory))
for item in st.session_state.chathistory:
    if item['role'] == 'user':
        message(item['content'], is_user=True)
    elif item['role'] == 'assistant':
        message(item['content'], is_user=False)
message(user_input, is_user=True)
message(respond(user_input), is_user=False)
