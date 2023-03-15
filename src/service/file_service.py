import src.third.open_ai as openai


def file_upload(audio_file):
    audio_file.save("./record.webm")
    trans = open("./record.webm", "rb")
    resp = openai.audio_transcribe(trans)
    if not resp:
        return None
    return resp.get("text")
