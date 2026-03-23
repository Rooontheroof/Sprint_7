import requests
import random
import string

BASE_URL = 'https://qa-scooter.praktikum-services.ru'


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []


def login_courier(login, password):
    response = requests.post(
        f'{BASE_URL}/api/v1/courier/login',
        json={"login": login, "password": password}
    )
    if response.status_code == 200:
        return response.json().get('id')
    return None


def delete_courier(courier_id):
    requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
