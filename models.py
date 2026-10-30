import psycopg2
from config import DB_CONFIG

def get_db():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

class Contact:
    def __init__(self, id=None, name=None, phone=None):
        self.id = id
        self.name = name
        self.phone = phone

    @classmethod
    def get_all(cls, db):
        cursor = db.cursor()
        cursor.execute("SELECT id, name, phone FROM contacts ORDER BY name")
        rows = cursor.fetchall()
        cursor.close()
        return [cls(id=row[0], name=row[1], phone=row[2]) for row in rows]

    @classmethod
    def get_by_id (cls, db, contact_id):
        cursor = db.cursor()
        cursor.execute("SELECT id, name, phone FROM contacts WHERE id = %s", (contact_id, ))
        row = cursor.fetchone()
        cursor.close()
        return cls(id=row[0], name=row[1], phone=row[2]) 

    @classmethod
    def find_by_name(cls, db, name):
        cursor = db.cursor()
        cursor.execute("SELECT id, name, phone FROM contacts WHERE name ILIKE %s", (f'%{name}%',))
        rows = cursor.fetchall()
        cursor.close()
        return [cls(id=row[0], name=row[1], phone=row[2]) for row in rows]



    def save(self, db): # ← метод для добавления
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, phone) VALUES (%s, %s) RETURNING id", 
            (self.name, self.phone)
        )
        self.id = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        return self

    def delete(self, db):
        if self.id is None:
            return
        cursor = db.cursor()
        cursor.execute("DELETE FROM contacts WHERE id=%s", (self.id,))
        db.commit()
        cursor.close()

    def __repr__(self):
        return f'<Contact {self.name}: {self.phone}>'
