from rdflib import Graph

from src.cms.count_min_sketch import CMS
from src.query_templates.queries import obj_predicate_query, sub_predicate_query, bound_sub_predicate_query


def check_length(prefixes,endings, length):
    if len(endings) != length or len(prefixes) != length:
        raise ValueError('Prefix or endings has the wrong length')


def count_object_object(cms_predicate1: CMS, cms_predicate2: CMS, prefixes, endings,  graph: Graph,
                        noise_operation=None):
    # sub 1 und sub2 können aber müssen nicht gleich sein, lese sie als sub1 und sub2
    # Query1 ?s1 :predicate1 ?o -> p1_result
    # Query2 ?s2 :predicate2 ?o -> p2_result
    check_length(prefixes,endings, 2)

    p1_result = obj_predicate_query(graph, prefixes[0], endings[0])
    for result in p1_result:
        cms_predicate1.count(result.obj)
    p2_result = obj_predicate_query(graph, prefixes[1], endings[1])
    for result in p2_result:
        cms_predicate2.count(result.obj)

    objects = set([result.obj for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    if noise_operation is not None:
        cms_predicate1.remove_noise(noise_operation)
        cms_predicate2.remove_noise(noise_operation)
    for obj in objects:
        c1 = cms_predicate1.get_min(obj)
        c2 = cms_predicate2.get_min(obj)
        count += c1 * c2
    return count


def count_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, prefixes, endings,  graph: Graph,
                         noise_operation=None):
    check_length(endings, prefixes, 2)

    p1_result = obj_predicate_query(graph, prefixes[0], endings[0])
    for result in p1_result:
        cms_predicate1.count(result.obj)

    p2_result = sub_predicate_query(graph, prefixes[1], endings[1])
    for result in p2_result:
        cms_predicate2.count(result.sub)

    results = set([result.sub for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    if noise_operation is not None:
        cms_predicate1.remove_noise(noise_operation)
        cms_predicate2.remove_noise(noise_operation)
    for result in results:
        c1 = cms_predicate1.get_min(result)
        c2 = cms_predicate2.get_min(result)
        count += c1 * c2
    return count



def count_bound_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, prefixes, endings,
                               graph: Graph, noise_operation=None):
    check_length(endings, prefixes, 3)

    p1_result = obj_predicate_query(graph, prefixes[0], endings[0])
    for result in p1_result:
        cms_predicate1.count(result.obj)
    p2_result = bound_sub_predicate_query(graph, prefixes=[prefixes[1], prefixes[2]], endings=[endings[1], endings[2]])
    for result in p2_result:
        cms_predicate2.count(result.sub)

    results = set([result.sub for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    if noise_operation is not None:
        cms_predicate1.remove_noise(noise_operation)
        cms_predicate2.remove_noise(noise_operation)
    for result in results:
        c1 = cms_predicate1.get_min(result)
        c2 = cms_predicate2.get_min(result)
        count += c1 * c2
    return count
