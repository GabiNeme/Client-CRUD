from flask_testing import TestCase

from website import create_app, db
from website.models import *

class BaseTestCase(TestCase):

    def create_app(self):

        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///test_database.db'
        return app
    
    def setUp(self):
        db.create_all()
        client = Client(name='Cliente teste', phone='05511999999999', income='105281.25')
        db.session.add(client)
        address = Address(street='street', complement='complement', district='district',
                city='city', state='state', postal_code='postal_code', country='country', client_id=client.id)
        
        client.address = address
        db.session.add(address)
        db.session.commit()
        bank_account_1 = BankAccount(client_id=client.id, bank='bank1', agency='0001', account='123456')
        bank_account_2 = BankAccount(client_id=client.id, bank='bank2', agency='0002', account='123456')
        
        db.session.add(bank_account_1)
        db.session.add(bank_account_2)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()