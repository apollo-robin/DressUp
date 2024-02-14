import firebase_admin
from firebase_admin import credentials, initialize_app
from LibUserFunctions import *
from PIL import Image

favicon = Image.open("favicon.jpg")
st.set_page_config( page_title="DressUp", page_icon=favicon)

# Initialize App if not already
if not firebase_admin._apps:
    cred = credentials.Certificate(
        "C://Users//robin//OneDrive - Indian Institute of Management//Self Projects//Outfit "
        "Recommendation//dressup-2eeb0-5f6a92426646.json")
    initialize_app(cred, {'storageBucket': 'dressup-2eeb0.appspot.com'})


st.markdown(f'<p style= "font-weight: bold; text-align:center; font-family:Courier; font-size:48px">'
            'Dress Up'
            ' <p>',
            unsafe_allow_html=True)


def home_page():
    st.markdown(f'<p style= "text-align:center; font-size:18px">'
                'Welcome to Dress Up!<br>'
                'your wardrobe at your fingertips<br>'
                'Look at all your clothes at once,<br> skip the hassle of digging your physical wardrobe<br><br>'
                ' <p>',
                unsafe_allow_html=True)

    st.markdown(f'<p style= "text-align:center; font-family:Courier; font-size:22px">'
                'Swipe > Select > Wear <br>'
                ' <p>',
                unsafe_allow_html=True)

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    new_user = st.radio("Have you set up your Digital Wardrobe?",
                        options=["Yes, take me there!", "No, help me build one"], index=None, key="new_user_input")

    if new_user == "Yes, take me there!":
        login_form()
    elif new_user == "No, help me build one":
        signup_form()


if 'login_user_id' in st.session_state:
    st.markdown(f"<p style= 'font-size:18px'>Hi {st.session_state.login_user_id}, you're "
                f"already logged in.You can choose to Go to your wardrobe or Add New Outfits.<p>",
                unsafe_allow_html=True)
else:
    home_page()
