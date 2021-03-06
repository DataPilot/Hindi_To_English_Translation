import requests
import streamlit as st
from moviepy.editor import *
from moviepy.video.VideoClip import VideoClip
from pydub import AudioSegment
from textblob import TextBlob

st.title("Video --> Text --> Urdu Translation")
st.write()

subscription_key = 'be934929aaa74b068f1aa6ec0e32e3f8'
url = "https://centralindia.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=hi-IN"

headers = {
    'Content-type': 'audio/wav;codec="audio/pcm";',
    'Ocp-Apim-Subscription-Key': 'be934929aaa74b068f1aa6ec0e32e3f8',
}

uploaded_file = st.file_uploader("Choose an mp4 video file...")
st.header("Processing Video")
if uploaded_file is not None:
    with open("sample.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
        video = VideoFileClip("sample.mp4")
        st.write("converting to readable wave format")
        video.audio.write_audiofile("sample.mp3")
        sound = AudioSegment.from_mp3("sample.mp3")
        sound.export("sample.wav", format="wav")
        st.write("Format conversion successful!")

    with open("sample.wav", 'rb') as payload:
        st.header("Processing Audio")
        response = requests.request("POST", url, headers=headers, data=payload)
        long_text = response.text.split('DisplayText":')[
            1].split(',"Offset')[0]
        st.subheader("Speech To Text Result")
        st.write(long_text)

        st.header("Translating to Urdu")
        blob_ = TextBlob(long_text)
        output = blob_.translate(to='ur')
        st.subheader("Translation Result")
        st.write(output)
