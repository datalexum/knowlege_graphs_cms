import rdflib
import pprint


def remove_duplicates(lst):
    result = []
    for element in lst:
        if element not in result:
            result.append(element)
    return result


def object_object_join(data_graph, prefixes, endings):
    pres = []
    # removes doubles
    # Cant use list(set( because it will jumble the order
    prefixes = remove_duplicates(prefixes)
    query_prefix = """    """

    for idx, prefix in enumerate(prefixes):
        query_prefix = query_prefix + """PREFIX pre""" + str(idx + 1) + """: """ + prefix + """\n    """
        pres.append("""pre""" + str(idx + 1) + """:""")

    join_query = query_prefix + """
    SELECT ?sub1 ?obj ?sub2
    WHERE 
    {
        ?sub1 """ + pres[0] + endings[0] + """ ?obj.
        ?sub2 """ + pres[(1 % len(pres))] + endings[1] + """ ?obj.
    }
    """
    # print("obj obj")
    # print(join_query)
    return data_graph.query(join_query)


def object_subject_join(data_graph, prefixes, endings):
    pres = []
    # removes doubles
    # Cant use list(set( because it will jumble the order
    prefixes = remove_duplicates(prefixes)
    query_prefix = """    """

    for idx, prefix in enumerate(prefixes):
        query_prefix = query_prefix + """PREFIX pre""" + str(idx + 1) + """: """ + prefix + """\n    """
        pres.append("""pre""" + str(idx + 1) + """:""")

    join_query = query_prefix + """
    SELECT ?sub ?obj1 ?obj2
    WHERE 
    {
        ?sub """ + pres[0] + endings[0] + """ ?obj1.
        ?obj1 """ + pres[(1 % len(pres))] + endings[1] + """ ?obj2.
    }
    """
    # print("obj sub")
    # print(join_query)
    return data_graph.query(join_query)


def bound_object_subject_join(data_graph, prefixes, endings):
    preIndex = [1, 2, 3]
    existingprefixes = []
    # removes doubles
    query_prefix = """    """

    counter = 0
    for idx, prefix in enumerate(prefixes):
        breakCon = False
        for value in existingprefixes:
            if value == prefix:
                breakCon = True
                break
        if breakCon == False:
            counter = counter + 1
            existingprefixes.append(prefix)
            query_prefix = query_prefix + """PREFIX pre""" + str(counter) + """: """ + prefix + """\n    """
        preIndex[idx] = counter

    join_query = query_prefix + """
    SELECT ?sub ?obj1
    WHERE 
    {
        ?sub pre""" + str(preIndex[0]) + """:""" + endings[0] + """ ?obj1.
        ?obj1 pre""" + str(preIndex[1]) + """:""" + endings[1] + """ pre""" + str(preIndex[2]) + """:""" + endings[2] + """.
    }
    """
    # print("bound obj sub")
    # print(join_query)
    return data_graph.query(join_query)


def sub_predicate_query(data_graph, prefix, predicate):
    # print(predicate)
    # need to be seperated to sub predicate query and obj predicate query for maximum efficiency, otherwise
    # both values would be queried each time
    query = """PREFIX pre1: """ + prefix + """
    SELECT ?sub  
    WHERE 
    {
        ?sub pre1:""" + predicate + """ ?obj.
    }
    """
    print(query)
    return data_graph.query(query)


def obj_predicate_query(data_graph, prefix, predicate):
    # print(predicate)
    # need to be seperated to sub predicate query and obj predicate query for maximum efficiency, otherwise
    # both values would be queried each time
    query = """PREFIX pre1: """ + prefix + """
    SELECT ?obj  
    WHERE 
    {
        ?sub pre1:""" + predicate + """ ?obj.
    }
    """
    # print(query)
    return data_graph.query(query)


def bound_sub_predicate_query(data_graph, prefixes, endings):
    # print(prefixes)
    # print(endings)
    pres = []
    # removes doubles
    # Cant use list(set( because it will jumble the order
    prefixes = remove_duplicates(prefixes)
    query_prefix = """    """

    for idx, prefix in enumerate(prefixes):
        query_prefix = query_prefix + """PREFIX pre""" + str(idx + 1) + """: """ + prefix + """\n    """
        pres.append("""pre""" + str(idx + 1) + """:""")

    query = query_prefix + """
    SELECT ?sub
    WHERE
    {
        ?sub """ + pres[0] + endings[0] + """ """ + pres[(1 % len(pres))] + endings[1] + """.
    }
    """
    # print("bound pred")
    # print(query)
    return data_graph.query(query)
