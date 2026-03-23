import pytest
import allure
import requests
from helpers import BASE_URL, register_new_courier_and_return_login_password, login_courier, delete_courier, generate_random_string


@allure.suite('Создание курьера')
class TestCreateCourier:

    @allure.title('Курьера можно создать')
    @allure.description('Успешная регистрация — курьер существует в системе')
    def test_create_courier_success(self):
        creds = register_new_courier_and_return_login_password()
        assert creds, 'Регистрация не удалась'
        login, password, _ = creds

        courier_id = login_courier(login, password)
        assert courier_id is not None
        delete_courier(courier_id)

    @allure.title('Успешный запрос возвращает 201')
    def test_create_courier_returns_201(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)
        assert response.status_code == 201

        courier_id = login_courier(payload['login'], payload['password'])
        if courier_id:
            delete_courier(courier_id)

    @allure.title('Успешный запрос возвращает {"ok": true}')
    def test_create_courier_returns_ok_true(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)
        assert response.json() == {"ok": True}

        courier_id = login_courier(payload['login'], payload['password'])
        if courier_id:
            delete_courier(courier_id)

    @allure.title('Нельзя создать двух курьеров с одинаковым логином — код 409')
    def test_cannot_create_duplicate_courier(self):
        creds = register_new_courier_and_return_login_password()
        assert creds
        login, password, first_name = creds

        response = requests.post(
            f'{BASE_URL}/api/v1/courier',
            json={"login": login, "password": password, "firstName": first_name}
        )
        assert response.status_code == 409

        courier_id = login_courier(login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title('При дублирующем логине возвращается сообщение об ошибке')
    def test_duplicate_courier_returns_error_message(self):
        creds = register_new_courier_and_return_login_password()
        assert creds
        login, password, first_name = creds

        response = requests.post(
            f'{BASE_URL}/api/v1/courier',
            json={"login": login, "password": password, "firstName": first_name}
        )
        assert 'message' in response.json()

        courier_id = login_courier(login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title('Без поля login возвращается 400')
    def test_create_courier_without_login_returns_400(self):
        response = requests.post(
            f'{BASE_URL}/api/v1/courier',
            json={"password": generate_random_string(10), "firstName": generate_random_string(10)}
        )
        assert response.status_code == 400

    @allure.title('Без поля password возвращается 400')
    def test_create_courier_without_password_returns_400(self):
        response = requests.post(
            f'{BASE_URL}/api/v1/courier',
            json={"login": generate_random_string(10), "firstName": generate_random_string(10)}
        )
        assert response.status_code == 400

    @allure.title('При отсутствии обязательного поля возвращается текст ошибки')
    def test_create_courier_without_required_field_returns_error_message(self):
        response = requests.post(
            f'{BASE_URL}/api/v1/courier',
            json={"login": generate_random_string(10)}
        )
        assert response.json().get('message') == 'Недостаточно данных для создания учетной записи'
