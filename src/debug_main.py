from database_loader.database_loader import DatabaseLoader
from src.utils.count import count_object_object, count_object_subject, count_bound_object_subject
from query_templates.queries import object_object_join, object_subject_join, bound_object_subject_join
from src.cms.count_min_sketch import CMS
import numpy as np

RDF_O_O_PRED_PREFIX_1 = "<https://test.com/whatever#>"
RDF_O_O_PRED_PREFIX_2 = "<https://test.com/whatever#>"
RDF_O_O_PREDICATE_1 = "predicate"
RDF_O_O_PREDICATE_2 = "predicate2"

RDF_O_O_PREFIXES = [RDF_O_O_PRED_PREFIX_1, RDF_O_O_PRED_PREFIX_2]
RDF_O_O_ENDINGS = [RDF_O_O_PREDICATE_1, RDF_O_O_PREDICATE_2]

RDF_O_S_PRED_PREFIX_1 = "<https://test.com/whatever#>"
RDF_O_S_PRED_PREFIX_2 = "<https://test.com/whatever#>"
RDF_O_S_PREDICATE_1 = "predicate"
RDF_O_S_PREDICATE_2 = "predicate2"

RDF_O_S_PREFIXES = [RDF_O_S_PRED_PREFIX_1, RDF_O_S_PRED_PREFIX_2]
RDF_O_S_ENDINGS = [RDF_O_S_PREDICATE_1, RDF_O_S_PREDICATE_2]

RDF_B_O_S_PRED_PREFIX_1 = "<https://test.com/whatever#>"
RDF_B_O_S_PRED_PREFIX_2 = "<https://test.com/whatever#>"
RDF_B_O_S_PREDICATE_1 = "predicate"
RDF_B_O_S_PREDICATE_2 = "predicate2"
RDF_B_O_S_OBJ_PREFIX = "<https://test.com/whateverAAA#>"
RDF_B_O_S_OBJECT = "endobject"

RDF_B_O_S_PREFIXES = [RDF_B_O_S_PRED_PREFIX_1, RDF_B_O_S_PRED_PREFIX_2, RDF_B_O_S_OBJ_PREFIX]
RDF_B_O_S_ENDINGS = [RDF_B_O_S_PREDICATE_1, RDF_B_O_S_PREDICATE_2, RDF_B_O_S_OBJECT]



def o_o_join(graph):
    o_o_cms_p1 = CMS(10, 2)
    o_o_cms_p2 = CMS(10, 2)

    o_o_cms_result = count_object_object(cms_predicate1=o_o_cms_p1, cms_predicate2=o_o_cms_p2, endings=RDF_O_O_ENDINGS,
                                         prefixes=RDF_O_O_PREFIXES, graph=graph, cms_precalculated=False)

    o_o_query_result = object_object_join(data_graph=graph, endings=RDF_O_O_ENDINGS, prefixes=RDF_O_O_PREFIXES)

    # for result in o_o_query_result:
    #    print(f"{result.sub1} {result.obj} {result.sub2}")
    print(f"CMS Result: {o_o_cms_result}, Query Result: {len(o_o_query_result)}")


def noise_o_o_join(graph):
    o_o_cms_p1 = CMS(10, 2)
    o_o_cms_p2 = CMS(10, 2)

    o_o_cms_result = count_object_object(cms_predicate1=o_o_cms_p1, cms_predicate2=o_o_cms_p2, endings=RDF_O_O_ENDINGS,
                                         prefixes=RDF_O_O_PREFIXES, graph=graph, noise_operation=np.amin, cms_precalculated=False)

    o_o_query_result = object_object_join(data_graph=graph, endings=RDF_O_O_ENDINGS, prefixes=RDF_O_O_PREFIXES)

    # for result in o_o_query_result:
    #    print(f"{result.sub1} {result.obj} {result.sub2}")
    print(f"CMS Result: {o_o_cms_result}, Query Result: {len(o_o_query_result)}")


def o_s_join(graph):
    o_s_cms_p1 = CMS(10, 2)
    o_s_cms_p2 = CMS(10, 2)

    o_s_cms_result = count_object_subject(cms_predicate1=o_s_cms_p1, cms_predicate2=o_s_cms_p2, endings=RDF_O_S_ENDINGS,
                                          prefixes=RDF_O_S_PREFIXES, graph=graph, cms_precalculated=False)

    o_s_query_result = object_subject_join(data_graph=graph, endings=RDF_O_S_ENDINGS, prefixes=RDF_O_S_PREFIXES)

    # for result in o_s_query_result:
    #    print(f"{result.sub} {result.obj1} {result.obj2}")
    print(f"CMS Result: {o_s_cms_result}, Query Result: {len(o_s_query_result)}")


