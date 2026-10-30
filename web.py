from models import Contact, get_db
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")



@app.get('/', response_class=HTMLResponse)
def index(request: Request, db = Depends(get_db)):
    data = Contact.get_all(db)
    return templates.TemplateResponse(request=request, name='contacts.html', context={"data": data})

@app.post('/add')
def add(name: str = Form(...), phone: str = Form(...), db = Depends(get_db)):
    if name and phone:
        contact = Contact(name=name, phone=phone)
        contact.save(db)
    return RedirectResponse(url='/', status_code=303)

@app.post('/delete/{id}')
def delete(id: int, db = Depends(get_db)):
    contact = Contact.get_by_id(db, id)
    if contact:
        contact.delete(db)
    return RedirectResponse(url='/', status_code = 303)



@app.post('/edit/{id}')
def edit_contact(id: int, name: str = Form(...), phone: str = Form(...), db = Depends(get_db)):
    contact = Contact.get_by_id(db, id)
    
    if not contact:
        return RedirectResponse(url='/', status_code=303)
    if name and phone:
        contact.name = name
        contact.phone = phone
        contact.save(db)

    return RedirectResponse(url='/', status_code=303)

@app.get('/edit/{id}', response_class=HTMLResponse)
def edit_page(request: Request, id: int, db = Depends(get_db)):
    contact = Contact.get_by_id(db, id)
    if not contact:
        return RedirectResponse(url='/', status_code=303)
    return templates.TemplateResponse(request=request, name='edit.html', context={"contact": contact})

@app.post('/find', response_class=HTMLResponse)
def find_cont(request: Request, name: str = Form(...), db = Depends(get_db)):
    data = Contact.find_by_name(db, name)
    return templates.TemplateResponse(request=request, name='contacts.html', context={"data": data})

    

