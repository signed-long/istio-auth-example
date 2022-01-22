import pytest
from app import create_app, db
import json


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='function')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()
    db.session.commit()

    yield  # this is where the testing happens!

    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def register_default_user(test_client):
    body = {"email": "user@email.com", "password": "pass"}
    test_client.post(
        '/auth/register',
        data=json.dumps(body),
        content_type='application/json',
    )

    yield  # this is where the testing happens!
