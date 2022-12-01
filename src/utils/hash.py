import functools
import random
from abc import ABC, abstractmethod

import mmh3
from Crypto.Util import number


class HashFunctionGenerator(ABC):

    @abstractmethod
    def get_function(self, max_value=20, param=0):
        pass


class BasicHashFunctionGenerator(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, param=None):
        if param is None:
            param = random.randrange(0, 10000)
        return functools.partial(self._hash_function, max_value, param)

    @staticmethod
    def _hash_function(max_value: int, param: int, word: str):
        sum_ordinals = param
        for letter in word:
            sum_ordinals += ord(letter)
        return sum_ordinals % max_value


class MultiplicationHashFunctionGenerator(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, param=None):
        if param is None:
            param = random.randrange(0, 10000)
        return functools.partial(self._hash_function, max_value, param)

    @staticmethod
    def _hash_function(max_value: int, param: int, word: str):
        sum_ordinals = 0
        for letter in word:
            sum_ordinals += ord(letter) * param
        return sum_ordinals % max_value


class IndipendentHashFunction(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, param=None):
        if param is None:
            param = number.getPrime(16)
        else:
            if not number.isPrime(param):
                raise Exception("param must be prime")

        a = random.randrange(0, param - 1)
        b = random.randrange(0, param - 1)
        return functools.partial(self._hash_function, max_value, param, a, b)

    @staticmethod
    def _hash_function(max_value: int, P: int, a: int, b: int, word: str):
        x = sum([ord(letter) for letter in word])
        return ((a * x + b) % P) % max_value


class MMH3(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, param=None):
        if param is None:
            param = random.randrange(0, 10000)
        return functools.partial(self._hash_function, max_value, param)

    @staticmethod
    def _hash_function(max_value: int, param: int, word: str):
        return mmh3.hash(word, param) % max_value