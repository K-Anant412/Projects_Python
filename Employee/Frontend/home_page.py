import streamlit as st
import base64
import os
import pandas as pd
import requests

base_url = "http://127.0.0.1:5001/api/v1"

if 'view' not in st.session_state:
    st.session_state.view = None
    
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
            
            dept_menu = ["menu", "Add Department", "Show Departments", "Update Department", "Delete Department", "Show Employees"]
            emp_menu = ["menu", "Add Employee", "Update Employee", "Show Employees", "Search Employee", "Delete"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Employee"):
                    st.session_state.view = "employee"
                            
            with col2:
                if st.button("Department"):
                    st.session_state.view = "department"
        
            if st.session_state.view == "employee":
                st.subheader("Manage Employees")
                choice = st.selectbox("Action", emp_menu)
                
                if choice == "Add Employee":
                    st.subheader("Add new employee")
                    
                    with st.form("add_form"):
                        name = st.text_input("name")
                        city = st.text_input("city")
                        email = st.text_input("email")
                        salary = st.number_input("salary", min_value=0)
                        department = st.text_input("department")
                        
                        submit = st.form_submit_button("Add Employee")
                        
                        if submit:
                            data = {"name":name, "city":city, "email":email, "salary":salary, "department":department}
                            try:
                                response = requests.post(f"{base_url}/employee/add_employee", json=data)
                                if response.status_code == 200:
                                    st.success("User added!")
                                else:
                                    st.error("Failed to add user.")
                            except Exception as e:
                                st.error(f"Server Error: {e}")
        
                elif choice == "Update Employee":
                    pass
                
                elif choice == "Show Employees":
                    st.subheader("Employees")
                    
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        page = st.number_input("Pages", min_value=1, value=1, step=1)
                    with c2:
                        emp_per_page = st.selectbox("Employees per page", options=[5, 10, 15, 20, 25, 30])
                        
                    url = f"{base_url}/employee/show_employee"
                    params = {
                        "page": int(page),
                        "per_page": int(emp_per_page)
                    }
                    
                    if st.button("Fetch Employees"):
                        response = requests.get(url, params=params)
                    
                        if response.status_code == 200:
                            raw_data = response.json()
                            
                            if "Data" in raw_data:
                                employee_list = raw_data["Data"]
                                
                                if employee_list:
                                    df = pd.DataFrame(employee_list)
                                    
                                    # Optional: Clean up column names
                                    df.columns = [col.capitalize() for col in df.columns]
                                    
                                    st.subheader("Employee List")
                                    st.dataframe(df, use_container_width=True, hide_index=True)
                                else:
                                    st.warning("No employees found on this page.")
                            else:
                                st.error("The API response format is unexpected.")
                                st.write(raw_data)                
        except Exception as e:
            st.error(e)
