import pytest
import allure
import requests
from helpers import BASE_URL


@allure.suite('Список заказов')
class TestGetOrders:

    @allure.title('Запрос списка заказов возвращает 200')
    def test_get_orders_returns_200(self):
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        assert response.status_code == 200

    @allure.title('Тело ответа содержит список заказов')
    def test_get_orders_returns_list(self):
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        assert 'orders' in response.json()

    @allure.title('Список заказов не пустой')
    def test_get_orders_list_is_not_empty(self):
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        orders = response.json().get('orders')
        assert isinstance(orders, list)
        assert len(orders) > 0
