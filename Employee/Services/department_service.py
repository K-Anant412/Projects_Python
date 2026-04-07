from DataBase.database import db
from Utils.Response import error_response, success_response
from Utils.Check_role import check_superadmin
from Utils.Validation import department_validation
from Modules.department_module import Department

def create_department(data, role):
    try:
        user = check_superadmin(role)
        if user:
            return user
        error = department_validation(data)
        if error:
            return error_response("enter department name")
        department = Department(name=data["name"])
        db.session.add(department)
        db.session.commit()
        result = {
            "id": department.id,
            "name": department.name
        }
        return success_response("department was created" , result)
    except Exception as e:
        return error_response(str(e))
    
def show_all_department():
    try:
        data = Department.query.all()
        result = []
        for dep in data:
            result.append({
                "Id":dep.id,
                "Department": dep.name
            })
        return success_response("Departments", result)
    except Exception as e:
        return error_response(str(e))

def update_department(id, data, role):
    try:
        error = check_superadmin(role)
        if error:
            return error
        dep = Department.query.get(id)
        if not dep:
            return error_response("department not found")
        if "name" in data:
            dep.name = data["name"]
        return success_response("department was updated")
    except Exception as e:
        return error_response(str(e))

def delete_department(id, role):
    try:
        error = check_superadmin(role)
        if error:
            return error
        dep = Department.query.get(id)
        if not dep:
            return error_response("department not found")
        db.session.delete(id)
        db.session.commit()
        return success_response("department was deleted") 
    except Exception as e:
        return error_response(str(e))