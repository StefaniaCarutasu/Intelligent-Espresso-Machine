from rasputin.__init__ import create_app
from flask_testing import TestCase
import json

username = 'admin3'
email = 'admin3@gmail.com'
password = 'admin1234'
confirm_password = 'admin1234'

username_login = 'user'
password_login = 'user1234'

beverage_type = 1
roast_type = 'Medium'
syrup = ''
time = '11:15 AM'

program_id = 1

new_username = 'Stefi'
dob = ''


class RasputinApiTestCase(TestCase):
    def create_app(self):
        return create_app({'TESTING': True})

    def register(self, username, email, password, confirm_password):
        return self.client.post('/auth/api/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.client.post('/auth/api/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/api/logout', follow_redirects=True)

    def program_coffee(self, beverage_type, roast_type, syrup, time):
        return self.client.post('/profile/api/program', data=dict(
            beverage_type=beverage_type,
            roast_type=roast_type,
            syrup=syrup,
            time=time
        ), follow_redirects=True)

    def coffee_preference(self, beverage_type, roast_type, syrup):
        return self.client.post('/profile/api/preference', data=dict(
            beverage_type=beverage_type,
            roast_type=roast_type,
            syrup=syrup
        ), follow_redirects=True)

    def delete_program(self, program_id):
        return self.client.post('/profile/api/delete-programmed-coffee', data=dict(
            id=program_id
        ), follow_redirects=True)

    def edit_profile(self, username, dob):
        return self.client.post('/profile/api/user-profile', data=dict(
            username=username,
            birth_date=dob
        ), follow_redirects=True)

    def home(self, beverage_type, roast_type, syrup):
        return self.client.post('/api', data=dict(
            beverage_type=beverage_type,
            roast_type=roast_type,
            syrup=syrup
        ), follow_redirects=True)

    def make_favorite(self):
        return self.client.get('/profile/api/make-favorite', follow_redirects=True)

    def start_coffee(self, beverage_type, roast_type, syrup):
        return self.client.post('/api/start_coffee', data=dict(
            beverage_type=beverage_type,
            roast_type=roast_type,
            syrup=syrup
        ), follow_redirects=True)


    def test_1(self):
        assert 1 == 1