from rdflib import Graph, Namespace
from rdflib.namespace import XSD
from rdflib.plugins.sparql import prepareQuery
from typing import Tuple


def main():
    g = Graph()
    AQP_DATA = Namespace("http://www.airqualitypredictor.org/data/")
    AQP_CLASSES = Namespace("http://www.airqualitypredictor.org/ontology/")
    AQP_PROPERTIES = Namespace("http://www.airqualitypredictor.org/ontology#")

    g.parse('../ontology/ontology.owl', format='ttl')
    g.parse('output-diciembre-utf8.ttl', format='ttl')

    # Query 1
    query = """
            SELECT ?control_station
            WHERE{
                ?control_station a aqp_classes:Suburban .
            }
            LIMIT 10
            """
    q = prepareQuery(query, initNs={"aqp_data": AQP_DATA, "aqp_classes": AQP_CLASSES, "aqp_properties": AQP_PROPERTIES})
    result = g.query(q)
    print("Query 1:")
    for row in result:
        print(row)

    # Query 2
    query = """
            SELECT ?sub ?max_value ?day
            WHERE{
                ?sub a aqp_classes:PM10 .
                ?sub aqp_properties:hasMaxValue ?max_value .
                ?sub aqp_properties:atDay ?day .
                FILTER(?day = 1)
            }
            ORDER BY DESC(?max_value) LIMIT 10
            """
    q = prepareQuery(query, initNs={"aqp_data": AQP_DATA, "aqp_classes": AQP_CLASSES, "aqp_properties": AQP_PROPERTIES})
    result = g.query(q)
    print("\nQuery 2:")
    print("Top 10 stations with the highest PM10 concentration in the first day of the year")
    # print("Max value of temperature in December 2020:")
    for row in result:
        print(row)

    # Query 3
    control_station = 4
    date = "2019-12-01"
    query = f"""
            SELECT ?max_PM10 ?max_NO_2 ?max_O_3 ?date1
            WHERE {"{"}
            {"{"}
                {"{"}
                    ?sub1 a aqp_classes:PM10 .
                    ?sub1 aqp_properties:hasMaxValue ?max_PM10 .
                    ?sub1 aqp_properties:isFrom aqp_data:{control_station} .
                    ?sub1 aqp_properties:atDate ?date1 .
                    FILTER (?date1 = "{date}"^^xsd:date) .
                {"}"}
                UNION
                {"{"}
                    ?sub2 a aqp_classes:NO2 .
                    ?sub2 aqp_properties:hasMaxValue ?max_N0_2 .
                    ?sub2 aqp_properties:isFrom aqp_data:{control_station} .
                    ?sub2 aqp_properties:atDate ?date2 .
                    FILTER(?date2 = "{date}"^^xsd:date) .
                {"}"}
            {"}"}
            UNION 
            {"{"}
                ?sub3 a aqp_classes:O_3 .
                ?sub3 aqp_properties:hasMaxValue ?max_O_3 .
                ?sub3 aqp_properties:isFrom aqp_data:{control_station} .
                ?sub3 aqp_properties:atDate ?date3 .
                FILTER(?date3 = "{date}"^^xsd:date) .
            {"}"}
        {"}"}
            """

    q = prepareQuery(query, initNs={"aqp_data": AQP_DATA,
                                    "aqp_classes": AQP_CLASSES,
                                    "aqp_properties": AQP_PROPERTIES,
                                    "xsd": XSD})
    result = g.query(q)
    print("\nQuery 3:")
    print(get_no2_pm10_o3(control_station, date, g))

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


def get_no2_pm10_o3(control_station, date, g) -> Tuple[float or None, float or None, float or None]:

    # Namespaces
    AQP_DATA = Namespace("http://www.airqualitypredictor.org/data/")
    AQP_CLASSES = Namespace("http://www.airqualitypredictor.org/ontology/")
    AQP_PROPERTIES = Namespace("http://www.airqualitypredictor.org/ontology#")

    query = f"""
            SELECT ?max_PM10 ?max_NO_2 ?max_O_3
            WHERE {"{"}
            {"{"}
                {"{"}
                    ?sub1 a aqp_classes:PM10 .
                    ?sub1 aqp_properties:hasMaxValue ?max_PM10 .
                    ?sub1 aqp_properties:isFrom aqp_data:{control_station} .
                    ?sub1 aqp_properties:atDate ?date1 .
                    FILTER (?date1 = "{date}"^^xsd:date) .
                {"}"}
                UNION
                {"{"}
                    ?sub2 a aqp_classes:NO2 .
                    ?sub2 aqp_properties:hasMaxValue ?max_N0_2 .
                    ?sub2 aqp_properties:isFrom aqp_data:{control_station} .
                    ?sub2 aqp_properties:atDate ?date2 .
                    FILTER(?date2 = "{date}"^^xsd:date) .
                {"}"}
            {"}"}
            UNION 
            {"{"}
                ?sub3 a aqp_classes:O_3 .
                ?sub3 aqp_properties:hasMaxValue ?max_O_3 .
                ?sub3 aqp_properties:isFrom aqp_data:{control_station} .
                ?sub3 aqp_properties:atDate ?date3 .
                FILTER(?date3 = "{date}"^^xsd:date) .
            {"}"}
        {"}"}
            """

    q = prepareQuery(query, initNs={"aqp_data": AQP_DATA,
                                    "aqp_classes": AQP_CLASSES,
                                    "aqp_properties": AQP_PROPERTIES,
                                    "xsd": XSD})

    for no2, pm10, o3 in g.query(q):
        no2 = no2.toPython() if no2 is not None else None
        pm10 = pm10.toPython() if pm10 is not None else None
        o3 = o3.toPython() if o3 is not None else None

        return no2, pm10, o3

    return None, None, None


if __name__ == "__main__":
    main()
