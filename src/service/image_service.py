import src.third.open_ai as openai
import json


def generate_image(prompt):
    response = openai.generate_image(prompt=prompt)
    print("generate image response: %s" % json.dumps(response, ensure_ascii=False))
    return response


def edit_image(file_name, mask, prompt):
    response = openai.edit_image(file_name=file_name, mask=mask, prompt=prompt)
    print("edit image response: %s" % json.dumps(response, ensure_ascii=False))
    return response


def vary_image(file_name):
    response = openai.vary_image(file_name=file_name)
    print("vary image response: %s" % json.dumps(response, ensure_ascii=False))
    return response
