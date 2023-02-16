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
            temperature=0.6,
            max=2048
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
