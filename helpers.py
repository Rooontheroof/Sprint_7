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


cleanup_courier = []


def perform_cleanup():
    for creds in cleanup_courier:
        courier_id = login_courier(creds["login"], creds["password"]) if "login" in creds and "password" in creds else None
        if courier_id:
            delete_courier(courier_id)


registered_courier_data = register_new_courier_and_return_login_password()
if registered_courier_data:
    registered_courier = {"login": registered_courier_data[0], "password": registered_courier_data[1], "firstName": registered_courier_data[2]}
    cleanup_courier.append(registered_courier)
else:
    registered_courier = None
