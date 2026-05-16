from DataBase.database import db
from datetime import datetime

class Payroll(db.Model):

    __tablename__ = "payroll"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id")
    )

    month = db.Column(db.Integer)

    year = db.Column(db.Integer)

    total_salary = db.Column(db.Float)

    total_deduction = db.Column(db.Float)

    bonus = db.Column(db.Float)

    final_salary = db.Column(db.Float)

    generated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )