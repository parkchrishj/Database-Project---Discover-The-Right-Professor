from pymongo import MongoClient
from random import randint


class MyMongoClient:

    def __init__(self):
        self.client = MongoClient(port=27017)

    def close(self):
        self.client.close()

    def find_all_faculty_names(self):
        with self.client as client:
            db = client.academicworld
            cursor = db.faculty.find({}, {"name": 1}).limit(300).sort("name")
            profnames = []
            for document in cursor:
                if 'name' in document:
                    profnames.append(document['name'])
        return profnames

    def update_output(self, n_clicks, dropdown, note):
        m_db = self.client.academicworld
        cursor = m_db.Notes.find()
        noteslist = []
        for document in cursor:
            noteslist.append(document)
        return noteslist

    def insert_note(self, dropdown, note):
        m_db = self.client.academicworld
        notes_db = m_db.Notes
        cursor = notes_db.find({}, {"name": 1})
        exist = []
        for document in cursor:
            exist.append(document['name'])
        if dropdown in exist:
            notes_db.update_one({'name': dropdown}, {"$set": {"note": note}})
        else:
            new_note = {
                "name": f"{dropdown}",
                "note": f"{note}"
            }
            notes_db.insert_one(new_note)

    def delete_note(self, dropdown):
        m_db = self.client.academicworld
        notes_db = m_db.Notes
        notes_db.delete_one({"name": dropdown})

    def get_notes(self):
        m_db = self.client.academicworld
        notes_db = m_db.Notes
        notes = []
        for document in notes_db.find({}, {"name": 1, "note": 1}):
            notes.append({'Name': document['name'], 'Notes': document['note']})
        return notes

    def update_output9(self, n_clicks, dropdown, note):
        m_db = self.client.academicworld
        cursor = m_db.favs.find()
        noteslist = []
        for document in cursor:
            noteslist.append(document)
        return noteslist

    def insert_fav(self, dropdown, note):
        m_db = self.client.academicworld
        favs_db = m_db.favs
        cursor = favs_db.find({}, {"name": 1})
        exist = []
        for document in cursor:
            exist.append(document['name'])
        print(exist, dropdown, note)
        if dropdown in exist:
            favs_db.update_one({'name': dropdown}, {"$set": {"note": note}})
        else:
            new_fav = {
                "name": f"{dropdown}",
                "note": f"{note}"
            }
            favs_db.insert_one(new_fav)

    def delete_fav(self, dropdown):
        m_db = self.client.academicworld
        favs_db = m_db.favs
        favs_db.delete_one({"name": dropdown})

    def get_favs(self):
        m_db = self.client.academicworld
        favs_db = m_db.favs
        favs = []
        for document in favs_db.find({}, {"name": 1, "note": 1}):
            favs.append({'Name': document['name'], 'Notes': document['note']})
        return favs
