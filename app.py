import librosa
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
from youtube_transcript_api import YouTubeTranscriptApi

import numpy as np
# import deepspeech
#
# model_file_path = 'deepspeech-0.9.3-models.pbmm'
# model = deepspeech.Model(model_file_path)

app = Flask(__name__)

questions = []

def correct_grammar(text):
    url = "https://v1.genr.ai/api/circuit-element/correct-grammar"

    payload = {
        "text": text,
        "temperature": 0
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    return response.text


def generate_questions(text, number):
    url = "https://v1.genr.ai/api/circuit-element/generate-questions"

    payload = {
        "text": text,
        "temperature": 0,
        "questions": number
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    # print(response.text)
    return response.text


def change_language(text, language):
    pass


def get_response(link):
    import requests
    filename = "audio.wav"

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {'authorization': "b2954594ba2543268070bf45ba7d7c97"}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                             headers=headers,
                             data=read_file(filename))

    print(response.json())


    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {"audio_url": response.json()['upload_url']}
    headers = {
        "authorization": "b2954594ba2543268070bf45ba7d7c97",
    }

    # endpoint = "https://api.assemblyai.com/v2/transcript"
    # json = {"audio_url": "https://bit.ly/3yxKEIY"}
    # headers = {
    #     "authorization": "YOUR-API-TOKEN",
    # }
    response = requests.post(endpoint, json=json, headers=headers)
    print(response.json())
    # while True:
    #     response = requests.get(endpoint, json=json, headers=headers)
    #     if response.json()["status"] == "processing":
    #         break
    # response = requests.get(endpoint, json=json, headers=headers)
    # print(response)
    # print(response.json()['transcripts'])

    endpoint = "https://api.assemblyai.com/v2/transcript/YOUR-TRANSCRIPT-ID-HERE"
    headers = {
        "authorization": "YOUR-API-TOKEN",
    }
    response = requests.get(endpoint, headers=headers)
    print(response.json())





@app.route("/")
def index():
    return render_template("index.html")


@app.route("/formInput", methods=['POST'])
def input():
    link = request.form.get("inputText")
    print(link)

    video_link = link
    v_index = video_link.index("v=")
    video_id = video_link[v_index + 2:]

    srt = YouTubeTranscriptApi.get_transcript(video_id)
    text_list = []
    for transcript in srt:
        text_list.append(transcript['text'])

    text = ' '.join(text_list)
    print(text)

    # Generating Mp4 file from youtube link
    # yt = YouTube(link)
    # stream = yt.streams.get_audio_only()
    # stream.download(filename="video.mp4")


    # transcribed_audio_file_name = "audio.wav"
    # zoom_video_file_name = "video.mp4"
    #
    # audioclip = AudioFileClip(zoom_video_file_name)
    # audioclip.write_audiofile(transcribed_audio_file_name)

    # text = get_response(link)
    # text = "Generating random paragraphs can be an excellent way for writers to get their creative flow going at the beginning of the day. The writer has no idea what topic random paragraph will be about when it appears. These forces the writer to use creativity to complete one of three common writing challenges. The writer can use the paragraph a the first one of a short story and build upon it. A second option is to use the random paragraph somewhere in a short story they create. The thi option is to have the random paragraph be the ending paragraph in a short story. No matter which of these challenges is undertook, the writer is forced to use creativity to incorporate the paragraph into their writing."

    return render_template("index.html", text=text)


@app.route("/correctGrammar", methods=['POST'])
def correctGrammar():
    text = request.form.get("text")
    return render_template("questions.html", text=text)


@app.route("/question", methods=['POST'])
def question():
    number = request.form.get("number")
    print(number)
    return render_template("questions.html")


@app.route("/questionGenerate", methods=['POST'])
def askQuestions():
    text = request.form.get("text")
    number = request.form.get("number")
    ques_dic = generate_questions(text, number)
    print(ques_dic)

    questions_str = ques_dic.split(':')[1]
    questions_list = questions_str.split('\\n')
    questions_list[0] = questions_list[0][1:]
    questions_list[len(questions_list)-1] = questions_list[len(questions_list)-1][:-2]
    print(questions_list)
    global questions
    questions = questions_list
    return render_template("display.html", questions=questions_list)


# @app.route("/language", methods=['POST'])
# def language():
#     lang = request.form.get("language")
#     url = "https://v1.genr.ai/api/circuit-element/translate-text"
#     temp_questions = []
#
#     global questions
#     for question in questions:
#         payload = {
#             "text": question,
#             "temperature": 0.3,
#             "target_language": lang
#         }
#         headers = {"Content-Type": "application/json"}
#
#         response = requests.request("POST", url, json=payload, headers=headers)
#
#         print(response.text)
#         temp_questions.append(response.text)
#
#     print(temp_questions)
#     return render_template("display.html", questions=temp_questions)



if __name__ == "__main__":
    app.run()

# {"output":"1. What are the three common writing challenges that can be undertaken when using a random paragraph?\n2. How can a random paragraph be used to start a short story?\n3. What are the benefits of using a random paragraph to get creative flow going?\n4. How can a random paragraph be used in the middle of a short story?\n5. What are the advantages of using a random paragraph as the ending of a short story?"}

