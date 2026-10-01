"""Tests for function-call-in-default-argument."""
# pylint: disable=missing-docstring,unused-argument,dangerous-default-value,line-too-long
# pylint: disable=too-few-public-methods,unnecessary-lambda-assignment,unnecessary-lambda
import asyncio
import time
from uuid import uuid4


def default_key() -> str:
    return f"{uuid4()}.json"


def bad_call(key=default_key()):  # [function-call-in-default-argument]
    return key


def bad_kwonly(*, key=default_key()):  # [function-call-in-default-argument]
    return key


def bad_attribute_call(now=time.time()):  # [function-call-in-default-argument]
    return now


def bad_nested(values=[default_key()]):  # [function-call-in-default-argument]
    return values


def bad_expression(value=1 + len("abc")):  # [function-call-in-default-argument]
    return value


def bad_two(a=default_key(), b=default_key()):  # [function-call-in-default-argument, function-call-in-default-argument]
    return a, b


async def bad_async(key=default_key()):  # [function-call-in-default-argument]
    await asyncio.sleep(0)
    return key


class Klass:
    def bad_method(self, key=default_key()):  # [function-call-in-default-argument]
        return key


bad_lambda = lambda key=default_key(): key  # [function-call-in-default-argument]


def good_none(key=None):
    if key is None:
        key = default_key()
    return key


def good_constants(a=1, b="x", c=(1, 2), d=None, e=-1):
    return a, b, c, d, e


def good_immutable_calls(a=tuple(), b=frozenset(), c=int("1"), d=str(), e=object()):
    return a, b, c, d, e


def good_lambda_default(callback=lambda: default_key()):
    # the call only runs when the lambda is called
    return callback


def good_reference(factory=default_key):
    return factory
