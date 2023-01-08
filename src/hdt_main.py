from rdflib import Graph
from rdflib_hdt import HDTStore, optimize_sparql
from database_loader.database_loader import DatabaseLoader
from query_templates.queries import object_object_join, object_subject_join, bound_object_subject_join
from src.cms.count_min_sketch import CMS
from utils.count import count_object_object

if __name__ == '__main__':
    # Load an HDT file. Missing indexes are generated automatically
    # You can provide the index file by putting them in the same directory than the HDT file.
    # Calling this function optimizes the RDFlib SPARQL engine for HDT documents

    optimize_sparql()

    data_graph = Graph(store=HDTStore("../watdiv/watdiv_10M_lars.hdt"))

    # for triple in data_graph:
    # dumme idee too many
    #    print(triple)


    RDF_O_O_PRED_PREFIX_1 = "<http://www.geonames.org/ontology#>"
    RDF_O_O_PRED_PREFIX_2 = "<http://schema.org/>"
    RDF_O_O_PREDICATE_1 = "parentCountry"
    RDF_O_O_PREDICATE_2 = "nationality"

    RDF_O_O_PREFIXES = [RDF_O_O_PRED_PREFIX_1, RDF_O_O_PRED_PREFIX_2]
    RDF_O_O_ENDINGS = [RDF_O_O_PREDICATE_1, RDF_O_O_PREDICATE_2]

    o_o_cms_p1 = CMS(10, 2)
    o_o_cms_p2 = CMS(10, 2)

    o_o_cms_result = count_object_object(cms_predicate1=o_o_cms_p1, cms_predicate2=o_o_cms_p2, endings=RDF_O_O_ENDINGS,
                                         prefixes=RDF_O_O_PREFIXES, graph=data_graph)

    o_o_query_result = object_object_join(data_graph=data_graph, endings=RDF_O_O_ENDINGS, prefixes=RDF_O_O_PREFIXES)


    #print(f" Query Result: {o_o_query_result}")
    print(f"CMS Result: {o_o_cms_result}, Query Result: {o_o_query_result}")
