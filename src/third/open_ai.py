import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_completion(dialog):
    try:
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model="gpt-4.0",
            messages=dialog
        )
    except Exception as e:
        print(e)
        return None
