import requests
import os
import allure

from dotenv import load_dotenv
from core.settings.environments import Environments
from core.settings.config import Users, Timeouts
from core.clients.endpoints import Endpoints

load_dotenv()


class ApiClient:
    def __init__(self):
        environment = os.getenv('ENVIRONMENT')
        try:
            environment = Environments[environment]
        except KeyError:
            raise ValueError(f"Unsupported environment: {environment}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json'
        }

    def get_base_url(self, environment: Environments) -> str:
        if environment == Environments.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environments.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
            return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
            return response.json()

    def ping(self):
        with allure.step('Ping api client'):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
            return response.status_code

    def auth(self):
        with allure.step('Getting authenticate'):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}"
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        token = response.json().get("token")
        with allure.step('Updating header with authorization'):
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    @allure.title("Получение информации о бронировании по ID")
    def get_booking_by_id(self, booking_id):
        with allure.step("Отправка запроса на получение информации о бронировании по ID"):
            response = requests.get(url=f"{self.base_url}/booking/{booking_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == booking_id
        return response.json()