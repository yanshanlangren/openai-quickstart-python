import src.third.open_ai as openai
import json


def transcribe(audio_file_name):
    response = openai.transcribe_voice(audio_file_name=audio_file_name)
    print("fine tuned model response: %s" % json.dumps(response, ensure_ascii=False))
    return response
