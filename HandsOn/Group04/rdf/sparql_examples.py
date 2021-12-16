from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.plugins.sparql import prepareQuery


def main():
    g = Graph()
    AQP_DATA = Namespace("http://www.airqualitypredictor.org/data/")
    AQP_CLASSES = Namespace("http://www.airqualitypredictor.org/ontology/")
    AQP_PROPERTIES = Namespace("http://www.airqualitypredictor.org/ontology#")

    g.parse('../ontology/ontology.owl', format='ttl')
    g.parse('output-diciembre-utf8.ttl', format='ttl')

    # # Query 1
    # query = """
    #         SELECT ?control_station
    #         WHERE{
    #             ?control_station a aqp_classes:Suburban .
    #         }
    #         LIMIT 10
    #         """
    # q = prepareQuery(query, initNs={"aqp_data": AQP_DATA, "aqp_classes": AQP_CLASSES, "aqp_properties": AQP_PROPERTIES})
    # result = g.query(q)
    # print("Query 1:")
    # for row in result:
    #     print(row)

    # # Query 2
    # query = """
    #         SELECT ?sub ?max_value ?day
    #         WHERE{
    #             ?sub a aqp_classes:PM10 .
    #             ?sub aqp_properties:hasMaxValue ?max_value .
    #             ?sub aqp_properties:atDay ?day .
    #             FILTER(?day = 1.0)
    #         }
    #         ORDER BY DESC(?max_value) LIMIT 10
    #         """
    # q = prepareQuery(query, initNs={"aqp_data": AQP_DATA, "aqp_classes": AQP_CLASSES, "aqp_properties": AQP_PROPERTIES})
    # result = g.query(q)
    # print("\nQuery 2:")
    # print("Top 10 stations with the highest PM10 concentration in the first day of the year")
    # # print("Max value of temperature in December 2020:")
    # for row in result:
    #     print(row)

    # # Query 3
    # control_station = 58  # ?max_N0_2 ?max_0_3 ?max_PM2.5
    # query = f"""
    #         SELECT ?sub1 ?max_PM10
    #         WHERE {"{"}
    #             ?sub1 a aqp_classes:PM10 .
    #             ?sub1 aqp_properties:hasMaxValue ?max_PM10 .
    #             ?sub1 apq_properties:controlStation {control_station} .
    #         {"}"}
    #         """
    #
    # print(query)
    # q = prepareQuery(query, initNs={"aqp_data": AQP_DATA, "aqp_classes": AQP_CLASSES, "aqp_properties": AQP_PROPERTIES})
    # result = g.query(q)
    # print("\nQuery 3:")
    # for row in result:
    #     print(row)

    # Query 4: see all properties of a measurement
    query = """
            SELECT DISTINCT ?prop
            WHERE{
                ?sub a aqp_classes:PM10 .
                ?sub ?prop ?value .
            }
            """
    q = prepareQuery(query, initNs={"aqp_data": AQP_DATA, "aqp_classes": AQP_CLASSES, "aqp_properties": AQP_PROPERTIES})
    result = g.query(q)
    print("\nQuery 4:")
    for row in result:
        print(row)


if __name__ == "__main__":
    main()
