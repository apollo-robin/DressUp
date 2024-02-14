from LibUploadFunctions import *

st.markdown(f'<p style= "font-weight: bold; text-align:center; font-family:Courier; font-size:48px">'
            'Dress Up'
            ' <p>',
            unsafe_allow_html=True)

if 'login_user_id' not in st.session_state:
    st.markdown(f'<p style= "font-size:18px">Please login, to enter your digital wardrobe<p>',
                unsafe_allow_html=True)
    st.stop()

with st.sidebar.expander("Filters", expanded=False):
    wear_type = []
    category = []
    sleeve_length = []
    dress_length = []
    gender = st.multiselect("This fits:", gender_list, default=None)

    if len(gender):
        wear_type = st.multiselect("Top/Bottom/Foot wear", wear_list, default=None)

    category_list = []
    if 'Women' in gender:
        if 'Topwear' in wear_type:
            category_list += w_top_category_list
        if 'Bottomwear' in wear_type:
            category_list += w_bottom_category_list
        if 'Footwear' in wear_type:
            category_list += w_foot_category_list
    if 'Men' in gender:
        if 'Topwear' in wear_type:
            category_list += m_top_category_list
        if 'Bottomwear' in wear_type:
            category_list += m_bottom_category_list
        if 'Footwear' in wear_type:
            category_list += m_foot_category_list

    category_list = list(set(category_list))
    if len(wear_type):
        category = st.multiselect("Category", category_list, default=None)

    if "Topwear" in wear_type:
        sleeve_length = st.multiselect("Sleeve Length", sleeve_length_list, default=None)

    if "Dress" in category:
        dress_length = st.multiselect("Dress Length", dress_length_list, default=None)

    filters = {
        'gender': gender,
        'wear_type': wear_type,
        'category': category,
        'sleeve_length': sleeve_length,
        'dress_length': dress_length
    }
    apply_filters = st.button("Apply Filters")


outfit_container = st.empty()
with outfit_container.container():
    image_urls = get_outfits_with_filter(db, st.session_state.login_user_id, {})
    show_outfits(image_urls)


if apply_filters:
    outfit_container.empty()
    image_urls = get_outfits_with_filter(db, st.session_state.login_user_id, filters)
    show_outfits(image_urls)