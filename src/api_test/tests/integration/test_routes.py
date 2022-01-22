

def test_hello_routes(test_client):
    '''
    Tests the registration route.
    '''
    response = test_client.get(
        '/public/hello',
        content_type='application/json',
    )
    assert response.status_code == 200

    response = test_client.get(
        '/private/hello',
        content_type='application/json',
    )
    assert response.status_code == 200
