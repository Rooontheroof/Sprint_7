import pytest
import allure
import requests
from constants import BASE_URL


from order_data import ORDER_BASE


@allure.suite('Создание заказа')
@pytest.mark.parametrize('color', [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    [],
], ids=['BLACK', 'GREY', 'BLACK_and_GREY', 'no_color'])
class TestCreateOrder:

    @allure.title('Создание заказа возвращает 201')
    def test_create_order_returns_201(self, color):
        payload = {**ORDER_BASE, "color": color}
        response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)
        assert response.status_code == 201

    @allure.title('Тело ответа содержит track')
    def test_create_order_returns_track(self, color):
        payload = {**ORDER_BASE, "color": color}
        response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)
        assert 'track' in response.json()
