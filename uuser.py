from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

from db import db
from models import UsermModel
from schema_mak import UserSchema




blp = Blueprint("userm", __name__ ,description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
   
    def post(self, user_data):
        if UsermModel.query.filter(UsermModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UsermModel(
            username=user_data["username"],
            pasword=pbkdf2_sha256.hash(user_data["pasword"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UsermModel.query.filter(
            UsermModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["pasword"], user.pasword):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")
