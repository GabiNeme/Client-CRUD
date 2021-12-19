from datetime import timezone
from sqlalchemy.orm import backref

from sqlalchemy.sql.schema import ForeignKey
from . import db
from sqlalchemy import func

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20))
    name = db.Column(db.String(150))
    income = db.Column(db.Float)
    registration_date = db.Column(db.Date(), default = func.now())
    address = db.relationship("Address", uselist=False, backref="client")
    bank_accounts = db.relationship('BankAccount')

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    street = db.Column(db.String(150))
    complement = db.Column(db.String(50))
    district = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    country = db.Column(db.String(50))

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(20))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))