import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/completions", methods=["POST"])
def completions():
    try:
        animal = request.form["animal"]
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
        print("completions response: %s" % response)
        # return redirect(url_for("index", result=response.choices[0].text))
        # return response.choices[0].text
        return response
    except Exception as e:
        print(e)
    # return request.args.get("result")
    return request


@app.route("/models", methods=["GET"])
def models():
    try:
        response = openai.Model.list()
        print("models response: %s" % response)
    except Exception as e:
        print(e)
    return request


@app.route("/models/<model_id>", methods=["GET"])
def model(model_id):
    try:
        response = openai.Model.get(model_id)
        print("model response: %s" % response)
    except Exception as e:
        print(e)
    return request


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
        print("edit response: %s" % response)
    except Exception as e:
        print(e)
    return request


@app.route("/images/generations", methods=["POST"])
def generate_images():
    try:
        prompt = request.form["prompt"]
        response = openai.Edit.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        print("generate image response: %s" % response)
    except Exception as e:
        print(e)
    return request
