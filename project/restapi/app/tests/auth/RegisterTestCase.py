from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, URLPatternsTestCase

from ...models import CustomUser


class BaseTestClass:
    urlpatterns = [
        path('api/', include('app.urls')),
    ]


class RegisterTest(APITestCase, URLPatternsTestCase, BaseTestClass):
    """
    Class that tests register view
    """

    def test_register_view_creates_user_successfully(self) -> None:
        """
        Tests that POST /register/ creates user
        """
        url = reverse('register')

        response = self.client.post(
            url,
            format='json',
            data={
                "full_name": "user name",
                "email": "user4@user.user",
                "password": "user4"
            })
        user = CustomUser.objects.get(email='user4@user.user')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Checks if request was handled correctly
        self.assertEqual(bool(user), True)  # Checks if user exists in database

    def test_register_view_returns_token(self) -> None:
        """
        Tests that register view returns access token if response code is 201
        """
        url = reverse('register')
        data = {
            "full_name": "user name",
            "email": "user4@user.user",
            "password": "user4"
        }

        response = self.client.post(
            url,
            format='json',
            data=data
        )

        token = response.json()['token']

        self.assertTrue(bool(token))  # Check if token was returned

        token_object = Token.objects.get(key=token)

        self.assertTrue(bool(token_object))  # Check if token exists in database

        user = CustomUser.objects.get(id=token_object.user.id)

        self.assertTrue(bool(user))  # Check if this token belongs to created user
