import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from app.core.models import Metric, Tag


def pytest_configure():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 0,
        'OPTIONS': {},
        'TIME_ZONE': 'UTC',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }

    settings.CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

@pytest.fixture(scope="session", autouse=True)
def auth_backends() -> None:
    """Переопределение на стандартную аутентификацию"""
    settings.AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

@pytest.fixture(scope="session", autouse=True)
def disable_custom_middleware() -> None:
    """Отключение кастомных миддлварей, чтобы не мешали тестам"""
    settings.MIDDLEWARE = [mw for mw in settings.MIDDLEWARE if mw.startswith("django")]


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def auth_client(test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    return client

@pytest.fixture
def test_metric(test_user):
    return Metric.objects.create(user=test_user, name="test metric")

@pytest.fixture
def test_tag(db):
    return Tag.objects.create(name="test tag")