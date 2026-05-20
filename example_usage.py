"""
Example script demonstrating programmatic use of ChromaGoggles modules.
This shows how to use the modules without the Streamlit interface.
"""
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from image_processor import ImageAnalyzer
from visualizer import (
    create_channel_comparison,
    create_hcl_comparison,
    create_density_plots,
    create_colorspace_comparison,
    create_rgb_scatter_plots,
    create_hcl_scatter_plots,
)


def analyze_image(image_path):
    """
    Analyze an image and display all visualizations.

    Args:
        image_path: Path to the image file
    """
    print(f"Analyzing image: {image_path}")

    # Load and analyze image
    analyzer = ImageAnalyzer(image_path)

    print(f"Image size: {analyzer.width} x {analyzer.height} pixels")

    # Get RGB channels
    r_channel, g_channel, b_channel = analyzer.get_rgb_channels()
    print(f"RGB channels extracted")

    # Get HCL values
    hue, chroma, luminance = analyzer.get_hcl()
    print(f"HCL values calculated")
    print(f"  - Hue range: {hue.min():.2f}° to {hue.max():.2f}°")
    print(f"  - Chroma range: {chroma.min():.2f} to {chroma.max():.2f}")
    print(f"  - Luminance range: {luminance.min():.2f} to {luminance.max():.2f}")

    # Get color spaces
    hsv = analyzer.get_hsv()
    lab = analyzer.get_lab()
    ycbcr = analyzer.get_ycbcr()
    print(f"Color spaces converted")

    # Create visualizations
    print("\nCreating visualizations...")

    # RGB channel comparison
    fig1 = create_channel_comparison(r_channel, g_channel, b_channel)
    fig1.savefig('output_rgb_channels.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: output_rgb_channels.png")
    plt.close(fig1)

    # HCL comparison
    fig2 = create_hcl_comparison(hue, chroma, luminance)
    fig2.savefig('output_hcl_comparison.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: output_hcl_comparison.png")
    plt.close(fig2)

    # Density plots
    fig3 = create_density_plots(hue, chroma, luminance)
    fig3.savefig('output_density_plots.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: output_density_plots.png")
    plt.close(fig3)

    # RGB scatter plots
    fig5 = create_rgb_scatter_plots(r_channel, g_channel, b_channel)
    fig5.savefig('output_rgb_scatter.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: output_rgb_scatter.png")
    plt.close(fig5)

    # HCL scatter plots
    fig6 = create_hcl_scatter_plots(hue, chroma, luminance)
    fig6.savefig('output_hcl_scatter.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: output_hcl_scatter.png")
    plt.close(fig6)

    # Color space comparison
    fig4 = create_colorspace_comparison(analyzer.original_image, hsv, lab, ycbcr)
    fig4.savefig('output_colorspace_comparison.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: output_colorspace_comparison.png")
    plt.close(fig4)

    print("\nAnalysis complete! Check the output_*.png files.")


def create_example_image():
    """
    Create a sample gradient image for demonstration.
    """
    print("Creating example gradient image...")

    # Create a colorful gradient
    width, height = 400, 300
    img_array = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            # Create a rainbow gradient
            hue = (x / width) * 360
            saturation = 1.0
            value = 1.0 - (y / height) * 0.5  # Gradient from bright to darker

            # Convert HSV to RGB (simple conversion)
            h = hue / 60
            i = int(h)
            f = h - i
            p = value * (1 - saturation)
            q = value * (1 - saturation * f)
            t = value * (1 - saturation * (1 - f))

            if i == 0:
                r, g, b = value, t, p
            elif i == 1:
                r, g, b = q, value, p
            elif i == 2:
                r, g, b = p, value, t
            elif i == 3:
                r, g, b = p, q, value
            elif i == 4:
                r, g, b = t, p, value
            else:
                r, g, b = value, p, q

            img_array[y, x] = [int(r * 255), int(g * 255), int(b * 255)]

    # Save the example image
    img = Image.fromarray(img_array, 'RGB')
    img.save('example_gradient.png')
    print("✓ Saved: example_gradient.png")

    return 'example_gradient.png'


if __name__ == "__main__":
    print("=" * 60)
    print("ChromaGoggles - Programmatic Example")
    print("=" * 60)
    print()

    # Create an example image
    example_path = create_example_image()
    print()

    # Analyze it
    analyze_image(example_path)

    print()
    print("=" * 60)
    print("To analyze your own image, use:")
    print("  poetry run python example_usage.py")
    print("Then modify the script to point to your image file.")
    print()
    print("Or use the interactive web interface:")
    print("  ./run.sh")
    print("=" * 60)
