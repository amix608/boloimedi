from db import db


class UsermModel(db.Model):
    __tablename__ = "userm"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pasword = db.Column(db.String(80), nullable=False)