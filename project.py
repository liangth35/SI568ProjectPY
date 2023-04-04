import streamlit as st
from streamlit_chat import message
import openai
from audio_recorder_streamlit import audio_recorder
import wave
import random


def respond(prompt):
    '''
    call gpt-3.5 api to respond to prompt,
    add prompt and response to chat history in session state
    args:
        prompt: string, prompt to gpt-3.5
    return:
        None
    '''
    try:
        st.session_state.chathistory.append({"role": "user", "content": prompt})
        ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.chathistory,
        )
        st.session_state.chathistory.append({"role": "assistant", "content": ans['choices'][0]['message']['content']})
    except:
        st.error("Error when requesting gpt response")

def clear_history():
    '''
    clear chat history and text input from session state
    args:
        None
    return:
        None
    '''
    st.session_state.chathistory = [{"role": "system", "content": "You a helpuful assistant."}]
    st.session_state.text_input = ''


def send_audio():
    '''
    save audio bytes to a wav file, then
    send the audio file to whisper api and get the transcription,
    then call respond function to get the response to the transcription from gpt-3.5 api
    args:
        None
    return:
        None
    '''
    try:
        if len(st.session_state.audio_bytes)>100:
            with wave.open("out.wav", "wb") as output_file:
                num_channels = 2
                sample_width = 2
                frame_rate = 44100
                num_frames = len(st.session_state.audio_bytes) // (num_channels * sample_width)
                compression_type = "NONE"
                compression_name = "not compressed"
                output_file.setparams((num_channels, sample_width, frame_rate, num_frames, compression_type, compression_name))
                output_file.writeframes(st.session_state.audio_bytes)

            audio_file = open("out.wav", "rb")
            result = openai.Audio.transcribe("whisper-1", audio_file)
            respond(result.text)
        else:
            st.error("Audio too short")
    except:
        st.error("Record audio first")

def send_text():
    '''
    call respond function to get the response to the text input from gpt-3.5 api if text input is not empty,
    then clear text input from session state
    args:
        None
    return:
        None
    '''
    if st.session_state.text_input!='':
        respond(st.session_state.text_input)
        st.session_state.text_input=''

# Start of streamlit app
st.title("Audio chatBot")
openai.api_key = st.secrets["API_KEY"]
if "chathistory" not in st.session_state: # initialize chat history in session state
    st.session_state.chathistory = [{"role": "system", "content": "You a helpuful assistant."}]

# audio recorder widget
st.session_state.audio_bytes = audio_recorder(pause_threshold=1)
st.button("Send Audio", key="send_audio", on_click=send_audio)

# text input widget
if 'text_input' not in st.session_state:st.session_state.text_input=''
st.text_input("Enter text: ",placeholder='ask anything', key="text_input", value=st.session_state.text_input, on_change=send_text)

# chat history widget
st.button("Clear History", key="clear_button", on_click=clear_history)
for item in reversed(st.session_state.chathistory):
    if item['role'] == 'user':
        message(item['content'], is_user=True, key=random.randint(0, 1000000))
    elif item['role'] == 'assistant':
        message(item['content'], is_user=False, key=random.randint(0, 1000000))