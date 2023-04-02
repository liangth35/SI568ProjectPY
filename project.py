import streamlit as st
from streamlit_chat import message
import openai

openai.api_key = st.secrets["API_KEY"]
st.title("chatBot : Streamlit + openAI")

chathistory = [{"role": "system", "content": "You a helpuful assistant."}]

def respond(prompt):
    chathistory.append({"role": "user", "content": prompt})
    ans = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chathistory,
    )
    chathistory.append({"role": "assistant", "content": ans['choices'][0]['message']['content']})
    return ans['choices'][0]['message']['content']

user_input = st.text_input("Ask gpt anything: ","Hello, how are you?", key="input")
message(user_input, is_user=True)
message(respond(user_input))