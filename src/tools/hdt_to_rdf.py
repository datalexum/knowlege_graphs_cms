import hdt
import rdflib
import rdflib_hdt.hdt_store
from tqdm import tqdm


def hdt_to_rdf(path: str):
    # Load the HDT file

    doc = hdt.HDTDocument(path)

    # Create a new RDF graph
    g = rdflib.Graph()

    # Iterate over the triples in the HDT file and add them to the RDF graph
    for s, p, o in tqdm(doc.search_triples("", "", "")[0], total=doc.search_triples("", "", "")[1]):
        if o.startswith("http://") or o.startswith("https://"):
            # o is a URI
            g.add((rdflib.URIRef(s), rdflib.URIRef(p), rdflib.URIRef(o)))
        else:
            # o is a literal
            g.add((rdflib.URIRef(s), rdflib.URIRef(p), rdflib.Literal(o)))

    # Serialize the RDF graph to an NT file
    with open("result.nt", "w") as f:
        f.write(g.serialize(format='turtle'))


def main():
    hdt_to_rdf('/home/alsch/PycharmProjects/knowlege_graphs_cms/data/watdiv/watdiv_10M_lars.hdt')


if __name__ == '__main__':
    main()
