#!/usr/bin/env python
# coding: utf-8

# **Task 06: Modifying RDF(s)**


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS


github_storage = "https://raw.githubusercontent.com/AndreaCimminoArriaga/LinkedData2021-2022/main/Assignment4/"


g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage + "/resources/example5.rdf", format="xml")


# Create a new class named Researcher


ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)
print("------")

# **TASK 6.1: Create a new class named "University"**


ns = Namespace("http://somewhere#")
g.add((ns.University, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s, p, o)
print("------")

# **TASK 6.2: Add "Researcher" as a subclass of "Person"**


g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
for s, p, o in g.triples((None, RDFS.subClassOf, None)):
    print(s, p, o)
print("------")

# **TASK 6.3: Create a new individual of Researcher named "Jane Smith"**


g.add((ns.JaneSmith, ns.Researcher, Literal("Jane Smith")))
for s, p, o in g.triples((None, ns.Researcher, None)):
    print(s, p, o)
print("---6.3---")

# **TASK 6.4: Add to the individual JaneSmith the fullName, given and family names**

vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
g.add((ns.JaneSmith, vcard.FN, Literal('Jane Smith')))
g.add((ns.JaneSmith, vcard.given, Literal('Jane')))
g.add((ns.JaneSmith, vcard.Family, Literal('Smith')))
for s, p, o in g.triples((ns.JaneSmith, None, None)):
    print(s, p, o)

print("------")
# **TASK 6.5: Add UPM as the university where John Smith works**

g.add((ns.JohnSmith, vcard.workIn, ns.UPM))
for s, p, o in g.triples((ns.JohnSmith, None, None)):
    print(s, p, o)

print("------")
