import streamlit as st
import requests

base_url = "http://127.0.0.1:5001/api/v1"

def signup_form():
    st.header("Create new Account")
    
    name = st.text_input("Full name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Admin", "Employee"])
    
    if st.button("Register"):
        payload = {
            "user_name":name,
            "email":email,
            "password":password,
            "role":role
        }
        
        try:
            full_url = f"{base_url}/auth/Register"
            response = requests.post(full_url, json=payload)
            
            if response.status_code == 200 or response.status_code == 201:
                st.success("Registration Successful!")
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_role = role
                
                st.rerun()
            else:
                error_data = response.json()
                print(error_data)
                st.error(f"Status {response.status_code}: {error_data.get('message', 'Validation Error')}")
                if 'errors' in error_data:
                    st.json(error_data['errors'])
        except Exception as e:
            st.error(f"Connection failed: {e}")