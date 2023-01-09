from src.utils.hash import MMH3, HashFunctionGenerator
import numpy as np
import copy


class CMS:
    def __init__(self, width: int, depth: int = None, seeds: list = None, hash_functions: list = None,
                 hash_function_generator: HashFunctionGenerator = UniversalHashFunction(),
                 increment_decrement: bool = False):

        self.width = width
        self.depth = depth
        self.increment_decrement = increment_decrement

        if hash_functions is not None and hash_function_generator is not None:
            print("Info: Can only use either parsed hash_functions or generator, hash_functions are prioritized")
        if hash_functions is not None and len(hash_functions) > 0:
            self.hash_functions = hash_functions
            if self.increment_decrement:
                if len(self.hash_functions) % 2 != 0:
                    raise CMSInputError('To use increment and decrement you need to supply an even amount of hash '
                                        'functions!')
                self.depth = len(self.hash_functions) / 2
            else:
                self.depth = len(self.hash_functions)
        elif hash_function_generator is not None and (self.depth is not None or seeds is not None):
            self.hash_functions = []
            if seeds is None:
                if self.depth is not None:
                    anmount = self.depth if not self.increment_decrement else copy.copy(self.depth) * 2
                    for i in range(anmount):
                        self.hash_functions.append(hash_function_generator.get_function(self.width))
                else:
                    raise CMSInputError('If you generate hash functions in CMS you have to provide seeds or depth.')
            else:
                if len(seeds) % 2 != 0:
                    raise CMSInputError('To use increment and decrement you need to supply an even anmount of seeds!')
                for seed in seeds:
                    self.hash_functions.append(hash_function_generator.get_function(self.width, seed))
        else:
            raise CMSInputError("Either depth, hash_functions, or seeds has to be set!")

        self.cms = np.zeros([self.depth, self.width], dtype=int)
        self.cms_copy = np.zeros([self.depth, self.width], dtype=int)

    def count(self, obj: str):
        for row, function in enumerate(self.hash_functions):
            col = function(obj)
            if self.increment_decrement and row >= len(self.hash_functions) / 2:
                # int(), even though it's always full numbers because python type conversion using division
                self._sub(int(row - len(self.hash_functions) / 2), col)
            else:
                self._add(row, col)

    def get_min(self, obj: str) -> int:
        temp_values = []
        for row in range(self.depth):
            col = self.hash_functions[row](obj)
            temp_values.append(self.cms[row, col])
        return min(temp_values)

    def remove_noise(self, operation):
        self.cms = np.subtract(self.cms, operation(self.cms))
        np.where(self.cms < 0, self.cms, 0)

    def _add(self, row, col):
        self.cms[row, col] += 1

    def _sub(self, row, col):
        if self.cms[row, col] < 1:
            self.cms[row, col] = 0
        else:
            self.cms[row, col] += -1

    def printCMS(self):
        print(self.cms)


class CMSInputError(Exception):
    """Raised when the CMS gets supplied by a forbidden input."""
    pass
