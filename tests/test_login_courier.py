from urllib import response

import pytest
import allure
import requests
from helpers import BASE_URL, register_new_courier_and_return_login_password, login_courier, delete_courier


@allure.suite('Логин курьера')
class TestLoginCourier:

    @allure.title('Курьер может авторизоваться — код 200')
    def test_courier_can_login(self):
        creds = register_new_courier_and_return_login_password()
        assert creds
        login, password, _ = creds

        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            json={"login": login, "password": password}
        )
        assert response.status_code == 200

        delete_courier(response.json().get('id'))

    @allure.title('Успешный запрос возвращает id')
    def test_login_returns_id(self):
        creds = register_new_courier_and_return_login_password()
        assert creds
        login, password, _ = creds

        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            json={"login": login, "password": password}
        )
        assert 'id' in response.json()

        delete_courier(response.json()['id'])

    @allure.title('Без поля login возвращается 400')
    def test_login_without_login_field_returns_400(self):
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            json={"password": "somepassword"}
        )
        assert response.status_code == 400

    @allure.title('Без поля password возвращается 400')
    def test_login_without_password_field_returns_400(self):
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            json={"login": "somelogin"}
        )
        assert response.status_code == 400

    @allure.title('При отсутствии обязательного поля возвращается текст ошибки')
    def test_login_without_fields_returns_error_message(self):
        response = requests.post(
        f'{BASE_URL}/api/v1/courier/login',
        json={}
    )

        assert response.status_code == 400

        try:
            body = response.json()
        except ValueError:
            pytest.fail(f"Response is not JSON: {response.text}")

        assert body.get('message') == 'Недостаточно данных для входа'

    @allure.title('При неверном пароле возвращается 404')
    def test_login_with_wrong_password_returns_404(self):
        creds = register_new_courier_and_return_login_password()
        assert creds
        login, password, _ = creds

        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            json={"login": login, "password": "wrongpassword"}
        )
        assert response.status_code == 404

        courier_id = login_courier(login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title('При неверном логине возвращается 404')
    def test_login_with_wrong_login_returns_404(self):
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            json={"login": "nonexistentuser12345", "password": "somepassword"}
        )
        assert response.status_code == 404

    @allure.title('При несуществующем пользователе возвращается сообщение об ошибке')
    def test_login_nonexistent_courier_returns_error_message(self):
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            json={"login": "nonexistentuser12345", "password": "somepassword"}
        )
        assert 'message' in response.json()
