from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db
from website.models import Address, Client
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('layouts/base.html')


@views.route('/clients')
def clients():
    clients = Client.query.all()
    return render_template('home/clients.html', clients=clients)


@views.route('/icons.html')
def icons():
    return render_template('home/icons.html')

@views.route('/clients/update/<clientId>', methods=['GET', 'POST'])
def client_update(clientId):
    
    client = Client.query.get(clientId)
    if request.method == 'POST':
        company_name = request.form.get('company-name')
        phone = request.form.get('phone')
        income = request.form.get('income')
        #registration_date = request.form.get('registration-date')

        if len(company_name) < 2:
            flash('A razão social deve ter pelo menos 2 caracteres.', category='error')
        else:
            client.name = company_name
            client.phone = phone
            client.income = income
            db.session.commit()
            flash('As informações foram salvas com sucesso.', category='success')
            return redirect(url_for('views.clients'))    
    else:
        return render_template('home/client-edit.html', title="Editar cliente", client=client)


@views.route('/clients/create', methods=['GET', 'POST'])
def client_create():
    if request.method == 'POST':
        company_name = request.form.get('company-name')
        phone = request.form.get('phone')
        income = request.form.get('income')

        street = request.form.get('street')
        complement = request.form.get('complement')
        district = request.form.get('district')
        city = request.form.get('city')
        state = request.form.get('state')
        postal_code = request.form.get('postal-code')
        country = request.form.get('country')

        if len(company_name) < 2:
            flash('A razão social deve ter pelo menos 2 caracteres.', category='error')
        else:
            new_client = Client(name=company_name, phone=phone, income=income)
            new_address = Address(street=street, complement=complement, district=district,
                city=city, state=state, postal_code=postal_code, country=country, client_id=new_client.id)
            new_client.address = new_address
            db.session.add(new_client)
            db.session.add(new_address)
            db.session.commit()
            flash('As informações foram salvas com sucesso.', category='success')
            return redirect(url_for('views.clients'))
    
    return render_template('home/client-edit.html', title="Novo cliente")

@views.route('/clients/delete', methods=['POST'])
def client_delete():
    client = json.loads(request.data)
    client_id = client['clientId']
    client = Client.query.get(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()
    return jsonify({})


@views.route('/clients/details', methods=['GET', 'POST'])
def client_details():
    client = Client.query.get(1)  
    return render_template('home/client-details.html', client=client)