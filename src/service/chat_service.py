from src.third import open_ai as openai
from src.third.tencent_tts import tts
import json
import re

dialog = []


def chat(prompt):
    global dialog
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
    response = openai.chat_completion(dialog=dialog)
    print("chat completion response: %s" % json.dumps(response, ensure_ascii=False))
    if not response:
        return {}
    dialog.append({
        "role": "assistant",
        "content": response.get("choices")[0].get("message").get("content")
    })
    return {"dialog": dialog}


def voice_chat(prompt):
    global dialog
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
    response = openai.chat_completion(dialog=dialog)
    if not response:
        return {}
    dialog.append({
        "role": "assistant",
        "content": response.get("choices")[0].get("message").get("content")
    })
    resp_content = response.get("choices")[0].get("message").get("content")
    if len(resp_content) < 150:
        print("whole content:[%s]" % resp_content)
        audio = tts(resp_content)
    else:
        print("first 150:[%s]" % resp_content[:150])
        audio = tts(resp_content[:150])
    return {"dialog": dialog, "audio": audio}


def stream_voice_chat(prompt):
    global dialog
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
    response = openai.chat_completion(dialog=dialog, stream=True)

    def generate():
        buffer = ""
        for data in response:
            text = data['choices'][0]
            if text and text.get("delta") and text.get("delta").get("content"):
                ret_str = text.get("delta").get("content")
                print("ret string: [%s]" % json.dumps(text.get("delta"), ensure_ascii=False))
                if re.search(r"\W", ret_str) is not None:
                    print("buffer:[%s]" % buffer)
                    audio = tts(buffer)
                    yield audio
                    buffer = ""
                else:
                    buffer += ret_str

    # dialog.append({
    #     "role": "assistant",
    #     "content": response.get("choices")[0].get("message").get("content")
    # })
    # resp_content = response.get("choices")[0].get("message").get("content")
    return {"dialog": dialog, "audio": generate()}
