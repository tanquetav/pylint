from uuid import uuid4


def store(data, key=f"{uuid4()}.json"):  # [function-call-in-default-argument]
    return key, data
