Task6:
* line49, you are asked to add an individual of Researcher for which you used `g.add((ns.JaneSmith, ns.Researcher, Literal("Jane Smith")))`. However this generates the triple `http://somewhere#JaneSmith http://somewhere#Researcher Jane Smith` that is not correct. The solution would be:
	```g.add((ns.JaneSmith, RDF.type, ns.Researcher))
	g.add((ns.JaneSmith, vcard.name, Literal("Jane Smith")))
	 ```
Task7:
* TASK 7.1, warning, you missed the SPARQL query for printing all subclasses of "Person"