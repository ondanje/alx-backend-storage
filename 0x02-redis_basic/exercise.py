#!/usr/bin/env python3
"""
importing redis, typing and uuid modules
"""
from types import UnionType
import redis
import typing
from typing import Union, Optional, Callable
import uuid
import sys


class Cache:
    def __init__(self) -> None:
        """
        __init__ method, store an instance of the Redis
        client as a private variable
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: typing.Union[str, bytes, int, float]) -> str:
        """
        method that takes a data argument and returns a string
        the data can be a str, bytes, int or float
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionType:
        """
        get method that take a key string argument and
        an optional Callable argument named fn
        """
        result = self._redis.get(key)
        if result is None:
            return None
        if fn is not None:
            result = fn(result)
        return result

    def get_str(self, key: str) -> typing.Union[str, None]:
        """
        get_str and get_int that will automatically parametrize
        Cache.get with the correct conversion function.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> typing.Union[int, None]:
        """
        get_str and get_int that will automatically parametrize
        Cache.get with the correct conversion function.
        """
        return self.get(key, int)
