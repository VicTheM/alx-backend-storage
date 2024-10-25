#!/usr/bin/env python3
"""
Defines a Cache class
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator Function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper Function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator Function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper Function"""
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        output = method(self, *args, **kwargs)

        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, output)

        return output
    return wrapper


class Cache:
    """Represents a cache"""
    def __init__(self):
        """Initialize the class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates a random key

        Keyword arguments:
        data -- Input data to store in Redis
        Return: Key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float, None]:
        """Gets and convert the data back to the desired format
        """
        data = self._redis.get(key)
        if fn and data:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Gets and convert the data a string data"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Gets and convert the data an int data"""
        return self.get(key, fn=int)


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function"""
    if method is None or not hasattr(method, '__self__'):
        return
    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return

    key = method.__qualname__
    input_key = "{}:inputs".format(key)
    output_key = "{}:outputs".format(key)
    count = 0

    if redis_store.exists(key) != 0:
        count = int(redis_store.get(key))
    inputs = redis_store.lrange(input_key, 0, -1)
    outputs = redis_store.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(key, count))
    for ins, outs in list(zip(inputs, outputs)):
        print("{}(*{}) -> {}".format(
            key,
            ins.decode("utf-8"),
            outs.decode("utf-8")
            ))