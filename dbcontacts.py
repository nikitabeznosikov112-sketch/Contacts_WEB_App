import psycopg2
from config import DB_CONFIG  

conn = psycopg2.connect(
    dbname='postgres',   
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port']
)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute("CREATE DATABASE contacts_db;")
conn.close()


conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL
    )
''')
conn.commit()
conn.close()

print("База и таблица созданы")