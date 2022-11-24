from database_loader.database_loader import DatabaseLoader


if __name__ == '__main__':

    datalist = [["https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl","ttl"]]
    Loader = DatabaseLoader(datalist)
    Loader.add_Databases([["../data/dummyDataFile.nt",""]])

    data_graph = Loader.return_Databases()
    #print(data)
    #for triple in data_graph:
    #    print(triple)

    join_query = """
    PREFIX ac:  <https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl#>
    PREFIX w3: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xmn: <http://xmlns.com/foaf/0.1/>  
    SELECT ?x ?duplic ?y
    WHERE 
    {
        ?x w3:type ?duplic .
        ?y ac:discipline ?duplic .
    }
    """

    results = data_graph.query(join_query)
    print("Results are")
    for result in results:
        print(f"{result.x} {result.duplic} {result.y}")