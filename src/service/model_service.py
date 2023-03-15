import src.third.open_ai as openai


def get(model_id):
    return openai.get_model(model_id)


def list():
    return openai.list_model()
