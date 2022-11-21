import rdflib
import pprint


class DatabaseLoader:

    def __init__(self, dataBaseLinksList: list):
        self.dataBaseLinksList = dataBaseLinksList
        self.dataBase = rdflib.Graph()
        for link in dataBaseLinksList:
            self.dataBase.parse(link, format="ttl")
    """
        for linkidx in range (0, len(dataBaseLinksList),1):
            print("hi")
            if dataBaseLinksList[linkidx][0] == "":
                self.dataBase.parse(dataBaseLinksList[linkidx])
            elif link[0] == "ttl":
                self.dataBase.parse(link, format="ttl")
        for triple in self.dataBase:
            pprint.pprint(triple)
    """

    def add_Databases(self, dataBaseLinksList: list):
        print(dataBaseLinksList)
    """
        for link in dataBaseLinksList:
            if link[0] == "":
                self.dataBase.parse(link)
            elif link[0] == "ttl":
                self.dataBase.parse(link, format="ttl")
    """

    def return_Databases(self):
        return self.dataBase

