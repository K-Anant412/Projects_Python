import streamlit as st
import requests

base_url = "http://127.0.0.1:5001"

st.title("Employee Management System")
st.write("welcome to my employee management system")

menu = st.sidebar.selectbox("Menu", ["Employee", "Department"])

if menu == "Employee":
    
    emp_menu = st.sidebar.selectbox("select", ["Show all", "Add employee", "Update employee", "Delete employee", "Find by ID", "Find by salary"])
    