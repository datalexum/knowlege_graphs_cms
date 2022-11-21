from abc import ABC, abstractmethod


class HashFunctionGenerator(ABC):

    @abstractmethod
    def get_function(self, min_value=0, max_value=20):
        pass
