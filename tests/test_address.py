from base import BaseTestCase
from flask import url_for
import json

class AddressCRUDTestCase(BaseTestCase):
    
    def test_create_new_client_address(self):
        response = self.client.post(
            url_for('views.client_create'),
            data=self.defaultClient(),
            follow_redirects=True
        )
        self.assertIn(self.default_street, response.data.decode())
        self.assertIn(self.default_complement, response.data.decode())
        self.assertIn(self.default_district, response.data.decode())
        self.assertIn(self.default_city, response.data.decode())
        self.assertIn(self.default_state, response.data.decode())
        self.assertIn(self.default_postal_code, response.data.decode())
        self.assertIn(self.default_country, response.data.decode())

    
    def test_client_adress_update(self):
        response = self.client.post(
            url_for('views.client_update', clientId=1),
            data=self.defaultClient(),
            follow_redirects=True
        )
        self.assertIn(self.default_street, response.data.decode())
        self.assertIn(self.default_complement, response.data.decode())
        self.assertIn(self.default_district, response.data.decode())
        self.assertIn(self.default_city, response.data.decode())
        self.assertIn(self.default_state, response.data.decode())
        self.assertIn(self.default_postal_code, response.data.decode())
        self.assertIn(self.default_country, response.data.decode())