import src.third.open_ai as openai
import json


def fine_tuned_completion(fine_tuned_model, prompt):
    response = openai.fine_tuned_completion(fine_tuned_model=fine_tuned_model, prompt=prompt)
    print("fine tuned model response: %s" % json.dumps(response, ensure_ascii=False))
    return response
