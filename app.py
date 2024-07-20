import streamlit as st
from PIL import Image

# Set the title and header
st.title('Denta Vision')
st.header('Upload a Tooth Image to Determine the Age')

# Custom CSS for background image
page_bg_img = '''
<style>
body {
    background-image: url("https://img.freepik.com/free-vector/happy-kid-sitting-big-tooth-white-background_1308-92753.jpg?t=st=1721447628~exp=1721451228~hmac=36e9f8e5199589c02c6f717f8b98cb4b1da57b04b17de019d65ca294d61d3c66&w=360");
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
