import src.third.open_ai as openai
import json


def file_upload(audio_file):
    audio_file.save("./record.webm")
    trans = open("./record.webm", "rb")
    resp = openai.audio_transcribe(trans)
    print("audio transcriptions response: %s" % json.dumps(resp, ensure_ascii=False))
    if not resp:
        return None
    return resp.get("text")
