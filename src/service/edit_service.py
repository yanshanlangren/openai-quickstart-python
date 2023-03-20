import src.third.open_ai as openai
import json


def edit(prompt, instruction):
    response = openai.edit(prompt=prompt, instruction=instruction)
    print("edit response: %s" % json.dumps(response, ensure_ascii=False))
    return response
