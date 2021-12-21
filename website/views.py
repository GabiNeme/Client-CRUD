from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db
from website.models import Address, BankAccount, Client
import json
import locale

views = Blueprint('views', __name__, template_folder='templates')

@views.route('/')
def home():
    return render_template('home/home.html', segment="home")


@views.route('/clients')
def clients():
    clients = Client.query.all()
    return render_template('home/clients.html', clients=clients)


@views.route('/icons.html')
def icons():
    return render_template('home/page-404.html')

@views.route('/clients/update/<clientId>', methods=['GET', 'POST'])
def client_update(clientId):
    client = Client.query.get(clientId)
    if not client:
        return render_template('home/page-404.html') 

    if request.method == 'POST':
        passed_validation, message = check_client_validation_rules(request)

        if  passed_validation:
            client = retrieve_client_from_request(request, client)
            address = retrieve_address_from_request(request, client.address)
            db.session.commit()
            return redirect(url_for('views.client_details', clientId=client.id))    
        else: 
            flash(message, category='error')

    return render_template('home/client-edit.html', title="Editar cliente", client=client)


@views.route('/clients/create', methods=['GET', 'POST'])
def client_create():
    if request.method == 'POST':        
        passed_validation, message = check_client_validation_rules(request)

        if passed_validation:
            client = retrieve_client_from_request(request)
            address = retrieve_address_from_request(request, client.id)
            client.address = address
            db.session.add(client)
            db.session.add(address)
            db.session.commit()
            return redirect(url_for('views.client_details', clientId=client.id))    
        else: 
            flash(message, category='error')
    return render_template('home/client-edit.html', title="Novo cliente")

@views.route('/clients/delete', methods=['POST'])
def client_delete():
    client = json.loads(request.data)
    client_id = client['clientId']
    if client:
        db.session.query(BankAccount).filter(BankAccount.client_id==client_id).delete()
        db.session.query(Address).filter(Address.client_id==client_id).delete()
        db.session.query(Client).filter(Client.id==client_id).delete()
        db.session.commit()
        flash('O cliente foi apagado com sucesso.', category='success')

    return jsonify({})


@views.route('/clients/details/<clientId>', methods=['GET', 'POST'])
def client_details(clientId):
    client = Client.query.get(clientId)
    if not client:
        return render_template('home/page-404.html') 

    if request.method == 'POST':
        passed_validation, message = check_bank_account_validation_rules(request)

        if passed_validation:

            bank = request.form.get('bank')
            agency = request.form.get('agency')
            account = request.form.get('account')
            new_bank_account = BankAccount(client_id=client.id, bank=bank, agency=agency, account=account)
            db.session.add(new_bank_account)
            db.session.commit()
            flash('As informações foram salvas com sucesso.', category='success')
        else:
            flash(message, category='error')

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
    company_name = request.form.get('company_name')
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
    postal_code = request.form.get('postal_code')
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

def check_client_validation_rules(request):
    company_name = request.form.get('company_name')
    phone = request.form.get('phone')
    income = request.form.get('income')

    if len(company_name) < 2:
        return False, 'A razão social da empresa deve ter pelo menos 2 caracteres.'
    elif len(phone) < 8:
        return False, 'O telefone deve ter pelo menos 8 dígitos.'
    elif len(income) < 1:
        return False, 'O preenchimento do faturamento é obrigatório.'
    elif not is_float(income):
        return False, 'O faturamento deve ser um número.'
    elif float(income) < 0:
        return False, 'O faturamento deve ser maior que zero.'
    return True, ''

def is_float(value_string):
    try:
        float(value_string)
    except ValueError:
        return False
    return True

def check_bank_account_validation_rules(request):
    bank = request.form.get('bank')
    agency = request.form.get('agency')
    account = request.form.get('account')

    if len(bank) < 2:
        return False, 'O nome do banco deve ter pelo menos 2 caracteres.'
    elif len(agency) < 1:
        return False, 'O preenchimento da agência é obrigatório.'
    elif len(account) < 1:
        return False, 'O preenchimento da conta é obrigatório.'
    return True, ''