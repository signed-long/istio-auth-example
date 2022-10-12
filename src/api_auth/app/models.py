from app import db
import pyotp
from app import bcrypt
import uuid
from sqlalchemy.dialects.postgresql import UUID
import datetime


# ----------------------------------------------------------------------
#
# Upon changing these models run 'flask db migrate && flask db upgrade'
# in your dev environment, then in any commit with this model change
# also push the updated files in the /migrations folder.
#
# ----------------------------------------------------------------------

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

    def __init__(self, email, password):
        '''
        Creates a user.
        '''
        self.email = email
        self.set_pw_hash(password)

    def check_pw_hash(self, pt_password):
        '''
        Checks a given password against the user's password hash.
        '''
        return bcrypt.check_password_hash(self.password_hash, pt_password)

    def set_pw_hash(self, pt_password):
        '''
        Sets a user's password hash given a password.
        '''
        pw_hash = bcrypt.generate_password_hash(pt_password)
        self.password_hash = pw_hash.decode("utf-8")
