from typing import Any

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from app.core.models import Metric, Tag


@pytest.fixture(scope="session", autouse=True)
def auth_backends() -> None:
    """Переопределение на стандартную аутентификацию"""
    settings.AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)


@pytest.fixture(scope="session", autouse=True)
def disable_custom_middleware() -> None:
    """Отключение кастомных миддлварей, чтобы не мешали тестам"""
    settings.MIDDLEWARE = [mw for mw in settings.MIDDLEWARE if mw.startswith("django")]


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_user(db: Any) -> User:
    user = get_user_model()
    return user.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def auth_client(test_user: User) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=test_user)
    return client


@pytest.fixture
def test_metric(test_user: User) -> Metric:
    return Metric.objects.create(user=test_user, name="test metric")


@pytest.fixture
def test_tag(db: Any) -> Tag:
    return Tag.objects.create(name="test tag")
