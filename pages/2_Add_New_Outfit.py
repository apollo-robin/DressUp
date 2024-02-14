from streamlit_cropperjs import st_cropperjs
from LibUploadFunctions import *
from time import sleep

st.markdown(f'<p style= "font-weight: bold; text-align:center; font-family:Courier; font-size:48px">'
            'Dress Up'
            ' <p>',
            unsafe_allow_html=True)

if 'login_user_id' not in st.session_state:
    st.markdown(f'<p style= "font-size:18px">Please login first to add new outfits<p>',
                unsafe_allow_html=True)
    st.stop()

if 'save_clicked' not in st.session_state:
    st.session_state.save_clicked = False

if 'file_uploader_key' not in st.session_state:
    st.session_state.file_uploader_key = 0

st.markdown(f'<p style= "font-size:18px">Add new outfits here<p>',
            unsafe_allow_html=True)

outfit_to_add = st.file_uploader("Add new outfits here", type=["png", "jpg", "jpeg"],
                                 key=st.session_state.file_uploader_key, label_visibility="collapsed",
                                 accept_multiple_files=False)

st.caption('Please add images of only _one_ outfit at a time')

cropper_container = st.empty()
outfit_container = st.container()

if outfit_to_add:
    bytes_image = outfit_to_add.read()
    with cropper_container:
        cropped_image = st_cropperjs(bytes_image, btn_text="Crop", key="cropper")
    if cropped_image:
        image_wo_bg = remove_bg(bytes_image)
        cropper_container.empty()
        with outfit_container:
            st.image(image_wo_bg, use_column_width="always")
            if st.button("Save"):
                st.session_state.save_clicked = True

if 'save_clicked' in st.session_state:
    if st.session_state.save_clicked:
        metadata = metadata_selector()
        if metadata and st.button("Store in Wardrobe"):
            image_url = upload_image(image_wo_bg)
            store_success = store_in_db(db, st.session_state.login_user_id, image_url, metadata)
            if store_success:
                st.success("Yay! Your outfit has beed added to your wardrobe")
                sleep(4)
                st.session_state.save_clicked = False
                st.session_state["file_uploader_key"] += 1
                st.rerun()
            else:
                st.error("Oopsie! Somwthing's not right. Try again, please")
