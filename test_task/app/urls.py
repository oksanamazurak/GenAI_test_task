from django.urls import path
from .views import RegisterView, GetBalanceView, CurrencyRateView, HistoryView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "app"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("balance/", GetBalanceView.as_view(), name="balance"),
    path("currency/", CurrencyRateView.as_view(), name="currency"),
    path("history/", HistoryView.as_view(), name="history"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
