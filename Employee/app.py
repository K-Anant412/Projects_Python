from flask import Flask
from flask_restx import Api
from config import config
from DataBase.database import db

# import class from Module folder to create tables
from Modules.employee_module import Employee 
from Modules.user_module import User
from Modules.department_module import Department

# from Routes folder import custom route 
from Routes.auth_route import auth_routes
from Routes.employee import (employee_routes, delete_emp_route, find_emp_route, update_emp_route)
from Routes.department import department_routes

app = Flask(__name__)

# for database connection
app.config.from_object(config) 
db.init_app(app)

with app.app_context():
    db.create_all()
    
api = Api(
          app, 
          title="employee management AIP",
          description="a simple employee management API build with Flask", 
          doc="/swagger"
          ) 
api.add_namespace(auth_routes)  
api.add_namespace(employee_routes)
api.add_namespace(department_routes)
api.add_namespace(delete_emp_route)
api.add_namespace(find_emp_route)
api.add_namespace(update_emp_route)
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)
   