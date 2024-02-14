import streamlit as st
from firebase_admin import auth
import json
import requests
from streamlit_extras.switch_page_button import switch_page

FIREBASE_WEB_API_KEY = st.secrets.web_api_key
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


# Function to create a new user
def create_user(username, email, password, confirm_password):
    if password != confirm_password:
        st.error("Passwords do not match.")
        return False
    else:
        try:
            user = auth.create_user(email=email, password=password, uid=username)
            st.success("Your Digital Wardrobe is now ready to be stacked")
            return True
        except ValueError as error:
            st.error(error.args[0])
        else:
            st.error("Uh,ho! Something went wrong on our end. Please try again.")
    return False


# Function to take a new user to a login page
def update_new_user(success):
    if success:
        st.session_state.new_user_input = "Yes, take me there!"


# Function to create the signing up form
def signup_form():
    with st.form(key="signup_form"):
        username = st.text_input("Username", placeholder="Your Digital Wardrobe's name")
        email = st.text_input("Email", placeholder="Tell us your email id")
        password = st.text_input("Password", placeholder="Choose a strong one", type="password")
        confirm_password = st.text_input("Confirm Password", placeholder="Make sure you remember")
        signup = st.form_submit_button("Let's build my digital wardrobe")
    if signup:
        create_success = create_user(username, email, password, confirm_password)
        if create_success:
            st.button("Go to wardrobe", on_click=update_new_user, args=[create_success])


# Function to create the login form
def login_form():
    with st.form(key="login_form"):
        email = st.text_input("Email", placeholder="Enter your email here")
        password = st.text_input("Password", placeholder="Your password goes here", type="password")
        login = st.form_submit_button("Show me my clothes")
    if login:
        user_id = login_with_email_and_password(email, password)
        if user_id:
            st.write(user_id)
            if 'login_user_id' not in st.session_state:
                st.session_state.login_user_id = user_id
                # st.experimental_rerun()
                switch_page('Go_to_Wardrobe')


# Function to log in an user
def login_with_email_and_password(email, password, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })
    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload).json()
    if 'localId' in r:
        return r['localId']
    if 'error' in r:
        st.error("Invalid  Credentials")
        return None
