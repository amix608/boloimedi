from flask import Flask, jsonify
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schema_mak import StoreSchema
from models.store import StoreModel
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schema_mak import Storeupdateschema



blp = Blueprint("Stores", __name__, description="Operations on stores")
 


 
 
@blp.route("/store")
class xura(MethodView):
   @jwt_required()
   @blp.response(200,StoreSchema(many=True))
   def get(self):
        return StoreModel.query.all()

   @jwt_required()
   @blp.arguments(StoreSchema)
   @blp.response(201,StoreSchema)
   def post(self,axali_data):
        store=StoreModel(**axali_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="hui")
        return store

       
@blp.route("/store/<string:store_id>")
class xura1(MethodView):
    @jwt_required()
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store
    @jwt_required()
    def delete(self,store_id):
         store=StoreModel.query.get_or_404(store_id)
         db.session.delete(store)
         db.session.commit()
         return{"message":"wavshale store"}
    @jwt_required()
    @blp.response(200,StoreSchema)
    @blp.arguments(Storeupdateschema)
    def put(self,store_data,store_id):
        mimgeb=StoreModel.query.get(store_id)
        if mimgeb:
           mimgeb.name=store_data["name"]
        else:
            mimgeb=StoreModel(**store_data)
        db.session.add(mimgeb)
        db.session.commit()
        return mimgeb

   