from DataBase.database import db
from Modules.employee_module import Employee

class Attendance(db.Model):
    __tablename__ = "employee_attendance"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    time = db.Column(db.DateTime, default=db.func.current_timestamp())
    employee = db.relationship('Employee', backref='attendances')