import tqdm
from rdflib import Graph

import time

from src.cms.count_min_sketch import CMS
from src.query_templates.queries import obj_predicate_query, sub_predicate_query, bound_sub_predicate_query


def check_length(prefixes, endings, length):
    if len(endings) != length or len(prefixes) != length:
        raise ValueError('Prefix or endings has the wrong length')


def combine_results(p1_result, p2_result):
    objects = set(p2_result) & set(p1_result)
    return objects


def count_if_not_precalculated(cms_precalculated, cms_predicate1, cms_predicate2, p1_result, p2_result):
    if not cms_precalculated:
        for result in tqdm.tqdm(p1_result, leave=False, desc="P1 Counting: "):
            cms_predicate1.count(result)
        for result in tqdm.tqdm(p2_result, leave=False, desc="P2 Counting: "):
            cms_predicate2.count(result)
        tqdm.tqdm.write('Counting finished.')


def apply_noise_opperation_if_supplied(cms_predicate1, cms_predicate2, noise_operation):
    if noise_operation is not None:
        cms_predicate1.remove_noise(noise_operation)
        cms_predicate2.remove_noise(noise_operation)
        tqdm.tqdm.write('Noise removed')


def calculate_count(cms_predicate1, cms_predicate2, p1_result, p2_result):
    count = 0
    start = time.time_ns()
    for obj in combine_results(p1_result, p2_result):
        c1 = cms_predicate1.get_min(obj)
        c2 = cms_predicate2.get_min(obj)
        count += c1 * c2
    counttime = time.time_ns() - start
    return count, counttime


def count_object_object(cms_predicate1: CMS, cms_predicate2: CMS, prefixes, endings, graph: Graph,
                        cms_precalculated: bool, noise_operation=None, p1_result=None, p2_result=None):
    check_length(prefixes, endings, 2)
    if p1_result is None:
        tqdm.tqdm.write("p1 not supplied, calculating...")
        p1_result = obj_predicate_query(graph, prefixes[0], endings[0])
        p1_result = [result.result for result in p1_result]
    if p2_result is None:
        tqdm.tqdm.write("p2 not supplied, calculating...")
        p2_result = obj_predicate_query(graph, prefixes[1], endings[1])
        p2_result = [result.result for result in p2_result]

    count_if_not_precalculated(cms_precalculated, cms_predicate1, cms_predicate2, p1_result, p2_result)
    apply_noise_opperation_if_supplied(cms_predicate1, cms_predicate2, noise_operation)

    return calculate_count(cms_predicate1, cms_predicate2, p1_result, p2_result)


def count_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, prefixes, endings, graph: Graph,
                         cms_precalculated: bool, noise_operation=None, p1_result=None, p2_result=None):
    check_length(endings, prefixes, 2)
    if p1_result is None:
        tqdm.tqdm.write("p1 not supplied, calculating...")
        p1_result = obj_predicate_query(graph, prefixes[0], endings[0])
        p1_result = [result.result for result in p1_result]
    if p2_result is None:
        tqdm.tqdm.write("p2 not supplied, calculating...")
        p2_result = sub_predicate_query(graph, prefixes[1], endings[1])
        p2_result = [result.result for result in p2_result]

    count_if_not_precalculated(cms_precalculated, cms_predicate1, cms_predicate2, p1_result, p2_result)
    apply_noise_opperation_if_supplied(cms_predicate1, cms_predicate2, noise_operation)

    return calculate_count(cms_predicate1, cms_predicate2, p1_result, p2_result)


def count_bound_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, prefixes, endings,
                               graph: Graph, cms_precalculated: bool, noise_operation=None, p1_result=None,
                               p2_result=None):
    check_length(endings, prefixes, 3)

    if p1_result is None:
        p1_result = obj_predicate_query(graph, prefixes[0], endings[0])
        p1_result = [result.result for result in p1_result]
    if p2_result is None:
        p2_result = bound_sub_predicate_query(graph, prefixes=[prefixes[1], prefixes[2]],
                                              endings=[endings[1], endings[2]])
        p2_result = [result.result for result in p2_result]

    count_if_not_precalculated(cms_precalculated, cms_predicate1, cms_predicate2, p1_result, p2_result)
    apply_noise_opperation_if_supplied(cms_predicate1, cms_predicate2, noise_operation)

    return calculate_count(cms_predicate1, cms_predicate2, p1_result, p2_result)
