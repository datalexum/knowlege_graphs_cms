import tqdm
from rdflib import Graph

from src.cms.count_min_sketch import CMS
from src.query_templates.queries import obj_predicate_query, sub_predicate_query, bound_sub_predicate_query


def check_length(prefixes, endings, length):
    if len(endings) != length or len(prefixes) != length:
        raise ValueError('Prefix or endings has the wrong length')


def count_object_object(cms_predicate1: CMS, cms_predicate2: CMS, prefixes, endings, graph: Graph,
                        noise_operation=None, p1_result=None, p2_result=None):
    # sub 1 und sub2 können aber müssen nicht gleich sein, lese sie als sub1 und sub2
    # Query1 ?s1 :predicate1 ?o -> p1_result
    # Query2 ?s2 :predicate2 ?o -> p2_result
    check_length(prefixes, endings, 2)
    if p1_result is None:
        p1_result = obj_predicate_query(graph, prefixes[0], endings[0])
        p1_result = [result.obj for result in p1_result]
    if p2_result is None:
        p2_result = obj_predicate_query(graph, prefixes[1], endings[1])
        p2_result = [result.obj for result in p2_result]

    for result in p1_result:
        cms_predicate1.count(result)
    for result in p2_result:
        cms_predicate2.count(result)

    count = 0
    if noise_operation is not None:
        cms_predicate1.remove_noise(noise_operation)
        cms_predicate2.remove_noise(noise_operation)
    for obj in combine_results(p1_result, p2_result):
        c1 = cms_predicate1.get_min(obj)
        c2 = cms_predicate2.get_min(obj)
        count += c1 * c2
    return count


def combine_results(p1_result, p2_result):
    objects = set(p2_result) & set(p1_result)
    return objects


def count_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, prefixes, endings, graph: Graph,
                         noise_operation=None, p1_result=None, p2_result=None):
    check_length(endings, prefixes, 2)
    if p1_result is None:
        tqdm.tqdm.write("p1 not supplied, calculating...")
        p1_result = obj_predicate_query(graph, prefixes[0], endings[0])
        p1_result = [result.obj for result in p1_result]
    if p2_result is None:
        tqdm.tqdm.write("p2 not supplied, calculating...")
        p2_result = sub_predicate_query(graph, prefixes[1], endings[1])
        p2_result = [result.sub for result in p2_result]
    for result in tqdm.tqdm(p1_result, leave=False, desc="P1 Counting: "):
        cms_predicate1.count(result)
    for result in tqdm.tqdm(p2_result, leave=False, desc="P2 Counting: "):
        cms_predicate2.count(result)
    tqdm.tqdm.write('Counting finished.')
    #Till here seems correct

    if noise_operation is not None:
        cms_predicate1.remove_noise(noise_operation)
        cms_predicate2.remove_noise(noise_operation)
    tqdm.tqdm.write('Noise added')

    #Till here seems correct
    count = 0
    for result in combine_results(p2_result, p1_result):
        c1 = cms_predicate1.get_min(result)
        c2 = cms_predicate2.get_min(result)
        count += c1 * c2

    return count


def count_bound_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, prefixes, endings,
                               graph: Graph, noise_operation=None, p1_result=None, p2_result=None):
    check_length(endings, prefixes, 3)

    if p1_result is None:
        p1_result = obj_predicate_query(graph, prefixes[0], endings[0])
        p1_result = [result.obj for result in p1_result]
    if p2_result is None:
        p2_result = bound_sub_predicate_query(graph, prefixes=[prefixes[1], prefixes[2]],
                                              endings=[endings[1], endings[2]])
        p2_result = [result.sub for result in p2_result]

    for result in p1_result:
        cms_predicate1.count(result)
    for result in p2_result:
        cms_predicate2.count(result)

    count = 0
    if noise_operation is not None:
        cms_predicate1.remove_noise(noise_operation)
        cms_predicate2.remove_noise(noise_operation)
    for result in combine_results(p2_result, p1_result):
        c1 = cms_predicate1.get_min(result)
        c2 = cms_predicate2.get_min(result)
        count += c1 * c2
    return count
