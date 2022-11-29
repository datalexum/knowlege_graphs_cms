import sys

import numpy as np
import mmh3


class CMS:
    def __init__(self, width: int, depth: int, seeds=None):
        self.width = width
        self.depth = depth
        self.cms = np.zeros([self.depth, self.width], dtype=int)
        self.seeds = seeds
        if self.seeds is None:
            self.seeds = np.random.randint(sys.maxsize, size=self.depth)
        elif depth != len(seeds):
            print("Error, Anzahl der übergebnen Hashfunktionen != depth des CMS")

    def count(self, obj: str):
        for row, seed in enumerate(self.seeds):
            col = mmh3.hash(obj, seed) % self.width
            self._add(row, col)

    def get_min(self, obj: str) -> int:
        temp_values = []
        for row, seed in enumerate(self.seeds):
            col = mmh3.hash(obj, seed) % self.width
            temp_values.append(self.cms[row, col])
        return min(temp_values)

    def _add(self, row, col):
        self.cms[row, col] += 1

    def printCMS(self):
        print(self.cms)
