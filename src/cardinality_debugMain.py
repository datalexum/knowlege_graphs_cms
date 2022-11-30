from database_loader.database_loader import DatabaseLoader
from query_templates.queries import object_object_join, object_subject_join, bound_object_subject_join
from src.cms.count_min_sketch import CMS
from utils.count import count_object_object

if __name__ == '__main__':
    Loader = DatabaseLoader([["../data/cardinality_testing.nt", ""]])

    data_graph = Loader.return_Databases()
    # for triple in data_graph:
    #    print(triple)

    pred_prefix_1 = "<https://test.com/whatever#>"
    pred_prefix_2 = "<https://test.com/whatever#>"

    # o_o_results = object_object_join(data_graph = data_graph, predicate1 = "predicate", predicate2 = "predicate2", pred_prefix_1 = pred_prefix_1, pred_prefix_2 = pred_prefix_2)

    # print("Results for obj obj")
    # for result in o_o_results:
    #    print(f"{result.sub1} {result.obj} {result.sub2}")
    # print(len(o_o_results))
    cms_p1 = CMS(10, 2)
    cms_p2 = CMS(10, 2)

    cms_result = count_object_object(cms_p1, cms_p2, "<https://test.com/whatever#predicate>",
                                     "<https://test.com/whatever#predicate2>", data_graph)
    query_result = len(object_object_join(data_graph=data_graph, predicate1="predicate", predicate2="predicate2",
                                      pred_prefix_1=pred_prefix_1, pred_prefix_2=pred_prefix_2))

    print(f"CMS Result: {cms_result}, Query Result: {query_result}")
