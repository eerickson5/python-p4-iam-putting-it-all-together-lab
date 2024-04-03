from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    @hybrid_property
    def password_hash(self):
        raise Exception("Cannot access password hash.")
    
    @password_hash.setter
    def password_hash(self, pw):
        pw_hash = bcrypt.generate_password_hash(pw.encode("utf-8"))
        self._password_hash = pw_hash.decode("utf-8")


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    pass