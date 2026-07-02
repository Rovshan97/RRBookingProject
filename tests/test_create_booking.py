import allure
from allure_commons.model2 import TEST_CASE_PATTERN
from pydantic import ValidationError
from conftest import generate_random_booking_data
from core.models.booking import BookingResponse
import requests
import json
import pytest


@allure.feature("Test creating booking")
@allure.story("Successfully creating booking with custom data")
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2019-01-10",
            "checkout": "2019-01-15",
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature("Test creating booking")
@allure.story("Successfully creating booking with random data")
def test_create_booking_with_random_data(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature("Test creating booking")
@allure.story("Create booking with empty data")
def test_create_booking_with_empty_data(api_client):
    booking_data = {}
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        response = api_client.create_booking(booking_data)

    response = exc_info.value.response
    assert response.status_code != 200, f"Ожидалась ошибка, но получен статус 200. Ответ: {response.text}"

    assert response.status_code in [400, 500], f"Ожидался статус 400 или 500, получен {response.status_code}. Ответ: {response.text}"

    print(f"Тест пройден. Статус: {response.status_code}")


@allure.feature("Test creating booking")
@allure.story("Сreating booking without lastname")
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2019-01-10",
            "checkout": "2019-01-15",
        },
        "additionalneeds": "Dinner"
    }
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        response = api_client.create_booking(booking_data)

    response = exc_info.value.response

    assert response.status_code != 200, f"Ожидалась ошибка, но получен статус 200. Ответ: {response.text}"

    assert response.status_code in [400, 500], f"Ожидался статус 400 или 500, получен {response.status_code}. Ответ: {response.text}"

    print(f"Тест пройден. Статус: {response.status_code}")
