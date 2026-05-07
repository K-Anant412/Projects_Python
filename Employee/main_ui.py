import streamlit as st 
from Frontend.register import signup_form
from Frontend.home_page import home

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def main():
    if not st.session_state.logged_in:
        
        st.sidebar.title("Welcome")
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)
        
        if choice == "Register":
            signup_form()
        elif choice == "Login": # just for UI design.....
            home()
        else:
            st.info("Login functionality goes here")
            
            
    else:
        st.title("Main Dashboard")
        st.write("You are now logged in!")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        # home()
if __name__ == "__main__":
    main()