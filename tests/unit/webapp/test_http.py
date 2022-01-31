from rasputin.__init__ import create_app
from flask_testing import TestCase

username = 'admin'
email = 'admin@gmail.com'
password = 'admin1234'
confirm_password = 'admin1234'

username_login = 'stefi'
password_login = 'stefi1234'


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
        self.login(username, password)

        request = self.client.get('/refill/coffee', follow_redirects=True)
        html = request.data.decode()
        print(html)

        assert request.status_code == 200

    def test_refill_milk(self):
        self.login(username, password)

        request = self.client.get('/refill/milk', follow_redirects=True)
        html = request.data.decode()
        print(html)

        assert request.status_code == 200

    def test_refill_syrup(self):
        self.login(username, password)

        request = self.client.get('/refill/syrup', follow_redirects=True)
        html = request.data.decode()
        print(html)

        assert request.status_code == 200
