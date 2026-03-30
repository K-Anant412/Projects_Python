# from Database.database import db
from DataBase.database import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = "emolpyees"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    salary = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)