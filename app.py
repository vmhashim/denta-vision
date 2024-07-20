import streamlit as st
from PIL import Image
import cv2
import numpy as np
import tempfile

# Frontend: Streamlit interface with grayish background and custom file uploader
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: red;
        font-size: 50px;
        font-weight: bold;
    }
    body {
        background-color: #f0f0f0;  /* Grayish background color */
    }
    .file-upload-wrapper {
        text-align: center;
        padding: 20px;
    }
    .file-upload-wrapper label {
        display: inline-block;
        border: 2px solid #cccccc;
        border-radius: 12px;
        padding: 20px;
        background-color: #e0e0e0;
        cursor: pointer;
        font-size: 20px;
        font-weight: bold;
        width: 300px;  /* Adjust width */
        height: 150px;  /* Adjust height */
        line-height: 110px;  /* Center text vertically */
        text-align: center;
        transition: background-color 0.3s ease;
    }
    .file-upload-wrapper label:hover {
        background-color: #d0d0d0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">DENTA VISION</div>', unsafe_allow_html=True)
st.write("Upload a Tooth Image to Determine the Age")

# Custom file uploader
st.markdown(
    """
    <div class="file-upload-wrapper">
        <label for="file-upload">
            <input type="file" id="file-upload" accept="image/png, image/jpeg" style="display: none;" />
            Drag or click to upload an image
        </label>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="uploader")

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
                                            enhanced.shape[1]
