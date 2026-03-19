from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = "auth"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
]
