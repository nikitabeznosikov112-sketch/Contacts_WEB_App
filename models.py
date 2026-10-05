import psycopg2
from config import DB_CONFIG

class Contact:
    def __init__(self, id=None, name=None, phone=None):
        self.id = id
        self.name = name
        self.phone = phone

    @staticmethod
    def get_connection():
        return psycopg2.connect(**DB_CONFIG)

    @classmethod
    def get_all(cls):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone FROM contacts ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], phone=row[2]) for row in rows]

    @classmethod
    def get_by_id (cls, contact_id):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone FROM contacts WHERE id = %s", (contact_id, ))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row[0], name=row[1], phone=row[2]) 

    @classmethod
    def find_by_name(cls, name):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone FROM contacts WHERE name ILIKE %s", (f'%{name}%',))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], phone=row[2]) for row in rows]

    def save(self):
        conn =self.get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s) RETURNING id", (self.name, self.phone)) 
            self.id = cursor.fetchone()[0]
        else:
            cursor.execute("UPDATE contacts SET name = %s, phone = %s WHERE id = %s", (self.name, self.phone, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is None:
            return
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id=%s", (self.id,))
        conn.commit()
        conn.close()

    def __repr__(self):
        return f'<Contact {self.name}: {self.phone}>'
