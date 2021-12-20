from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db
from website.models import Address, BankAccount, Client
import json
import locale

views = Blueprint('views', __name__, template_folder='templates')

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
        client = retrieve_client_from_request(request, client)
        address = retrieve_address_from_request(request, client.address)
        db.session.commit()
        return redirect(url_for('views.client_details', clientId=client.id))    
    else:
        return render_template('home/client-edit.html', title="Editar cliente", client=client)


@views.route('/clients/create', methods=['GET', 'POST'])
def client_create():
    if request.method == 'POST':
        client = retrieve_client_from_request(request)
        address = retrieve_address_from_request(request, client.id)
        client.address = address
        db.session.add(client)
        db.session.add(address)
        db.session.commit()
        flash('As informações foram salvas com sucesso.', category='success')
        return redirect(url_for('views.client_details', clientId=client.id))    
    
    return render_template('home/client-edit.html', title="Novo cliente")

@views.route('/clients/delete', methods=['POST'])
def client_delete():
    client = json.loads(request.data)
    client_id = client['clientId']
    client = Client.query.get(client_id)
    address = Address.query.filter_by(client_id=client_id).first()
    if client:
        db.session.delete(client)
        db.session.delete(address)
        db.session.commit()
    return jsonify({})


@views.route('/clients/details/<clientId>', methods=['GET', 'POST'])
def client_details(clientId):
    client = Client.query.get(clientId)  
    if request.method == 'POST':
        bank = request.form.get('bank')
        agency = request.form.get('agency')
        account = request.form.get('account')
        new_bank_account = BankAccount(client_id=client.id, bank=bank, agency=agency, account=account)
        db.session.add(new_bank_account)
        db.session.commit()
        flash('As informações foram salvas com sucesso.', category='success')

    return render_template('home/client-details.html', client=client)


@views.route('/clients/details/deletebankaccount', methods=['POST'])
def bank_account_delete():
    bank = json.loads(request.data)
    bank_id = bank['bankId']
    bank = BankAccount.query.get(bank_id)
    if bank:
        db.session.delete(bank)
        db.session.commit()
    return jsonify({})


@views.app_template_filter()
def currency_format(value):
    return locale.currency(value, grouping=True)


def retrieve_client_from_request(request, client=None):
    company_name = request.form.get('company-name')
    phone = request.form.get('phone')
    income = request.form.get('income')

    if client:
        client.name = company_name
        client.phone = phone
        client.income = income
    else:
        client = Client(name=company_name, phone=phone, income=income)
    return client

def retrieve_address_from_request(request, address=None, client_id=None):
    street = request.form.get('street')
    complement = request.form.get('complement')
    district = request.form.get('district')
    city = request.form.get('city')
    state = request.form.get('state')
    postal_code = request.form.get('postal-code')
    country = request.form.get('country')

    if address:
        address.street = street
        address.complement = complement
        address.district = district
        address.city = city
        address.state = state
        address.postal_code = postal_code
        address.country = country
    else:            
        address = Address(street=street, complement=complement, district=district,
                city=city, state=state, postal_code=postal_code, country=country, client_id=client_id)
    return address