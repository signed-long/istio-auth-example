

def test_liveness_probes(test_client):
    '''
    Tests the liveness and readiness probes.
    '''
    response = test_client.post('/readiness')
    assert response.status_code == 200

    response = test_client.post('/liveness')
    assert response.status_code == 200
