from flask import request
from DataBase.database import db
from Modules.user_module import User
from Utils.Response import success_response, error_response
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash

auth_routes = Namespace("auth", description="authentication API")
user_model = auth_routes.model("User", {"user_name":fields.String(required=True), 
                                        "email":fields.String(required=True), 
                                        "password":fields.String(required=True)
                                        }
                               )

@auth_routes.route("/Register")
class Register(Resource):
    @auth_routes.expect(user_model)
    def post(self):
        data = request.get_json()
        existing_user = User.query.filter_by(user_name=data["user_name"]).first()
        
        if existing_user:
            return error_response("user already exist", 400)
        
        user = User(
            user_name = data["user_name"],
            email = data["email"],
            password = generate_password_hash(data["password"])
        )

        db.session.add(user)
        db.session.commit()
        
        return success_response("User register successfully", 200)