from base import BaseTestCase
from flask import url_for
import json

class ClientCRUDTestCase(BaseTestCase):

    def test_create_new_client(self):
        response = self.client.post(
            '/clients/create',
            data=self.defaultClient(),
            follow_redirects=True
        )
        self.assertIn(self.default_company_name, response.data.decode())
        self.assertIn(self.default_phone, response.data.decode())
        self.assertIn(self.default_income_formated, response.data.decode())
        response = self.client.get(url_for('views.clients'))
        self.assertIn(self.default_company_name, response.data.decode())

    
    def test_client_income_format(self):
        new_client = self.defaultClient()
        new_client['income'] = '1100200.75'
        response = self.client.post(
            url_for('views.client_create'),
            data=new_client,
            follow_redirects=True
        )
        self.assertIn("R$ 1.100.200,75", response.data.decode())
    
    def test_client_update(self):
        response = self.client.post(
            url_for('views.client_update', clientId=1),
            data=self.defaultClient(),
            follow_redirects=True
        )
        self.assertIn(self.default_company_name, response.data.decode())
        self.assertIn(self.default_phone, response.data.decode())
        self.assertIn(self.default_income_formated, response.data.decode())
        response = self.client.get(url_for('views.clients'))
        self.assertIn(self.default_company_name, response.data.decode())
    
    def test_client_delete(self):
        response = self.client.post(
            url_for('views.client_delete'),
            data=json.dumps( dict(clientId=1) ),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertIn('{}\n', response.data.decode())
        response = self.client.get(url_for('views.clients'))
        self.assertNotIn(self.default_company_name, response.data.decode())
    

class ClientValidationRulesTestCase(BaseTestCase):

    def test_refuse_update_to_empty_company_name(self):
        new_client = self.defaultClient()
        new_client['company_name'] = ''
        response = self.client.post(
            url_for('views.client_update', clientId=1),
            data=new_client,
            follow_redirects=True
        )
        self.assertIn('Editar cliente', response.data.decode())
    
    def test_refuse_update_to_empty_phone(self):
        new_client = self.defaultClient()
        new_client['phone'] = ''
        response = self.client.post(
            url_for('views.client_update', clientId=1),
            data=new_client,
            follow_redirects=True
        )
        self.assertIn('Editar cliente', response.data.decode())
    
    def test_refuse_update_to_empty_income(self):
        new_client = self.defaultClient()
        new_client['income'] = ''
        response = self.client.post(
            url_for('views.client_update', clientId=1),
            data=new_client,
            follow_redirects=True
        )
        self.assertIn('Editar cliente', response.data.decode())
    
    def test_refuse_update_to_negative_income(self):
        new_client = self.defaultClient()
        new_client['income'] = '-150.86'
        response = self.client.post(
            url_for('views.client_update', clientId=1),
            data=new_client,
            follow_redirects=True
        )
        self.assertIn('Editar cliente', response.data.decode())

    def test_refuse_create_empty_company_name(self):
        new_client = self.defaultClient()
        new_client['company_name'] = ''
        response = self.client.post(
            url_for('views.client_create'),
            data=new_client,
            follow_redirects=True
        )
        self.assertIn('Novo cliente', response.data.decode())
    
    def test_refuse_create_empty_phone(self):
        new_client = self.defaultClient()
        new_client['phone'] = ''
        response = self.client.post(
            url_for('views.client_create'),
            data=new_client,
            follow_redirects=True
        )
        self.assertIn('Novo cliente', response.data.decode())
    
    def test_refuse_update_to_empty_income(self):
        new_client = self.defaultClient()
        new_client['income'] = ''
        response = self.client.post(
            url_for('views.client_create'),
            data=new_client,
            follow_redirects=True
        )
        self.assertIn('Novo cliente', response.data.decode())
    
    def test_refuse_update_to_negative_income(self):
        new_client = self.defaultClient()
        new_client['income'] = '-150.86'
        response = self.client.post(
            url_for('views.client_create'),
            data=new_client,
            follow_redirects=True
        )
        self.assertIn('Novo cliente', response.data.decode())