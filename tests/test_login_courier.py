import pytest
import allure
import requests
from helpers import generate_random_string, login_courier, delete_courier
from constants import BASE_URL


LOGIN_URL = f"{BASE_URL}/api/v1/courier/login"
CREATE_URL = f"{BASE_URL}/api/v1/courier"
ERROR_MESSAGE = 'Недостаточно данных для входа'


@pytest.fixture
def registered_courier():
    payload = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

    requests.post(CREATE_URL, json=payload)

    yield payload

    courier_id = login_courier(payload["login"], payload["password"])
    if courier_id:
        delete_courier(courier_id)


@allure.suite('Логин курьера')
class TestLoginCourier:

    @allure.title('POST /courier/login возвращает 200 при валидных данных')
    def test_courier_can_login(self, registered_courier):
        with allure.step('Логинимся валидным курьером'):
            response = requests.post(
                LOGIN_URL,
                json={
                    "login": registered_courier["login"],
                    "password": registered_courier["password"]
                }
            )

        assert response.status_code == 200

    @allure.title('POST /courier/login возвращает id')
    def test_login_returns_id(self, registered_courier):
        with allure.step('Логинимся'):
            response = requests.post(
                LOGIN_URL,
                json={
                    "login": registered_courier["login"],
                    "password": registered_courier["password"]
                }
            )

        assert 'id' in response.json()

    @allure.title('Без login возвращается 400')
    def test_login_without_login_field_returns_400(self):
        with allure.step('Отправляем запрос без login'):
            response = requests.post(
                LOGIN_URL,
                json={"password": "somepassword"}
            )

        assert response.status_code == 400

    @allure.title('Без password возвращается 400')
    def test_login_without_password_field_returns_400(self):
        with allure.step('Отправляем запрос без password'):
            response = requests.post(
                LOGIN_URL,
                json={"login": "somelogin"}
            )

        assert response.status_code == 400

    @allure.title('Без обязательных полей возвращается ошибка')
    def test_login_without_fields_returns_error_message(self):
        with allure.step('Отправляем пустой запрос'):
            response = requests.post(LOGIN_URL, json={})

        assert response.status_code == 400

        body = response.json()
        assert body.get('message') == ERROR_MESSAGE

    @allure.title('Неверный пароль → 404')
    def test_login_with_wrong_password_returns_404(self, registered_courier):
        with allure.step('Логинимся с неправильным паролем'):
            response = requests.post(
                LOGIN_URL,
                json={
                    "login": registered_courier["login"],
                    "password": "wrongpassword"
                }
            )

        assert response.status_code == 404

    @allure.title('Неверный логин → 404')
    def test_login_with_wrong_login_returns_404(self):
        with allure.step('Логинимся с несуществующим логином'):
            response = requests.post(
                LOGIN_URL,
                json={
                    "login": generate_random_string(10),
                    "password": "somepassword"
                }
            )

        assert response.status_code == 404

    @allure.title('Несуществующий пользователь → сообщение об ошибке')
    def test_login_nonexistent_courier_returns_error_message(self):
        with allure.step('Логинимся несуществующим пользователем'):
            response = requests.post(
                LOGIN_URL,
                json={
                    "login": generate_random_string(10),
                    "password": "somepassword"
                }
            )

        assert 'message' in response.json()