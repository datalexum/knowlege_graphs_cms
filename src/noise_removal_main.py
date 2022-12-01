from database_loader.database_loader import DatabaseLoader
from query_templates.queries import object_object_join
from src.cms.count_min_sketch import CMS
from utils.count import noise_count_object_object


if __name__ == '__main__':
    Loader = DatabaseLoader([["../data/cardinality_testing.nt", ""]])

    data_graph = Loader.return_Databases()
    # for triple in data_graph:
    #    print(triple)

    pred_prefix_1 = "<https://test.com/whatever#>"
    pred_prefix_2 = "<https://test.com/whatever#>"


    o_o_cms_p1 = CMS(10, 2)
    o_o_cms_p2 = CMS(10, 2)

    o_o_cms_result = noise_count_object_object(o_o_cms_p1, o_o_cms_p2, "<https://test.com/whatever#predicate>",
                                     "<https://test.com/whatever#predicate2>", data_graph)

    o_o_query_result = len(object_object_join(data_graph=data_graph, predicate1="predicate", predicate2="predicate2",
                                      pred_prefix_1=pred_prefix_1, pred_prefix_2=pred_prefix_2))

    print(f"CMS Result: {o_o_cms_result}, Query Result: {o_o_query_result}")