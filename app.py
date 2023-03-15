import json
import os

import openai
from flask import Flask, render_template, request

from src.tts.tencent_tts import tts

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/completions", methods=["POST"])
def completions():
    try:
        animal = request.form["prompt"]
        print(animal)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=animal,
            # suffix="",
            max_tokens=2048,
            temperature=0.6,
            # top_p=1,
            # n=1,
            # stream=False,
            # logprobs=None,
            # echo=False,
            # stop=None,
            # presence_penalty=0,
            # frequency_penalty=0,
            # best_of=0,
            # logit_bias=0,
            # user="",
        )
        print("completions response: %s" % json.dumps(response, ensure_ascii=False))
        # return redirect(url_for("index", result=response.choices[0].text))
        # return response.choices[0].text
        return response
    except Exception as e:
        print(e)
    # return request.args.get("result")
    return {}


@app.route("/models", methods=["GET"])
def models():
    try:
        response = openai.Model.list()
        print("models response: %s" % json.dumps(response, ensure_ascii=False))
    except Exception as e:
        print(e)
    return {}


@app.route("/models/<model_id>", methods=["GET"])
def model(model_id):
    try:
        response = openai.Model.get(model_id)
        print("model response: %s" % json.dumps(response, ensure_ascii=False))
    except Exception as e:
        print(e)
    return {}


@app.route("/edits", methods=["POST"])
def edits():
    try:
        _input = request.form["input"]
        instruction = request.form["instruction"]
        response = openai.Edit.create(
            model="text-davinci-003",
            input=_input,
            instruction=instruction,
        )
        print("edit response: %s" % json.dumps(response, ensure_ascii=False))
    except Exception as e:
        print(e)
    return {}


@app.route("/images/generations", methods=["POST"])
def generate_images():
    try:
        prompt = request.form["prompt"]
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        print("generate image response: %s" % json.dumps(response, ensure_ascii=False))
        return response
    except Exception as e:
        print(e)
    return {}


@app.route("/images/edit", methods=["POST"])
def edit_images():
    try:
        file_name = request.form["file_name"]
        mask = request.form["mask"]
        prompt = request.form["prompt"]
        response = openai.Image.create(
            image=open(file_name, "rb"),
            mask=open(mask, "rb"),
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        print("generate image response: %s" % json.dumps(response, ensure_ascii=False))
    except Exception as e:
        print(e)
    return {}


@app.route("/images/variations", methods=["POST"])
def vary_images():
    try:
        file_name = request.form["file_name"]
        response = openai.Image.create(
            image=open(file_name),
            n=1,
            size="1024x1024",
        )
        print("generate image response: %s" % json.dumps(response, ensure_ascii=False))
    except Exception as e:
        print(e)
    return {}


@app.route("/fine_tuned/list", methods=["GET"])
def fine_tuned_list():
    try:
        response = openai.Model.list()
        print("fine tuned list response: %s" % json.dumps(response, ensure_ascii=False))
    except Exception as e:
        print(e)
    return {}


@app.route("/fine_tuned/completions", methods=["POST"])
def fine_tuned_completions():
    try:
        fine_tuned_model = request.form["fine_tuned_model"]
        prompt = request.form["prompt"]
        response = openai.Completion.create(
            model=fine_tuned_model,
            prompt=prompt
        )
        print("generate image response: %s" % json.dumps(response, ensure_ascii=False))
    except Exception as e:
        print(e)
    return {}


@app.route("/audio/transcriptions", methods=["POST"])
def audio_transcriptions():
    try:
        audio_file_name = request.form["file_path"]
        audio_file = open(audio_file_name, "rb")
        response = openai.Audio.transcribe("whisper-1", audio_file)
        print("audio transcriptions response: %s" % json.dumps(response, ensure_ascii=False))
        return response
    except Exception as e:
        print(e)
    return {}


dialog = []


@app.route("/chat/completions", methods=["POST"])
def chat():
    global dialog
    try:
        prompt = request.form["prompt"]
        if not dialog:
            dialog.append({
                "role": "system",
                "content": prompt
            })
        else:
            dialog.append({
                "role": "user",
                "content": prompt
            })
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model="gpt-4.0",
            messages=dialog
        )
        print("chat completion response: %s" % json.dumps(response, ensure_ascii=False))
        dialog.append({
            "role": "assistant",
            "content": response.get("choices")[0].get("message").get("content")
        })
        return {"dialog": dialog}
    except Exception as e:
        print(e)
    return {}


@app.route("/file/upload", methods=["POST"])
def file_upload():
    try:
        audio_file = request.files["audio"]
        print(audio_file)
        audio_file.save("./record.webm")
        trans = open("./record.webm", "rb")
        response = openai.Audio.transcribe("whisper-1", trans)
        print("audio transcriptions response: %s" % json.dumps(response, ensure_ascii=False))

        prompt = response.get("text")

        global dialog
        try:
            # prompt = request.form["prompt"]
            # system = request.form["system"]

            # if system and not dialog:
            #     dialog.append({
            #         "role": "system",
            #         "content": system
            #     })
            if dialog:
                dialog.append({
                    "role": "user",
                    "content": prompt
                })
            else:
                dialog.append({
                    "role": "system",
                    "content": prompt
                })
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                # model="gpt-4.0",
                messages=dialog
            )
            print("chat completion response: %s" % json.dumps(response, ensure_ascii=False))
            resp_content = response.get("choices")[0].get("message").get("content")
            dialog.append({
                "role": "assistant",
                "content": resp_content
            })
            if len(resp_content) < 150:
                print("whole content")
                audio = tts(resp_content)
            else:
                print("first 150:[%s]" % resp_content[:150])
                audio = tts(resp_content[:150])
            return {"dialog": dialog, "audio": audio}
        except Exception as e:
            print(e)
        return {}
    except Exception as e:
        print(e)
    return {}
