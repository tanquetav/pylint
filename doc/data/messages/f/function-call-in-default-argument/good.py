from uuid import uuid4


def store(data, key=None):
    if key is None:
        key = f"{uuid4()}.json"
    return key, data
