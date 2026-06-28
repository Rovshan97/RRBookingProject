from core.clients.api_client import ApiClient
import pytest
from datetime import datetime, timedelta, date
from faker import Faker


@pytest.fixture(scope='session')
def api_client():
    client = ApiClient()
    client.auth()
    return client

@pytest.fixture
def booking_dates():
    today = date.today()
    checkin_date = today + timedelta(days=5)
    checkout_date = today + timedelta(days=10)

    return {
        "checkin": checkin_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d")
    }

@pytest.fixture
def generate_random_booking_data(booking_dates):
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    bookingdates = booking_dates,
    additionalneeds = faker.sentence(nb_words=3)

    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates,
        "additionalneeds": additionalneeds,
    }

    return data