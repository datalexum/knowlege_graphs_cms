import functools
from abc import ABC, abstractmethod


class HashFunctionGenerator(ABC):

    @abstractmethod
    def get_function(self, max_value=20, param=0):
        pass

    @staticmethod
    @abstractmethod
    def _hash_function(max_value: int, param: int, word: str):
        pass


class BasicHashFunctionGenerator(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, param=0):
        return functools.partial(self._hash_function, max_value, param)

    @staticmethod
    def _hash_function(max_value: int, param: int, word: str):
        sum_ordinals = param
        for letter in word:
            sum_ordinals += ord(letter)
        return sum_ordinals % max_value


class MultiplicationHashFunctionGenerator(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, param=1):
        return functools.partial(self._hash_function, max_value, param)

    @staticmethod
    def _hash_function(max_value: int, param: int, word: str):
        sum_ordinals = 0
        for letter in word:
            sum_ordinals += ord(letter) * param
        return sum_ordinals % max_value
