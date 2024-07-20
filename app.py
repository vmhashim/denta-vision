import streamlit as st
from PIL import Image

# Set the title and header
st.title('Denta Vision')
st.header('Upload a Tooth Image to Determine the Age')

# Custom CSS for background image
page_bg_img = '''
<style>
body {
    background-image: url("https://drive.google.com/file/d/1ldfOYvTr0HJBa_wcXTjYgpImjCWrKSes/view?usp=drive_link");
    background-size: cover;
}
</style>
'''

# Inject CSS with st.markdown
st.markdown(page_bg_img, unsafe_allow_html=True)

# File uploader and image processing
uploaded_file = st.file_uploader('Upload an image', type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Tooth Image', use_column_width=True)
    st.write('Processing the image to determine the age...')
    determined_age = 25  # This would be your actual age determination logic
    st.success(f'The determined age is: {determined_age} years')

st.write('Denta Vision - A tool to determine the age from tooth images')
