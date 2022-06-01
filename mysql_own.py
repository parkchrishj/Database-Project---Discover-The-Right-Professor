import mysql.connector
import pandas as pd


class MySQLClient:

    def __init__(self):
        self.cnx = mysql.connector.connect(
            user='root', database='academicworld')
        drop_prof = ("DROP INDEX `prof_name` ON faculty;")
        drop_pub = ("DROP INDEX `pub_name` ON publication;")
        # 1. indexing
        create_index_prof = ("CREATE INDEX prof_name ON faculty (id);")
        create_index_pub = ("CREATE INDEX pub_name ON publication (id)")
        cursor = self.cnx.cursor()
        try:
            cursor.execute(create_index_prof)
        except:
            cursor.execute(drop_prof+create_index_prof, multi=True)
        try:
            cursor.execute(create_index_pub)
        except:
            cursor.execute(drop_pub+create_index_pub, multi=True)
        # 2. stored procedure
        test = ("DELIMITER //"
                " CREATE PROCEDURE top_venues(IN faculty_name VARCHAR(50))"
                " BEGIN"
                " select publication.venue, count(*), sum(publication.num_citations) from faculty"
                " join faculty_publication on faculty.id = faculty_publication.faculty_id"
                " join publication on publication.id=faculty_publication.publication_id"
                " where faculty.name=faculty_name"
                " group by publication.venue"
                " order by count(*) desc"
                " END //"
                " DELIMITER ; ")
        drop_procedure = ("DROP PROCEDURE IF EXISTS top_venues;")
        try:
            cursor.execute(test)
        except:
            cursor.execute(drop_procedure+test, multi=True)
        # 3. view
        create_view_faculty_names = ("CREATE VIEW faculty_names AS"
                                     " SELECT name"
                                     " from faculty"
                                     " ORDER BY trim(faculty.name)")
        drop_view_faculty_names = ("DROP VIEW faculty_names")
        try:
            cursor.execute(create_view_faculty_names)
        except:
            cursor.execute(drop_view_faculty_names +
                           create_view_faculty_names, multi=True)
        self.cnx.close()
        self.cnx = mysql.connector.connect(
            user='root', database='academicworld')

    def close(self):
        self.cnx.close()

    def get_faculty_pub_citation_count(self, faculty_name):
        cursor = self.cnx.cursor()
        query = ("select publication.year, count(*), sum(publication.num_citations) from faculty"
                 " join faculty_publication on faculty.id = faculty_publication.faculty_id"
                 " join publication on publication.id=faculty_publication.publication_id"
                 " where faculty.name=%s"
                 " group by publication.year")
        cursor.execute(query, (faculty_name,))

        pubcount = []
        for year, count, citations in cursor:
            pubcount.append(
                {'year': year, 'count': count, 'citations': citations})
        pubcount_df = pd.DataFrame.from_dict(
            sorted(pubcount, key=lambda d: d['year']))
        pubcount_df.columns = [
            'Year', 'Publication Count', 'Number of Citations']
        return pubcount_df

    def get_top_pub_list(self, faculty_name):
        cursor = self.cnx.cursor()
        query = ("select publication.title, publication.num_citations, publication.year, publication.venue from faculty"
                 " join faculty_publication on faculty.id = faculty_publication.faculty_id"
                 " join publication on publication.id=faculty_publication.publication_id"
                 " where faculty.name=%s"
                 " order by publication.num_citations desc")
        cursor.execute(query, (faculty_name,))

        toppubs = {}
        toppubslist = []
        for title, citations, year, venue in cursor:
            toppubs[title] = (citations, year, venue)
            toppubslist.append({'Title': title, 'Citations': citations,
                               'Year': year, 'Venue': venue})
        return toppubslist

    def get_top_venue_list(self, faculty_name):
        cursor = self.cnx.cursor()
        cursor.callproc('top_venues', (faculty_name,))
        topvenues = []
        iter = cursor.stored_results()
        for thing in iter:
            items = thing.fetchall()
            for venue, count, citations in items:
                if venue:
                    topvenues.append(
                        {'Venue': venue, 'Number of Publications': count, 'Number of Citations': citations})
        return topvenues

    def find_all_faculty_names(self):
        cursor = self.cnx.cursor()
        cursor.execute("SELECT * from faculty_names")
        profnames = []
        for faculty in cursor:
            profnames.append(faculty[0])
        return profnames
