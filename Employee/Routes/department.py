from flask import request
from flask_restx import Namespace, Resource, fields
from Services.department_service import (create_department, delete_department, update_department, show_all_department)

department_routes = Namespace("department", description="creating department")
department_model = department_routes.model("Department",{"name":fields.String(required=True, description="enter department name")})
@department_routes.route("/add_department")
class create_dep(Resource):
    @department_routes.doc(params={
        "role":{
            "in":"header",
            "description": "user role superadmin",
            "required": True
        }
    })
    @department_routes.expect(department_model)    
    def post(self):
        role = request.headers.get("role")
        data = request.get_json()
        return create_department(data, role)
@department_routes.route("/show_department")
class show_dep(Resource):
    def get(self):
        return show_all_department()
@department_routes.route("/update_department/<int:id>")
class update_dep(Resource):
    @department_routes.expect(department_model)
    @department_routes.param("id", "department_id", _in="path", required=True)
    @department_routes.doc(params={
          "role":{
              "in":"header",
              "description": "user role superadmin",
              "required": True
          }      
    })
    def put(self, id):
        role = request.headers.get("role")
        data = request.get_json()
        return update_department(id, data, role)
@department_routes.route("/delete_department/<int:id>")
class remove_dep(Resource):
    @department_routes.param("id", "department_id", _in="path", required=True)
    @department_routes.doc(params={
        "role":{
            "in":"header",
            "description": "user role superadmin",
            "required": True
        }
    })
    def delete(self, id):
        role = request.headers.get("role")
        return delete_department(id, role)