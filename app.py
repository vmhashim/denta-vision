import streamlit as st
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Frontend: Streamlit interface
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: red;
        font-size: 50px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    return estimated_age, feature_scores

def analyze_gender_characteristics(width_height_ratio):
    if width_height_ratio > 0.95:
        return "The width-to-height ratio suggests characteristics more commonly associated with male teeth."
    elif width_height_ratio < 0.85:
        return "The width-to-height ratio suggests characteristics more commonly associated with female teeth."
    else:
        return "The width-to-height ratio is in an intermediate range and doesn't strongly suggest male or female characteristics."

# Processing the uploaded image
if uploaded_file is not None:
    # Save the uploaded image to a temporary file
    image = Image.open(uploaded_file)
    image_path = 'uploaded_image.jpg'
    image.save(image_path)
    
    st.image(image, caption='Uploaded Tooth Image', use_column_width=True)
    st.write('Processing the image to determine the age...')
    
    # Preprocess and analyze the image
    enhanced, segmented = preprocess_image(image_path)
    features = extract_features(enhanced, segmented)
    estimated_age, feature_scores = estimate_age(features)
    gender_analysis = analyze_gender_characteristics(features[-1])
    
    # Display results
    st.write(f'Estimated Age: {estimated_age:.1f} years')
    st.write(f'Gender Analysis: {gender_analysis}')
    st.write(f'Width-to-Height Ratio: {features[-1]:.2f}')
    
    feature_names = ['Attrition', 'Periodontosis', 'Secondary Dentin', 'Cementum Apposition', 'Root Resorption', 'Root Transparency']
    st.write("\nFeature Scores:")
    for name, score in zip(feature_names, feature_scores):
        st.write(f"{name}: {score}")
    
    # Display preprocessing results as images
    st.write("Enhanced and Segmented Images:")
    st.image(enhanced, caption='Enhanced Image', use_column_width=True)
    st.image(segmented, caption='Segmented Image', use_column_width=True)
