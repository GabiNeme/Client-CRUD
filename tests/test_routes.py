import unittest
from flask import url_for
from base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    def test_flask_set_up_correctly(self):
        response = self.client.get(url_for('views.home'))
        self.assertEqual(response.status_code, 200)

    def test_clients_page_loads(self):
        response = self.client.get('/clients')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Clientes' in response.data)
        self.assertTrue(b'Nossos clientes' in response.data)
    
    def test_client_details_page_loads(self):
        response = self.client.get(url_for('views.client_details', clientId=1))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Cliente teste' in response.data)
    
    def test_update_client_page_loads(self):
        response = self.client.get(url_for('views.client_update', clientId=1))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Editar cliente' in response.data)
        self.assertTrue(b'Cliente teste' in response.data)

    def test_create_client_page_loads(self):
        response = self.client.get(url_for('views.client_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Novo cliente' in response.data)