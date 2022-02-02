from rasputin.__init__ import create_app
from flask_testing import TestCase
import json

username = 'admina2'
email = 'admina2@gmail.com'
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

    def test_auth(self):
        # post register
        res = self.register(username, email, password, confirm_password)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Account created succesfully!'

        # post login
        res = self.login(username, password)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Logged in succesfully!'

        # post logout
        res = self.logout()
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Logged out successfully!'

    def test_make_coffee(self):
        # post login
        res = self.login(username_login, password_login)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Logged in succesfully!'

        # post make coffee
        res = self.start_coffee(1, roast_type, syrup)
        json_res = json.loads(res.data.decode())

        while res.status_code == 200:
            res = self.start_coffee(1, roast_type, syrup)
            json_res = json.loads(res.data.decode())

        assert (json_res['status'] == 'Please, refill the machine with coffee. Is running low.') or \
               (json_res['status'] == "Please, refill the machine with milk. Is running low.") or \
               (json_res['status'] == 'Please, refill the machine with syrup. Is running low.')

        res = self.client.get('/refill/api/coffee', follow_redirects=True)
        assert res.status_code == 200

        res = self.client.get('/refill/api/milk', follow_redirects=True)
        assert res.status_code == 200

        res = self.client.get('/refill/api/syrup', follow_redirects=True)
        assert res.status_code == 200

    def test_edit_profile(self):
        # post login
        res = self.login(username_login, password_login)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Logged in succesfully!'

        # post edit username
        res = self.edit_profile(new_username, dob)
        json_res = json.loads(res.data.decode())

        assert json_res['status'] == 'User profile updated successfully'
        assert res.status_code == 200

        self.edit_profile(username_login, dob)

        # post set preference
        res = self.coffee_preference(beverage_type, roast_type, syrup)
        json_res = json.loads(res.data.decode())

        assert json_res['status'] == 'Preference list updated successfully!'

        # post set programmed coffee
        res = self.program_coffee(beverage_type, roast_type, syrup, time)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Preprogrammed coffee has been successfully saved!'






