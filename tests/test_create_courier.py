import pytest
import allure
import requests
from helpers import login_courier, delete_courier, generate_random_string, cleanup_courier, courier_payload
from constants import BASE_URL, CREATE_COURIER_URL, ERROR_MESSAGE


@allure.suite('Создание курьера')
class TestCreateCourier:

    @allure.title('Курьера можно создать')
    def test_create_courier_success(self):
        payload = courier_payload()
        with allure.step('Отправляем запрос на создание курьера'):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        cleanup_courier.append(payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title('Успешный запрос возвращает 201')
    def test_create_courier_returns_201(self):
        payload = courier_payload()
        with allure.step('Отправляем запрос'):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        cleanup_courier.append(payload)

        assert response.status_code == 201

    @allure.title('Успешный запрос возвращает ok true')
    def test_create_courier_returns_ok_true(self):
        payload = courier_payload()

        with allure.step('Отправляем запрос'):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        cleanup_courier.append(payload)

        assert response.json() == {"ok": True}

    @allure.title('Нельзя создать двух курьеров с одинаковым логином')
    def test_cannot_create_duplicate_courier(self):
        payload = courier_payload()

        with allure.step('Создаем первого курьера'):
            requests.post(CREATE_COURIER_URL, json=payload)

        cleanup_courier.append(payload)

        with allure.step('Создаем второго курьера с тем же логином'):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        assert response.status_code == 409

    @allure.title('При дублирующем логине возвращается сообщение об ошибке')
    def test_duplicate_courier_returns_error_message(self):
        payload = courier_payload()
        with allure.step('Создаем курьера'):
            requests.post(CREATE_COURIER_URL, json=payload)

        cleanup_courier.append(payload)

        with allure.step('Пробуем создать дубликат'):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        assert 'message' in response.json()

    @allure.title('Без login возвращается 400')
    def test_create_courier_without_login_returns_400(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        with allure.step('Отправляем запрос без login'):
            response = requests.post(CREATE_COURIER_URL, json=payload)


        assert response.status_code == 400

        cleanup_courier.append(payload)

    @allure.title('Без password возвращается 400')
    def test_create_courier_without_password_returns_400(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        with allure.step('Отправляем запрос без password'):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        assert response.status_code == 400

        cleanup_courier.append(payload)

    @allure.title('При отсутствии обязательных полей возвращается текст ошибки')
    def test_create_courier_without_required_field_returns_error_message(self):
        payload = {
            "login": generate_random_string(10)
        }

        with allure.step('Отправляем некорректный запрос'):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        assert response.json().get('message') == ERROR_MESSAGE

        cleanup_courier.append(payload)