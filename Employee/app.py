from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from config import config
from DataBase.database import db

# from Routes folder import custom route 
from Routes.auth_route import auth_routes
from Routes.employee import employee_route
from Routes.department import department_routes

app = Flask(__name__)
CORS(app)

# for database connection
app.config.from_object(config) 
app.secret_key = "myProject123SessionKey"
db.init_app(app)

with app.app_context():
    db.create_all()
    
api = Api(
          app, 
          title="employee management API",
          description="a simple employee management API build with Flask", 
          doc="/swagger",
          endpoint='/api/v1'
          ) 
api.add_namespace(auth_routes)  
api.add_namespace(employee_route)
api.add_namespace(department_routes)
     
if __name__ == "__main__":
    app.run(debug=True, port=5001)