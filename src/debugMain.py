from database_loader.database_loader import DatabaseLoader


if __name__ == '__main__':
    #datalist = [["https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl","ttl"]]
    datalist = ["https://raw.githubusercontent.com/maribelacosta/linkeddata/master/data/alan_turing.ttl"]
    Loader = DatabaseLoader(datalist)
    #Loader.add_Databases("../data/dummyDataFile.nt")

    data = Loader.return_Databases()
    print(data)
    for triple in data:
        print(triple)