import functools
from abc import ABC, abstractmethod


class HashFunctionGenerator(ABC):

    @abstractmethod
    def get_function(self, max_value=20, add_param=0):
        pass

    @staticmethod
    @abstractmethod
    def _hash_function(max_value: int, add_param: int, word: str):
        pass


class BasicHashFunctionGenerator(HashFunctionGenerator, ABC):
    def get_function(self, max_value=20, add_param=0):
        return functools.partial(self._hash_function, max_value, add_param)

    @staticmethod
    def _hash_function(max_value: int, add_param: int, word: str):
        sum_ordinals = add_param
        for letter in word:
            sum_ordinals += ord(letter)
        return sum_ordinals % max_value
