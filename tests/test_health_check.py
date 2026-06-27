import allure
import pytest
import requests


@allure.feature("Test ping")
@allure.story("Test connection")
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Expected status 201 but got {status_code}"

@allure.feature("Test ping")
@allure.story("Test server unavailability")
def test_ping_server_unavailable(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=Exception("server unavailable"))
    with pytest.raises(Exception, match="server unavailable"):
        api_client.ping()

@allure.feature("Test ping")
@allure.story("Test wrong HTTP method")
def test_ping_wrong_http_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 405"):
        api_client.ping()

@allure.feature("Test ping")
@allure.story("Test server error")
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 500"):
        api_client.ping()

@allure.feature("Test ping")
@allure.story("Test wrong URL")
def test_ping_not_found(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 404"):
        api_client.ping()

@allure.feature("Test ping")
@allure.story("Test connection with different success code")
def test_ping_success_different_success_code(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 200"):
        api_client.ping()

@allure.feature("Test ping")
@allure.story("Test timeout")
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=requests.exceptions.Timeout())
    with pytest.raises(requests.exceptions.Timeout):
        api_client.ping()

@allure.feature("Test create booking")
@allure.story("Test create new booking")
def test_create_booking(api_client, mocker, generate_random_booking_data):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 200"):
        api_client.create_booking(generate_random_booking_data)


