from datetime import datetime
from sqlalchemy import extract
from DataBase.database import db
from Modules.employee_module import Employee
from Modules.attendance_module import Attendance
from Modules.payroll_module import Payroll
from Utils.Response import (
    success_response,
    error_response
)

def generate_payroll(id):

    try:
        employee = db.session.get( Employee, id )

        if not employee:
            return error_response( "Employee not found" )

        current_month = datetime.now().month
        current_year = datetime.now().year

        existing_payroll = Payroll.query.filter_by(
            employee_id=id,
            month=current_month,
            year=current_year
        ).first()

        if existing_payroll:
            return error_response( "Payroll already generated" )

        records = Attendance.query.filter(
            Attendance.employee_id == id,
            extract(
                "month",
                Attendance.attendance_date
            ) == current_month,
            extract(
                "year",
                Attendance.attendance_date
            ) == current_year
        ).all()

        present_days = 0
        absent_days = 0
        half_days = 0
        sick_leaves = 0

        for record in records:
            if record.status == "Present":
                present_days += 1
            elif record.status == "Absent":
                absent_days += 1
            elif record.status == "Half Day":
                half_days += 1
            elif record.status == "Sick Leave":
                sick_leaves += 1

        monthly_salary = employee.salary
        daily_salary = monthly_salary / 30
        unpaid_leaves = max( 0, absent_days - 2 )
        absent_deduction = ( unpaid_leaves * daily_salary )
        half_day_deduction = ( half_days * (daily_salary * 0.5))
        total_deduction = ( absent_deduction + half_day_deduction)
        final_salary = ( monthly_salary - total_deduction)

        attendance_percentage = ( ( present_days + (half_days * 0.5) ) / 30 ) * 100
        bonus = 0

        if attendance_percentage >= 95:
            bonus = monthly_salary * 0.20
        elif attendance_percentage >= 90:
            bonus = monthly_salary * 0.15
        elif attendance_percentage >= 80:
            bonus = monthly_salary * 0.10

        payroll = Payroll(
            employee_id=id,
            month=current_month,
            year=current_year,
            total_salary=round( monthly_salary, 2 ),
            total_deduction=round( total_deduction, 2 ),
            bonus=round( bonus, 2 ),
            final_salary=round( final_salary + bonus, 2 )
        )
        db.session.add(payroll)
        db.session.commit()

        result = {
            "Employee ID": employee.id,
            "Employee Name": employee.name,
            "Department": (
                employee.department.name
                if employee.department
                else "No Department"
            ),
            "Month": current_month,
            "Year": current_year,
            "Monthly Salary": round( monthly_salary, 2),
            "Present Days": present_days,
            "Absent Days": absent_days,
            "Half Days": half_days,
            "Sick Leaves": sick_leaves,
            "Paid Leaves": min( 2, absent_days),
            "Unpaid Leaves": unpaid_leaves,
            "Attendance Percentage": round( attendance_percentage, 2 ),
            "Total Deduction": round( total_deduction, 2 ),
            "Bonus": round( bonus, 2 ),
            "Final Salary": round( final_salary + bonus, 2  )
        }

        return success_response(
            "Payroll generated successfully",
            result
        )
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))

def get_payroll(id):

    try:
        current_month = datetime.now().month
        current_year = datetime.now().year
        payroll = Payroll.query.filter_by(
            employee_id=id,
            month=current_month,
            year=current_year
        ).first()

        if not payroll:
            return error_response(
                "Payroll not found"
            )

        employee = payroll.employee
        result = {
            "Employee ID": employee.id,
            "Employee Name": employee.name,
            "Department": (
                employee.department.name
                if employee.department
                else "No Department"
            ),
            "Month": payroll.month,
            "Year": payroll.year,
            "Total Salary": payroll.total_salary,
            "Total Deduction": payroll.total_deduction,
            "Bonus": payroll.bonus,
            "Final Salary": payroll.final_salary
        }

        return success_response(
            "Payroll fetched successfully",
            result
        )

    except Exception as e:
        return error_response(str(e))

def yearly_bonus_report(id):

    try:
        employee = db.session.get(
            Employee,
            id
        )

        if not employee:
            return error_response(
                "Employee not found"
            )
        current_year = datetime.now().year
        payrolls = Payroll.query.filter(
            Payroll.employee_id == id,
            Payroll.year == current_year
        ).all()

        total_bonus = 0
        total_salary = 0
        monthly_reports = []

        for payroll in payrolls:
            total_bonus += payroll.bonus
            total_salary += payroll.final_salary
            monthly_reports.append({
                "Month": payroll.month,
                "Salary": payroll.final_salary,
                "Bonus": payroll.bonus
            })

        result = {
            "Employee ID": employee.id,
            "Employee Name": employee.name,
            "Department": (
                employee.department.name
                if employee.department
                else "No Department"
            ),
            "Year": current_year,
            "Total Yearly Bonus": round( total_bonus, 2 ),
            "Total Yearly Salary": round( total_salary, 2 ),
            "Monthly Reports": monthly_reports
        }

        return success_response(
            "Yearly bonus report fetched",
            result
        )

    except Exception as e:
        return error_response(str(e))