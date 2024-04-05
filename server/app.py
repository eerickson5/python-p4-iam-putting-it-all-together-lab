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

            user.password_hash= request.json.get("password")
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            return make_response(user.to_dict(), 201)
        except ValueError as e:
            return make_response({"error": f"Invalid User Details: {e}"}, 422)

class CheckSession(Resource):
    def get(self):
        if session.get("user_id"):
            user = User.query.filter(User.id == session["user_id"]).first()
            return make_response(user.to_dict(), 200)
        else:
            return make_response({"message": "No user logged in"}, 401)

class Login(Resource):
    def post(self):
        user = User.query.filter(User.username == request.json.get("username")).first()
        if user and user.authenticate(request.json.get("password")):
            session["user_id"] = user.id
            return make_response(user.to_dict(), 200)
        else:
            return make_response({"error": "Invalid credentials."}, 401)
    

class Logout(Resource):
    def delete(self):
        if session.get("user_id"):
            session["user_id"] = None
            return make_response({}, 204)
        else:
            return make_response({"message": "Not logged in"}, 401)

class RecipeIndex(Resource):
    def get(self):
        if session["user_id"]:
            recipes = [rec.to_dict() for rec in Recipe.query.filter(Recipe.user_id == session["user_id"]).all()]
            return make_response(recipes, 200)
        else:
            return make_response({"error": "Not logged in"}, 401)
        
    def post(self):
        if session["user_id"]:
            try:
                recipe = Recipe(
                    title=request.json.get("title"),
                    instructions=request.json.get("instructions"),
                    minutes_to_complete=request.json.get("minutes_to_complete"),
                    user_id=session["user_id"]
                )
                db.session.add(recipe)
                db.session.commit()
                return make_response(recipe.to_dict(), 201)
            except ValueError as e:
                return make_response( {"message": str(e)}, 422)
        else:
            return make_response({"error": "Not logged in"}, 401)



api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)