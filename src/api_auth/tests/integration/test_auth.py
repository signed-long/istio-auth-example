import json


def test_valid_register(test_client, init_database):
    '''
    Tests the registration route.
    '''
    body = {"email": "user@email.com", "password": "pass"}
    response = test_client.post(
        '/auth/register',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 201

    response = test_client.post(
        '/auth/login',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 200


def test_invalid_registers(test_client, init_database):
    '''
    Tests invalid register attempts.
    '''
    body = {"email": "testUser@test.ca"}
    response = test_client.post(
        '/auth/register',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 400

    body = {"password": "pass"}
    response = test_client.post(
        '/auth/register',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 400

    body = {"something_else": "idk"}
    response = test_client.post(
        '/auth/register',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 400

    body = {}
    response = test_client.post(
        '/auth/register',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 400

    response = test_client.post(
        '/auth/register',
        content_type='application/json',
    )
    assert response.status_code == 400


def test_valid_login(test_client, init_database, register_default_user):
    '''
    Tests invalid register attempts.
    '''
    body = {"email": "user@email.com", "password": "pass"}
    response = test_client.post(
        '/auth/login',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert data["data"]["access_token"]


def test_invalid_login(test_client, init_database, register_default_user):
    body = {"email": "NoUser@test.ca", "password": "pass"}
    response = test_client.post(
        '/auth/login',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 401

    body = {"email": "user@email.com", "password": "wrong_pass"}
    response = test_client.post(
        '/auth/login',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 401

    body = {"email": "user@email.com"}
    response = test_client.post(
        '/auth/login',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 400

    body = {"password": "pass"}
    response = test_client.post(
        '/auth/login',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 400

    body = {}
    response = test_client.post(
        '/auth/login',
        data=json.dumps(body),
        content_type='application/json',
    )
    assert response.status_code == 400

    response = test_client.post(
        '/auth/login',
        content_type='application/json',
    )
    assert response.status_code == 400
