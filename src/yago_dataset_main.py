from database_loader.database_loader import DatabaseLoader
from query_templates.queries import object_object_join, object_subject_join, bound_object_subject_join
from src.cms.count_min_sketch import CMS
from utils.count import count_object_object,count_subject_object

if __name__ == '__main__':
    Loader = DatabaseLoader([["../data/yago-1.0.0-turtle_abridged.ttl","ttl"]])

    data_graph = Loader.return_Databases()
    # for triple in data_graph:
    #    print(triple)

    pred_prefix_1 = "<file:///C:/Users/Lukas/PycharmProjects/knowlege_graphs_cms/data/>"
    pred_prefix_2 = "<file:///C:/Users/Lukas/PycharmProjects/knowlege_graphs_cms/data/>"

    # print("Results for obj obj")
    # for result in o_o_results:
    #    print(f"{result.sub1} {result.obj} {result.sub2}")
    # print(len(o_o_results))

    o_o_cms_p1 = CMS(10, 2)
    o_o_cms_p2 = CMS(10, 2)

    o_o_cms_result = count_object_object(o_o_cms_p1, o_o_cms_p2, "<file:///C:/Users/Lukas/PycharmProjects/knowlege_graphs_cms/data/actedIn>",
                                     "<file:///C:/Users/Lukas/PycharmProjects/knowlege_graphs_cms/data/bornOnDate>", data_graph)

    o_o_query_result = len(object_object_join(data_graph=data_graph, predicate1="actedIn", predicate2="bornOnDate",
                                      pred_prefix_1=pred_prefix_1, pred_prefix_2=pred_prefix_2))

    print(f"CMS Result: {o_o_cms_result}, Query Result: {o_o_query_result}")
