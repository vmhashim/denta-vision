import streamlit as st
from PIL import Image

st.title('Denta Vision')
st.header('Upload a Tooth Image to Determine the Age')

uploaded_file = st.file_uploader('Upload an image', type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Tooth Image', use_column_width=True)
    st.write('Processing the image to determine the age...')
    determined_age = 25
    st.success(f'The determined age is: {determined_age} years')

st.write('Denta Vision - A tool to determine the age from tooth images')

