import numpy as np


class CMS:
    def __init__(self, width: int, hash_functions: list):
        self.width = width
        self.hash_functions = hash_functions
        self.cms = np.zeros((len(self.hash_functions), self.width))

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

    def _add(self, row, col):
        self.cms[row, col] += 1
