import streamlit as st
import requests
import pandas as pd

base_url = "http://127.0.0.1:5001/api/v1"

st.title("Employee Management System")
st.write("welcome to my employee management system")

menu = st.sidebar.selectbox("Menu", ["Home", "Employee", "Department"])

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
elif menu == "Department":
    dep_menu = st.sidebar.selectbox("select",[
                                                "Show all",
                                                "Add departent",
                                                "Update department",
                                                "Remove department"
                                               ])