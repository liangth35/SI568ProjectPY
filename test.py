import whisper
import ffmpeg
import numpy as np
import os
print(os.getcwd()) 
def get_audio_buffer(filename: str, start: int, length: int):
    out, _ = (
        ffmpeg.input(filename, threads=0)
        .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000, ss=start, t=length)
        .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
    )

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

model = whisper.load_model("base")
with open("audio.wav", "rb") as file:
    result = model.transcribe(get_audio_buffer("audio.wav", 0, 10))
    print(result)