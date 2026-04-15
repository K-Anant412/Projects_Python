from DataBase.database import db
from Utils.Response import success_response, error_response
from Modules.user_module import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from flask_mail import Message

def send_message(to_email, name):
    msg = Message(
        subject="Rigesrtation Successful",
        sender="",
        recipients=[to_email]  
    )
    msg.body = f"""
        Hello {name},

        Your account has been successfully created 🎉

        Welcome to our Employee Management System!

        Regards,
        Team
        """
    mail.send(msg)
    
def rigester_user(data):
    try:
        user = User.query.filter_by(user_name=data["user_name"]).first()
        if user:
            return error_response("user already exist", 400)
        role = data.get("role", "Admin")
        if role not in ["admin", "superadmin"]:
            return error_response("not exist", 400)
        user = User(
            user_name= data["user_name"],
            email= data["email"],
            password= generate_password_hash(data["password"]),
            role = role
        )
        
        send_message(data["email"], data["user_name"])
        
        db.session.add(user)
        db.session.commit()
        return success_response("new user added", 200)
    except Exception as e:
        return error_response(str(e))
    
def login(data):
    try:
        user = User.query.filter_by(email=data["email"]).first()
        
        if user and check_password_hash(user.password, data["password"]):
            session["user_id"] = user.id
            session["role"] = user.role
            return success_response("Login successful",{
                "ID":user.id,
                "Role":user.role
            })
            
        return error_response("invalid username or password")
    except Exception as e:
        return error_response(str(e))