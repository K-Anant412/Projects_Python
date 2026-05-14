from DataBase.database import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = "employee_attendance"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey('employees.id'),
        nullable=False
    )

    attendance_date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    punch_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    employee = db.relationship(
        'Employee',
        backref='attendances'
    )