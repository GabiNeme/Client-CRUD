from datetime import timezone

from sqlalchemy.sql.schema import ForeignKey
from . import db
from sqlalchemy import func

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20))
    company_name = db.Column(db.String(150), unique=True)
    income = db.Column(db.Float)
    registration_date = db.Column(db.DateTime(timezone=False), default = func.now())
    bank_accounts = db.relationship('BankAccount')

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(20))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))