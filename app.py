import streamlit as st
from PIL import Image
import cv2
import numpy as np
import tempfile

# Frontend: Streamlit interface with logo, title, and background image
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: black;  /* Changed to black color */
        font-size: 50px;
        font-weight: bold;
        margin-top: 20px;
    }
    .logo {
        display: block;
        margin: 0 auto;
        width: 100px;  /* Set width to 100px */
        height: 110px; /* Set height to 110px */
        object-fit: cover; /* Maintain aspect ratio, cover the container */
    }
    body {
        background: url('https://raw.githubusercontent.com/vmhashim/denta-vision/main/assets/bg.jpg') no-repeat center center fixed; 
        background-size: cover;  /* Cover the entire window */
    }
    .footer {
        position: fixed;
        bottom: 10px;
        left: 10px;
        font-size: 12px;
        color: #000000; /* Black color for text */
    }
    .stFileUploader > div {
        border-radius: 12px;  /* Rounded corners */
        border: 2px solid #ccc;  /* Border color */
        padding: 20px;  /* Padding around the button */
        background-color: #ffffff;  /* Background color of the upload area */
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1); /* Shadow for a subtle 3D effect */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the logo
st.markdown('<img class="logo" src="https://raw.githubusercontent.com/vmhashim/denta-vision/main/assets/logo.jpg" alt="Logo">', unsafe_allow_html=True)

st.markdown('<div class="title">DENTA VISION</div>', unsafe_allow_html=True)
st.write("Upload a Tooth Image to Determine the Age")

# File uploader and image processing
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)
    _, segmented = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return enhanced, segmented

def extract_features(enhanced, segmented):
    attrition = np.mean(segmented) / 255.0
    periodontosis = np.mean(segmented[:50, :]) / 255.0
    secondary_dentin = 1 - np.mean(enhanced[enhanced.shape[0]//3:2*enhanced.shape[0]//3, 
                                            enhanced.shape[1]//3:2*enhanced.shape[1]//3]) / 255.0
    cementum = np.mean(segmented[3*segmented.shape[0]//4:, :]) / 255.0
    root_resorption = 1 - cementum
    transparency = np.mean(enhanced[3*enhanced.shape[0]//4:, :]) / 255.0
    
    tooth_width = np.sum(segmented, axis=0).max()
    tooth_height = np.sum(segmented, axis=1).max()
    width_height_ratio = tooth_width / tooth_height if tooth_height != 0 else 0
    
    return [attrition, periodontosis, secondary_dentin, cementum, root_resorption, transparency, width_height_ratio]

def score_feature(value):
    if value < 0.25:
        return 0
    elif value < 0.5:
        return 1
    elif value < 0.75:
        return 2
    else:
        return 3

def estimate_age(features):
    age_features = features[:6]
    feature_scores = [score_feature(f) for f in age_features]
    total_score = sum(feature_scores)
    estimated_age = 20 + (total_score * 3)
    return estimated_age

# Processing the uploaded image
if uploaded_file is not None:
    # Use a temporary file to save the uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name
    
    st.image(uploaded_file, caption='Uploaded Tooth Image', use_column_width=True)
    st.write('Processing the image to determine the age...')
    
    # Preprocess and analyze the image
    enhanced, segmented = preprocess_image(temp_file_path)
    features = extract_features(enhanced, segmented)
    estimated_age = estimate_age(features)
    
    # Display only the estimated age
    st.write(f'Estimated Age: {estimated_age:.1f} years')

# Footer
st.markdown(
    """
    <div class="footer">
        Powered by<br>
        Abdul Rehaman<br>
        Bilal Khan<br>
        Mohammad Hisham Hassan<br>
        V M Hashim
    </div>
    """,
    unsafe_allow_html=True
)
