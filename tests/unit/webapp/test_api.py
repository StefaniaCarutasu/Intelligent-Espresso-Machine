from rasputin.__init__ import create_app
from flask_testing import TestCase
import json

username = 'admin5'
email = 'admin5@gmail.com'
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

    def test_login(self):
        # post wrong username
        res = self.login(f"{username_login}x", password_login)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Incorrect username.'

        # post wrong password
        res = self.login(username_login, f"{password_login}x")
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Incorrect password.'

        # post 
        res = self.login(username_login, password_login)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Logged in succesfully!'

    def test_make_favorite(self):
        # get
        self.login(username_login, password_login)

        """
        res = self.make_favorite()
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == "Favourite coffee doesn't exist."
        """

        self.coffee_preference(beverage_type, roast_type, syrup)

        res = self.make_favorite()
        json_res = json.loads(res.data.decode())

        assert json_res['status'] == 'Rasputin is working on favorite coffee...'
        assert res.status_code == 200
        assert json_res['status'] == 'Rasputin is working on favorite coffee...'

    def test_register(self):
        # post missing username
        res = self.register('', email, password, confirm_password)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Username is required.'

        # post missing email
        res = self.register(username, "", password, confirm_password)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Email is required.'

        # post missing password
        res = self.register(username, email, '', confirm_password)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Password is required.'

        # post missing confirm password
        res = self.register(username, email, password, '')
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Confirmation password is required.'

        # post password and confirm password don't match
        res = self.register(username, email, password, f"{confirm_password}x")
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == "Password and confirmation password don't match."

        # post
        res = self.register(username, email, password, confirm_password)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Account created succesfully!'

        # user already exists
        res = self.register(username, email, password, confirm_password)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == f"User {username} is already registered."

    def test_logout(self):
        res = self.logout()
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Logged out successfully!'

    def test_refill_coffee(self):
        res = self.login(username_login, password_login)

        res = self.client.get('/refill/api/coffee', follow_redirects=True)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Rasputin is now full on coffee.'
        assert json_res['data']['coffee_quantity'] == 1000

    def test_refill_milk(self):
        self.login(username_login, password_login)

        res = self.client.get('/refill/api/milk', follow_redirects=True)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Rasputin is now full on milk.'
        assert json_res['data']['milk_quantity'] == 1000


    def test_refill_syrup(self):
        self.login(username_login, password_login)

        res = self.client.get('/refill/api/syrup', follow_redirects=True)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Rasputin is now full on syrup.'
        assert json_res['data']['syrup_quantity'] == 100

    def test_program(self):
        self.login(username_login, password_login)

        # post missing beverage type
        res = self.program_coffee('', roast_type, syrup, time)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Beverage type is required.'

        # post missing roast type
        res = self.program_coffee(beverage_type, '', syrup, time)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Roast type is required.'

        # post missing time
        res = self.program_coffee(beverage_type, roast_type, syrup, '')
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Time is required.'

        # post
        res = self.program_coffee(beverage_type, roast_type, syrup, time)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Preprogrammed coffee has been successfully saved!'

        assert json_res['data']['beverage_type'] == str(beverage_type)
        assert json_res['data']['username'] == username_login
        assert json_res['data']['roast_type'] == roast_type
        assert json_res['data']['time'] == time

    def test_preference(self):
        self.login(username_login, password_login)

        # post missing beverage type
        res = self.coffee_preference('', roast_type, syrup)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Beverage type is required.'

        # post missing roast type
        res = self.coffee_preference(beverage_type, '', syrup)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Roast type is required.'

        # post
        res = self.coffee_preference(beverage_type, roast_type, syrup)
        json_res = json.loads(res.data.decode())

        assert json_res['status'] == 'Preference list updated successfully!'

        assert res.status_code == 200
        assert json_res['data']['username'] == username_login
        assert json_res['data']['beverage_type'] == str(beverage_type)
        assert json_res['data']['roast_type'] == roast_type

    """
    def test_delete_program(self):
        self.login(username_login, password_login)

        # post
        res = self.delete_program(program_id)

        assert res.status_code == 200
    """

    def test_profile(self):
        self.login(username_login, password_login)

        # post missing username
        res = self.edit_profile('', dob)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Username required.'

        # post
        res = self.edit_profile(new_username, dob)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'User profile updated successfully'
        assert json_res['data']['username'] == new_username
        assert json_res['data']['birth_date'] == (None if not dob else dob)

        self.edit_profile(username_login, dob)

    def test_home(self):
        self.login(username_login, password_login)
        
        # post missing beverage type
        res = self.home('', roast_type, syrup)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Beverage type is required.'

        # post missing roast type
        res = self.home(beverage_type, '', syrup)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Roast type is required.'

        # post
        res = self.home(1, roast_type, syrup)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Rasputin is working on your coffee...'


    def test_start_coffee(self):
        self.login(username_login, password_login)

        # post missing beverage type
        res = self.start_coffee('', roast_type, syrup)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Beverage type is required.'

        # post missing roast type
        res = self.start_coffee(beverage_type, '', syrup)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 403
        assert json_res['status'] == 'Roast type is required.'

        # post
        res = self.start_coffee(1, roast_type, syrup)
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Rasputin is working on your coffee...'
