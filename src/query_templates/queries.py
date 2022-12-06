import rdflib
import pprint


def object_object_join(data_graph, predicate1, predicate2, pred_prefix_1, pred_prefix_2):

    pre1 = """pre1:"""
    pre2 = """pre2:"""
    prefixes =  """PREFIX pre1: """ + pred_prefix_1
    if pred_prefix_1 != pred_prefix_2:
        prefixes = prefixes + """PREFIX pre2: """ + pred_prefix_2
    else:
        pre2 = pre1

    join_query = prefixes + """
    SELECT ?sub1 ?obj ?sub2
    WHERE 
    {
        ?sub1 """ + pre1 + predicate1 + """ ?obj.
        ?sub2 """ + pre2 + predicate2 + """ ?obj.
    }
    """
    #print("obj obj")
    #print(join_query)
    #print(pre1)
    #print(pre2)
    #print(predicate1)
    #print(predicate2)
    return data_graph.query(join_query)


def object_subject_join(data_graph, predicate1, predicate2, pred_prefix_1, pred_prefix_2):
    pre1 = """pre1:"""
    pre2 = """pre2:"""
    prefixes = """PREFIX pre1: """ + pred_prefix_1
    if pred_prefix_1 != pred_prefix_2:
        prefixes = prefixes + """PREFIX pre2: """ + pred_prefix_2
    else:
        pre2 = pre1

    join_query = prefixes + """
    SELECT ?sub ?obj
    WHERE 
    {
        ?sub """ + pre1 + predicate1 + """ ?obj.
        ?obj """ + pre2 + predicate2 + """ ?obj2.
    }
    """
    #print("obj sub")
    #print(join_query)
    return data_graph.query(join_query)


def bound_object_subject_join(data_graph, predicate1, predicate2, object1, pred_prefix_1, pred_prefix_2,obj_prefix_1):
    pre1 = """pre1:"""
    pre2 = """pre2:"""
    pre3 = """pre3:"""
    prefixes = """PREFIX pre1: """ + pred_prefix_1 + """ """

    if pred_prefix_1 != pred_prefix_2:
        prefixes = prefixes + """PREFIX pre2: """ + pred_prefix_2 + """ """
    else:
        pre2 = pre1

    if obj_prefix_1 == pred_prefix_1:
        pre3 = pre1
    elif obj_prefix_1 == pred_prefix_2:
        pre3 = pre2
    else:
        prefixes = prefixes + """PREFIX pre3: """ + obj_prefix_1 + """ """


    join_query = prefixes + """
    SELECT ?sub 
    WHERE 
    {
        ?sub """ + pre1 + predicate1 + """ ?obj.
        ?obj """ + pre2 + predicate2 + """ """+ pre3 + object1+""".
    }
    """
    #print("bound obj sub")
    #print(join_query)
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
        ?sub """ + predicate + object + """.
    }
    """
    return data_graph.query(query)