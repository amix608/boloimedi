from db import db
class ItemModel(db.Model):
    __tablename__="item"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    price=db.Column(db.Float(precision=2),unique=False,nullable=False)
    store_id=db.Column(db.String,db.ForeignKey("store.id"),unique=True,nullable=False)
    stores=db.relationship("StoreModel",back_populates="item")
    