def noise_o_s_join(graph):
    o_s_cms_p1 = CMS(10, 2)
    o_s_cms_p2 = CMS(10, 2)

    o_s_cms_result = count_object_subject(cms_predicate1=o_s_cms_p1, cms_predicate2=o_s_cms_p2, endings=RDF_O_S_ENDINGS,
                                          prefixes=RDF_O_S_PREFIXES, graph=graph, noise_operation=np.amin, cms_precalculated=False)

    o_s_query_result = object_subject_join(data_graph=graph, endings=RDF_O_S_ENDINGS, prefixes=RDF_O_S_PREFIXES)

    # for result in o_s_query_result:
    #    print(f"{result.sub} {result.obj1} {result.obj2}")
    print(f"CMS Result: {o_s_cms_result}, Query Result: {len(o_s_query_result)}")


def b_o_s_join(graph):
    b_o_s_cms_p1 = CMS(10, 2)
    b_o_s_cms_p2 = CMS(10, 2)

    b_o_s_cms_result = count_bound_object_subject(cms_predicate1=b_o_s_cms_p1, cms_predicate2=b_o_s_cms_p2,
                                                  endings=RDF_B_O_S_ENDINGS, prefixes=RDF_B_O_S_PREFIXES, graph=graph, cms_precalculated=False)

    b_o_s_query_result = bound_object_subject_join(data_graph=graph, endings=RDF_B_O_S_ENDINGS,
                                                   prefixes=RDF_B_O_S_PREFIXES)

    # for result in b_o_s_query_result:
    #    print(f"{result.sub} {result.obj1}")
    print(f"CMS Result: {b_o_s_cms_result}, Query Result: {len(b_o_s_query_result)}")


def noise_b_o_s_join(graph):
    b_o_s_cms_p1 = CMS(10, 2)
    b_o_s_cms_p2 = CMS(10, 2)

    b_o_s_cms_result = count_bound_object_subject(cms_predicate1=b_o_s_cms_p1, cms_predicate2=b_o_s_cms_p2,
                                                  endings=RDF_B_O_S_ENDINGS, prefixes=RDF_B_O_S_PREFIXES, graph=graph,
                                                  noise_operation=np.amin, cms_precalculated=False)

    b_o_s_query_result = bound_object_subject_join(data_graph=graph, endings=RDF_B_O_S_ENDINGS,
                                                   prefixes=RDF_B_O_S_PREFIXES)

    # for result in b_o_s_query_result:
    #    print(f"{result.sub} {result.obj1}")
    print(f"CMS Result: {b_o_s_cms_result}, Query Result: {len(b_o_s_query_result)}")


if __name__ == '__main__':
    o_o_Loader = DatabaseLoader([["../data/o_o_cardinality_testing.nt", ""]])
    o_o_rdf_graph = o_o_Loader.return_Databases()

    o_s_Loader = DatabaseLoader([["../data/o_s_cardinality_testing.nt", ""]])
    o_s_rdf_graph = o_s_Loader.return_Databases()

    b_o_s_Loader = DatabaseLoader([["../data/b_o_s_cardinality_testing.nt", ""]])
    b_o_s_rdf_graph = b_o_s_Loader.return_Databases()

    o_o_join(o_o_rdf_graph)
    noise_o_o_join(o_o_rdf_graph)
    o_s_join(o_s_rdf_graph)
    noise_o_s_join(o_s_rdf_graph)
    b_o_s_join(b_o_s_rdf_graph)
    noise_b_o_s_join(b_o_s_rdf_graph)
"""
    optimize_sparql()

    PREDICATE_1 = 'parentCountry'
    PREDICATE_2 = 'nationality'
    PREFIX_1 = '<http://www.geonames.org/ontology#>'
    PREFIX_2 = '<http://schema.org/>'
    hdt_graph = Graph(store=HDTStore("../watdiv/watdiv_10M_lars.hdt"))

    o_o_results = object_object_join(data_graph=hdt_graph, predicate1=PREDICATE_1, predicate2=PREDICATE_2,pred_prefix_1=PREFIX_1, pred_prefix_2=PREFIX_2)
    print(len(o_o_results))
"""
