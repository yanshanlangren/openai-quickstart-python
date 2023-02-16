import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/ask", methods=["POST"])
def ask():
    try:
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=animal,
            temperature=0.6,
        )
        print("get response: %s" % response)
        # return redirect(url_for("index", result=response.choices[0].text))
        return response.choices[0].text
    except Exception as e:
        print(e)
    return request.args.get("result")

# def generate_prompt(animal):
#     return """Suggest three names for an animal that is a superhero.
#
# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(
#         animal.capitalize()
#     )
