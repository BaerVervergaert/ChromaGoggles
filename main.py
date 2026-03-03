"""
ArtAnalyzer - Image Color Space Analysis Tool (Refactored)

A comprehensive image analysis application that visualizes color space
transformations and statistical distributions using a modular architecture.
"""
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

# Import the new modular components
from artanalyzer.ui import TabFactory
# Import all color spaces to trigger registration
import artanalyzer.colorspaces  # noqa: F401


def main():
    st.set_page_config(
        page_title="ArtAnalyzer",
        page_icon="🎨",
        layout="wide"
    )

    st.title("🎨 ArtAnalyzer - Image Color Space Analysis")
    st.markdown("""
    Upload an image to analyze its color properties across different color spaces.
    This tool extracts color channels, transforms between color spaces, and displays 
    various visualizations with statistical distributions.
    """)

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff']
    )

    if uploaded_file is not None:
        # Load image
        image = Image.open(uploaded_file)

        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert PIL Image to numpy array
        import numpy as np
        rgb_image = np.array(image)

        # Display original image
        st.header("Original Image")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption='Original Image', use_container_width=True)

        # Image information
        height, width = rgb_image.shape[:2]
        st.info(f"Image size: {width} × {height} pixels")

        # Create all tabs dynamically using TabFactory
        TabFactory.create_all_tabs(rgb_image)

    else:
        st.info("👆 Please upload an image to begin analysis")

        # Show sample information
        st.markdown("""
        ### Features:
        - **RGB Channel Analysis**: View individual red, green, and blue channels with statistics
        - **HSV Analysis**: Hue, Saturation, and Value decomposition with statistical distributions
        - **LAB Analysis**: CIELAB color space with L*, A*, and B* channels and scatter plots
        - **HCL Analysis**: Hue, Chroma, and Luminance (LCh) perceptually uniform color space
        - **XYZ Analysis**: CIE XYZ tristimulus color space
        - **LUV Analysis**: CIELUV perceptually uniform color space
        - **YCbCr Analysis**: Color space used in video and image compression
        - **Advanced Visualizations**: Scatter plots, density plots, and histograms for all color spaces
        - **Modular Architecture**: Easy to extend with new color spaces and visualizations
        
        ### Supported formats:
        PNG, JPG, JPEG, BMP, TIFF
        
        ### Color Spaces:
        Each color space provides unique insights into image color properties:
        - **RGB**: Direct pixel values from the image sensor
        - **HSV**: Intuitive representation of color (Hue), purity (Saturation), and brightness (Value)
        - **LAB**: Perceptually uniform, excellent for color differences
        - **HCL (LCh)**: Cylindrical LAB, combines perceptual uniformity with intuitive hue angles
        - **XYZ**: Foundation of color science, based on human vision
        - **LUV**: Alternative to LAB, preferred for additive color mixing
        - **YCbCr**: Separates luminance from chrominance, used in JPEG/MPEG
        """)


if __name__ == '__main__':
    main()

