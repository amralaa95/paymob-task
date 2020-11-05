import json

from django.test import TestCase
from .models import Promo, DeductPromo
from .fixtures_factory import PromoFactory
from profiles.fixtures_factory import UserFactory


class PromoTests(TestCase):
    def setUp(self):
        self.admin_user = UserFactory(username="admin", phone_number="", is_staff=True, role="ADMIN")
        self.admin_user.set_password('admin')
        self.admin_user.save()

        self.normal_user1 = UserFactory(username="normal1",
                                        phone_number="+201011286913",
                                        is_staff=False,
                                        role="NORMAL")
        self.normal_user1.set_password('normal')
        self.normal_user1.save()

        self.normal_user2 = UserFactory(username="normal2",
                                        phone_number="+201231286970",
                                        is_staff=False,
                                        role="NORMAL")
        self.normal_user2.set_password('normal')
        self.normal_user2.save()

        self.promo1 = PromoFactory(user=self.normal_user1,
                                   promo_amount=10,
                                   start_time="2020-11-04T08:30:00Z",
                                   end_time="2020-11-30T08:30:00Z")
        self.promo1.save()

        self.promo2 = PromoFactory(user=self.normal_user2,
                              promo_amount=23,
                              start_time="2020-11-04T08:30:00Z",
                              end_time="2020-11-30T08:30:00Z")
        self.promo2.save()
        DeductPromo.objects.create(promo=self.promo2, amount=9)

        self.promo3 = PromoFactory(user=self.normal_user1,
                                   promo_amount=14,
                                   start_time="2020-11-04T08:30:00Z",
                                   end_time="2020-11-30T08:30:00Z")
        self.promo3.save()

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

    def test_admin_can_create_promo_normal_user(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # create promo for normal user
        response = self.client.post(
            '/api/v1/promos/',
            data=json.dumps({
                "user": self.normal_user1.id,
                "promo_type": "string",
                "promo_amount": 3,
                "is_active": True,
                "description": "string",
                "start_time": "2020-11-04T08:30:00Z",
                "end_time": "2020-11-30T08:30:00Z"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(201, response.status_code)
        response = response.json()
        del response['id']
        del response['created']
        del response['modified']
        del response['promo_code']
        self.assertEquals(
            {
                "promo_type": "string",
                "promo_amount": 3,
                "is_active": True,
                "description": "string",
                "start_time": "2020-11-04T08:30:00Z",
                "end_time": "2020-11-30T08:30:00Z",
                "user": self.normal_user1.id
            }, response)

        self.assertEquals(4, Promo.objects.count())

    def test_admin_fail_create_promo_admin_user(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # create promo for admin user
        response = self.client.post(
            '/api/v1/promos/',
            data=json.dumps({
                "user": self.admin_user.id,
                "promo_type": "string",
                "promo_amount": 3,
                "is_active": True,
                "description": "string",
                "start_time": "2020-11-04T08:30:00Z",
                "end_time": "2020-11-30T08:30:00Z"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(406, response.status_code)
        response = response.json()

        self.assertEquals({"detail": "Can't assign promo code for admin user"}, response)

    def test_normal_fail_create_promo(self):

        # get admin access token
        access_token = self._get_access_token("normal1", "normal")

        # create promo
        response = self.client.post(
            '/api/v1/promos/',
            data=json.dumps({
                "user": self.normal_user1.id,
                "promo_type": "string",
                "promo_amount": 3,
                "is_active": True,
                "description": "string",
                "start_time": "2020-11-04T08:30:00Z",
                "end_time": "2020-11-30T08:30:00Z"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(403, response.status_code)
        response = response.json()

        self.assertEquals({"detail": "You do not have permission to perform this action."}, response)

    def test_admin_can_get_all_promos(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # get all promos
        response = self.client.get(
            '/api/v1/promos/',
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(200, response.status_code)
        response = response.json()

        self.assertEquals(3, Promo.objects.count())

    def test_normal_get_promos(self):

        # get admin access token
        access_token = self._get_access_token("normal1", "normal")

        # get user's promos
        response = self.client.get(
            '/api/v1/promos/',
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(200, response.status_code)
        response = response.json()

        self.assertEquals(2, len(response))

    def test_admin_can_update_promo(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # update promo
        response = self.client.patch(
            f'/api/v1/promos/{self.promo1.id}/',
            data=json.dumps({
                "user": self.normal_user1.id,
                "promo_type": "string",
                "promo_amount": 30,
                "is_active": False,
                "description": "string",
                "start_time": "2020-11-04T08:30:00Z",
                "end_time": "2020-12-30T08:30:00Z"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(200, response.status_code)
        response = response.json()
        del response['id']
        del response['created']
        del response['modified']
        del response['promo_code']
        self.assertEquals(
            {
                "promo_type": "string",
                "promo_amount": 30,
                "is_active": False,
                "description": "string",
                "start_time": "2020-11-04T08:30:00Z",
                "end_time": "2020-12-30T08:30:00Z",
                "user": self.normal_user1.id
            }, response)

    def test_normal_fail_update_promo(self):

        # get admin access token
        access_token = self._get_access_token("normal1", "normal")

        # update promo
        response = self.client.patch(
            f'/api/v1/promos/{self.promo1.id}/',
            data=json.dumps({
                "user": self.normal_user1.id,
                "promo_type": "string",
                "promo_amount": 3,
                "is_active": True,
                "description": "string",
                "start_time": "2020-11-04T08:30:00Z",
                "end_time": "2020-11-30T08:30:00Z"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(403, response.status_code)
        response = response.json()

        self.assertEquals({"detail": "You do not have permission to perform this action."}, response)


    def test_admin_fail_update_user_for_used_promo(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # update promo
        response = self.client.patch(
            f'/api/v1/promos/{self.promo2.id}/',
            data=json.dumps({
                "user": self.normal_user1.id,
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(406, response.status_code)
        response = response.json()

        self.assertEquals({"detail": "Can't change the user, this promo was used."}, response)

    def test_admin_can_delete_promo(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # delete promo
        response = self.client.delete(
            f'/api/v1/promos/{self.promo1.id}/',
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(204, response.status_code)
        self.assertEquals(2, Promo.objects.count())

    def test_normal_fail_delete_promo(self):

        # get admin access token
        access_token = self._get_access_token("normal1", "normal")

        # delete promo
        response = self.client.delete(
            f'/api/v1/promos/{self.promo1.id}/',
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(403, response.status_code)
        response = response.json()

        self.assertEquals({"detail": "You do not have permission to perform this action."}, response)

    def test_normal_can_get_promo_points(self):

        # get admin access token
        access_token = self._get_access_token("normal1", "normal")

        # get promo points
        response = self.client.get(
            f'/api/v1/points/get_points/{self.promo1.id}/',
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(200, response.status_code)
        response = response.json()
        self.assertEquals({
            'remaining_points': 10,
            'active': True,
            'promo_code': self.promo1.promo_code
        }, response)

    def test_admin_fail_get_promo_points(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # get promo points
        response = self.client.get(
            f'/api/v1/points/get_points/{self.promo1.id}/',
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(403, response.status_code)
        response = response.json()

        self.assertEquals({"detail": "You do not have permission to perform this action."}, response)

    def test_normal_can_use_promo_points(self):

        # get admin access token
        access_token = self._get_access_token("normal1", "normal")

        # use promo points
        response = self.client.post(
            f'/api/v1/points/use_promo/',
            data=json.dumps({
                "promo_code": self.promo1.promo_code,
                "amount": 3,
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(200, response.status_code)
        response = response.json()
        self.assertEquals({'success': f'Deducted from {self.promo1.promo_code} with amount 3'}, response)

        # try to dedcuct more than remaining
        response = self.client.post(
            f'/api/v1/points/use_promo/',
            data=json.dumps({
                "promo_code": self.promo1.promo_code,
                "amount": 8,
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEquals(400, response.status_code)
        response = response.json()
        self.assertEquals({'error': 'Amount should be less than or equal remaining amount'}, response)

    def test_normal_can_use_promo_points_without_promo_code(self):

        # get admin access token
        access_token = self._get_access_token("normal1", "normal")

        # use promo points
        response = self.client.post(
            f'/api/v1/points/use_promo/',
            data=json.dumps({
                "amount": 5,
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(200, response.status_code)
        response = response.json()
        self.assertEquals({'success': f'Deducted from {self.promo1.promo_code} with amount 5'}, response)

        # try to dedcuct more than remaining
        response = self.client.post(
            f'/api/v1/points/use_promo/',
            data=json.dumps({
                "amount": 8,
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEquals(200, response.status_code)
        response = response.json()
        self.assertEquals({'success': f'Deducted from {self.promo3.promo_code} with amount 8'}, response)

        # try to dedcuct more than remaining of all promos
        response = self.client.post(
            f'/api/v1/points/use_promo/',
            data=json.dumps({
                "amount": 10,
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEquals(400, response.status_code)
        response = response.json()
        self.assertEquals({'error': "There's no Promo code is avilable"}, response)

    def test_admin_fail_use_promo_points(self):

        # get admin access token
        access_token = self._get_access_token("admin", "admin")

        # use promo points
        response = self.client.post(
            f'/api/v1/points/use_promo/',
            data=json.dumps({
                "amount": 3,
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEquals(403, response.status_code)
        response = response.json()

        self.assertEquals({"detail": "You do not have permission to perform this action."}, response)
