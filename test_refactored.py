"""
Test script for the refactored ArtAnalyzer.
"""
import numpy as np
from PIL import Image
from artanalyzer.core.registry import ColorSpaceRegistry
from artanalyzer.visualizations import ChannelComparisonViz, DensityPlotViz, ScatterPlotViz
from artanalyzer.core.statistics import StatisticsCalculator
import artanalyzer.colorspaces  # Register all color spaces

def test_with_image(image_path):
    """Test all functionality with a real image."""
    print(f"Testing with image: {image_path}")

    # Load image
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    rgb_image = np.array(image)

    print(f"Image size: {rgb_image.shape}")

    # Get all color spaces
    colorspaces = ColorSpaceRegistry.get_all()
    print(f"\nTesting {len(colorspaces)} color spaces:")

    for cs in colorspaces:
        print(f"\n  {cs.display_name}:")

        # Test conversion
        try:
            converted = cs.convert_from_rgb(rgb_image)
            channels = cs.get_channels(rgb_image)
            print(f"    ✓ Conversion successful: {len(channels)} channels")
        except Exception as e:
            print(f"    ✗ Conversion failed: {e}")
            continue

        # Test channel visualization
        try:
            viz = ChannelComparisonViz()
            fig = viz.create(cs, rgb_image)
            print(f"    ✓ Channel visualization created")
        except Exception as e:
            print(f"    ✗ Channel viz failed: {e}")

        # Test statistics
        if cs.supports_statistics_tab():
            try:
                # Test density plots
                viz = DensityPlotViz()
                fig = viz.create(cs, rgb_image)
                print(f"    ✓ Density plots created")

                # Test scatter plots
                if cs.supports_scatter_plots():
                    viz = ScatterPlotViz()
                    fig = viz.create(cs, rgb_image)
                    print(f"    ✓ Scatter plots created")

                # Test statistics
                stats = StatisticsCalculator.calculate(cs, rgb_image)
                print(f"    ✓ Statistics calculated: {len(stats)} channels")
            except Exception as e:
                print(f"    ✗ Statistics failed: {e}")

    print("\n🎉 All tests completed!")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        test_with_image(sys.argv[1])
    else:
        # Use example image if available
        import os
        if os.path.exists('example_gradient.png'):
            test_with_image('example_gradient.png')
        else:
            print("Please provide an image path as argument")
            print("Usage: python test_refactored.py <image_path>")

