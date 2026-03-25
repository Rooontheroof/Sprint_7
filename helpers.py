import requests
import random
import string
from constants import CREATE_COURIER_URL, CREATE_URL, LOGIN_COURIER_URL


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(CREATE_COURIER_URL, json=payload)

    if response.status_code == 201:
        return login, password, first_name
    return None


def login_courier(login, password):
    response = requests.post(
        LOGIN_COURIER_URL,
        json={"login": login, "password": password}
    )
    if response.status_code == 200:
        return response.json().get('id')
    return None


def delete_courier(courier_id):
    requests.delete(f"{CREATE_COURIER_URL}/{courier_id}")

def courier_payload():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }


def cleanup_courier():
    created = []

    yield created

    for creds in created:
        courier_id = login_courier(creds["login"], creds["password"])
        if courier_id:
            delete_courier(courier_id)

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
