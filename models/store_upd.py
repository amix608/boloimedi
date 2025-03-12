from db import db
class updatestore(db.Model):
    __tablename__="updstore"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)