import allure
import pytest
import requests
from faker import Faker


@allure.feature("Test create booking")
@allure.story("Successfully creating booking")
def test_create_booking(api_client, generate_random_booking_data):
    with allure.step("Отправка запроса на создание бронирования"):
        response = api_client.create_booking(generate_random_booking_data)

    with allure.step("Проверка, что бронирование создано"):
        assert response is not None, "Ответ не должен быть пустым"
        assert "bookingid" in response, "Ответ должен содержать bookingid"
        assert isinstance(response["bookingid"], int), "bookingid должен быть числом"
        assert response["bookingid"] > 0, "bookingid должен быть положительным числом"

    with allure.step("Проверка, что данные сохранены правильно"):
        booking = response["booking"]
        assert booking["firstname"] == generate_random_booking_data["firstname"]
        assert booking["lastname"] == generate_random_booking_data["lastname"]
        assert booking["totalprice"] == generate_random_booking_data["totalprice"]
        assert booking["depositpaid"] == generate_random_booking_data["depositpaid"]
        assert booking["bookingdates"] == generate_random_booking_data["bookingdates"]
        assert booking["additionalneeds"] == generate_random_booking_data["additionalneeds"]
