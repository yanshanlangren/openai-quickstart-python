from src.third import open_ai as openai
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
    return dialog
