from flask import request
from flask_restx import Namespace, Resource, fields
from Services.auth_service import rigester_user, login

auth_routes = Namespace("auth", description="authentication API")
user_model = auth_routes.model("User", {
                                        "user_name":fields.String(required=True), 
                                        "email":fields.String(required=True), 
                                        "password":fields.String(required=True),
                                        "role":fields.String(reuqired=True)
                                        }
                               )
@auth_routes.route("/Register")
class Register(Resource):
    @auth_routes.expect(user_model)
    def post(self):
        data = request.get_json()
        return rigester_user(data)
    
login_model = auth_routes.model("Login", {
                                        "email":fields.String(required=True),
                                        "password":fields.String(required=True)
                                        })
@auth_routes.route("/login")    
class Login(Resource):
    @auth_routes.expect(login_model)
    def post(self):
        data = request.get_json()
        return login(data)