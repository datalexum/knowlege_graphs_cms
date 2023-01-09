import functools
import random
from abc import ABC, abstractmethod
from typing import List

from Crypto.Util import number


class HashFunctionGenerator(ABC):

    @abstractmethod
    def get_function(self, max_value=20, seed=0):
        pass


class BasicHashFunction(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, seed=None):
        if seed is None:
            # For simplicitie’s sake capped at 10k
            seed = random.randrange(0, 10000)
        return functools.partial(self._hash_function, max_value, seed)

    @staticmethod
    def _hash_function(max_value: int, seed: int, word: str):
        sum_ordinals = seed
        for letter in word:
            sum_ordinals += ord(letter)
        return sum_ordinals % max_value


class MultiplicationHashFunctionGenerator(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, seed=None):
        if seed is None:
            seed = random.randrange(0, 10000)
        return functools.partial(self._hash_function, max_value, seed)

    @staticmethod
    def _hash_function(max_value: int, seed: int, word: str):
        sum_ordinals = 0
        for letter in word:
            sum_ordinals += ord(letter) * seed
        return sum_ordinals % max_value


class IndependentHashFunction(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, seed=None):
        if seed is None:
            seed = number.getPrime(16)
        else:
            if not number.isPrime(seed):
                raise ValueError("seed must be prime")

        a = random.randrange(0, seed - 1)
        b = random.randrange(0, seed - 1)
        return functools.partial(self._hash_function, max_value, seed, a, b)

    @staticmethod
    def _hash_function(max_value: int, P: int, a: int, b: int, word: str):
        x = sum([ord(letter) for letter in word])
        return ((a * x + b) % P) % max_value


class UniversalHashFunction(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, seed=None):
        if seed is None:
            seed = number.getPrime(16)
        else:
            if not number.isPrime(seed):
                raise ValueError("m must be prime")

        a = [random.randrange(0, seed) for _ in range(seed)]
        b = random.randrange(0, seed)
        return functools.partial(self._hash_function, max_value, seed, a, b)

    @staticmethod
    def _hash_function(max_value: int, m: int, a: List[int], b: int, word: str):
        return ((sum([a[i % len(a)] * ord(word[i]) for i in range(len(word))]) + b) % m) % max_value
