"""
Simple test to verify the image processing modules work correctly.
Run with: poetry run python test_basic.py
"""
import numpy as np
from PIL import Image
from image_processor import ImageAnalyzer

def create_test_image():
    """Create a simple test image with known colors."""
    # Create a 100x100 RGB image
    img_array = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Red square (top-left)
    img_array[0:50, 0:50] = [255, 0, 0]
    
    # Green square (top-right)
    img_array[0:50, 50:100] = [0, 255, 0]
    
    # Blue square (bottom-left)
    img_array[50:100, 0:50] = [0, 0, 255]
    
    # White square (bottom-right)
    img_array[50:100, 50:100] = [255, 255, 255]
    
    return Image.fromarray(img_array, 'RGB')

def test_rgb_channels():
    """Test RGB channel extraction."""
    print("Testing RGB channel extraction...")
    img = create_test_image()
    analyzer = ImageAnalyzer(img)
    
    r, g, b = analyzer.get_rgb_channels()
    
    assert r.shape == (100, 100), "Red channel shape incorrect"
    assert g.shape == (100, 100), "Green channel shape incorrect"
    assert b.shape == (100, 100), "Blue channel shape incorrect"
    
    # Check top-left red square
    assert r[25, 25] == 255, "Red channel value incorrect"
    assert g[25, 25] == 0, "Green channel value incorrect in red area"
    assert b[25, 25] == 0, "Blue channel value incorrect in red area"
    
    print("✓ RGB channel extraction works correctly")

def test_hcl_extraction():
    """Test HCL extraction."""
    print("Testing HCL extraction...")
    img = create_test_image()
    analyzer = ImageAnalyzer(img)
    
    hue, chroma, luminance = analyzer.get_hcl()
    
    assert hue.shape == (100, 100), "Hue shape incorrect"
    assert chroma.shape == (100, 100), "Chroma shape incorrect"
    assert luminance.shape == (100, 100), "Luminance shape incorrect"
    
    # White should have maximum luminance
    assert luminance[75, 75] > 90, "White luminance should be high"
    
    print("✓ HCL extraction works correctly")

def test_color_spaces():
    """Test color space conversions."""
    print("Testing color space conversions...")
    img = create_test_image()
    analyzer = ImageAnalyzer(img)
    
    hsv = analyzer.get_hsv()
    lab = analyzer.get_lab()
    ycbcr = analyzer.get_ycbcr()
    luv = analyzer.get_luv()
    xyz = analyzer.get_xyz()
    gray = analyzer.get_grayscale()
    
    assert hsv.shape == (100, 100, 3), "HSV shape incorrect"
    assert lab.shape == (100, 100, 3), "LAB shape incorrect"
    assert ycbcr.shape == (100, 100, 3), "YCbCr shape incorrect"
    assert luv.shape == (100, 100, 3), "LUV shape incorrect"
    assert xyz.shape == (100, 100, 3), "XYZ shape incorrect"
    assert gray.shape == (100, 100), "Grayscale shape incorrect"
    
    print("✓ Color space conversions work correctly")

def test_image_properties():
    """Test image property extraction."""
    print("Testing image properties...")
    img = create_test_image()
    analyzer = ImageAnalyzer(img)
    
    assert analyzer.width == 100, "Width incorrect"
    assert analyzer.height == 100, "Height incorrect"
    assert analyzer.original_image.shape == (100, 100, 3), "Image shape incorrect"
    
    print("✓ Image properties work correctly")

if __name__ == "__main__":
    print("\n=== Running ArtAnalyzer Tests ===\n")
    
    try:
        test_image_properties()
        test_rgb_channels()
        test_hcl_extraction()
        test_color_spaces()
        
        print("\n=== All tests passed! ===")
        print("\nYou can now run the application with:")
        print("  ./run.sh")
        print("  or")
        print("  poetry run streamlit run main.py")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        exit(1)

