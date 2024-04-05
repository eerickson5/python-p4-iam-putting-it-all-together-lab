from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship("Recipe", back_populates="user")

    serialize_only = ('id','username', 'image_url','bio')

    @validates('username', 'password')
    def validate_username_password(self, key, address):
        if len(address) > 1:
            return address
        else:
            raise ValueError(f"{key} too short")
    
        
    @validates("image_url", 'bio')
    def validate_image_bio(self, key, address):
        if len(address) > 1:
            return address
        else:
            raise ValueError(f"{key} too short")

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Cannot access password hash.")
    
    @password_hash.setter
    def password_hash(self, pw):
        pw_hash = bcrypt.generate_password_hash(pw.encode("utf-8"))
        self._password_hash = pw_hash.decode("utf-8")


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, db.CheckConstraint("LENGTH(instructions) > 49"), nullable=False )
    minutes_to_complete = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates='recipes')