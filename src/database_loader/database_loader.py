import rdflib
import pprint


class DatabaseLoader:

    def __init__(self, dataBaseLinksList: list):
        self.dataBaseLinksList = dataBaseLinksList
        self.dataBase = rdflib.Graph()

        for linkidx, link in enumerate(dataBaseLinksList):
            #print(linkidx)
            #print(link)
            #print(dataBaseLinksList[linkidx][1])

            if dataBaseLinksList[linkidx][1] == "":
                self.dataBase.parse(dataBaseLinksList[linkidx][0])
            elif dataBaseLinksList[linkidx][1] == "ttl":
                self.dataBase.parse(dataBaseLinksList[linkidx][0], format="ttl")
            else:
                print("Unknown database type")
        print("Database created")


    def add_Databases(self, dataBaseLinksList: list):
        print(dataBaseLinksList)

        for linkidx, link in enumerate(dataBaseLinksList):
            if dataBaseLinksList[linkidx][1] == "":
                self.dataBase.parse(dataBaseLinksList[linkidx][0])
            elif dataBaseLinksList[linkidx][1] == "ttl":
                self.dataBase.parse(dataBaseLinksList[linkidx][0], format="ttl")
            else:
                print("Unknown database type")

        print("Database changed")


    def return_Databases(self):
        return self.dataBase

