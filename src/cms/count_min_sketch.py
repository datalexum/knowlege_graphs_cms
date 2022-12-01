import numpy as np
from src.utils.hash import MMH3, HashFunctionGenerator
import numpy as np
import mmh3
import sys


class CMS:
    def __init__(self, width: int, depth: int = None, seeds: list = None, hash_functions: list = None,
                 hash_function_generator: HashFunctionGenerator = MMH3()):
        self.width = width
        self.depth = depth
        if hash_functions is not None and len(hash_functions) > 0:
            self.hash_functions = hash_functions
            self.depth = len(self.hash_functions)
        elif hash_function_generator is not None and (self.depth is not None or seeds is not None):
            self.hash_functions = []
            if seeds is None:
                if self.depth is not None:
                    for i in range(self.depth):
                        self.hash_functions.append(hash_function_generator.get_function(self.width))
                else:
                    raise Exception('If you generate hash functions in CMS you have to provide seeds or depth.')
            else:
                for seed in seeds:
                    self.hash_functions.append(hash_function_generator.get_function(self.width, seed))
        else:
            raise Exception("Either depth or hash_functions has to be set.")
        self.depth = len(self.hash_functions)
        self.cms = np.zeros([self.depth, self.width], dtype=int)
        self.cms_copy = np.zeros([self.depth, self.width], dtype=int)


    def count(self, obj: str):
        for row, function in enumerate(self.hash_functions):
            col = function(obj)
            self._add(row, col)

    def get_min(self, obj: str) -> int:
        temp_values = []
        for row, function in enumerate(self.hash_functions):
            col = function(obj)
            temp_values.append(self.cms[row, col])
        return min(temp_values)

    def remove_noise(self):
        self.cms_copy = np.copy(self.cms)
        for row in self.cms_copy:
            print("Before",row)
            row = np.subtract(row, np.amin(row))
            print("After",row)
    def noise_removal_get_min(self, obj: str) -> int:
        temp_values = []
        for row, function in enumerate(self.hash_functions):
            col = function(obj)
            temp_values.append(self.cms_copy[row, col])
        return min(temp_values)

    def _add(self, row, col):
        self.cms[row, col] += 1

    def printCMS(self):
        print(self.cms)