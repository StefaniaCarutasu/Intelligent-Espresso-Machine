from rasputin.__init__ import create_app
from flask_testing import TestCase
import json

username = 'claudia_'
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


class RasputinApiTestCase(TestCase):
    def create_app(self):
        return create_app({'TESTING': True})

    def login(self, username, password):
            return self.client.post('/auth/api/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def make_favorite(self):
        return self.client.get('/profile/api/make-favorite', follow_redirects=True)


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
        res = self.make_favorite()
        json_res = json.loads(res.data.decode())

        assert res.status_code == 200
        assert json_res['status'] == 'Rasputin is working on favorite coffee...'