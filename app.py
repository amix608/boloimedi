from flask import Flask, jsonify
import os
from flask import Flask
from flask_smorest import Api
from db import db
import models
import secrets
from blocklist import BLOCKLIST
from ss import blp as StoreBlueprint
from flask_migrate import Migrate

from ii import blp as ItemBlueprint
from uuser import blp as UserBlueprint
from flask_jwt_extended import JWTManager




def create_app(db_url=None):
 app=Flask(__name__)
 
 
 app.config["PROPAGATE_EXCEPTIONS"] = True
 app.config["API_TITLE"] = "Stores REST API"
 app.config["API_VERSION"] = "v1"
 app.config["OPENAPI_VERSION"] = "3.0.3"
 app.config["OPENAPI_URL_PREFIX"] = "/"
 app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
 app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
 app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABESA_URL","sqlite:///data.db")
 app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
 app.config["PROPAGATE_EXCEPTIONS"] = True
 db.init_app(app)
 
 migrate=Migrate(app,db)
 api=Api(app)
 
 app.config["JWT_SECRET_KEY"]="262784093388246059040945468442683876552"
 jwt=JWTManager(app)
 
 @jwt.token_in_blocklist_loader
 def token_inbloklist(jwt_header,jwt_payload):
     return jwt_payload["jti"] in BLOCKLIST
 @jwt.expired_token_loader
 def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

 @jwt.invalid_token_loader
 def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

 @jwt.unauthorized_loader
 def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

 
 

 

 api.register_blueprint(StoreBlueprint)
 api.register_blueprint(ItemBlueprint)
 api.register_blueprint(UserBlueprint)
 
 
 
 return app
