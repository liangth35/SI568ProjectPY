import streamlit as st
from streamlit_chat import message
import streamlit.secrets as secrets
import openai

openai.api_key = secrets["API_KEY"]
st.title("chatBot : Streamlit + openAI")

def respond(prompt):
    ans = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You a helpuful assistant."},
            # {"role": "user", "content": "Who won the world series in 2020?"},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            # {"role": "user", "content": "What's the difference between spin lock and mutex?"},
            {"role": "user", "content": prompt},
        ]
    )
    return(ans['choices'][0]['message']['content']) 

user_input = st.text_input("You: ","Hello, how are you?", key="input")
message(user_input, is_user=True)
message(respond(user_input))