from src.third import open_ai as openai
from src.third.tencent_tts import tts
import json

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
    resp_content = response.get("choices")[0].get("message").get("content")

    if len(resp_content) < 150:
        print("whole content")
        audio = tts(resp_content)
    else:
        print("first 150:[%s]" % resp_content[:150])
        audio = tts(resp_content[:150])

    if not response:
        return {}
    dialog.append({
        "role": "assistant",
        "content": response.get("choices")[0].get("message").get("content")
    })
    return {"dialog": dialog, "audio": audio}
