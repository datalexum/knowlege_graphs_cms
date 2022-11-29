from database_loader.database_loader import DatabaseLoader
from query_templates.queries import object_object_join,object_subject_join,bound_object_subject_join

if __name__ == '__main__':

    datalist = [["https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl","ttl"]]
    Loader = DatabaseLoader(datalist)

    Loader.add_Databases([["../data/dummyDataFile.nt",""]])

    data_graph = Loader.return_Databases()
    #print(data)
    #for triple in data_graph:
    #    print(triple)

    #join_query = """
    #PREFIX ac:  <https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl#>
    #PREFIX w3: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #PREFIX xmn: <http://xmlns.com/foaf/0.1/>
    #SELECT ?x ?duplic ?y
    #WHERE
    #{
    #    ?x w3:type ?duplic .
    #    ?y ac:discipline ?duplic .
    #}
    #"""
    #print(join_query)
    #w3 = "w3"
    #test_query = """
    #PREFIX ac:  <https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl#>
    #PREFIX w3: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #SELECT ?x ?duplic ?y
    #WHERE
    #{
    #    ?x """ + w3 + """:type ?duplic .
    #    ?y ac:discipline ?duplic .
    #}
    #"""
    #print(test_query)

    #results = data_graph.query(test_query)
    #print("Results are")

    #for result in results:
    #    print(f"{result.x} {result.duplic} {result.y}")
    pred_prefix_1 = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
    pred_prefix_2 = "<https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl#>"
    obj_prefix_1 = "<https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl#>"

    o_o_results = object_object_join(data_graph = data_graph, predicate1 = "type", predicate2 = "discipline", pred_prefix_1 = pred_prefix_1, pred_prefix_2 = pred_prefix_2)

    o_s_results = object_subject_join(data_graph = data_graph, predicate1 = "type", predicate2 = "discipline", pred_prefix_1 = pred_prefix_1, pred_prefix_2 = pred_prefix_2)

    bound_o_s_results = bound_object_subject_join(data_graph = data_graph, predicate1 = "type", predicate2 = "discipline", object1 = "University_of_Cambridge", pred_prefix_1 = pred_prefix_1, pred_prefix_2 = pred_prefix_2,obj_prefix_1 = obj_prefix_1)

    print("Results for obj obj")
    for result in o_o_results:
        print(f"{result.sub1} {result.obj} {result.sub2}")
    #print("Results for obj sub")
    #for result in o_s_results:
    #    print(f"{result.sub} {result.obj}")
    #print("Results for bound obj sub")
    for result in bound_o_s_results:
        print(f"{result.sub}")
    print(len(o_o_results))