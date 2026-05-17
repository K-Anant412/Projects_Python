from flask_restx import ( Namespace, Resource )
from Services.payroll_service import (
    generate_payroll,
    get_payroll,
    yearly_bonus_report
)

payroll_route = Namespace( "payroll", description="Payroll Management APIs" )

@payroll_route.route("/generate/<int:id>")
@payroll_route.param( "id", "Employee ID")
class GeneratePayroll(Resource):
    def post(self, id):
        return generate_payroll(id)

@payroll_route.route("/employee/<int:id>")
@payroll_route.param( "id", "Employee ID" )
class EmployeePayroll(Resource):
    def get(self, id):
        return get_payroll(id)

@payroll_route.route("/yearly_bonus/<int:id>")
@payroll_route.param( "id", "Employee ID" )
class YearlyBonus(Resource):
    def get(self, id):
        return yearly_bonus_report(id)