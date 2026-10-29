from models import Contact
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
import os



@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    data = Contact.get_all()
    return templates.TemplateResponse(request=request, name='contacts.html', context={"data": data})

@app.post('/add')
def add(name: str = Form(...), phone: str = Form(...)):

    if name and phone:
        contact=Contact(name=name, phone=phone)
        contact.save()
 
    return RedirectResponse(url='/', status_code=303)

@app.post('/delete/{id}')
def delete(id: int):
    contact = Contact.get_by_id(id)
    if contact:
        contact.delete()
    return RedirectResponse(url='/', status_code = 303)



@app.post('/edit/{id}')
def edit_contact(id: int, name: str = Form(...), phone: str = Form(...)):
    contact = Contact.get_by_id(id)
    
    if not contact:
        return RedirectResponse(url='/', status_code=303)
    
    if name and phone:
        contact.name = name
        contact.phone = phone
        contact.save()

    return RedirectResponse(url='/', status_code=303)

@app.get('/edit/{id}', response_class=HTMLResponse)
def edit_page(request: Request, id: int):
    contact = Contact.get_by_id(id)
    if not contact:
        return RedirectResponse(url='/', status_code=303)
    return templates.TemplateResponse(request=request, name='edit.html', context={"contact": contact})

@app.post('/find', response_class=HTMLResponse)
def find_cont(request: Request, name: str = Form(...)):
    data = Contact.find_by_name(name)
    return templates.TemplateResponse(request=request, name='contacts.html', context={"data": data})

    

