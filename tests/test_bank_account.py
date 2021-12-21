from base import BaseTestCase
from flask import url_for
import json

class BankAccountCRUDTestCase(BaseTestCase):
    
    def test_create_new_bank_account(self):
        response = self.client.post(
            url_for('views.client_details', clientId=1),
            data=dict(
                bank='Bank1',
                agency='0001',
                account='123456',
            ),
            follow_redirects=True
        )
        self.assertIn("As informações foram salvas com sucesso.", response.data.decode())
        self.assertIn('Bank1', response.data.decode())
        self.assertIn('0001', response.data.decode())
        self.assertIn('123456', response.data.decode())

    
    def test_delete_bank_account(self):
        response = self.client.post(
            url_for('views.bank_account_delete'),
            data=json.dumps( dict(bankId=1) ),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual('{}\n', response.data.decode())
    

class BankAccountValidationRulesTestCase(BaseTestCase):

    def test_refuse_create_empty_bank_name(self):
        response = self.client.post(
            url_for('views.client_details', clientId=1),
            data=dict(
                bank='',
                agency='0001',
                account='refuse_empty_bank_name',
            ),
            follow_redirects=True
        )
        self.assertNotIn('refuse_empty_bank_name', response.data.decode())
        self.assertNotEqual('{}\n', response.data.decode())


    def test_refuse_create_empty_agency(self):
        response = self.client.post(
            url_for('views.client_details', clientId=1),
            data=dict(
                bank='bank',
                agency='',
                account='refuse_empty_agency',
            ),
            follow_redirects=True
        )
        self.assertNotIn('refuse_empty_agency', response.data.decode())
        self.assertNotEqual('{}\n', response.data.decode())

    def test_refuse_create_empty_account(self):
        response = self.client.post(
            url_for('views.client_details', clientId=1),
            data=dict(
                bank='bank',
                agency='refuse_empty_account',
                account='',
            ),
            follow_redirects=True
        )
        self.assertNotIn('refuse_empty_account', response.data.decode())
        self.assertNotEqual('{}\n', response.data.decode())