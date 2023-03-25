import openai

openai.api_key = "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"


def func():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        stream=True,
        max_tokens=5,
        n=1,
        stop=None,
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": "你是一个拉胯仔, 拉胯仔每句话都会加上\"我尼玛\"."},
            {
                "role": "user",
                "content": "你好",
            }
        ]
    )
    # response = requests.get('https://www.example.com', stream=True)
    print(response)
    # text = response['choices'][0]['message']

    # def generate():
    #     yield text
    #
    # generate()
    text = response['choices'][0]['message']
    yield text
    print(text)


def stream_response():
    response = openai.Completion.create(
        engine="davinci",
        prompt="Hello, world!",
        max_tokens=5,
        n=1,
        stop=None,
        temperature=0.5,
    )
    text = response['choices'][0]['text']

    def generate():
        yield text

    return generate()


# resp = stream_response()
# while(True):
#     print(resp.)

# def generate():
#     yield text
#
#
# print(generate())

# from flask import Flask, Response
# import requests
#
# app = Flask(__name__)


# @app.route('/')
# def stream_response():
#     response = requests.get('https://www.example.com', stream=True)
#     return Response(response.iter_content(chunk_size=1024), mimetype='text/plain')
#
#
# if __name__ == '__main__':
#     app.run()


# from flask import Flask, Response
# import openai
#
# openai.api_key = "YOUR_API_KEY"
#
# app = Flask(__name__)


# @app.route('/')
# def stream_response():
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt="Hello, world!",
#         max_tokens=5,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )
#     text = response['choices'][0]['text']
#
#     def generate():
#         yield text
#
#     return Response(generate(), mimetype='text/plain')


# if __name__ == '__main__':
#     app.run()
