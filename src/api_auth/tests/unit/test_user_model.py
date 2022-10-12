from app.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, and password_hash fields are defined correctly
    """
    user = User('email@gmail.com', 'TestPass')
    assert user.email == 'email@gmail.com'
    assert user.password_hash != 'TestPass'
    assert user.check_pw_hash('TestPass')
