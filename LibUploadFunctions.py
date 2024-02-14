import streamlit as st
import rembg
from PIL import Image
from firebase_admin import storage
from io import BytesIO
import random
from google.cloud import firestore
import io
from google.cloud.firestore_v1 import FieldFilter
import json
from google.oauth2 import service_account

key = json.loads(st.secrets.service_account_key)
creds = service_account.Credentials.from_service_account_info(key)
db = firestore.Client(credentials=creds)

@st.cache_data
def remove_bg(bytes_image):
    image = Image.open(io.BytesIO(bytes_image))
    return rembg.remove(image, bgcolor=[255, 255, 255, 255])


def upload_image(image):
    try:
        image_stream = BytesIO()
        image.save(image_stream, format='png')
        image_stream.seek(0)
        bucket = storage.bucket('dressup-2eeb0.appspot.com')
        blob = bucket.blob(str(random.randint(1, 1000000000)))
        blob.upload_from_file(image_stream, content_type='image/png')
        blob.make_public()
        image_stream.close()
        return blob.public_url
    except:
        return None


def store_in_db(db, user_id, image_url, metadata):
    try:
        doc_ref = db.collection(user_id).document()
        doc_ref.set({
            'image_1': image_url,
            'gender': metadata['gender'],
            'category': metadata['category'],
            'wear_type': metadata['wear_type'],
            'sleeve_length': metadata['sleeve_length'],
            'dress_length': metadata['dress_length']
        })
        return True
    except:
        return False


gender_list = ["Women", "Men"]
wear_list = ["Topwear", "Bottomwear", "Footwear"]
m_top_category_list = ["T-shirt", "Shirt", "Sweatshirt", "Sweater", "Jacket"]
m_bottom_category_list = ["Jeans", "Trousers", "Shorts", "Track Pants"]
m_foot_category_list = ["Sport Shoes", "Formal Shoes", "Casual Shoes", "Sandals & Floaters"]

w_top_category_list = ["Dress", "Top", "Tee", "Shirt", "Sweatshirt", "Sweater", "Jacket", "Kurti", "Suit"]
w_bottom_category_list = ["Jeans", "Trousers", "Shorts", "Palazzo", "Legging", "Track Pants", "Salvar"]
w_foot_category_list = ["Heels", "Sport Shoes", "Formal Shoes", "Casual Shoes", "Sandals & Floaters", "Boots"]

sleeve_length_list = ["Full Sleeves", "Half Sleeves", "Sleeveless"]
dress_length_list = ["Mini", "Midi", "Maxi"]


def metadata_selector():
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)
    gender = None
    wear_type = None
    category = None
    sleeve_length = None
    dress_length = None
    gender = c1.selectbox("This fits:", gender_list, index=None)
    if gender:
        wear_type = c2.selectbox("Top/Bottom/Foot wear", wear_list, index=None)
        if wear_type:
            if gender == "Women":
                if wear_type == "Topwear":
                    category = c3.selectbox("Category", w_top_category_list, index=None)
                elif wear_type == "Bottomwear":
                    category = c3.selectbox("Category", w_bottom_category_list, index=None)
                else:
                    category = c3.selectbox("Category", w_foot_category_list, index=None)
            else:
                if wear_type == "Topwear":
                    category = c3.selectbox("Category", m_top_category_list, index=None)
                elif wear_type == "Bottomwear":
                    category = c3.selectbox("Category", m_bottom_category_list, index=None)
                else:
                    category = c3.selectbox("Category", m_foot_category_list, index=None)
        if category and wear_type == "Topwear":
            sleeve_length = c4.selectbox("Sleeve Length", sleeve_length_list, index=None)
        if category == "Dress":
            dress_length = c5.selectbox("Dress Length", dress_length_list, index=None)

    if category:
        return {
            'gender': gender,
            'wear_type': wear_type,
            'category': category,
            'sleeve_length': sleeve_length,
            'dress_length': dress_length
        }
    else:
        return False


def get_outfits_with_filter(_db, user_id, filters):
    query = db.collection(user_id)
    for key, value in filters.items():
        if len(value):
            query = query.where(filter=FieldFilter(key,'in',value))
    docs = query.stream()
    image_urls = []
    for doc in docs:
        doc_fields = doc.to_dict()
        image_urls.append(doc_fields['image_1'])
    return image_urls


def show_outfits(image_urls,on_load:bool = False):
    message = "OOPSIE! There's nothing in your wardrobe." if on_load else "OOPSIE! Currently no outfit matches your selected filters"
    if not len(image_urls):
        st.markdown(f"<p style= 'font-size:18px'>{message}<br>Maybe it's time to shop :)<p>",
                    unsafe_allow_html=True)
        st.stop()
    for url in image_urls:
        with st.container(border=True):
            st.image(url, use_column_width="always")