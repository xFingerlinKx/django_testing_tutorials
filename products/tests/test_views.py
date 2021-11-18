import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
# noinspection PyUnresolvedReferences
from products.views import product_detail


@pytest.fixture(scope='module')
def factory():
    """
    Фабрика RequestFactory использует тот же API, что и тестовый клиент.
    Однако вместо того, чтобы вести себя как браузер, RequestFactory
    предоставляет способ создания экземпляра запроса, который может быть
    использован в качестве первого аргумента любого представления.
    Это означает, что вы можете тестировать функцию представления так же,
    как и любую другую функцию - как черный ящик, с точно известными
    входами, тестируя определенные выходы.
    """
    return RequestFactory()


@pytest.fixture
def product(db):
    return mixer.blend('products.Product')


@pytest.fixture
def path():
    return reverse('detail', kwargs={'pk': 1})


def test_product_detail_authenticated(factory, product, path):
    request = factory.get(path)
    request.user = mixer.blend(User)

    response = product_detail(request, pk=1)
    assert response.status_code == 200


def test_product_detail_unauthenticated(factory, product, path):
    request = factory.get(path)
    request.user = AnonymousUser()

    response = product_detail(request, pk=1)
    assert 'accounts/login' in response.url
