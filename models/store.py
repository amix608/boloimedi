
from db import db
 
class StoreModel(db.Model):
    __tablename__="store"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),unique=False,nullable=False)
  
    item=db.relationship("ItemModel",back_populates="stores",lazy="dynamic")
    
   