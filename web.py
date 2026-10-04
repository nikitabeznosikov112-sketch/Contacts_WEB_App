from flask import Flask, render_template, request, redirect, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'gugugaga'

DB_CONFIG = {
    'dbname': 'contacts_db',
    'user': 'postgres',
    'password': 'sadcatman123',
    'host': 'localhost',
    'port': '5432',
   
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_contacts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM contacts ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_contact(name, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
    conn.commit()
    conn.close()

def change_contact(contact_id, name, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET name = %s, phone = %s WHERE id = %s", (name, phone, contact_id))
    conn.commit()
    conn.close()

def find_contact(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM contacts WHERE name = %s", (name,))
    founds=cursor.fetchall()
    conn.close()
    return founds
    
@app.route('/')
def index():
    contacts = get_contacts()
    return render_template('contacts.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()

    if name and phone:
        add_contact(name, phone)
        flash('Контакт добавлен!','success')
    else:
        flash('Не все поля заполнены!', 'error')    
    return redirect('/')

@app.route('/delete/<int:contact_id>', methods=['POST'])
def delete(contact_id):
    delete_contact(contact_id)
    flash('Контакт удален', 'success')
    return redirect('/')

@app.route('/edit/<int:contact_id>', methods=['POST'])
def edit_contact(contact_id):
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()

    if name and phone:
        change_contact(contact_id, name, phone)
        flash('Контакт обновлен!', 'success')
    else:
        flash('Не все поля заполнены!', 'error')

    return redirect('/')

@app.route('/edit/<int:contact_id>', methods=['GET'])
def edit_form(contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM contacts WHERE id = %s", (contact_id,))
    contact = cursor.fetchone()
    conn.close

    if not contact:
        return redirect('/')

    return render_template('edit.html', contact=contact)

@app.route('/find', methods=["POST"])
@app.route('/find/', methods=["POST"])
def find_cont():
    name = request.form.get('name', '').strip()

    if not name:
        return redirect('/')
    contacts = find_contact(name)
    return render_template('contacts.html', contacts=contacts)


if __name__ == '__main__':
    app.run(debug=True)


    

