import rdflib
import pprint


def remove_duplicates(lst):
    result = []
    for element in lst:
        if element not in result:
            result.append(element)
    return result

def object_object_join(data_graph, endings, prefixes):
    pres = []
    #removes doubles
    prefixes = list(set(prefixes))
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
    print("obj obj")
    print(join_query)
    return data_graph.query(join_query)



def object_subject_join(data_graph, endings, prefixes):
    pres = []
    #removes doubles
    prefixes = list(set(prefixes))
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
    print("obj sub")
    print(join_query)
    return data_graph.query(join_query)


def bound_object_subject_join(data_graph, endings, prefixes):
    pres = []
    #removes doubles
    prefixes = list(set(prefixes))
    query_prefix = """    """

    for idx, prefix in enumerate(prefixes):
        query_prefix = query_prefix+ """PREFIX pre"""+ str(idx+1) + """: """ + prefix + """\n    """
        pres.append ("""pre""" + str(idx+1)+ """:""")

    join_query = query_prefix + """
    SELECT ?sub ?obj1
    WHERE 
    {
        ?sub """ +pres[0] + endings[0] + """ ?obj1.
        ?obj1 """ + pres[(1%len(pres))] + endings[1] + """ \""""+ endings[2]+"""\".
    }
    """
    print("bound obj sub")
    print(join_query)
    return data_graph.query(join_query)

def predicate_query(data_graph, predicate):


    query = """
    SELECT ?sub ?obj 
    WHERE 
    {
        ?sub """ + predicate + """ ?obj.
    }
    """
    return data_graph.query(query)

def bound_predicate_query(data_graph, predicate, object):


    query = """
    SELECT ?sub
    WHERE
    {
        ?sub """ + predicate +""" \""""+ object + """\".
    }
    """
    # print("bound pred")
    # print(query)
    return data_graph.query(query)
