from rasputin.__init__ import create_app
from flask_testing import TestCase

username = 'claudia_maria_7'
password = 'test1234'


class MyViewTestCase(TestCase):
    def create_app(self):
        return create_app({'TESTING': True})

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
        html = res.data.decode()

        assert res.status_code == 200
        assert 'Log In' in html

        # post wrong username
        res = self.login(f"{username}x", password)

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Incorrect username.'

        # post wrong password
        res = self.login(username, f"{password}x")

        assert res.status_code == 200
        assert self.get_context_variable('status') == 'Incorrect password.'

        # post 
        res = self.login(username, password)
        html = res.data.decode()

        assert res.status_code == 200

    def test_logout(self):
        res = self.logout()

        assert res.status_code == 200

    def test_refill_coffee(self):
        self.login(username, password)

        request = self.client.get('/refill/coffee', follow_redirects=True)
        html = request.data.decode()
        print(html)

        assert request.status_code == 200