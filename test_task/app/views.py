import os
import requests
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from dotenv import load_dotenv
from drf_yasg.utils import swagger_auto_schema
from .models import CurrencyExchange, UserBalance
from .serializers import (
    CurrencyExchangeSerializer,
    UserSerializer,
    UserBalanceSerializer,
)
from drf_yasg import openapi

load_dotenv()
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")


class RegisterView(APIView):
    """
    User registration endpoint. Allows users to register with a username and password.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: "User registered successfully.", 400: "Invalid data."},
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
            UserBalance.objects.create(user=user, balance=1000)
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBalanceView(APIView):
    """
    Retrieve the current balance of the authenticated user.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserBalanceSerializer, 403: "Authentication failed."}
    )
    def get(self, request):
        balance = UserBalance.objects.get(user=request.user)
        return Response({"balance": balance.balance})


class CurrencyRateView(APIView):
    """
    Get exchange rate for a specified currency code. User's balance must be > 0 to perform the operation.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CurrencyExchangeSerializer,
        responses={
            200: "Exchange rate fetched.",
            403: "Zero balance.",
            400: "Invalid currency code.",
            500: "API error.",
        },
    )
    def post(self, request):
        currency_code = request.data.get("currency_code", "").upper()
        user_balance = UserBalance.objects.get(user=request.user)

        if user_balance.balance <= 0:
            return Response({"error": "Zero balance"}, status=status.HTTP_403_FORBIDDEN)

        response = requests.get(
            f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/UAH"
        )

        if response.status_code != 200:
            return Response(
                {"error": "Failed to get exchange rate."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        data = response.json()
        rate = data["conversion_rates"].get(currency_code)

        if not rate:
            return Response(
                {"error": "Wrong currency code"}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            CurrencyExchange.objects.create(
                user=request.user, currency_code=currency_code, rate=rate
            )
            user_balance.balance -= 1
            user_balance.save()

        return Response(
            {"currency": currency_code, "rate": rate, "balance": user_balance.balance}
        )


class HistoryView(APIView):
    """
    Retrieve user's currency exchange transaction history, optionally filterable by currency code or date.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the user's currency exchange history",
        manual_parameters=[
            openapi.Parameter(
                "currency",
                openapi.IN_QUERY,
                description="Currency code to filter by (optional)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Date to filter by (optional, format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: CurrencyExchangeSerializer(many=True),
            403: "Authentication failed.",
        },
    )
    def get(self, request):
        currency = request.query_params.get("currency")
        date = request.query_params.get("date")
        history = CurrencyExchange.objects.filter(user=request.user)

        if currency:
            history = history.filter(currency_code=currency)
        if date:
            history = history.filter(created_at__date=date)

        serializer = CurrencyExchangeSerializer(history, many=True)
        return Response(serializer.data)
