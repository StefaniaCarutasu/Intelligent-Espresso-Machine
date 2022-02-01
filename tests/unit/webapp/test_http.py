from rasputin.__init__ import create_app
from flask_testing import TestCase

username = 'admin'
email = 'admin@gmail.com'
password = 'admin1234'
confirm_password = 'admin1234'

username_login = 'user'
password_login = 'user1234'

beverage_type = 'Espresso'
roast_type = 'Medium'
syrup = ''
time = '11:15 AM'

program_id = 1

new_username = 'Stefi'
dob = ''

class RasputinTestCase(TestCase):
    def create_app(self):
        return create_app({'TESTING': True})

    def register(self, username, email, password, confirm_password):
        return self.client.post('/auth/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.client.post('/auth/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)

    def program_coffee(self, beverage_type, roast_type, syrup, time):
        return self.client.post('/profile/program', data=dict(
            beverage_type=beverage_type,
            roast_type=roast_type,
            syrup=syrup,
            time=time
        ), follow_redirects=True)

    def coffee_preference(self, beverage_type, roast_type, syrup):
        return self.client.post('/profile/preference', data=dict(
            beverage_type=beverage_type,
            roast_type=roast_type,
            syrup=syrup
        ), follow_redirects=True)

    def delete_program(self, program_id):
        return self.client.post('/profile/delete-programmed-coffee', data=dict(
            id=program_id
        ), follow_redirects=True)

    def edit_profile(self, username, dob):
        return self.client.post('/profile/user-profile', data=dict(
            username=username,
            birth_date=dob
        ), follow_redirects=True)

    def home(self, beverage_type, roast_type, syrup):
        return self.client.post('/', data=dict(
            beverage_type=beverage_type,
            roast_type=roast_type,
            syrup=syrup
        ), follow_redirects=True)


    def test_login(self):
        # get
        res = self.client.get('/auth/login')
        html = res.data.decode()  # html-ul intors

        assert res.status_code == 200
        assert 'Log In' in html

        # post wrong username
        res = self.login(f"{username_login}x", password_login)

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Incorrect username.'

        # post wrong password
        res = self.login(username_login, f"{password_login}x")

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Incorrect password.'

        # post 
        res = self.login(username_login, password_login)
        html = res.data.decode()

        assert res.status_code == 200

    def test_register(self):
        # get
        res = self.client.get('/auth/register')
        html = res.data.decode()  # html-ul intors

        assert res.status_code == 200
        assert 'Join Today' in html

        # post missing username
        res = self.register('', email, password, confirm_password)

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Username is required.'

        # post missing email
        res = self.register(username, "", password, confirm_password)

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Email is required.'

        # post missing password
        res = self.register(username, email, '', confirm_password)

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Password is required.'

        # post missing confirm password
        res = self.register(username, email, password, '')

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Confirmation password is required.'

        # post password and confirm password don't match
        res = self.register(username, email, password, f"{confirm_password}x")

        assert res.status_code == 200
        assert self.get_context_variable('status') == "Password and confirmation password don't match."

        # post
        res = self.register(username, email, password, confirm_password)
        html = res.data.decode()

        assert res.status_code == 200

        # user already exists
        res = self.register(username, email, password, confirm_password)

        assert res.status_code == 200
        assert self.get_context_variable('status') == f"User {username} is already registered."

    def test_logout(self):
        res = self.logout()

        assert res.status_code == 200

    def test_refill_coffee(self):
        self.login(username_login, username_login)

        request = self.client.get('/refill/coffee', follow_redirects=True)
        html = request.data.decode()
        print(html)

        assert request.status_code == 200

    def test_refill_milk(self):
        self.login(username_login, username_login)

        request = self.client.get('/refill/milk', follow_redirects=True)
        html = request.data.decode()
        print(html)

        assert request.status_code == 200

    def test_refill_syrup(self):
        self.login(username_login, username_login)

        request = self.client.get('/refill/syrup', follow_redirects=True)
        html = request.data.decode()
        print(html)

        assert request.status_code == 200

    def test_program(self):
        self.login(username_login, password_login)

        # get
        res = self.client.get('/profile/program')
        html = res.data.decode()  # html-ul intors

        assert res.status_code == 200
        assert 'Coffee options' in html

        # post missing beverage type
        res = self.program_coffee("", roast_type, syrup, time)
        print(res.data.decode())


        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Beverage type is required.'

        # post missing roast type
        res = self.program_coffee(beverage_type, '', syrup, time)

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Roast type is required.'

        # post missing time
        res = self.program_coffee(beverage_type, roast_type, syrup, '')
        assert self.get_context_variable('status') == 'Time is required.'

        assert res.status_code == 200

    def test_preference(self):
        self.login(username_login, password_login)

        # get
        res = self.client.get('/profile/preference')
        html = res.data.decode()  # html-ul intors

        assert res.status_code == 200
        assert 'Coffee options' in html

        # post missing beverage type
        res = self.coffee_preference('', roast_type, syrup)

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Beverage type is required.'

        # post missing roast type
        res = self.coffee_preference(beverage_type, '', syrup)
        assert self.get_context_variable('status') == 'Roast type is required.'

        assert res.status_code == 200

    """
    def test_delete_program(self):
        self.login(username_login, password_login)

        # post
        res = self.delete_program(program_id)

        assert res.status_code == 200
    """

    def test_profile(self):
        self.login(username_login, password_login)

        # get
        res = self.client.get('/profile/user-profile')
        html = res.data.decode()  # html-ul intors

        assert res.status_code == 200
        assert 'Profile' in html

        # post missing username
        res = self.edit_profile('', dob)

        assert res.status_code == 200

        # post

        res = self.edit_profile(new_username, dob)

        assert res.status_code == 200

    def test_home(self):
        # get user not logged in
        res = self.client.get('/')
        html = res.data.decode()  # html-ul intors

        assert res.status_code == 200
        assert 'Coffee options' not in html

        self.login(username_login, password_login)

        # get user logged in
        res = self.client.get('/')
        html = res.data.decode()  # html-ul intors

        assert res.status_code == 200
        assert 'Coffee options' in html


        # post missing beverage type
        res = self.home('', roast_type, syrup)

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Beverage type is required.'

        # post missing roast type
        res = self.coffee_preference(beverage_type, '', syrup)
        assert self.get_context_variable('status') == 'Roast type is required.'

        assert res.status_code == 200



