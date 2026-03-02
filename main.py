"""
ArtAnalyzer - Image Color Space Analysis Tool

A comprehensive image analysis application that visualizes RGB channels,
color space transformations, and statistical distributions.
"""
import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from image_processor import ImageAnalyzer
from visualizer import (
    create_channel_comparison,
    create_rgb_colored_comparison,
    create_hcl_comparison,
    create_density_plots,
    create_rgb_density_plots,
    create_colorspace_comparison,
    create_rgb_scatter_plots,
    create_hcl_scatter_plots,
    create_xyz_visualization,
    create_hsv_comparison,
    create_hsv_density_plots,
    create_hsv_scatter_plots,
    create_lab_comparison,
    create_lab_density_plots,
    create_lab_scatter_plots,
)


def main():
    st.set_page_config(
        page_title="ArtAnalyzer",
        page_icon="🎨",
        layout="wide"
    )

    st.title("🎨 ArtAnalyzer - Image Color Space Analysis")
    st.markdown("""
    Upload an image to analyze its color properties across different color spaces.
    This tool extracts RGB channels, Hue-Chroma-Luminance values, and displays 
    various color space representations with statistical distributions.
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

        # Create analyzer
        analyzer = ImageAnalyzer(image)

        # Display original image
        st.header("Original Image")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption='Original Image', use_container_width=True)

        # Image information
        st.info(f"Image size: {analyzer.width} × {analyzer.height} pixels")

        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "RGB Channels",
            "RGB Statistics",
            "HSV Channels",
            "HSV Statistics",
            "LAB Channels",
            "LAB Statistics",
            "Hue-Chroma-Luminance",
            "HCL Statistics",
            "Color Spaces",
            "Advanced Analysis"
        ])

        with tab1:
            st.header("RGB Channel Decomposition")

            # Get RGB channels
            r_channel, g_channel, b_channel = analyzer.get_rgb_channels()
            red_img, green_img, blue_img = analyzer.get_rgb_channel_images()

            # Show grayscale channels
            st.subheader("Grayscale Representation")
            fig_channels = create_channel_comparison(r_channel, g_channel, b_channel)
            st.pyplot(fig_channels)
            plt.close()

            # Show colored channels
            st.subheader("Colored Representation")
            fig_colored = create_rgb_colored_comparison(red_img, green_img, blue_img)
            st.pyplot(fig_colored)
            plt.close()

        with tab2:
            st.header("RGB Statistical Distribution")

            r_channel, g_channel, b_channel = analyzer.get_rgb_channels()

            # Show RGB histograms
            fig_rgb_density = create_rgb_density_plots(r_channel, g_channel, b_channel)
            st.pyplot(fig_rgb_density)
            plt.close()

            # Show scatter plots
            st.subheader("RGB Channel Relationships")
            fig_rgb_scatter = create_rgb_scatter_plots(r_channel, g_channel, b_channel)
            st.pyplot(fig_rgb_scatter)
            plt.close()

            # Show statistics
            st.subheader("Channel Statistics")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Red Mean", f"{r_channel.mean():.2f}")
                st.metric("Red Std Dev", f"{r_channel.std():.2f}")
                st.metric("Red Min/Max", f"{r_channel.min()} / {r_channel.max()}")

            with col2:
                st.metric("Green Mean", f"{g_channel.mean():.2f}")
                st.metric("Green Std Dev", f"{g_channel.std():.2f}")
                st.metric("Green Min/Max", f"{g_channel.min()} / {g_channel.max()}")

            with col3:
                st.metric("Blue Mean", f"{b_channel.mean():.2f}")
                st.metric("Blue Std Dev", f"{b_channel.std():.2f}")
                st.metric("Blue Min/Max", f"{b_channel.min()} / {b_channel.max()}")

        with tab3:
            st.header("HSV Channel Decomposition")
            st.markdown("""
            The HSV color space represents colors using:
            - **Hue**: The color type (0-180° in OpenCV)
            - **Saturation**: Color intensity/purity (0-255)
            - **Value**: Brightness (0-255)
            """)

            # Get HSV values
            hsv = analyzer.get_hsv()

            # Show HSV images
            fig_hsv = create_hsv_comparison(hsv)
            st.pyplot(fig_hsv)
            plt.close()

        with tab4:
            st.header("HSV Statistical Distribution")

            hsv = analyzer.get_hsv()

            # Show density plots
            fig_hsv_density = create_hsv_density_plots(hsv)
            st.pyplot(fig_hsv_density)
            plt.close()

            # Show scatter plots
            st.subheader("HSV Dimension Relationships")
            fig_hsv_scatter = create_hsv_scatter_plots(hsv, analyzer.original_image)
            st.pyplot(fig_hsv_scatter)
            plt.close()

            # Show statistics
            st.subheader("HSV Statistics")
            col1, col2, col3 = st.columns(3)

            hue_values = hsv[:, :, 0].flatten()
            saturation_values = hsv[:, :, 1].flatten()
            value_values = hsv[:, :, 2].flatten()

            with col1:
                st.metric("Hue Mean", f"{hue_values.mean():.2f}")
                st.metric("Hue Std Dev", f"{hue_values.std():.2f}")
                st.metric("Hue Min/Max", f"{hue_values.min():.0f} / {hue_values.max():.0f}")

            with col2:
                st.metric("Saturation Mean", f"{saturation_values.mean():.2f}")
                st.metric("Saturation Std Dev", f"{saturation_values.std():.2f}")
                st.metric("Saturation Min/Max", f"{saturation_values.min():.0f} / {saturation_values.max():.0f}")

            with col3:
                st.metric("Value Mean", f"{value_values.mean():.2f}")
                st.metric("Value Std Dev", f"{value_values.std():.2f}")
                st.metric("Value Min/Max", f"{value_values.min():.0f} / {value_values.max():.0f}")

        with tab5:
            st.header("LAB Channel Decomposition")
            st.markdown("""
            The LAB (CIELAB) color space represents colors using:
            - **L***: Lightness (0-100)
            - **A***: Green-Red axis (-127 to 127)
            - **B***: Blue-Yellow axis (-127 to 127)
            """)

            # Get LAB values
            lab = analyzer.get_lab()

            # Show LAB images
            fig_lab = create_lab_comparison(lab)
            st.pyplot(fig_lab)
            plt.close()

        with tab6:
            st.header("LAB Statistical Distribution")

            lab = analyzer.get_lab()

            # Show density plots
            fig_lab_density = create_lab_density_plots(lab)
            st.pyplot(fig_lab_density)
            plt.close()

            # Show scatter plots
            st.subheader("LAB Dimension Relationships")
            fig_lab_scatter = create_lab_scatter_plots(lab, analyzer.original_image)
            st.pyplot(fig_lab_scatter)
            plt.close()

            # Show statistics
            st.subheader("LAB Statistics")
            col1, col2, col3 = st.columns(3)

            l_values = lab[:, :, 0].flatten()
            a_values = lab[:, :, 1].flatten()
            b_values = lab[:, :, 2].flatten()

            with col1:
                st.metric("L* Mean", f"{l_values.mean():.2f}")
                st.metric("L* Std Dev", f"{l_values.std():.2f}")
                st.metric("L* Min/Max", f"{l_values.min():.2f} / {l_values.max():.2f}")

            with col2:
                st.metric("A* Mean", f"{a_values.mean():.2f}")
                st.metric("A* Std Dev", f"{a_values.std():.2f}")
                st.metric("A* Min/Max", f"{a_values.min():.2f} / {a_values.max():.2f}")

            with col3:
                st.metric("B* Mean", f"{b_values.mean():.2f}")
                st.metric("B* Std Dev", f"{b_values.std():.2f}")
                st.metric("B* Min/Max", f"{b_values.min():.2f} / {b_values.max():.2f}")

        with tab7:
            st.header("Hue, Chroma, and Luminance (LCh)")
            st.markdown("""
            The LCh color space represents colors using:
            - **Hue**: The color angle (0-360°)
            - **Chroma**: Color intensity/saturation
            - **Luminance**: Brightness (L* from CIELAB)
            """)

            # Get HCL values
            hue, chroma, luminance = analyzer.get_hcl()

            # Show HCL images
            fig_hcl = create_hcl_comparison(hue, chroma, luminance)
            st.pyplot(fig_hcl)
            plt.close()

        with tab8:
            st.header("HCL Statistical Distribution")

            hue, chroma, luminance = analyzer.get_hcl()

            # Show density plots
            fig_density = create_density_plots(hue, chroma, luminance)
            st.pyplot(fig_density)
            plt.close()

            # Show scatter plots
            st.subheader("HCL Dimension Relationships")
            fig_hcl_scatter = create_hcl_scatter_plots(hue, chroma, luminance, analyzer.original_image)
            st.pyplot(fig_hcl_scatter)
            plt.close()

            # Show statistics
            st.subheader("HCL Statistics")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Hue Mean", f"{hue.mean():.2f}°")
                st.metric("Hue Std Dev", f"{hue.std():.2f}°")

            with col2:
                st.metric("Chroma Mean", f"{chroma.mean():.2f}")
                st.metric("Chroma Std Dev", f"{chroma.std():.2f}")

            with col3:
                st.metric("Luminance Mean", f"{luminance.mean():.2f}")
                st.metric("Luminance Std Dev", f"{luminance.std():.2f}")

        with tab9:
            st.header("Color Space Comparison")
            st.markdown("""
            Different color spaces represent the same image in various ways:
            - **HSV**: Hue, Saturation, Value
            - **LAB**: Lightness, A (green-red), B (blue-yellow)
            - **YCbCr**: Luma, Blue-difference, Red-difference
            """)

            # Get color spaces
            hsv = analyzer.get_hsv()
            lab = analyzer.get_lab()
            ycbcr = analyzer.get_ycbcr()

            # Show comparison
            fig_colorspaces = create_colorspace_comparison(
                analyzer.original_image, hsv, lab, ycbcr
            )
            st.pyplot(fig_colorspaces)
            plt.close()

        with tab10:
            st.header("Advanced Color Space Analysis")

            # LUV color space
            st.subheader("LUV Color Space")
            luv = analyzer.get_luv()

            fig, axes = plt.subplots(1, 3, figsize=(15, 5))

            # L* component (lightness): 0-100
            axes[0].imshow(luv[:, :, 0], cmap='gray', vmin=0, vmax=100)
            axes[0].set_title('L* (Lightness 0-100)')
            axes[0].axis('off')

            # U* component: typically ranges from -100 to 100
            axes[1].imshow(luv[:, :, 1], cmap='RdYlGn_r', vmin=-100, vmax=100)
            axes[1].set_title('U* component (green-red)')
            axes[1].axis('off')

            # V* component: typically ranges from -100 to 100
            axes[2].imshow(luv[:, :, 2], cmap='YlGnBu_r', vmin=-100, vmax=100)
            axes[2].set_title('V* component (yellow-blue)')
            axes[2].axis('off')

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            # XYZ color space
            st.subheader("XYZ Color Space (CIE 1931)")
            xyz = analyzer.get_xyz()

            fig_xyz = create_xyz_visualization(xyz)
            st.pyplot(fig_xyz)
            plt.close()

            # Grayscale
            st.subheader("Grayscale Conversion")
            gray = analyzer.get_grayscale()

            fig, ax = plt.subplots(1, 1, figsize=(8, 8))
            ax.imshow(gray, cmap='gray', vmin=0, vmax=255)
            ax.set_title('Grayscale')
            ax.axis('off')
            st.pyplot(fig)
            plt.close()

    else:
        st.info("👆 Please upload an image to begin analysis")

        # Show sample information
        st.markdown("""
        ### Features:
        - **RGB Channel Analysis**: View individual red, green, and blue channels with statistics
        - **HSV Analysis**: Hue, Saturation, and Value decomposition with statistical distributions
        - **LAB Analysis**: CIELAB color space with L*, A*, and B* channels and scatter plots
        - **HCL Analysis**: Hue, Chroma, and Luminance (LCh) decomposition
        - **Multiple Color Spaces**: Comprehensive analysis across HSV, LAB, YCbCr, LUV, XYZ
        - **Advanced Visualizations**: Scatter plots, density plots, and histograms for all color spaces
        
        ### Supported formats:
        PNG, JPG, JPEG, BMP, TIFF
        """)


if __name__ == '__main__':
    main()
