from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserBalance, CurrencyExchange
from django.utils.timezone import now
from unittest.mock import patch

class CurrencyExchangeTests(APITestCase):
    """
    Test currency exchange-related views.
    """

    def setUp(self):
        """Set up a test user and initial balance."""
        self.user = User.objects.create_user(username="test", password="123")
        self.user_balance = UserBalance.objects.create(user=self.user, balance=1000)
        self.token = self.get_jwt_token()
        self.auth_headers = {"Authorization": f"Bearer {self.token}"}

    def get_jwt_token(self):
        """Generate JWT token for authentication."""
        response = self.client.post("/token/", {"username": "test", "password": "123"})
        return response.data["access"]

    def test_get_balance(self):
        """Test fetching the user's balance."""
        response = self.client.get("/balance/", headers=self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["balance"], 1000)

    @patch("requests.get")
    def test_currency_rate(self, mock_get):
        """Test currency exchange rate retrieval."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"conversion_rates": {"USD": 40.0}}
        response = self.client.post("/currency/", {"currency_code": "USD"}, headers=self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["currency"], "USD")
        self.assertEqual(response.data["rate"], 40.0)
        self.assertEqual(response.data["balance"], 999)

    def test_currency_rate_zero_balance(self):
        """Test handling exchange when the user balance is zero."""
        self.user_balance.balance = 0
        self.user_balance.save()
        response = self.client.post("/currency/", {"currency_code": "USD"}, headers=self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_currency_rate_invalid_code(self):
        """Test handling invalid currency code."""
        response = self.client.post("/currency/", {"currency_code": "Wrong"}, headers=self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_history_view(self):
        """Test retrieving the user's currency exchange history."""
        CurrencyExchange.objects.create(user=self.user, currency_code="USD", rate=40.0, created_at=now())
        response = self.client.get("/history/", headers=self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["currency_code"], "USD")
