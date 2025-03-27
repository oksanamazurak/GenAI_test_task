from django.contrib import admin
from rest_framework import permissions
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Exchange API",
        default_version="v1",
        description="API for currency exchange operations",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="oksanamazurak18@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include("app.urls", namespace="app")),
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-schema",
    ),
]
