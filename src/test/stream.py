import requests

response = requests.get('https://www.example.com', stream=True)
for chunk in response.iter_content(chunk_size=1024):
    if chunk:
        print(chunk)

from flask import Flask, Response
import requests

app = Flask(__name__)


@app.route('/')
def stream_response():
    response = requests.get('https://www.example.com', stream=True)
    return Response(response.iter_content(chunk_size=1024), mimetype='text/plain')


if __name__ == '__main__':
    app.run()
