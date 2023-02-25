
from flask import Flask, render_template, request

import requests
from youtube_transcript_api import YouTubeTranscriptApi


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

    response = requests.post(endpoint, json=json, headers=headers)
    print(response.json())

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


@app.route("/language", methods=['POST'])
def language():
    lang = request.form.get("language")
    url = "https://v1.genr.ai/api/circuit-element/translate-text"
    temp_questions = []

    global questions
    print(questions)
    question_str = ""
    for i in questions:
        question_str += i
        question_str += "."

    payload = {
        "text": question_str,
        "temperature": 0.3,
        "target_language": lang
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    ques_dic = response.text
    # print(response.text)
    questions_str = ques_dic.split(':')[1]
    questions_list = questions_str.split('\\n')
    questions_list[0] = questions_list[0][1:]
    questions_list[len(questions_list) - 1] = questions_list[len(questions_list) - 1][:-2]
    # print(temp_questions)
    return render_template("display.html", questions=questions_list)



if __name__ == "__main__":
    app.run()

# {"output":"1. What are the three common writing challenges that can be undertaken when using a random paragraph?\n2. How can a random paragraph be used to start a short story?\n3. What are the benefits of using a random paragraph to get creative flow going?\n4. How can a random paragraph be used in the middle of a short story?\n5. What are the advantages of using a random paragraph as the ending of a short story?"}

