from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.plugins.sparql import prepareQuery


def main():
    g = Graph()
    AQP1 = Namespace("http://www.airqualitypredictor.org/data/")
    AQP2 = Namespace("http://www.airqualitypredictor.org/ontology#")

    g.parse('../ontology/ontology.owl', format='ttl')
    g.parse('output-with-links-utf8.ttl', format='ttl')

    # for s, p, o in g.triples((None, None, None)):
    #     print(s, p, o)

    # Query 0
    query = """
               SELECT ?temp
                WHERE{
                    ?temp a aqp:Temperature .
                }
               """
    q = prepareQuery(query, initNs={"aqp": AQP1, "aqp2": AQP2})
    result = g.query(q)
    print("Query 0:")
    for row in result:
        print(row)

    # # Query 1
    # query = """
    #         SELECT ?ctrlstation ?type
    #         WHERE{
    #             ?ctrlstation a ?type .
    #         }
    #         """
    # q = prepareQuery(query, initNs={"aqp": AQP})
    # result = g.query(q)
    # print("Query 1:")
    # for row in result:
    #     print(row)

    # Query 2
    query = """
            SELECT ?temp ?fecha
            WHERE{
                ?temp a aqp:Temperature .
                ?year a aqp:atYear .
                ?fecha a aqp:atDate .
                FILTER(?year = 2020)
            }
            """
    q = prepareQuery(query, initNs={"aqp": AQP1, "aqp2": AQP2})
    result = g.query(q)
    print("\nQuery 2:")
    for row in result:
        print(row)

    # Query 3
    query = """
            SELECT ?maxtemp ?fecha
            WHERE{
                ?sub a aqp:Suburban .
                ?temp a aqp:temperature .
                ?fecha a aqp:atDate .
                ?temp aqp:hasMaxValue ?maxtemp
                FILTER(?maxtemp > 15)
            }
            """
    q = prepareQuery(query, initNs={"aqp": AQP1, "aqp2": AQP2})
    result = g.query(q)
    print("\nQuery 3:")
    for row in result:
        print(row)

    # Query 4
    query = """
            SELECT ?sub
            WHERE{
                ?sub a aqp:Suburban .
            }
            """
    q = prepareQuery(query, initNs={"aqp": AQP1, "aqp2": AQP2})
    result = g.query(q)
    print("\nQuery 4:")
    for row in result:
        print(row)


if __name__ == "__main__":
    main()
