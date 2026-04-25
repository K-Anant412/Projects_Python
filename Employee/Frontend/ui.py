import streamlit as st
import requests
import pandas as pd

base_url = "http://127.0.0.1:5001/api/v1"

st.markdown("""
<style>
     .centered-title {
        display: flex;
        justify-content: center;
        align-items: left;
        flex-direction: column;
        width: 60vw;
        height: 60vh; 
    }
    .stApp {
        background-color: #C0E1D2;
    }
    
    h1, h2, h3 {
        color: #00FFAA;
    }

    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
    }
    .heading{
        font-size: 80px !important;
        font-weight: 700;
    }
    section[data-testid="stSidebar"] {
    background-color: #DC9B9B;
    }
</style>
""", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["Home", "Employee", "Department", "Sign-in"])

if menu == "Home":
   st.markdown("""
    <div class="centered-title">
        <p class="heading">Employee</p>
        <p class="heading">Management</p>
        <p class="heading">System</p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "Employee":
    emp_menu = st.sidebar.selectbox("select", [
                                                "Show all", 
                                                "Add employee", 
                                                "Update employee", 
                                                "Delete employee", 
                                                "Find by ID", 
                                                "Find by salary"
                                                ])
    if emp_menu == "Show all":
           
            st.header("Employee List")
            
            col1, col2 = st.columns(2)
            with col1:
                page = st.number_input("Page Number", min_value=1, value=1)
            with col2:
                per_page = st.selectbox("Employees per page",[1, 5, 10] ,index=1)
            
            if st.button("Show Employees"):
                params = {
                    "page": page,
                    "per_page": per_page
                }
                try:
                    full_url = f"{base_url}/employee/show_employee"
                    res = requests.get(full_url, params=params)
                    
                    if res.status_code == 200:
                        response_data = res.json()
                        
                        if isinstance(response_data, dict):
                            employees = response_data.get("Data", 
                                        response_data.get("data", 
                                        response_data.get("items", [])))
                        else:
                            employees = response_data

                        if employees and len(employees) > 0:
                            df = pd.DataFrame(employees)
                            
                            st.success("Data fetched successfully!")
                            st.subheader(f"Displaying {len(df)} Employees")
  
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.warning("No employee records found in the 'Data' list.")
                            
                    else:
                        st.error(f"API Error: {res.status_code}")
                        st.info(f"Details: {res.text}")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    
    elif emp_menu == "Add employee":
        st.header("Add new Employee")
        
        col1, col2, col3 = st.columns(3)
        
        with col2:
          name = st.text_input("Employee name") 
          city = st.text_input("employee city")
          email = st.text_input("employee email")
          salary = st.number_input("salary")
          department = st.selectbox("Department", ["HR", "Python Programmer", "UI/UX designer", "Java developer"])
          
          if st.button("Add Employee"):
              params = {
                  "name": name,
                  "city": city,
                  "email": email,
                  "salary": str(salary),
                  "department": department
              }
              
              try:
                full_url = f"{base_url}/employee/add_employee"
                res = requests.post(full_url, json=params)   
                
                if res.status_code == 200:
                    st.success("Employee was added") 
                else:
                    st.error(res.text)
                    
              except Exception as e:
                      st.error(e)
          
    elif emp_menu == "Update employee":
        st.header("Update Employee")
        
        emp_id = st.number_input("id")
        
        name = st.text_input("Employee name") 
        email = st.text_input("employee email")
        salary = st.number_input("salary")
   
        params = {
                  "name": name,
                  "email": email,
                  "salary": str(salary),
              }
        
        if st.button("Update Employee"):
            url = f"{base_url}/employee/update_employee/{int(emp_id)}"
            st.write(url)
            
            res = requests.put(url, json=params)
            
            if res.status_code == 200:
                st.success("Employee Updated")
            else:
                st.warning("Something wrong....")           

    elif emp_menu == "Find by ID":
        st.header("Find Employee by ID")
        
        emp_id = st.number_input("id", min_value=1, value=1)
        
        if st.button("Show Employee"):
            try:
                url = f"{base_url}/employee/emp_by_id/{emp_id}"
                res = requests.get(url)
                
                if res.status_code == 200:
                    data = res.json()

                    status = data.get("Status")
                    message = data.get("Message")
                    emp_data = data.get("Data")

                    df = pd.DataFrame([emp_data])

                    df["Status"] = status
                    df["Message"] = message

                    st.dataframe(df)
                else:
                    st.error("Something is wrong...")
            except Exception as e:
                st.error(e)

elif menu == "Department":
    dep_menu = st.sidebar.selectbox("select",[
                                                "Show all",
                                                "Add departent",
                                                "Update department",
                                                "Remove department"
                                               ])
elif menu == "Sign-in":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input("Enter username")
        password = st.text_input("Password")
    with col2:
        email = st.text_input("Enter email")
        role = st.text_input("Role")
        
        if st.button("Sign-in"):
                params = {
                    'user_name': name,
                    'email': email,
                    'password': password,
                    'role': role
                }
                try:
                    full_url = f"{base_url}/auth/Register" 
                    res = requests.post(full_url, json=params)
                    
                    if res.status_code == 200:
                        st.success("Thank you for Sign-in") 
                    else:
                        st.error(f"Error {res.status_code}: {res.text}")
                                         
                except Exception as e:
                    st.error(e)
        
    