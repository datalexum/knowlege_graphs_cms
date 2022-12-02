from database_loader.database_loader import DatabaseLoader
from query_templates.queries import object_object_join,object_subject_join,bound_object_subject_join

if __name__ == '__main__':

    datalist = [["../data/yago-1.0.0-turtle.ttl","ttl"]]#[["https://yago-knowledge.org/data/yago1/yago-1.0.0-turtle.7z","ttl"]]#[["https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl","ttl"]]
    Loader = DatabaseLoader(datalist)

    Loader.add_Databases([["../data/dummyDataFile.nt",""]])

    data_graph = Loader.return_Databases()
    #print(data)
    for idx, triple in enumerate(data_graph):
        print(triple)
        if idx > 20:
            break



"""
    pred_prefix_1 = "<file:///C:/Users/Lukas/PycharmProjects/knowlege_graphs_cms/data/>"#"<http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
    pred_prefix_2 = "<file:///C:/Users/Lukas/PycharmProjects/knowlege_graphs_cms/data/>"#"<https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl#>"
    #obj_prefix_1 = "<https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl#>"

    o_o_results = object_object_join(data_graph = data_graph, predicate1 = "actedIn", predicate2 = "bornOnDate", pred_prefix_1 = pred_prefix_1, pred_prefix_2 = pred_prefix_2)
"""
    #o_s_results = object_subject_join(data_graph = data_graph, predicate1 = "type", predicate2 = "discipline", pred_prefix_1 = pred_prefix_1, pred_prefix_2 = pred_prefix_2)

    #bound_o_s_results = bound_object_subject_join(data_graph = data_graph, predicate1 = "type", predicate2 = "discipline", object1 = "University_of_Cambridge", pred_prefix_1 = pred_prefix_1, pred_prefix_2 = pred_prefix_2,obj_prefix_1 = obj_prefix_1)
"""
    print("Results for obj obj")
    for result in o_o_results:
        print(f"{result.sub1} {result.obj} {result.sub2}")
"""

    #print("Results for obj sub")
    #for result in o_s_results:
    #    print(f"{result.sub} {result.obj}")
    #print("Results for bound obj sub")


    #for result in bound_o_s_results:
    #    print(f"{result.sub}")
    #print(len(o_o_results))