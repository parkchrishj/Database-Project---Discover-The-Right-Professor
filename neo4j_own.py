from neo4j import GraphDatabase


class MyNeo4jClient:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_top_pub_list(self, faculty_name):
        toppubslist = []
        with self.driver.session(database="academicworld") as session:
            result = session.run("MATCH (n:PUBLICATION)<-[:PUBLISH]-(:FACULTY{name: $name})"
                                 " RETURN n.title, n.numCitations, n.year, n.venue"
                                 " order by n.numCitations desc", name=faculty_name)
            for record in result:
                title, citations, year, venue = record.values()
                toppubslist.append(
                    {'Title': title, 'Citations': citations, 'Year': year, 'Venue': venue})
        return toppubslist
