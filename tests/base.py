from flask_testing import TestCase

from src import create_app, db
from src.models import *

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
    

    default_company_name="Company default"
    default_phone="0551133333333"
    default_income="11002525.02"
    default_street="street_default"
    default_complement="complement_default"
    default_district="district_default"
    default_city="city_default"
    default_state="state_default"
    default_postal_code="11111111"
    default_country="country_default"
    default_income_formated="R$ 11.002.525,02"

    def defaultClient(self):
        return dict(
            company_name=self.default_company_name, 
            phone=self.default_phone, 
            income=self.default_income, 
            street=self.default_street, 
            complement=self.default_complement, 
            district=self.default_district, 
            city=self.default_city, 
            state=self.default_state, 
            postal_code=self.default_postal_code, 
            country=self.default_country, 
            )