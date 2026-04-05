import streamlit as st
import requests

base_url = "http://127.0.0.1:5001"

st.title("Employee Management System")
st.write("welcome to my employee management system")

menu = st.sidebar.selectbox("Menu", ["Employee Dashboard", "Department"])