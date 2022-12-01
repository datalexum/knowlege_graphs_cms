import numpy as np
from rdflib import Graph
from src.query_templates.queries import o_o_predicate_query
from src.cms.count_min_sketch import CMS


def count_object_object(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph):
    # sub 1 und sub2 können aber müssen nicht gleich sein, lese sie als sub1 und sub2
    # Query1 ?s1 :predicate1 ?o -> p1_result
    # Query2 ?s2 :predicate2 ?o -> p2_result

    # TODO Put into seperate method to prevent repetetive code, can then be reused for other count functions
    p1_result = o_o_predicate_query(graph, predicate1)
    for result in p1_result:
        cms_predicate1.count(result.obj)
        cms_predicate1.printCMS()
        print(f"{result.sub} {result.obj}")

    p2_result = o_o_predicate_query(graph, predicate2)
    for result in p2_result:
        cms_predicate2.count(result.obj)
        cms_predicate2.printCMS()
        print(f"{result.sub} {result.obj}")

    # Zähle nur objecte die sowohl in der ersten als auch in der zweiten query vorkommen, alternativ könnte auch
    # nur die länge der listen verglichen werden, aber auch da kann es passieren das bestimmte objekte nur in eine
    # der queries vorkommen und dadurch das ergebnis der cms geskewed wird, sofern genug noise existiert

    objects = set([result.obj for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    for obj in objects:
        print(obj)
        c1 = cms_predicate1.get_min(obj)
        c2 = cms_predicate2.get_min(obj)
        print(f"sketch p1: {obj}: {c1}")
        print(f"sketch p2: {obj}: {c2}")
        count += c1 * c2
    return count

def noise_count_object_object(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph):
    # sub 1 und sub2 können aber müssen nicht gleich sein, lese sie als sub1 und sub2
    # Query1 ?s1 :predicate1 ?o -> p1_result
    # Query2 ?s2 :predicate2 ?o -> p2_result

    p1_result = o_o_predicate_query(graph, predicate1)
    for result in p1_result:
        cms_predicate1.count(result.obj)
        #cms_predicate1.printCMS()
        #print(f"{result.sub} {result.obj}")

    p2_result = o_o_predicate_query(graph, predicate2)
    for result in p2_result:
        cms_predicate2.count(result.obj)
        #cms_predicate2.printCMS()
        #print(f"{result.sub} {result.obj}")

    # Zähle nur objecte die sowohl in der ersten als auch in der zweiten query vorkommen, alternativ könnte auch
    # nur die länge der listen verglichen werden, aber auch da kann es passieren das bestimmte objekte nur in eine
    # der queries vorkommen und dadurch das ergebnis der cms geskewed wird, sofern genug noise existiert

    objects = set([result.obj for result in p2_result]) & set([result.obj for result in p1_result])

    count = 0
    cms_predicate1.remove_noise()
    cms_predicate2.remove_noise()
    for obj in objects:
        #print(obj)
        c1 = cms_predicate1.noise_removal_get_min(obj)
        c2 = cms_predicate2.noise_removal_get_min(obj)
        #print(f"sketch p1: {obj}: {c1}")
        #print(f"sketch p2: {obj}: {c2}")
        count += c1 * c2
    return count


def count_subject_object(cms_predicate1: CMS, cms_predicate2: CMS, predicate1, predicate2, graph: Graph):
    """
    cms_predicate1 for counting objects based on predicate1
    cms_predicate2 for counting subjects based on predicate2
    """

    # TODO: zur zeit wird predicate 2 zu subject und predicate 1 für object, die wahl was was ist, ist dabei random,
    #  macht gegebenenfalls sind, einmal in die eine richtung und einmal in die andere zu amchen und dann den
    #  mittelwert zu nehmen also min((op1,sp2),(sp1,op2))

    #Krux des Problems:
    # Wir wollen alle sub / obj paare die sowohl bei pred1 als auch bei pred2 sind zählen
    #   -> da das die sind die auch das erfüllen was die query macht
    # die cms zählen allerdings das allgemeine vorkommen von diesen objekten / subjekten
    # in der count funktion wird deshalb immer das allgemine vorkommen der objekte mit dem allgemeinen vorkommen der subjekte multipliziert
    # und deshalb sachen mehrfach gemoppelt
    # objekte unterschiedlicher zugehörigkeit können auch nicht voneinander getrennt werden ohne das mit im CMS abzuspeichern
    # Ergo: entweder ist das CMS falsch verstanden und implementiert oder das count obj * count subj falsch verstanden
    # wahrscheinlicher das zweite da obj_obj funktioniert


    p1_result = o_o_predicate_query(graph, predicate1)
    for result in p1_result:
        cms_predicate1.count(result.obj)
        cms_predicate1.printCMS()
        print(f"{result.sub} {result.obj}")
    print("all objects added")

    p2_result = o_o_predicate_query(graph, predicate2)
    for result in p2_result:
        cms_predicate2.count(result.sub)
        cms_predicate2.printCMS()
        print(f"{result.sub} {result.sub}")
    print("all subjects added")

    results = set(p1_result) & set(p2_result)
    print(results)
    count = 0
    for result in results:
        print(result)
        c1 = cms_predicate1.get_min(result.obj)
        c2 = cms_predicate2.get_min(result.sub)
        print(f"sketch p1: {result.obj}: {c1}")
        print(f"sketch p2: {result.sub}: {c2}")
        count += c1 * c2
    return count
