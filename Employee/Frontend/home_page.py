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
            
            emp_menu = ["menu", "Add Employee", "Update Employee", "Show Employees", "Search Employee", "Delete", "Find by ID"]
            dept_menu = ["menu", "Add Department", "Show Departments", "Update Department", "Delete Department", "Show Employees"]
            
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
                
                elif choice == "Show Employees":# display the employee list
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
                                    
                                    df.columns = [col.capitalize() for col in df.columns]
                                    
                                    st.subheader("Employee List")
                                    st.dataframe(df, use_container_width=True, hide_index=True)
                                else:
                                    st.warning("No employees found on this page.")
                            else:
                                st.error("The API response format is unexpected.")
                                st.write(raw_data)                
                
                elif choice == "Find by ID":
                    st.subheader("Employee")
                    
                    emp_id = st.number_input("enter id", min_value=1)                
                    url = f"{base_url}/employee/employee_by_id/{emp_id}"
                    
                    if st.button("Get Employee"):
                        response = requests.get(url)

                        if response.status_code == 200:
                            raw_data = response.json()
                            
                            if "Data" in raw_data:
                                employee = raw_data["Data"]
                                
                                df = pd.DataFrame([employee])
                                st.subheader("Employee Details:")
                                st.dataframe(df, use_container_width=True, hide_index=True)

                elif choice == "Update Employee":
                    st.subheader("Update Information")
                    
                    emp_id = st.number_input("enter employee id", min_value=1)
                    url = f"{base_url}/employee/update_employee/{emp_id}"
                    
                    name = st.text_input("name")
                    city = st.text_input("city")
                    email = st.text_input("email")
                    salary = st.number_input("salary", min_value=0)
                    department = st.text_input("department")
        
                    if st.button("Update"):
                        params = {
                            "name": name,
                            "city": city,
                            "email": email,
                            "salary": salary,
                            "department": department
                        }
                        
                        response = requests.put(url, json=params)
                        
                        if response.status_code == 200:
                            st.success("Information Updated")
                        else:
                            st.warning("Something went wrong")
                 
                elif choice == "Delete":
                    st.subheader("Remove Employee")
                     
                    emp_id = st.number_input("enter id", min_value=1) 
                    fetch_emp = f"{base_url}/employee/employee_by_id/{emp_id}"
                    url = f"{base_url}/employee/delete_employee/{emp_id}"
                    
                    if st.button("Show"):
                        fetch = requests.get(fetch_emp)
                        if fetch.status_code == 200:
                            raw_data = fetch.json()
                            
                            if "Data" in raw_data:
                                employee = raw_data["Data"]
                                
                                df = pd.DataFrame([employee])
                                st.subheader("Employee Details:")
                                st.dataframe(df, use_container_width=True, hide_index=True)
                                
                                if st.button("Delete"):
                                    response = requests.delete(url)
                        
                                    if response.status_code == 200:
                                        st.success("Employee removed")
                                    else:
                                         st.warning("Something wrong")     
                        else:
                            st.warning("Employee not found")
                         
                
                elif choice == "Search Employee":
                    st.subheader("Search Employee")
                    
                    emp_id = st.number_input("enter id", min_value=1)
                    name = st.text_input("enter name")
                    city = st.text_input("enter city")
                    department = st.text_input("enter department")
                    
                    data = {
                        "emp_id":emp_id,
                        "name":name,
                        "city":city,
                        "department":department
                    }
                    url = f"{base_url}/employee/get_emp"
                    if st.button("Search"):
                        response = requests.get(url)
                        
                        if response.status_code == 200:
                            raw_data = response.json()
                            
                            if "Data" in raw_data:
                                employee = raw_data["Data"]
                                df = pd.DataFrame([employee])
                                st.subheader("Details:")
                                st.dataframe(df)
                            else:
                                st.warning("Employee not found")
                
            elif st.session_state.view == "department":
                st.subheader("Manage Department")
                
                choice = st.selectbox("Action", dept_menu)
                
                if choice == "Add Department":
                    name = st.text_input("enter department name")
                    
                    if st.button("Add Department"):
                        url = f"{base_url}/department/add_department"
                        response = requests.post(url, json={"name":name})
                        
                        if response.status_code == 200:
                            st.success("New department was added")
                        else:
                            st.warning("Something wrong")
                            st.write(response.json())
                            
                elif choice == "Show Departments":
                    st.subheader("Departments:")
                    
                    url = f"{base_url}/department/show_department"
                    
                    if st.button("Show Departments"):
                        response = requests.get(url)
                        
                        if response.status_code == 200:
                            raw_data = response.json()
                            
                            if "Data" in raw_data:
                                department = raw_data["Data"]
                                df = pd.DataFrame(department)
                                st.dataframe(df, use_container_width=True, hide_index=True)
                
                elif choice == "Update Department":
                    st.subheader("Update Information")
                    
                    dept_id = st.number_input("department ID", min_value=1)
                    name = st.text_input("enter new department name")
                    url = f"{base_url}/department/update_department/{dept_id}"
                    
                    if st.button("update"):
                        response = requests.put(url, json={"name":name})
                        
                        if response.status_code == 200:
                            st.success("Department updated")
                        else:
                            st.warning("something wrong")
                            
                elif choice == "Show Employees":
                    st.subheader("Employee per department")
                    
                    url = f"{base_url}/department/show_emp_per_dept"
                    
                    if st.button("Show All"):
                        response = requests.get(url)
                        
                        if response.status_code == 200:
                            raw_data = response.json()
                            
                            if "Data" in raw_data:
                                departments = raw_data["Data"]
                                
                                df = pd.DataFrame(departments)
                                st.dataframe(df, use_container_width=True, hide_index=True)
       
                elif choice == "Delete Department":
                    st.subheader("Remove")
                    dept_id = st.number_input("department id", min_value=1)
                    fetch_dept = f"{base_url}/department/fetch_dept_id/{dept_id}"
                    if st.button("remove"):
                        response = requests.get(fetch_dept)
                        if response.status_code == 200:
                            data = response.json()
                            df = pd.DataFrame([data])    
                            st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(e)
