#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**



from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS


github_storage = "https://raw.githubusercontent.com/AndreaCimminoArriaga/LinkedData2021-2022/main/Assignment4/"


g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage + "/resources/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**


for s, p, o in g.triples((None, RDFS.subClassOf, None)):
    print(s, p, o)


for s, p, o in g.triples((None, None, None)):
    print(s, p, o)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**


from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")


for s, p, o in g.triples((None, RDF.type, None)):
    if ((o, RDFS.subClassOf, ns.Person) in g) or o == ns.Person:
        print(s)


q1 = prepareQuery('''
  SELECT 
    ?subject1
	WHERE { 
    {?subject1 a ns:Person.}
    UNION
    {?x rdfs:subClassOf ns:Person.
     ?subject1 a ?x.}
  } 
  ''',
  initNs = { "rdfs": RDFS, "ns": "http://somewhere#", "rdf": RDF}
)

for q in g.query(q1):
  print(q.subject1)


# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**



from rdflib.plugins.sparql import prepareQuery

for s, p, o in g.triples((None, RDF.type, None)):
    if o == ns.Person or ((o, RDFS.subClassOf, ns.Person) in g):
        for a, b, c in g.triples((s, None, None)):
            print(a, b, c)
            
# SPARQL

q2 = prepareQuery('''
  SELECT 
    ?subject1 ?pred1 ?obj1 ?pred2 ?obj2 
	WHERE { 
    {?subject1 a ns:Person.
     ?subject1 ?pred1 ?obj1. }
    UNION
    {?x rdfs:subClassOf ns:Person.
     ?subject1 a ?x.
     ?subject1 ?pred2 ?obj2}
  } 
  ''',
  initNs = { "rdfs": RDFS, "ns": "http://somewhere#", "rdf": RDF}
)

for q in g.query(q1):
  if not q.obj2:
    print(q.subject1, q.pred1, q.obj1)
    
  else:
    print(q.subject1, q.pred2, q.obj2)

