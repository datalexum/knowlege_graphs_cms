import random
from _csv import reader

from cms.count_min_sketch import CMS
from utils.hash import BasicHashFunctionGenerator


if __name__ == '__main__':
    b = BasicHashFunctionGenerator()
    hash_function_list = [b.get_function(max_value=100), b.get_function(max_value=100, add_param=11)]

    cms = CMS(100, hash_function_list)

    names = []
    with open('../data/names.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for idx, row in enumerate(csv_reader):
            names = names + [row[1]] * random.randint(0, 20)
            if idx == 500:
                break

    for name in names:
        cms.count(name)

    for name in random.choices(list(set(names)), k=15):
        print(f"{name} is {names.count(name)} times in the list and CMS says at least {cms.get_min(name)}")
