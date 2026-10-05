from flask import Flask, render_template, request, redirect, flash
from models import Contact
app = Flask(__name__)
app.secret_key = 'gugugaga'


@app.route('/')
def index():
    contacts = Contact.get_all()
    return render_template('contacts.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()

    if name and phone:
        contact=Contact(name=name, phone=phone)
        contact.save()
        flash('Контакт добавлен!','success')
    else:
        flash('Не все поля заполнены!', 'error')    
    return redirect('/')

@app.route('/delete/<int:contact_id>', methods=['POST'])
def delete(contact_id):
    contact = Contact.get_by_id(contact_id)
    if contact:
        contact.delete()
        flash('Контакт удален', 'success')
    return redirect('/')

@app.route('/edit/<int:contact_id>', methods=['GET'])
def edit_form(contact_id):
    contact = Contact.get_by_id(contact_id)
    
    if not contact:
        return redirect('/')
    
    return render_template('edit.html', contact=contact)


@app.route('/edit/<int:contact_id>', methods=['POST'])
def edit_contact(contact_id):
    contact = Contact.get_by_id(contact_id)
    
    if not contact:
        return redirect('/')
    
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    
    if name and phone:
        contact.name = name
        contact.phone = phone
        contact.save()
        flash('Контакт обновлён!', 'success')
    else:
        flash('Заполни все поля!', 'error')
    
    return redirect('/')


@app.route('/find', methods=["POST"])
@app.route('/find/', methods=["POST"])
def find_cont():
    name = request.form.get('name', '').strip()
    contacts = Contact.find_by_name(name)
    return render_template('contacts.html', contacts=contacts)


if __name__ == '__main__':
    app.run(debug=True)


    

