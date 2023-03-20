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


def audio_transcribe(trans):
    try:
        return openai.Audio.transcribe("whisper-1", trans)
    except Exception as e:
        print(e)
        return None


def list_model():
    try:
        return openai.Model.list()
    except Exception as e:
        print(e)
        return None


def get_model(model_id):
    try:
        return openai.Model.get(model_id)
    except Exception as e:
        print(e)
        return None


def completions(prompt):
    try:
        return openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            # suffix="",
            max_tokens=2048,
            temperature=0.6,
            # top_p=1,
            # n=1,
            # stream=False,
            # logprobs=None,
            # echo=False,
            # stop=None,
            # presence_penalty=0,
            # frequency_penalty=0,
            # best_of=0,
            # logit_bias=0,
            # user="",
        )
    except Exception as e:
        print(e)
    return None


def edit(prompt, instruction):
    try:
        return openai.Edit.create(
            model="text-davinci-003",
            input=prompt,
            instruction=instruction,
        )
    except Exception as e:
        print(e)
        return None


def generate_image(prompt):
    try:
        return openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
    except Exception as e:
        print(e)
        return None


def edit_image(file_name, mask, prompt):
    try:
        return openai.Image.create_edit(
            image=open(file_name, "rb"),
            mask=open(mask, "rb"),
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
    except Exception as e:
        print(e)
        return None


def vary_image(file_name):
    try:
        return openai.Image.create_variation(
            image=open(file_name, "rb"),
            n=1,
            size="1024x1024",
        )
    except Exception as e:
        print(e)
        return None


def fine_tuned_completion(fine_tuned_model, prompt):
    try:
        return openai.Completion.create(
            model=fine_tuned_model,
            prompt=prompt
        )
    except Exception as e:
        print(e)
        return None


def transcribe_voice(audio_file_name):
    try:
        audio_file = open(audio_file_name, "rb")
        return openai.Audio.transcribe("whisper-1", audio_file)
    except Exception as e:
        print(e)
        return None
