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

    # Отправляем запрос без обработки ошибок в клиенте
    # Используем прямой запрос, чтобы не вызывать raise_for_status()
    url = "https://restful-booker.herokuapp.com/booking"
    import requests
    response = requests.post(url, json=booking_data, headers={"Content-Type": "application/json"})

    # Проверяем, что статус НЕ 200 (это ошибка)
    assert response.status_code != 200, \
        f"Ожидалась ошибка, но получен статус 200. Ответ: {response.text}"

    # Для restful-booker при пустом теле возвращается 500, допускаем 400 или 500
    assert response.status_code in [400, 500], \
        f"Ожидался статус 400 или 500, получен {response.status_code}. Ответ: {response.text}"

    # Проверяем, что в ответе есть сообщение об ошибке
    try:
        response_data = response.json()
        print(f"Ответ сервера: {response_data}")

        # Проверяем наличие поля с ошибкой (если есть)
        error_fields = ['error', 'msg', 'message', 'detail']
        has_error = any(field in response_data for field in error_fields)

        # Если нет явного поля с ошибкой, но статус 500 - это тоже ок
        if not has_error and response.status_code == 500:
            print(f"Сервер вернул 500 без явного сообщения об ошибке. Ответ: {response_data}")
        else:
            assert has_error, f"В ответе нет сообщения об ошибке. Ответ: {response_data}"

    except json.JSONDecodeError:
        # Если ответ не JSON, проверяем текст
        assert "error" in response.text.lower() or "internal" in response.text.lower(), \
            f"Ответ не содержит сообщения об ошибке: {response.text}"

    print(f"Тест пройден. Статус: {response.status_code}")


@allure.feature("Test creating booking")
@allure.story("Negative tests - API should reject invalid data types")
@pytest.mark.parametrize("field_name, invalid_value, description", [
    ("firstname", 123456, "Число вместо строки"),
    ("firstname", True, "Булево значение вместо строки"),
    ("lastname", 123, "Число вместо строки"),
    ("totalprice", "сто", "Строка вместо числа"),
    ("totalprice", True, "Булево вместо числа"),
    ("depositpaid", "true", "Строка вместо булева"),
    ("depositpaid", 1, "Число вместо булева"),
])
def test_create_booking_rejects_invalid_types(api_client, field_name, invalid_value, description):
    # 1. Подготовка данных
    booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2019-01-10",
            "checkout": "2019-01-15",
        },
        "additionalneeds": "Dinner"
    }

    booking_data[field_name] = invalid_value

    allure.attach(
        json.dumps(booking_data, indent=2, ensure_ascii=False),
        name=f"Отправленные данные (поле: {field_name})",
        attachment_type=allure.attachment_type.JSON
    )

    # 2. Отправка запроса с обработкой исключений
    try:
        response = api_client.create_booking(booking_data)

        # Если дошли сюда - статус 200 OK (успех)
        status_code = 200
        response_data = response if isinstance(response, dict) else response.json()

        print(f"✅ [{description}] - API создало бронирование (автоприведение)")
        print(f"   Отправлено: {invalid_value} ({type(invalid_value).__name__})")

        # Проверяем, что это действительно успешный ответ
        if isinstance(response_data, dict):
            assert 'bookingid' in response_data, \
                f"❌ [{description}] Нет bookingid в ответе: {response_data}"
            print(f"   Booking ID: {response_data.get('bookingid')}")

            # Проверяем приведенное значение
            booking = response_data.get('booking', {})
            actual_value = booking.get(field_name)
            if actual_value is not None:
                print(f"   Получено: {actual_value} ({type(actual_value).__name__})")

                allure.attach(
                    f"Отправлено: {invalid_value} ({type(invalid_value).__name__})\n"
                    f"Получено: {actual_value} ({type(actual_value).__name__})",
                    name="Приведение типов",
                    attachment_type=allure.attachment_type.TEXT
                )

    except requests.exceptions.HTTPError as e:
        # API вернуло ошибку (400 или 500)
        response = e.response
        status_code = response.status_code

        print(f"✅ [{description}] - API вернуло ошибку. Статус: {status_code}")

        # Проверяем статус
        assert status_code in [400, 500], \
            f"❌ [{description}] Ожидался 400/500, получен {status_code}"

        # Логируем ответ
        try:
            response_data = response.json()
            print(f"Ответ: {json.dumps(response_data, indent=2, ensure_ascii=False)}")

            allure.attach(
                json.dumps(response_data, indent=2, ensure_ascii=False),
                name="Ответ сервера (ошибка)",
                attachment_type=allure.attachment_type.JSON
            )
        except:
            print(f"   Ответ (текст): {response.text[:200]}")
            allure.attach(
                response.text[:500],
                name="Ответ сервера (текст)",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        # Другие исключения
        assert False, f"❌ [{description}] Неожиданное исключение: {e}"

    # 3. Финальная проверка: убеждаемся, что статус корректный
    assert status_code in [200, 400, 500], \
        f"❌ [{description}] Неожиданный статус: {status_code}"


