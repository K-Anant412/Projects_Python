import streamlit as st
import requests

# Configuration
API_URL = "http://127.0.0.1:5001/api/v1/auth"

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = None

def login_user(email, password):
    try:
        response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
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
        response = requests.post(f"{API_URL}/Register", json=payload)
        if response.status_code == 200:
            st.success("Registration Successful! Please Login.")
        else:
            st.error(response.json().get("message", "Registration Failed"))
    except Exception as e:
        st.error(f"Connection Error: {e}")

# --- UI COMPONENTS ---

def auth_page():
    st.title("🚀 Employee Management System")
    
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
        
        # Navigation
        st.subheader("Management")
        choice = st.radio("Go to:", ["Employee", "Department", "Attendance", "Salary"])
        
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()

    # 2. Page Logic
    st.title(f"Welcome back, {st.session_state.user_data.get('user_name', 'User')}!")
    
    if choice == "Employee":
        st.subheader("Employee Management")
        sub_opt = st.selectbox("Action", ["Add Employee", "Delete Employee", "Update Employee", "View List"])
        st.info(f"You selected: {sub_opt}")
        # Call your Flask Employee routes here...

# --- APP FLOW ---
init_session()

if not st.session_state.authenticated:
    # This acts as your "Pop up" / Initial screen
    cols = st.columns([1, 2, 1])
    with cols[1]: # Center the form
        auth_page()
else:
    main_dashboard()