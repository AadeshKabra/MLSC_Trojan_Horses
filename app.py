from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_dl import YoutubeDL
from pytube import YouTube
import os
import speech_recognition as sr
import ffmpeg
import wave, math, contextlib
from moviepy.editor import AudioFileClip
import io
from pydub import AudioSegment
from pydub.silence import split_on_silence
from google.cloud import speech_v1p1beta1 as speech
import pyaudio
import speechmatics
import requests

app = Flask(__name__)


def get_response(link):
    {
        "upload_url": "https://cdn.assemblyai.com/upload/f4932e0c-4f0a-40b8-8994-bdae0c0980fb"
    }
    # endpoint = "https://api.assemblyai.com/v2/transcript"
    #
    # json = {
    #   "audio_url": link
    # }
    #
    # headers = {
    #   "Authorization": "5bc89d5b393647ca8c16be552ecea059",
    #   "Content-Type": "application/json"
    # }

    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {"audio_url": "https://bit.ly/3yxKEIY"}
    headers = {
        "authorization": "5bc89d5b393647ca8c16be552ecea059",
    }
    response = requests.post(endpoint, json=json, headers=headers)

    # response = requests.post(endpoint, json=json, headers=headers)
    return response


def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/formInput", methods=['POST'])
def input():
    link = request.form.get("inputText")
    print(link)

    # Generating Mp4 file from youtube link
    yt = YouTube(link)
    stream = yt.streams.get_audio_only()
    stream.download(filename="video.mp4")


    transcribed_audio_file_name = "audio.wav"
    zoom_video_file_name = "video.mp4"

    audioclip = AudioFileClip(zoom_video_file_name)
    audioclip.write_audiofile(transcribed_audio_file_name)


    API_ENDPOINT = "https://api.assemblyai.com/v2/upload"
    file_path = "video.mp4"
    headers = {
        "Authorization": "5bc89d5b393647ca8c16be552ecea059",
    }

    with open(file_path, "rb") as file:
        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            data=file,
        )

        # Get the ID of the uploaded file
        file_id = response.json()["upload_url"].split("/")[-1]



    API_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
    headers = {
        "Authorization": "5bc89d5b393647ca8c16be552ecea059",
        "Content-Type": "application/json",
    }

    data = {
        "audio_url": f"https://cdn.assemblyai.com/upload/{file_id}",
        "auto_highlights": True,
    }

    response = requests.post(
        API_ENDPOINT,
        headers=headers,
        json=data,
    )

    # Get the ID of the transcription job
    transcription_id = response.json()["id"]

    import requests
    import time

    API_ENDPOINT = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"
    headers = {
        "Authorization": "5bc89d5b393647ca8c16be552ecea059",
    }

    while True:
        response = requests.get(
            API_ENDPOINT,
            headers=headers,
        )
        response_data = response.json()
        status = response_data["status"]

        if status == "completed":
            transcript_text = response_data["text"]
            print(transcript_text)
            break

        time.sleep(5)
    # filename = "audio.wav"
    # headers = {'authorization': "YOUR-API-TOKEN"}
    # response = requests.post('https://api.assemblyai.com/v2/upload',
    #                          headers=headers,
    #                          data=read_file(filename))
    #
    # print(response.json())

    # response = get_response(link)
    # response_dic = response.json()
    # # parse(response)
    # print(response_dic)
    return render_template("text.html")


if __name__ == "__main__":
    app.run()



