from rdflib import Graph
from src.query_templates.queries import predicate_query
from src.cms.count_min_sketch import CMS


def count_object_object(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph):
    # sub 1 und sub2 können aber müssen nicht gleich sein, lese sie als sub1 und sub2
    # Query1 ?s1 :predicate1 ?o -> p1_result
    # Query2 ?s2 :predicate2 ?o -> p2_result


    # TODO Put into seperate method to prevent repetetive code, can then be reused for other count functions
    p1_result = predicate_query(graph,predicate1)
    for result in p1_result:
        cms_predicate1.count(result.obj)
        cms_predicate1.printCMS()
        print(f"{result.sub} {result.obj}")

    p2_result = predicate_query(graph,predicate2)
    for result in p2_result:
        cms_predicate2.count(result.obj)
        cms_predicate2.printCMS()
        print(f"{result.sub} {result.obj}")


    objects = list(set([result.obj for result in p2_result]))

    count = 0
    for obj in objects:
        c1 = cms_predicate1.get_min(obj)
        c2 = cms_predicate2.get_min(obj)
        print(f"sketch p1: {obj}: {c1}")
        print(f"sketch p2: {obj}: {c2}")
        count += c1 * c2
    return count
