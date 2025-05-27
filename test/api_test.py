"""
Written by Felipe Rey
"""
import random

import requests
import unittest
import os


class TestAPIClient:
    BASE_URL = 'http://localhost:8000'

    def create_lead(self, first_name, last_name, email, cv_file_path):
        """
        Submit lead form data to the endpoint
        """
        url = f"{self.BASE_URL}/leads/"
        # Prepare form data
        data = {
            'f_name': first_name,
            'l_name': last_name,
            'email': email
        }

        # Prepare file
        with open(cv_file_path, 'rb') as cv_file:
            files = {'cv': cv_file}

            response = requests.post(url, data=data, files=files)
            response.raise_for_status()

    def update_lead(self, jwt, lead_id, state):
        """
        Update lead status
        """
        url = f"{self.BASE_URL}/internal/leads/{lead_id}"
        payload = {"state": state}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {jwt}"
        }
        response = requests.patch(url, json=payload, headers=headers)
        response.raise_for_status()

    def list_lead(self, jwt, email=None, f_name=None, l_name=None, state=None):
        """
        List lead status
        """
        url = f"{self.BASE_URL}/internal/leads"
        qs = {}
        if email:
            qs['email'] = email
        if f_name:
            qs['f_name'] = f_name
        if l_name:
            qs['l_name'] = l_name
        if state:
            qs['state'] = state

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {jwt}"
        }

        response = requests.get(url, headers=headers, params=qs)
        response.raise_for_status()
        return response.json()

    def download_cv(self, jwt, lead_id, output_filename="downloaded_cv.pdf"):
        """
        Download CV for a specific lead
        """
        url = f"{self.BASE_URL}/internal/leads/{lead_id}/cv-download"
        headers = {
            "Authorization": f"Bearer {jwt}"
        }

        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        # Write the content to file
        with open(output_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


    def register_user(self, username, password):
        """
        Register a new user
        """
        url = f"{self.BASE_URL}/internal/auth/register"

        payload = {
            "username": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

    def login(self, username, password):
        """
        Login a user
        """
        url = f"{self.BASE_URL}/internal/auth/login"

        payload = {
            "username": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()



class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestAPIClient()
        with open("test_resume.pdf", "wb") as f:
            f.write(b"%PDF-1.4 ...content...")  # Dummy PDF content

    def tearDown(self):
        for f in ['test_resume.pdf', 'downloaded_cv.pdf']:
            if os.path.exists(f):
                os.remove(f)

    def test_flow(self):
        """should test create lead, register new user, login, list leads, update lead
        and download cv"""
        # create leads
        n_leads = 10
        email = f'test-{random.randint(1, 1<<20)}@example.com'
        for i in range(n_leads):
            self.client.create_lead(
                first_name=f'John_{n_leads}', last_name=f'Doe_{n_leads}',
                email=email, cv_file_path='test_resume.pdf')
        # register User
        username = f'testuser-{random.randint(1, 1<<20)}'
        password = 'testpassword'
        self.client.register_user(username, password)
        # Login
        jwt = self.client.login(username, password)['access_token']
        # List leads
        leads = self.client.list_lead(jwt, email=email, state='PENDING')
        assert len(leads) == n_leads
        # Update lead
        lead_id = leads[-1]['id']
        self.client.update_lead(jwt, lead_id, 'REACHED_OUT')
        leads = self.client.list_lead(jwt, email=email, state='PENDING')
        assert len(leads) == n_leads -1
        # Download CV
        self.client.download_cv(jwt, lead_id)
