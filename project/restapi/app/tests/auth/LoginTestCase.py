from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, URLPatternsTestCase

from ...models import CustomUser


class BaseTestClass:
    urlpatterns = [
        path('api/', include('app.urls')),
    ]


class LoginTest(APITestCase, URLPatternsTestCase, BaseTestClass):
    """
    Class that tests login view
    """

    def setUp(self) -> None:
        user_credentials = {
            "username": "user name",
            "email": "user4@user.user",
            "password": "user4"
        }
        user = CustomUser.objects.create_user(**user_credentials)
        url = reverse('login')
        response = self.client.post(
            url,
            format='json',
            data={
                "email": user_credentials['username'],
                "password": user_credentials['password']
            }
        )
        self.response = response
        self.user = user

    def test_login_function_works(self) -> None:
        """
        Tests login view works correctly if correct data was passed in request body
        """
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)  # Checks if request was correctly handled

    def test_login_returns_correct_access_token(self) -> None:
        """
        Tests that POST /login/ returns correct access token if response status code is 201
        """
        token = self.response.json()['token']
        user = Token.objects.get(user=self.user.id)

        self.assertTrue(bool(token))  # Check if returned token exists in database
        self.assertEqual(token, user.key)  # Check if this token belongs to user, whose credentials
                                           # were passed in request body
