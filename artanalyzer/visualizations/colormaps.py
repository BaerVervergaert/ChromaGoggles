"""
Custom colormap utilities for color space visualizations.
"""
import numpy as np
import matplotlib.colors as mcolors
from skimage import color


# Cache for custom colormaps
_colormap_cache = {}


def create_lch_hue_colormap():
    """
    Create a custom colormap for LCh hue that correctly maps hue angles to perceptual colors.

    LCh hue angles follow the perceptual color wheel:
    - 0° = Red
    - 90° = Yellow
    - 180° = Green
    - 270° = Blue
    - 360° = Red again

    Returns:
        A matplotlib ListedColormap for LCh hue visualization
    """
    if 'lch_hue' in _colormap_cache:
        return _colormap_cache['lch_hue']

    # Create a range of hue angles from 0 to 360 degrees
    n_colors = 360
    hue_angles = np.linspace(0, 360, n_colors)

    # Create a dummy LCh image with max chroma and luminance for pure color representation
    # Use high L* (65) and high C* (100) for vibrant colors
    hue_rad = np.radians(hue_angles)

    # Create LCh colors in cylindrical form
    rgb_colors = np.zeros((n_colors, 3))

    for i, h in enumerate(hue_rad):
        # Create LCh color with high luminance and chroma for vivid hue representation
        lch = np.array([65, 100, h])  # L*=65, C*=100, h=angle

        # Convert LCh to LAB
        lab = color.lch2lab(lch)

        # Convert LAB to RGB
        rgb = color.lab2rgb(lab.reshape(1, 1, 3)).reshape(3)

        # Clip values to valid RGB range [0, 1]
        rgb_colors[i] = np.clip(rgb, 0, 1)

    # Create a ListedColormap from the RGB colors
    cmap = mcolors.ListedColormap(rgb_colors)
    _colormap_cache['lch_hue'] = cmap
    return cmap


def get_colormap(colormap_name: str):
    """
    Get a colormap by name, including custom colormaps.

    Args:
        colormap_name: Name of the colormap

    Returns:
        Matplotlib colormap object
    """
    # Check if it's a custom colormap
    if colormap_name == 'lch_hue':
        return create_lch_hue_colormap()

    # Otherwise, use matplotlib's built-in colormaps
    try:
        import matplotlib.pyplot as plt
        return plt.get_cmap(colormap_name)
    except ValueError:
        # Fallback to viridis if colormap not found
        print(f"Warning: Colormap '{colormap_name}' not found, using 'viridis'")
        import matplotlib.pyplot as plt
        return plt.get_cmap('viridis')

