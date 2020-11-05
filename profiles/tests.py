import json

from django.test import TestCase

from .models import User
from .fixtures_factory import UserFactory


class UserTests(TestCase):
    def setUp(self):
        admin_user = UserFactory(username="admin", phone_number="", is_staff=True, role="ADMIN")
        admin_user.set_password('admin')
        admin_user.save()

        normal_user = UserFactory(username="normal",
                                  phone_number="+201121286973",
                                  is_staff=False,
                                  role="NORMAL")
        normal_user.set_password('normal')
        normal_user.save()

    def _get_access_token(self, username, password):

        response = self.client.post(
            '/api/v1/login/',
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type='application/json',
        )

        return response.json()['access']

    def test_admin_can_create_normal_user(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # create normal user
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                "username": "user1",
                "password": "pass",
                "role": "NORMAL",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(201, response.status_code)
        response = response.json()
        del response['id']
        del response['created']
        del response['modified']
        self.assertEquals({"username": "user1", "role": "NORMAL", "phone_number": None}, response)

        self.assertEquals(3, User.objects.count())

    def test_admin_can_get_users(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # get all users
        response = self.client.get(
            '/api/v1/users/',
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(200, response.status_code)
        response = response.json()

        self.assertEquals(2, User.objects.count())

    def test_normal_fail_create_normal_user(self):

        # get admin access token
        access_token = self._get_access_token("normal", "normal")

        # create normal user
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                "username": "user1",
                "password": "pass",
                "role": "NORMAL",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(403, response.status_code)
        response = response.json()

        self.assertEquals({"detail": "You do not have permission to perform this action."}, response)

    def test_normal_fail_get_users(self):

        # get admin access token
        access_token = self._get_access_token("normal", "normal")

        # get all users
        response = self.client.get(
            '/api/v1/users/',
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(403, response.status_code)
        response = response.json()

        self.assertEquals({"detail": "You do not have permission to perform this action."}, response)
