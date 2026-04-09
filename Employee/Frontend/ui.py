import streamlit as st
import requests

base_url = "http://127.0.0.1:5001"

st.title("Employee Management System")
st.write("welcome to my employee management system")

menu = st.sidebar.selectbox("Menu", ["Home", "Employee", "Department"])

# if menu != "Emplopyee" and menu != "Department":
#     pass
if menu == "Home":
    pass

elif menu == "Employee":
    emp_menu = st.sidebar.selectbox("select", [
                                                "Show all", 
                                                "Add employee", 
                                                "Update employee", 
                                                "Delete employee", 
                                                "Find by ID", 
                                                "Find by salary"
                                                ])
elif menu == "Department":
    dep_menu = st.sidebar.selectbox("select",[
                                                "Show all",
                                                "Add departent",
                                                "Update department",
                                                "Remove department"
                                               ])
    