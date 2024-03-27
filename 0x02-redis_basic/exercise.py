#!/usr/bin/env python3
"""
importing redis, typing and uuid modules
"""
from functools import wraps
import sys
import redis
from typing import Union, Optional, Callable
import uuid


Union_Types = Union[str, bytes, int, float]


def replay(method: Callable) -> None:
    """
    display the history of calls of afunction
    """
    key = method.__qualname__
    data = redis.Redis()
    hist = data.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, hist))
    inputs = data.lrange(key + ":inputs", 0, -1)
    outputs = data.lrange(key + ":outputs", 0, -1)
    for k, v in zip(inputs, outputs):
        print(f"{key}(*{k.decode('utf-8')}) -> {v.decode('utf-8')}")


def count_calls(method: Callable) -> Callable:
    """
    Increments a counter in Redis every time
    the function is called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Records the history of input arguments and output of
    the method
    """
    key = method.__qualname__
    i = "{}{}".format(key, ":inputs")
    o = "{}{}".format(key, ":outputs")

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res
    return wrapper


class Cache:
    def __init__(self):
        """
        __init__ method, store an instance of the Redis
        client as a private variable
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union_Types) -> str:
        """
        method that takes a data argument and returns a string
        the data can be a str, bytes, int or float
        """
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union_Types:
        """
        get method that take a key string argument and
        an optional Callable argument named fn
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self, key: str) -> int:
        """
        get_str and get_int that will automatically parametrize
        Cache.get with the correct conversion function.
        """
        return int.from_bytes(self.get(key), sys.byteorder)

    def get_str(self, key: str) -> str:
        """
        get_str and get_int that will automatically parametrize
        Cache.get with the correct conversion function.
        """
        return self.get(key).decode("utf-8")
