from django.core.exceptions import ObjectDoesNotExist
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, URLPatternsTestCase

from ...models import CustomUser


class BaseTestClass:
    urlpatterns = [
        path('api/', include('app.urls')),
    ]


class LogoutTest(APITestCase, URLPatternsTestCase, BaseTestClass):
    """
    Class that tests logout view
    """
    def setUp(self) -> None:
        user_credentials = {
            "username": "user name",
            "email": "user4@user.user",
            "password": "user4"
        }
        user = CustomUser.objects.create_user(**user_credentials)
        user_token = Token.objects.create(user=user).key
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + user_token)  # Pass bearer token
        response = self.client.get(url)

        self.response = response
        self.user = user
        self.token = user_token

    def test_logout_view_handles_request_successfully(self) -> None:
        """
        Tests that logout view handles request successfully
        """
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_logout_view_deletes_token_successfully(self) -> None:
        """
        Tests that GET /logout/ removes access token from database correctly
        """
        with self.assertRaises(expected_exception=ObjectDoesNotExist):
            Token.objects.get(key=self.token)
