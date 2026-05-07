import streamlit as st
import base64
import os
import pandas as pd
import requests

base_url = "http://127.0.0.1:5001/api/v1"

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def home():
    
    path_to_img = r"C:\Users\nohi4\OneDrive\Pictures\A\bg1.png"
    
    if os.path.exists(path_to_img):
        try:
            bin_str = get_base64(path_to_img)
            st.markdown(
            f"""
                <style>
                    .stApp {{
                    background-image: url("data:image/png;base64,{bin_str}");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    transform: scaleX(-1);
                    }}
                
                    .stApp > div{{
                    transform: scaleX(-1);    
                    }}
                    
                    html, body, .stApp {{
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: #C0E1D2;
                    }}
                    
                    div.stButton > button {{
                    background-color: #009688;
                    color: white;
                    border-radius: 20px;
                    height: 3em;
                    width: 100%;
                    border: 2px solid #00796B;
                    font-size: 18px;
                    transition: 0.3s;
                    }}
                    div.stButton > button:hover {{
                    background-color: #005f5f;
                    color: white;
                    }}
                </style>
                """
            , unsafe_allow_html=True)
            
            st.write("Hello, User......")
            
            emp_menu = ["Add Employee", "Update Employee", "Show Employees", "Search Employee", "Delete"]
            dept_menu = ["Add Department", "Show Departments", "Update Department", "Delete Department", "Show Employees"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Employee"):
                    st.selectbox("Options", emp_menu)
            with col2:
                if st.button("Department"):
                    st.selectbox("Options", dept_menu)
        
        except Exception as e:
            st.error(e)
