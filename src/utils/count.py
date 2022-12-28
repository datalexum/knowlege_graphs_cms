import numpy as np
from rdflib import Graph
from src.query_templates.queries import predicate_query, bound_predicate_query
from src.cms.count_min_sketch import CMS


def initialize_count_object_object(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph):
    p1_result = predicate_query(graph, predicate1)
    for result in p1_result:
        cms_predicate1.count(result.obj)
        # cms_predicate1.printCMS()
        # print(f"{result.sub} {result.obj}")
    p2_result = predicate_query(graph, predicate2)
    for result in p2_result:
        cms_predicate2.count(result.obj)
        # cms_predicate2.printCMS()
        # print(f"{result.sub} {result.obj}")
    return p1_result, p2_result


def count_object_object(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph):
    # sub 1 und sub2 können aber müssen nicht gleich sein, lese sie als sub1 und sub2
    # Query1 ?s1 :predicate1 ?o -> p1_result
    # Query2 ?s2 :predicate2 ?o -> p2_result

    p1_result, p2_result = initialize_count_object_object(cms_predicate1, cms_predicate2, predicate1, predicate2, graph)

    objects = set([result.obj for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    for obj in objects:
        # (obj)
        c1 = cms_predicate1.get_min(obj)
        c2 = cms_predicate2.get_min(obj)
        # print(f"sketch p1: {obj}: {c1}")
        # print(f"sketch p2: {obj}: {c2}")
        count += c1 * c2
    return count


def noise_count_object_object(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph,
                              noise_operation):
    # sub 1 und sub2 können aber müssen nicht gleich sein, lese sie als sub1 und sub2
    # Query1 ?s1 :predicate1 ?o -> p1_result
    # Query2 ?s2 :predicate2 ?o -> p2_result

    p1_result, p2_result = initialize_count_object_object(cms_predicate1, cms_predicate2, predicate1, predicate2, graph)

    objects = set([result.obj for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    cms_predicate1.remove_noise(noise_operation)
    cms_predicate2.remove_noise(noise_operation)
    for obj in objects:
        # print(obj)
        c1 = cms_predicate1.get_min(obj)
        c2 = cms_predicate2.get_min(obj)
        # print(f"sketch p1: {obj}: {c1}")
        # print(f"sketch p2: {obj}: {c2}")
        count += c1 * c2
    return count


def initialize_count_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph):
    p1_result = predicate_query(graph, predicate1)
    for result in p1_result:
        cms_predicate1.count(result.obj)
        # cms_predicate1.printCMS()
        # print(f"{result.obj}")
    # print("all objects added")

    p2_result = predicate_query(graph, predicate2)
    for result in p2_result:
        cms_predicate2.count(result.sub)
        # cms_predicate2.printCMS()
        # print(f"{result.sub}")
    # print("all subjects added")

    return p1_result, p2_result


def count_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph):
    """
    cms_predicate1 for counting objects based on predicate1
    cms_predicate2 for counting subjects based on predicate2
    """
    p1_result, p2_result = initialize_count_object_subject(cms_predicate1, cms_predicate2, predicate1, predicate2,
                                                           graph)

    results = set([result.sub for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    for result in results:
        # print(result)
        c1 = cms_predicate1.get_min(result)
        c2 = cms_predicate2.get_min(result)
        # print(f"sketch p1: {result}: {c1}")
        # print(f"sketch p2: {result}: {c2}")
        count += c1 * c2
    return count


def noise_count_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph,
                               noise_operation):
    p1_result, p2_result = initialize_count_object_subject(cms_predicate1, cms_predicate2, predicate1, predicate2,
                                                           graph)

    results = set([result.sub for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    cms_predicate1.remove_noise(noise_operation)
    cms_predicate2.remove_noise(noise_operation)
    for result in results:
        # print(result)
        c1 = cms_predicate1.get_min(result)
        c2 = cms_predicate2.get_min(result)
        # print(f"sketch p1: {result}: {c1}")
        # print(f"sketch p2: {result}: {c2}")
        count += c1 * c2
    return count


def initialize_count_bound_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, object,
                                          graph: Graph):
    p1_result = predicate_query(graph, predicate1)
    for result in p1_result:
        cms_predicate1.count(result.obj)
        # cms_predicate1.printCMS()
        # print(f"{result.obj}")
    # print("all objects added")

    p2_result = bound_predicate_query(graph, predicate2, object)
    for result in p2_result:
        cms_predicate2.count(result.sub)
        # cms_predicate2.printCMS()
        # print(f"{result.sub}")
    # print("all subjects added")

    return p1_result, p2_result


def count_bound_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, object, graph: Graph):
    """
    cms_predicate1 for counting objects based on predicate1
    cms_predicate2 for counting subjects based on predicate2
    """
    p1_result, p2_result = initialize_count_bound_object_subject(cms_predicate1, cms_predicate2, predicate1, predicate2,
                                                                 object, graph)

    results = set([result.sub for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    for result in results:
        # print(result)
        c1 = cms_predicate1.get_min(result)
        c2 = cms_predicate2.get_min(result)
        # print(f"sketch p1: {result}: {c1}")
        # print(f"sketch p2: {result}: {c2}")
        count += c1 * c2
    return count


def noise_count_bound_object_subject(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, object,
                                     graph: Graph, noise_operation):
    # TODO: andere joins und deren noise funktionen debuggen, sollten aber funktionieren, kann aber sein das irgendwo eine variable nicht geändert wurde
    p1_result, p2_result = initialize_count_bound_object_subject(cms_predicate1, cms_predicate2, predicate1, predicate2,
                                                                 object, graph)

    results = set([result.sub for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    cms_predicate1.remove_noise(noise_operation)
    cms_predicate2.remove_noise(noise_operation)
    for result in results:
        # print(result)
        c1 = cms_predicate1.get_min(result)
        c2 = cms_predicate2.get_min(result)
        # print(f"sketch p1: {result}: {c1}")
        # print(f"sketch p2: {result}: {c2}")
        count += c1 * c2
    return count
