import streamlit as st
from streamlit_chat import message
import openai
#from audio_recorder_streamlit import audio_recorder
# import whisper
import os
import numpy as np
from io import BytesIO
import streamlit.components.v1 as components
from st_custom_components import st_audiorec
import wave

openai.api_key = st.secrets["API_KEY"]
st.title("Audio chatBot")

if "chathistory" not in st.session_state:
    st.session_state.chathistory = [{"role": "system", "content": "You a helpuful assistant."}]

def respond(prompt):
    st.session_state.chathistory.append({"role": "user", "content": prompt})
    ans = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.chathistory,
    )
    st.session_state.chathistory.append({"role": "assistant", "content": ans['choices'][0]['message']['content']})

def clear_history():
    st.session_state.chathistory = [{"role": "system", "content": "You a helpuful assistant."}]
    st.session_state.text_input = ''

def send_audio():
    with wave.open("out.wav", "wb") as output_file:
        # set the number of audio channels (1 for mono, 2 for stereo)
        num_channels = 2
        # set the sample width (in bytes)
        sample_width = 2
        # set the frame rate (in Hz)
        frame_rate = 44100
        # set the number of frames
        num_frames = len(st.session_state.audio_bytes) // (num_channels * sample_width)
        # set the compression type and compression name
        compression_type = "NONE"
        compression_name = "not compressed"
        # set the parameters of the output file
        output_file.setparams((num_channels, sample_width, frame_rate, num_frames, compression_type, compression_name))
        # write the audio data to the output file
        output_file.writeframes(st.session_state.audio_bytes)

    audio_file = open("out.wav", "rb")
    result = openai.Audio.transcribe("whisper-1", audio_file)
    
    # if "model" not in st.session_state:
    #     st.session_state.model = whisper.load_model("tiny")
    # result = st.session_state.model.transcribe(st.session_state.audio_bytes.astype(np.float32))['text']

    respond(result.text)


st.session_state.audio_bytes = st_audiorec()

st.button("Send Audio", key="send_audio", on_click=send_audio)

st.text_input("You: ",placeholder='ask anything', key="text_input")
st.button("Clear History", key="clear_button", on_click=clear_history)

if st.session_state.text_input!='':
    respond(st.session_state.text_input)

for item in reversed(st.session_state.chathistory):
    if item['role'] == 'user':
        message(item['content'], is_user=True)
    elif item['role'] == 'assistant':
        message(item['content'], is_user=False)