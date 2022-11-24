import random
from sys import maxsize
from _csv import reader
import mmh3

from cms.count_min_sketch import CMS
from utils.hash import BasicHashFunctionGenerator, MultiplicationHashFunctionGenerator


if __name__ == '__main__':
    cms = CMS(2048, 10)

    names = []
    with open('../data/names.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for idx, row in enumerate(csv_reader):
            names = names + [row[1]]#* random.randint(0, 5)
            #if idx == 10000:
            #    break
    print(len(list(set(names))))

    #for name in names:
    #    cms.count(name)

    #for name in random.choices(list(set(names)), k=15):
    #    print(f"{name} is {names.count(name)} times in the list and CMS says at least {cms.get_min(name)}")
