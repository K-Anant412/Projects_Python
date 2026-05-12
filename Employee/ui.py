import streamlit as st
import requests
import base64
import os
import pandas as pd

AUTH_URL = "http://127.0.0.1:5001/api/v1/auth"

base_url = "http://127.0.0.1:5001/api/v1"

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

path_to_img = r"C:\Users\nohi4\OneDrive\Pictures\A\bg1.png"
if os.path.exists(path_to_img):
        bin_str = get_base64(path_to_img)
        st.markdown(
            f"""
            <style>
            .stApp {{
                    background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{bin_str}");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    transform: scaleX(-1);
                    }}
            .stApp > div{{
                    transform: scaleX(-1);    
                    }}
            [data-testid="stSidebar"] {{
                background: rgba(0, 0, 0, 0.35);
                backdrop-filter: blur(12px);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = None

def login_user(email, password):
    try:
        response = requests.post(f"{AUTH_URL}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state.authenticated = True
            # Store data for the Sidebar Card
            st.session_state.user_data = response.json().get("data", {})
            st.rerun()
        else:
            st.error("Invalid credentials")
    except Exception as e:
        st.error(f"Connection Error: {e}")

def register_user(username, email, password, role):
    payload = {
        "user_name": username,
        "email": email,
        "password": password,
        "role": role
    }
    try:
        response = requests.post(f"{AUTH_URL}/Register", json=payload)
        if response.status_code == 200:
            st.success("Registration Successful! Please Login.")
        else:
            st.error(response.json().get("message", "Registration Failed"))
    except Exception as e:
        st.error(f"Connection Error: {e}")

# COMPONENTS ---
def auth_page():
    st.title(" Employee Management System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                login_user(email, password)
                
    with tab2:
        with st.form("reg_form"):
            u_name = st.text_input("Full Name")
            u_email = st.text_input("Email")
            u_pass = st.text_input("Password", type="password")
            u_role = st.selectbox("Role", ["Employee", "Admin", "Superadmin"])
            submit_reg = st.form_submit_button("Create Account")
            if submit_reg:
                register_user(u_name, u_email, u_pass, u_role)

def main_dashboard():
    # 1. Sidebar Setup
    with st.sidebar:
        # User Card
        st.markdown(f"""
            <div style="padding:15px; border-radius:10px; background-color:#f0f2f6; margin-bottom:20px; border:1px solid #d1d5db">
                <h4 style="margin:0;">👤 {st.session_state.user_data.get('user_name', 'User')}</h4>
                <p style="color:gray; font-size:14px; margin:0;">Role: {st.session_state.user_data.get('Role', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation in check-box,
        st.subheader("Management")
        choice = st.radio("Go to:", ["Employee", "Department", "Attendance", "Salary"])
        
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()

    # 2. Page Logic
    st.title(f"Welcome ")
    
    if choice == "Employee":
        st.subheader("Employee Management")
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add", "Update", "Employee List", "Delete", "Search"])
        
        with tab1:
            st.subheader("Add New Employee")
            c1, c2 = st.columns(2)
            
            with st.form("add_form"):
                
                        with c1:
                                name = st.text_input("name")
                                city = st.text_input("city")
                                salary = st.number_input("salary", min_value=0)
                        
                        with c2:
                                email = st.text_input("email")
                                department = st.text_input("department")
                            
                        submit = st.form_submit_button("Add Employee")
        
                        if submit:
                            data = {
                                "name":name,
                                "city":city,
                                "email":email,
                                "salary":salary,
                                "department":department
                            }
                            try:
                                response = requests.post(f"{base_url}/employee/add_employee", json=data)
                                if response.status_code == 200:
                                    st.success("New employee added")
                                else:
                                    st.error("Failed to add user.")
                            except Exception as e:
                                st.error(f"Server Error: {e}")
                        
        with tab2:
            st.subheader("Update Employee")
            
            emp_id = st.number_input("employee ID", min_value=0)
            url = f"{base_url}/employee/employee_by_id/{emp_id}"
            update_url = f"{base_url}/employee/update_employee/{emp_id}"
            
            if st.button("Update"):
               response = requests.get(url)
               if response.status_code == 200:
                   raw_data = response.json()
                   
                   if "Data" in raw_data:
                       employee = raw_data["Data"]
                       c1, c2, = st.columns(2)
                       with c1:
                                name = st.text_input("name", value=employee.get("name"))
                                city = st.text_input("city", value=employee.get("city"))
                                salary = st.number_input("salary", min_value=0, value=employee.get("salary"))
                       with c2:
                                email = st.text_input("email", value=employee.get("email"))
                                department = st.text_input("department", value=employee.get("department"))
                    
                       if st.button("Save"):
                           params = {
                            "name": name,
                            "city": city,
                            "email": email,
                            "salary": salary,
                            "department": department
                            }
                           response = requests.put(update_url, json=params)
                           
                           if response.status_code == 200:
                               st.success("Information Updated")
                           else:
                               st.error("Server Error")
                               
        with tab3:
                st.subheader("Employee List")
                c1, c2 = st.columns(2)
                with c1:
                    page = st.number_input("Pages", min_value=1)
                with c2:
                    per_page = st.selectbox("Employees Per Page", options=[5, 10, 15, 20])
                    
                params = {
                    "page":int(page),
                    "per_page":int(per_page)
                }
                get_url = f"{base_url}/employee/show_employee"
                
                if st.button("Show Employees"):
                    response = requests.get(get_url, params=params)
                    
                    if response.status_code == 200:
                        raw_data = response.json()
                        
                        if "Data" in raw_data:
                            employees = raw_data["Data"]
                            df = pd.DataFrame(employees)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.error("Server problem")
                            
        with tab4:
            st.subheader("Remove Employee")
            
            emp_id_delete = st.number_input("employee ID", min_value=0, key="delete_employee")
            url = f"{base_url}/employee/employee_by_id/{emp_id_delete}"
            delete_url = f"{base_url}/employee/delete_employee/{emp_id_delete}"
            
            if st.button("Remove"):
                 response = requests.get(url)
                 
                 if response.status_code == 200:
                        raw_data = response.json()
                        
                        if "Data" in raw_data:
                            employee = raw_data["Data"]
                            c1, c2, = st.columns(2)
                            with c1:
                                        name = st.text_input("name", value=employee.get("name"))
                                        city = st.text_input("city", value=employee.get("city"))
                                        salary = st.number_input("salary", min_value=0, value=employee.get("salary"))
                            with c2:
                                        email = st.text_input("email", value=employee.get("email"))
                                        department = st.text_input("department", value=employee.get("department"))
                            
                            if st.button("Delete"):
                                result = requests.delete(delete_url)
                                
                                if result.status_code == 200:
                                    st.success("Employee Removed")
                                else:
                                    st.error("Server Error")
    elif choice == "Department":
        department_url = f"{base_url}/department"
        st.subheader("Department")
        tab1, tab2, tab3= st.tabs(["Show All", "Manage", "Employees"])
        
        with tab1:
            show_url = f"{department_url}/show_department"
            st.subheader("Departments:")
            
            response = requests.get(show_url)           
            if response.status_code == 200:
                    raw_data = response.json()
                    
                    if "Data" in raw_data:
                        department = raw_data["Data"]
                        df = pd.DataFrame(department)
                        st.dataframe(df, use_container_width=True, hide_index=True)
            
        with tab2:
            dept_choice = st.selectbox("Operations:", [" ", "Add Department", "Update Department", "Remove Department"])
            
            if dept_choice == "Add Department":
                st.subheader("Add Department")
                name = st.text_input("name", key="dept_name")
                
                if st.button("Add Department"):
                    full_url = f"{department_url}/add_department"
                    response = requests.post(full_url, json={"name":name})
                    
                    if response.status_code == 200:
                        st.success(f"{name}: Department Added")
                    else:
                        st.error("Server Error")
                        st.write(response.json())
                        
            elif dept_choice == "Update Department":
                st.subheader("Update Information")
                
                dept_id = st.number_input("department ID")
                name = st.text_input("name")
                update_url = f"{department_url}/update_department/{dept_id}"
                
                if st.button("Update"):
                    response = requests.put(update_url, json={"name":name})
                    
                    if response.status_code == 200:
                        st.success("Department updated")
                    else:
                        st.warning("something wrong")
            
            elif dept_choice == "Remove Department":
                st.subheader("Remove Department")
                
                dept_id = st.number_input("department id", min_value=1, key="remove_dept_key")
                fetch_dept = f"{base_url}/department/fetch_dept_id/{dept_id}"
                if st.button("remove"):
                    response = requests.get(fetch_dept)
                    if response.status_code == 200:
                        data = response.json()
                        df = pd.DataFrame([data])    
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        delete_dept_url = f"{department_url}/delete_department/{dept_id}"    
                        
                        if st.button("Delete"):
                            
                            result = requests.delete(delete_dept_url)
                            if result.status_code == 200:
                                st.success("This Department is no longer Used")
                            else:
                                st.warning("Server Error")
                                st.write(result.json())
        
        with tab3:
            st.subheader("Department Dashboard")
            
            department_dashboard_url = f"{department_url}/employww_per_deptartment"
            
            response = requests.get(department_dashboard_url)

            if response.status_code == 200:
                data = response.json()
                departments = data["Data"]
                df = pd.DataFrame(departments)

                total_departments = len(df)
                total_employees = df["Employees"].sum()

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Departments", total_departments)
                with col2:
                    st.metric("Total Employees", total_employees)

                st.divider()

                st.subheader("Employees Per Department")
                chart_df = df.set_index("Department")
                st.bar_chart(chart_df["Employees"])

                st.divider()

                st.subheader("Department Details")
                st.dataframe(df, use_container_width=True )
            else:
                st.error("Failed to load dashboard")
            
    elif choice == "Attendance":
        st.subheader("Employee Records")
        pass
    
    elif choice == "Salary":
        st.subheader("Salary Analysis")
        pass
        

init_session()

if not st.session_state.authenticated:
    cols = st.columns([1, 2, 1])
    with cols[1]: 
        auth_page()
else:
    main_dashboard()