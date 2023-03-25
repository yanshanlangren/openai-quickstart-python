import json
import os
import openai
from flask import Flask, render_template, request, Response
from src.service import chat_service
from src.service import file_service
from src.service import model_service
from src.service import completions_service
from src.service import edit_service
from src.service import image_service
from src.service import fine_tuned_service
from src.service import audio_service

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/completions", methods=["POST"])
def completions():
    prompt = request.form["prompt"]
    return completions_service.completions(prompt)


@app.route("/models", methods=["GET"])
def models():
    return model_service.list()


@app.route("/models/<model_id>", methods=["GET"])
def model(model_id):
    return model_service.get(model_id)


@app.route("/edits", methods=["POST"])
def edits():
    _input = request.form["input"]
    instruction = request.form["instruction"]
    return edit_service.edit(prompt=_input, instruction=instruction)


@app.route("/images/generations", methods=["POST"])
def generate_images():
    prompt = request.form["prompt"]
    return image_service.generate_image(prompt=prompt)


@app.route("/images/edit", methods=["POST"])
def edit_images():
    file_name = request.form["file_name"]
    mask = request.form["mask"]
    prompt = request.form["prompt"]
    return image_service.edit_image(file_name=file_name, mask=mask, prompt=prompt)


@app.route("/images/variations", methods=["POST"])
def vary_images():
    file_name = request.form["file_name"]
    response = image_service.vary_image(file_name=file_name)
    print("generate image response: %s" % json.dumps(response, ensure_ascii=False))
    return response


@app.route("/fine_tuned/list", methods=["GET"])
def fine_tuned_list():
    response = model_service.list()
    print("fine tuned list response: %s" % json.dumps(response, ensure_ascii=False))
    return response


@app.route("/fine_tuned/completions", methods=["POST"])
def fine_tuned_completions():
    fine_tuned_model = request.form["fine_tuned_model"]
    prompt = request.form["prompt"]
    response = fine_tuned_service.fine_tuned_completion(fine_tuned_model=fine_tuned_model, prompt=prompt)
    return response


@app.route("/audio/transcriptions", methods=["POST"])
def audio_transcriptions():
    audio_file_name = request.form["file_path"]
    response = audio_service.transcribe(audio_file_name=audio_file_name)
    return response


@app.route("/chat/completions", methods=["POST"])
def chat():
    prompt = request.form["prompt"]
    return chat_service.chat(prompt)


@app.route("/file/upload", methods=["POST"])
def file_upload():
    audio_file = request.files["audio"]
    prompt = file_service.file_upload(audio_file)
    return chat_service.voice_chat(prompt)


@app.route("/stream/chat", methods=["POST"])
def stream_chat():
    audio_file = request.files["audio"]
    prompt = file_service.file_upload(audio_file)
    print("prompt:%s" % prompt)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            stream=True,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个拉胯仔, 拉胯仔每句话都会加上\"我尼玛\"."},
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
    except Exception as e:
        print(e)
        return {}
    print(response)
    # _next = next(response['choices'][0])
    # print("_next:[%s]" % _next)
    # text = _next['text']

    text = next(response['choices'][0])['text']

    def generate():
        yield text

    return Response(generate(), mimetype='text/plain')
