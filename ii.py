from flask import Flask, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint,abort
from models.item import ItemModel
from schema_mak import ItemSchema,ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError
from db import db
blp = Blueprint("item", __name__, description="Operations on item")

@blp.route("/item")
class xura(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema(many=True))
    def get(self):
         d=ItemModel.query.all()
         sx=[]
         for s in d:
             sx.append(s)
         return sx
             

    
    @blp.arguments(ItemSchema)
    @blp.response(200,ItemSchema)
    @jwt_required()
    def post(self,axali_data):
        item=ItemModel(**axali_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,Message="cai dedaa")

        return item
    
    




@blp.route("/item/<string:item_id>")
class xura1(MethodView):
    @jwt_required(fresh=False)
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        return item
        
    @jwt_required()
    def delete(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"wavshale item"}
    
    
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    @jwt_required()
    def put(self,axali_data,item_id):
        itemn=ItemModel.query.get(item_id)
        if itemn:
         itemn.name=axali_data["name"]
         itemn.price=axali_data["price"]
        else :
            itemn=ItemModel(id=item_id,**axali_data)
        db.session.add(itemn)
        db.session.commit()
        return itemn
     