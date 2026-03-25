import pytest
import allure
import requests
from constants import BASE_URL, GET_ORDERS_URL


@allure.suite('Список заказов')
class TestGetOrders:

    @allure.title('GET /api/v1/orders возвращает статус 200')
    def test_get_orders_returns_200(self):
        with allure.step('Отправляем GET запрос на получение списка заказов'):
            response = requests.get(GET_ORDERS_URL)

        assert response.status_code == 200

    @allure.title('GET /api/v1/orders возвращает поле orders в теле ответа')
    def test_get_orders_returns_orders_field(self):
        with allure.step('Отправляем GET запрос'):
            response = requests.get(GET_ORDERS_URL)

        body = response.json()

        assert 'orders' in body
        assert isinstance(body['orders'], list)

    @allure.title('GET /api/v1/orders возвращает непустой список заказов')
    def test_get_orders_list_is_not_empty(self):
        with allure.step('Отправляем GET запрос'):
            response = requests.get(GET_ORDERS_URL)

        orders = response.json().get('orders')

        assert isinstance(orders, list)
        assert len(orders) > 0