from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db
from website.models import Client
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    clients = Client.query.all()
    return render_template('home/clients.html', clients=clients)


@views.route('/icons.html')
def icons():
    return render_template('home/icons.html')

@views.route('/client-edit', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        company_name = request.form.get('company-name')
        phone = request.form.get('phone')
        income = request.form.get('income')
        #registration_date = request.form.get('registration-date')

        if len(company_name) < 2:
            flash('A razão social deve ter pelo menos 2 caracteres.', category='error')
        else:
            new_client = Client(company_name=company_name, phone=phone, income=income)
            db.session.add(new_client)
            db.session.commit()
            flash('As informações foram salvas com sucesso.', category='success')
            return redirect(url_for('views.home'))
    
    return render_template('home/client-edit.html')

@views.route('/delete-client', methods=['POST'])
def delete_client():
    client = json.loads(request.data)
    client_id = client['clientId']
    client = Client.query.get(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()
    return jsonify({})