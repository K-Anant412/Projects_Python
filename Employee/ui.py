import streamlit as st
import requests
import base64
import os
import pandas as pd

AUTH_URL = "http://127.0.0.1:5001/api/v1/auth"

base_url = "http://127.0.0.1:5001/api/v1"

def get_base64(bin_file):
    with open(bin_file, "rb") as f:
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
        unsafe_allow_html=True,
    )

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = None

def login_user(email, password):
    try:
        response = requests.post(
            f"{AUTH_URL}/login", json={"email": email, "password": password}
        )
        if response.status_code == 200:
            st.session_state.authenticated = True
            st.session_state.user_data = response.json().get("Data", {})
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
        "role": role,
    }
    try:
        response = requests.post(f"{AUTH_URL}/Register", json=payload)
        if response.status_code == 200:
            st.success("Registration Successful! Please Login.")
        else:
            st.error(response.json().get("message", "Registration Failed"))
    except Exception as e:
        st.error(f"Connection Error: {e}")

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
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding:15px; border-radius:10px; background-color:#f0f2f6; margin-bottom:20px; border:1px solid #d1d5db">
                <h4 style="margin:0;">👤 {st.session_state.user_data.get('user_name', 'User')}</h4>
                <p style="color:gray; font-size:14px; margin:0;">Role: {st.session_state.user_data.get('Role', 'N/A')}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.subheader("Management")
        choice = st.radio("Go to:", ["Employee", "Department", "Attendance", "Salary"])
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()
    st.title(f"Welcome ")

    if choice == "Employee":
        st.subheader("Employee Management")
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Home" ,"Manage", "Employee List", "Search"]
        )
        employee_url = f"{base_url}/employee"
        
        with tab1:
            BASE_URL = "http://127.0.0.1:5001/api/v1"

            st.set_page_config(
                page_title="Employee Dashboard",
                layout="wide"
            )

            st.title("Employee Management Dashboard")
            st.caption("Manage employees, analytics, reports, and departments.")

            st.divider()

            response = requests.get(
                f"{BASE_URL}/employee/show_employee?page=1&per_page=10"
            )
            data = response.json()
            employees = data.get("Data", [])
            df = pd.DataFrame(employees)


            if not df.empty:
                total_emp = len(df)
                avg_salary = round(df["salary"].astype(float).mean(), 2)
                max_salary = df["salary"].astype(float).max()
                total_departments = df["department"].nunique()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Employees", total_emp)
                with col2:
                    st.metric("Departments", total_departments)
                with col3:
                    st.metric("Average Salary", f"₹ {avg_salary}")
                with col4:
                    st.metric("Highest Salary", f"₹ {max_salary}")

            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Department Distribution")
                dept_data = df["department"].value_counts()
                st.bar_chart(dept_data)
            with col2:
                st.subheader("Salary Distribution")
                salary_data = df["salary"].astype(float)
                st.line_chart(salary_data)

            st.divider()


            st.subheader("Recently Added Employees")
            recent_df = df.tail(5)
            st.dataframe(
                recent_df,
                use_container_width=True
            )
            
            st.divider()

            st.subheader("Top Paid Employees")
            top_salary = df.sort_values(
                by="salary",
                ascending=False
            ).head(5)
            st.dataframe(
                top_salary,
                use_container_width=True
            )
            
        with tab2:
            st.subheader("Manage Employees")
            
            choice = st.selectbox(">", options=["Add Employee", "Update Employee", "Remove Employee", "Reports"])
            if choice == "Add Employee":
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
                            "name": name,
                            "city": city,
                            "email": email,
                            "salary": salary,
                            "department": department,
                        }
                        try:
                            response = requests.post(
                                f"{employee_url}/add_employee", json=data
                            )
                            if response.status_code == 200:
                                st.success("New employee added")
                            else:
                                st.error("Failed to add user.")
                        except Exception as e:
                            st.error(f"Server Error: {e}")
            elif choice == "Update Employee":
                emp_id = st.number_input("Employee ID", min_value=1, step=1)
                fetch_url = f"{employee_url}/employee_by_id/{emp_id}"
                update_url = f"{employee_url}/update_employee/{emp_id}"
                
                if st.button("Fetch Employee"):
                    response = requests.get(fetch_url)
                    if response.status_code == 200:
                        raw_data = response.json()
                        if "Data" in raw_data:
                            st.session_state.employee = raw_data["Data"]
                        else:
                            st.error("Employee data not found")
                    else:
                        st.error("Employee not found")
                        
                if "employee" in st.session_state:
                    employee = st.session_state.employee
                    c1, c2 = st.columns(2)
                    with c1:
                        name = st.text_input("Name", value=employee.get("name", ""))
                        city = st.text_input("City", value=employee.get("city", ""))
                        salary = st.number_input(
                            "Salary", min_value=0, value=int(employee.get("salary", 0))
                        )
                    with c2:
                        email = st.text_input("Email", value=employee.get("email", ""))
                        department = st.text_input(
                            "Department", value=employee.get("department", "")
                        )
                        
                    if st.button("Save Changes"):
                        params = {
                            "name": name,
                            "city": city,
                            "email": email,
                            "salary": salary,
                            "department": department,
                        }
                        response = requests.put(update_url, json=params)
                        if response.status_code == 200:
                            st.session_state.employee = params
                        else:
                            st.error(response.text)
            elif choice == "Remove Employee":
                emp_id_delete = st.number_input( "employee ID", min_value=0, key="delete_employee" )
                url = f"{employee_url}/employee_by_id/{emp_id_delete}"
                delete_url = f"{employee_url}/delete_employee/{emp_id_delete}"

                if st.button("Remove"):
                    response = requests.get(url)

                    if response.status_code == 200:
                        raw_data = response.json()

                        if "Data" in raw_data:
                            employee = raw_data["Data"]
                            (
                                c1,
                                c2,
                            ) = st.columns(2)
                            with c1:
                                name = st.text_input("name", value=employee.get("name"))
                                city = st.text_input("city", value=employee.get("city"))
                                salary = st.number_input(
                                    "salary", min_value=0, value=employee.get("salary")
                                )
                            with c2:
                                email = st.text_input("email", value=employee.get("email"))
                                department = st.text_input(
                                    "department", value=employee.get("department")
                                )

                            if st.button("Delete"):
                                result = requests.delete(delete_url)

                                if result.status_code == 200:
                                    st.success("Employee Removed")
                                else:
                                    st.error("Server Error")
            elif choice == "Reports":
                API_URL = f"{employee_url}/get_pdf_data"

                if st.button("Download Employee PDF"):

                    response = requests.get(API_URL)

                    if response.status_code == 200:

                        st.download_button(
                            label="Click Here to Download",
                            data=response.content,
                            file_name="employees.pdf",
                            mime="application/pdf"
                        )

                        st.success("PDF generated successfully!")

                    else:
                        st.error("Failed to generate PDF")
        
        with tab3:
            st.subheader("Employee List")
            c1, c2 = st.columns(2)
            with c1:
                page = st.number_input("Pages", min_value=1)
            with c2:
                per_page = st.selectbox("Employees Per Page", options=[5, 10, 15, 20])

            params = {"page": int(page), "per_page": int(per_page)}
            get_url = f"{employee_url}/show_employee"

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
            st.subheader("Search Employee")

            emp_id = st.number_input("Employee ID:", min_value=1, key="search_key")
            employee_search_url = f"{employee_url}/employee_by_id/{emp_id}"

            if st.button("Search"):
                response = requests.get(employee_search_url)

                if response.status_code == 200:
                    raw_data = response.json()

                    if "Data" in raw_data:
                        employee = raw_data["Data"]
                        df = pd.DataFrame([employee])
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.warning(f"Error: {response.json()}")
    
    elif choice == "Department":
        department_url = f"{base_url}/department"
        st.subheader("Department")
        tab1, tab2, tab3 = st.tabs(["Show All", "Manage", "Employees"])

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
            dept_choice = st.selectbox(
                "Operations:",
                [" ", "Add Department", "Update Department", "Remove Department"],
            )

            if dept_choice == "Add Department":
                st.subheader("Add Department")
                name = st.text_input("name", key="dept_name")

                if st.button("Add Department"):
                    full_url = f"{department_url}/add_department"
                    response = requests.post(full_url, json={"name": name})

                    if response.status_code == 200:
                        st.success(f"{name}: Department Added")
                    else:
                        st.error("Server Error")
                        st.write(response.json())

            elif dept_choice == "Update Department":
                st.subheader("Update Information")

                dept_id = st.number_input("department ID", value=0)
                name = st.text_input("name")
                update_url = f"{department_url}/update_department/{dept_id}"

                if st.button("Update"):
                    response = requests.put(update_url, json={"name": name})

                    if response.status_code == 200:
                        st.success("Department updated")
                    else:
                        st.warning("something wrong")

            elif dept_choice == "Remove Department":
                st.subheader("Remove Department")

                dept_id = st.number_input(
                    "department id", min_value=1, key="remove_dept_key"
                )
                fetch_dept = f"{base_url}/department/fetch_dept_id/{dept_id}"
                if st.button("remove"):
                    response = requests.get(fetch_dept)
                    if response.status_code == 200:
                        data = response.json()
                        df = pd.DataFrame([data])
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        delete_dept_url = (
                            f"{department_url}/delete_department/{dept_id}"
                        )

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
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.error("Failed to load dashboard")
    
    elif choice == "Attendance":
        st.subheader("Employee Records")
        st.subheader("📋 Employee Attendance")

        try:
            response = requests.get(f"{base_url}/employee_records/employees")
            result = response.json()
            employees = result.get("Message", [])
        except Exception as e:
            st.error(f"Failed to fetch employees: {e}")
            st.stop()

        if not employees:
            st.warning("No employees found.")
            st.stop()

        attendance_records = []
        status_options = ["Present", "Absent", "Sick Leave", "Half Day"]
        with st.form("attendance_form"):
            for i, emp in enumerate(employees):
                current_status = emp.get("Attendance Marked", "Not Marked")
                with st.container(border=True):

                    col1, col2, col3 = st.columns([2, 2, 2])
                    with col1:
                        st.write(f"### 👤 {emp['Name']}")
                    with col2:
                        st.write(f"**ID:** {emp['ID']}")
                    with col3:
                        st.write(f"**Department:** {emp['Department']}")
                    st.info(f"Current Status: {current_status}")
                    selected_status = st.selectbox(
                        f"Attendance for {emp['Name']}",
                        status_options,
                        key=f"attendance_{emp['ID']}_{i}",
                    )

                    attendance_records.append(
                        {"employee_id": emp["ID"], "status": selected_status}
                    )

            submit = st.form_submit_button(
                "Submit Attendance", use_container_width=True
            )

        if submit:
            payload = {"records": attendance_records}
            try:
                response = requests.post(
                    f"{base_url}/employee_records/attendance", json=payload
                )
                result = response.json()
                if response.status_code in [200, 201]:
                    st.success(
                        result.get("message", "Attendance submitted successfully")
                    )
                    st.balloons()
                    st.rerun()
                else:
                    st.error(result.get("message", "Something went wrong"))
            except Exception as e:
                st.error(f"Failed to submit attendance: {e}")

        st.divider()

        st.subheader("📄 Today's Attendance")
        table_data = []
        for emp in employees:
            table_data.append(
                {
                    "Employee ID": emp["ID"],
                    "Name": emp["Name"],
                    "Department": emp["Department"],
                    "Attendance": emp.get("Attendance Marked", "Not Marked"),
                }
            )
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    elif choice == "Salary":
        st.subheader("Salary Analysis")
        emp_id = st.number_input("Employee ID:", min_value=1, key="employee_salary_id")
        employee_Search_url = f"{base_url}/employee_records/month_analysis/{emp_id}"
        if st.button("Calculate"):
            response = requests.get(employee_Search_url)

            if response.status_code == 200:
                raw_data = response.json()

                if "Data" in raw_data:
                    employee = raw_data["Data"]
                    df = pd.DataFrame([employee])
                    st.write("Employee Details:")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"Error: {response.json()}")
            else:
                st.warning(f"Error: {response.json()}")

init_session()

if not st.session_state.authenticated:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        auth_page()
else:
    main_dashboard()