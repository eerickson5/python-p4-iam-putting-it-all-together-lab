#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        try:
            user = User(
                username=request.json.get("username"),
                image_url=request.json.get("image_url"),
                bio=request.json.get("bio")
            )

            db.session.add(user)
            db.session.commit()
            user.password_hash= request.json.get("password")
            session["user_id"] = user.id
            return make_response(user.to_dict(), 201)
        except ValueError as e:
            return make_response({"error": f"Invalid User Details: {e}"}, 422)

class CheckSession(Resource):
    def get(self):
        if session["user_id"]:
            user = User.query.filter(User.id == session["user_id"]).first()
            return make_response(user.to_dict(), 200)
        else:
            return make_response({"message": "No user logged in"}, 401)

class Login(Resource):
    pass

class Logout(Resource):
    pass

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)