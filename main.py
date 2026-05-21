# Copyright (c) 2026 Baer Ververgaert. All rights reserved.
"""
ChromaGoggles - Image Color Space Analysis Tool (Refactored)

A comprehensive image analysis application that visualizes color space
transformations and statistical distributions using a modular architecture.
"""
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Import the new modular components
from chromagoggles.ui import TabFactory
from chromagoggles.core import ColorTransfer
from chromagoggles.visualizations import (
    create_color_transfer_comparison,
    create_histogram_comparison,
    create_statistics_table,
    create_difference_visualization,
)
# Import all color spaces to trigger registration
import chromagoggles.colorspaces  # noqa: F401


def main():
    st.set_page_config(
        page_title="ChromaGoggles",
        page_icon="🎨",
        layout="wide"
    )

    st.title("🎨 ChromaGoggles - Image Color Space Analysis")
    st.markdown("""
    Upload an image to analyze its color properties across different color spaces,
    or use the color transfer feature to match the colors of one image to another.
    """)

    # Create tabs for different features
    analysis_tab, transfer_tab = st.tabs(["📊 Color Analysis", "🎨 Color Transfer"])

    # ==================== COLOR ANALYSIS TAB ====================
    with analysis_tab:
        st.header("Color Space Analysis")

        # File uploader for analysis
        uploaded_file = st.file_uploader(
            "Choose an image file for analysis",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'],
            key='analysis_uploader'
        )

        if uploaded_file is not None:
            # Load image
            image = Image.open(uploaded_file)

            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Convert PIL Image to numpy array
            rgb_image = np.array(image)

            # Display original image
            st.subheader("Original Image")
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

            st.markdown("""
            ### Features:
            - **RGB Channel Analysis**: View individual red, green, and blue channels with statistics
            - **HSV Analysis**: Hue, Saturation, and Value decomposition with statistical distributions
            - **LAB Analysis**: CIELAB color space with L*, A*, and B* channels and scatter plots
            - **HCL Analysis**: Hue, Chroma, and Luminance (LCh) perceptually uniform color space
            - **Oklab Analysis**: Modern perceptual lightness-opponent space (L, a, b)
            - **Oklch Analysis**: Cylindrical Oklab space (L, C, H) with custom hue colormap
            - **LMS Analysis**: Cone-response space (L, M, S) approximating human vision
            - **XYZ Analysis**: CIE XYZ tristimulus color space
            - **LUV Analysis**: CIELUV perceptually uniform color space
            - **YCbCr Analysis**: Color space used in video and image compression
            - **Advanced Visualizations**: Scatter plots, density plots, and histograms for all color spaces
            
            ### Supported formats:
            PNG, JPG, JPEG, BMP, TIFF, WebP
            """)

    # ==================== COLOR TRANSFER TAB ====================
    with transfer_tab:
        st.header("🎨 Color Transfer")
        st.markdown("""
        Transfer the color distribution of one image (reference) to another image (source).
        This feature transforms the colors of the source image to match the color palette of the reference image.
        """)

        # Create two columns for file upload
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Source Image")
            st.caption("Image to be transformed")
            source_file = st.file_uploader(
                "Upload source image",
                type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'],
                key='source_uploader'
            )

        with col2:
            st.subheader("Reference Image")
            st.caption("Image providing the color palette")
            reference_file = st.file_uploader(
                "Upload reference image",
                type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'],
                key='reference_uploader'
            )

        if source_file is not None and reference_file is not None:
            # Load images
            source_img_pil = Image.open(source_file)
            reference_img_pil = Image.open(reference_file)

            # Convert to RGB
            if source_img_pil.mode != 'RGB':
                source_img_pil = source_img_pil.convert('RGB')
            if reference_img_pil.mode != 'RGB':
                reference_img_pil = reference_img_pil.convert('RGB')

            source_img = np.array(source_img_pil)
            reference_img = np.array(reference_img_pil)

            # Display original images
            col1, col2 = st.columns(2)
            with col1:
                st.image(source_img_pil, caption='Source Image', use_container_width=True)
                st.caption(f"Size: {source_img.shape[1]} × {source_img.shape[0]} pixels")
            with col2:
                st.image(reference_img_pil, caption='Reference Image', use_container_width=True)
                st.caption(f"Size: {reference_img.shape[1]} × {reference_img.shape[0]} pixels")

            # Method selection
            st.subheader("Transfer Method")

            col1, col2 = st.columns(2)
            with col1:
                method = st.radio(
                    "Select color transfer method:",
                    [
                        "Histogram Matching",
                        "Statistics Matching",
                        "Correlation Preserving",
                        "Nearest Reference Pixels",
                    ],
                    help=(
                        "Histogram: Matches distributions (subtle)\n"
                        "Statistics: Matches mean/std (aggressive)\n"
                        "Correlation Preserving: Preserves channel relationships (natural)\n"
                        "Nearest Reference Pixels: Replaces each scaled source pixel with the closest scaled reference pixel"
                    )
                )

            with col2:
                colorspace = st.selectbox(
                    "Color space:",
                    ["LAB", "RGB", "HSV", "HCL", "Oklab", "Oklch", "XYZ", "LUV", "YCbCr"],
                    help="LAB, HCL, Oklab and Oklch are perceptually oriented and often give strong results"
                )

            # Extra control for nearest-pixel method to balance quality/performance.
            working_size = None
            if method == "Nearest Reference Pixels":
                working_size = st.slider(
                    "Nearest-match working size",
                    min_value=32,
                    max_value=384,
                    value=160,
                    step=16,
                    help="Both images are scaled to this square resolution before nearest-pixel replacement"
                )

            # Perform color transfer
            st.subheader("Transferring colors...")

            with st.spinner("Processing..."):
                if method == "Histogram Matching":
                    transferred = ColorTransfer.match_histograms(
                        source_img,
                        reference_img,
                        colorspace=colorspace.lower()
                    )
                elif method == "Statistics Matching":
                    transferred = ColorTransfer.match_statistics(
                        source_img,
                        reference_img,
                        colorspace=colorspace.lower()
                    )
                elif method == "Correlation Preserving":
                    transferred = ColorTransfer.match_correlation_preserving(
                        source_img,
                        reference_img,
                        colorspace=colorspace.lower()
                    )
                else:  # Nearest Reference Pixels
                    transferred = ColorTransfer.match_nearest_reference_pixels(
                        source_img,
                        reference_img,
                        colorspace=colorspace.lower(),
                        working_size=working_size if working_size is not None else 160,
                    )

            # Display results
            st.subheader("Results")

            # Before/After comparison
            fig = create_color_transfer_comparison(
                source_img,
                reference_img,
                transferred,
                f"Color Transfer ({method}, {colorspace})"
            )
            st.pyplot(fig)
            plt.close(fig)

            # Histogram comparison
            st.subheader("Histogram Comparison")
            fig = create_histogram_comparison(
                source_img,
                reference_img,
                transferred,
                colorspace=colorspace.lower()
            )
            st.pyplot(fig)
            plt.close(fig)

            # Color difference analysis
            st.subheader("Color Difference Analysis")
            fig = create_difference_visualization(source_img, transferred)
            st.pyplot(fig)
            plt.close(fig)

            # Statistics table
            st.subheader("Statistics Comparison")
            stats_md = create_statistics_table(source_img, reference_img, transferred)
            st.markdown(stats_md)

            # Blending option
            st.subheader("Fine-tune Results")
            st.markdown("Blend between source and transferred to get intermediate results:")

            alpha = st.slider(
                "Blend factor:",
                min_value=0.0,
                max_value=1.0,
                value=1.0,
                step=0.05,
                help="0 = Original source, 1 = Full transfer, 0.5 = 50/50 blend"
            )

            if alpha != 1.0:
                blended = ColorTransfer.blend(source_img, transferred, alpha=alpha)
                st.subheader(f"Blended Result (α={alpha:.2f})")
                st.image(blended, use_container_width=True)

                # Show blended statistics
                if st.checkbox("Show blended statistics"):
                    blended_stats = create_statistics_table(source_img, reference_img, blended)
                    st.markdown(blended_stats)
            else:
                blended = transferred

            # Download button
            st.subheader("Download Result")

            col1, col2 = st.columns(2)
            with col1:
                result_pil = Image.fromarray(transferred.astype(np.uint8))
                st.download_button(
                    label="Download Full Transfer",
                    data=_image_to_bytes(result_pil),
                    file_name="color_transferred.png",
                    mime="image/png"
                )

            with col2:
                if alpha != 1.0:
                    blended_pil = Image.fromarray(blended.astype(np.uint8))
                    st.download_button(
                        label="Download Blended Result",
                        data=_image_to_bytes(blended_pil),
                        file_name="color_transferred_blended.png",
                        mime="image/png"
                    )

        else:
            st.info("👆 Please upload both a source and reference image to begin color transfer")

            st.markdown("""
            ### How Color Transfer Works:
            
            **Histogram Matching**: Transforms the pixel values of the source image so that each channel's histogram matches the reference image's histogram. This is done using cumulative distribution functions (CDFs).
            
            **Statistics Matching**: Adjusts the mean and standard deviation of each color channel in the source image to match the reference image. This is a more aggressive transformation.

            **Correlation Preserving**: Uses an optimal-transport-inspired linear transform to preserve relationships (covariances) between color dimensions, often producing smoother and more natural results.

            **Nearest Reference Pixels**: Scales both images to a common working size, then replaces each source pixel with the closest pixel from the scaled reference image in the selected color space.
            
            ### Color Spaces:
            
            - **LAB**: Perceptually uniform, excellent for color matching (recommended)
            - **HCL**: Perceptually uniform cylindrical color space, great for hue/chroma aware matching
            - **Oklab / Oklch**: Modern perceptual spaces with strong hue and lightness behavior
            - **RGB**: Simple channel-wise matching, may produce color casts
            - **HSV**: Separates hue, saturation, and value for intuitive color control
            - **XYZ / LUV / YCbCr**: Useful for technical workflows and alternative transfer behavior
            
            ### Tips:
            
            - LAB, HCL, Oklab, or Oklch usually gives the best perceptual results
            - Use histogram matching for subtle, natural-looking results
            - Use statistics matching for aggressive color transformation
            - Use correlation preserving when gradients and natural color relationships matter
            - Use nearest-reference pixels for palette-quantized, stylized effects
            - Use the blend slider to fine-tune the effect intensity
            """)


def _image_to_bytes(pil_image):
    """Convert PIL image to bytes for download."""
    import io
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    return buf.getvalue()


if __name__ == '__main__':
    main()
