"""
Visualization module for creating plots and displays of image analysis.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from skimage import color


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
    # Create a range of hue angles from 0 to 360 degrees
    n_colors = 360
    hue_angles = np.linspace(0, 360, n_colors)

    # Create a dummy LCh image with max chroma and luminance for pure color representation
    # Use high L* (80) and high C* (100) for vibrant colors
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
    return mcolors.ListedColormap(rgb_colors)


def create_channel_comparison(r_channel, g_channel, b_channel):
    """
    Create a comparison plot of RGB channels.

    Args:
        r_channel: Red channel array
        g_channel: Green channel array
        b_channel: Blue channel array

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(r_channel, cmap='Reds')
    axes[0].set_title('Red Channel')
    axes[0].axis('off')

    axes[1].imshow(g_channel, cmap='Greens')
    axes[1].set_title('Green Channel')
    axes[1].axis('off')

    axes[2].imshow(b_channel, cmap='Blues')
    axes[2].set_title('Blue Channel')
    axes[2].axis('off')

    plt.tight_layout()
    return fig


def create_rgb_colored_comparison(red_img, green_img, blue_img):
    """
    Create a comparison plot of RGB channels as colored images.

    Args:
        red_img: Red channel colored image
        green_img: Green channel colored image
        blue_img: Blue channel colored image

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(red_img)
    axes[0].set_title('Red Channel (Colored)')
    axes[0].axis('off')

    axes[1].imshow(green_img)
    axes[1].set_title('Green Channel (Colored)')
    axes[1].axis('off')

    axes[2].imshow(blue_img)
    axes[2].set_title('Blue Channel (Colored)')
    axes[2].axis('off')

    plt.tight_layout()
    return fig


def create_hcl_comparison(hue, chroma, luminance):
    """
    Create a comparison plot of Hue, Chroma, and Luminance.

    Args:
        hue: Hue array (0-360 degrees)
        chroma: Chroma array
        luminance: Luminance array (0-100)

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Hue - use custom LCh hue colormap for correct perceptual color representation
    lch_hue_cmap = create_lch_hue_colormap()
    im1 = axes[0].imshow(hue, cmap=lch_hue_cmap, vmin=0, vmax=360)
    axes[0].set_title('Hue (0-360°)')
    axes[0].axis('off')
    plt.colorbar(im1, ax=axes[0], fraction=0.046)

    # Chroma - scale to actual data range
    im2 = axes[1].imshow(chroma, cmap='gray', vmin=0, vmax=100)
    axes[1].set_title('Chroma')
    axes[1].axis('off')
    plt.colorbar(im2, ax=axes[1], fraction=0.046)

    # Luminance - scale 0-100 for L* values
    im3 = axes[2].imshow(luminance, cmap='gray', vmin=0, vmax=100)
    axes[2].set_title('Luminance (L* 0-100)')
    axes[2].axis('off')
    plt.colorbar(im3, ax=axes[2], fraction=0.046)

    plt.tight_layout()
    return fig


def create_density_plots(hue, chroma, luminance):
    """
    Create density plots for Hue, Chroma, and Luminance.

    Args:
        hue: Hue array (0-360 degrees)
        chroma: Chroma array
        luminance: Luminance array (0-100)

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Flatten arrays
    hue_flat = hue.flatten()
    chroma_flat = chroma.flatten()
    luminance_flat = luminance.flatten()

    # Hue histogram
    axes[0, 0].hist(hue_flat, bins=72, color='red', alpha=0.7, edgecolor='black')
    axes[0, 0].set_title('Hue Distribution')
    axes[0, 0].set_xlabel('Hue (degrees)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_xlim(0, 360)

    # Chroma histogram
    axes[0, 1].hist(chroma_flat, bins=50, color='green', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Chroma Distribution')
    axes[0, 1].set_xlabel('Chroma')
    axes[0, 1].set_ylabel('Frequency')

    # Luminance histogram
    axes[0, 2].hist(luminance_flat, bins=50, color='blue', alpha=0.7, edgecolor='black')
    axes[0, 2].set_title('Luminance Distribution')
    axes[0, 2].set_xlabel('Luminance (L*)')
    axes[0, 2].set_ylabel('Frequency')

    # Hue KDE plot
    try:
        sns.kdeplot(hue_flat, ax=axes[1, 0], fill=True, color='red', alpha=0.6)
        axes[1, 0].set_title('Hue Density (KDE)')
        axes[1, 0].set_xlabel('Hue (degrees)')
        axes[1, 0].set_ylabel('Density')
        axes[1, 0].set_xlim(0, 360)
    except Exception:
        axes[1, 0].text(0.5, 0.5, 'KDE not available', ha='center', va='center')

    # Chroma KDE plot
    try:
        sns.kdeplot(chroma_flat, ax=axes[1, 1], fill=True, color='green', alpha=0.6)
        axes[1, 1].set_title('Chroma Density (KDE)')
        axes[1, 1].set_xlabel('Chroma')
        axes[1, 1].set_ylabel('Density')
    except Exception:
        axes[1, 1].text(0.5, 0.5, 'KDE not available', ha='center', va='center')

    # Luminance KDE plot
    try:
        sns.kdeplot(luminance_flat, ax=axes[1, 2], fill=True, color='blue', alpha=0.6)
        axes[1, 2].set_title('Luminance Density (KDE)')
        axes[1, 2].set_xlabel('Luminance (L*)')
        axes[1, 2].set_ylabel('Density')
    except Exception:
        axes[1, 2].text(0.5, 0.5, 'KDE not available', ha='center', va='center')

    plt.tight_layout()
    return fig


def create_rgb_density_plots(r_channel, g_channel, b_channel):
    """
    Create density plots for RGB channels.

    Args:
        r_channel: Red channel array
        g_channel: Green channel array
        b_channel: Blue channel array

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Flatten arrays
    r_flat = r_channel.flatten()
    g_flat = g_channel.flatten()
    b_flat = b_channel.flatten()

    # Red histogram
    axes[0].hist(r_flat, bins=256, color='red', alpha=0.7, range=(0, 255))
    axes[0].set_title('Red Channel Distribution')
    axes[0].set_xlabel('Pixel Value')
    axes[0].set_ylabel('Frequency')

    # Green histogram
    axes[1].hist(g_flat, bins=256, color='green', alpha=0.7, range=(0, 255))
    axes[1].set_title('Green Channel Distribution')
    axes[1].set_xlabel('Pixel Value')
    axes[1].set_ylabel('Frequency')

    # Blue histogram
    axes[2].hist(b_flat, bins=256, color='blue', alpha=0.7, range=(0, 255))
    axes[2].set_title('Blue Channel Distribution')
    axes[2].set_xlabel('Pixel Value')
    axes[2].set_ylabel('Frequency')

    plt.tight_layout()
    return fig


def create_colorspace_comparison(original, hsv, lab, ycbcr):
    """
    Create a comparison of different color spaces.

    Args:
        original: Original RGB image
        hsv: HSV image
        lab: LAB image
        ycbcr: YCbCr image

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))

    # Original RGB
    axes[0, 0].imshow(original)
    axes[0, 0].set_title('Original (RGB)')
    axes[0, 0].axis('off')

    # HSV channels
    axes[0, 1].imshow(hsv[:, :, 0], cmap='hsv', vmin=0, vmax=180)
    axes[0, 1].set_title('HSV - Hue (0-180)')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(hsv[:, :, 1], cmap='gray', vmin=0, vmax=255)
    axes[0, 2].set_title('HSV - Saturation (0-255)')
    axes[0, 2].axis('off')

    axes[0, 3].imshow(hsv[:, :, 2], cmap='gray', vmin=0, vmax=255)
    axes[0, 3].set_title('HSV - Value (0-255)')
    axes[0, 3].axis('off')

    # LAB channels
    axes[1, 0].imshow(lab[:, :, 0], cmap='gray', vmin=0, vmax=100)
    axes[1, 0].set_title('LAB - L* (0-100)')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(lab[:, :, 1], cmap='RdYlGn_r', vmin=-127, vmax=127)
    axes[1, 1].set_title('LAB - A* (-127 to 127)')
    axes[1, 1].axis('off')

    axes[1, 2].imshow(lab[:, :, 2], cmap='YlGnBu_r', vmin=-127, vmax=127)
    axes[1, 2].set_title('LAB - B* (-127 to 127)')
    axes[1, 2].axis('off')

    # YCbCr Y channel
    axes[1, 3].imshow(ycbcr[:, :, 0], cmap='gray', vmin=0, vmax=255)
    axes[1, 3].set_title('YCbCr - Luma (0-255)')
    axes[1, 3].axis('off')

    plt.tight_layout()
    return fig


def create_rgb_scatter_plots(r_channel, g_channel, b_channel):
    """
    Create scatter plots showing relationships between RGB channels.
    Uses density-based alpha values to highlight concentrations.
    Colors points by their actual RGB values.

    Args:
        r_channel: Red channel array
        g_channel: Green channel array
        b_channel: Blue channel array

    Returns:
        Matplotlib figure
    """
    # Flatten arrays and sample for clarity (don't plot all pixels)
    r_flat = r_channel.flatten()
    g_flat = g_channel.flatten()
    b_flat = b_channel.flatten()

    # Sample pixels for better performance (every 10th pixel)
    sample_idx = np.arange(0, len(r_flat), 10)
    r_sample = r_flat[sample_idx]
    g_sample = g_flat[sample_idx]
    b_sample = b_flat[sample_idx]

    # Normalize RGB values to [0, 1] for color mapping
    rgb_colors = np.column_stack([r_sample, g_sample, b_sample]) / 255.0

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Calculate density-based alpha for Red vs Green using histogram binning
    h_rg, xedges, yedges = np.histogram2d(r_sample, g_sample, bins=20)
    x_indices = np.digitize(r_sample, xedges) - 1
    y_indices = np.digitize(g_sample, yedges) - 1
    counts_rg = h_rg[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_rg = np.clip(np.sqrt(counts_rg) / np.sqrt(counts_rg.max()) * 0.7 + 0.1, 0.1, 0.8)

    # Red vs Green - color by actual RGB values
    axes[0].scatter(r_sample, g_sample, alpha=alpha_rg, s=10, c=rgb_colors)
    axes[0].set_xlabel('Red')
    axes[0].set_ylabel('Green')
    axes[0].set_title('Red vs Green')
    axes[0].set_xlim(0, 255)
    axes[0].set_ylim(0, 255)
    axes[0].grid(True, alpha=0.3)

    # Calculate density-based alpha for Red vs Blue using histogram binning
    h_rb, xedges, yedges = np.histogram2d(r_sample, b_sample, bins=20)
    x_indices = np.digitize(r_sample, xedges) - 1
    y_indices = np.digitize(b_sample, yedges) - 1
    counts_rb = h_rb[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_rb = np.clip(np.sqrt(counts_rb) / np.sqrt(counts_rb.max()) * 0.7 + 0.1, 0.1, 0.8)

    # Red vs Blue - color by actual RGB values
    axes[1].scatter(r_sample, b_sample, alpha=alpha_rb, s=10, c=rgb_colors)
    axes[1].set_xlabel('Red')
    axes[1].set_ylabel('Blue')
    axes[1].set_title('Red vs Blue')
    axes[1].set_xlim(0, 255)
    axes[1].set_ylim(0, 255)
    axes[1].grid(True, alpha=0.3)

    # Calculate density-based alpha for Green vs Blue using histogram binning
    h_gb, xedges, yedges = np.histogram2d(g_sample, b_sample, bins=20)
    x_indices = np.digitize(g_sample, xedges) - 1
    y_indices = np.digitize(b_sample, yedges) - 1
    counts_gb = h_gb[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_gb = np.clip(np.sqrt(counts_gb) / np.sqrt(counts_gb.max()) * 0.7 + 0.1, 0.1, 0.8)

    # Green vs Blue - color by actual RGB values
    axes[2].scatter(g_sample, b_sample, alpha=alpha_gb, s=10, c=rgb_colors)
    axes[2].set_xlabel('Green')
    axes[2].set_ylabel('Blue')
    axes[2].set_title('Green vs Blue')
    axes[2].set_xlim(0, 255)
    axes[2].set_ylim(0, 255)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def create_hcl_scatter_plots(hue, chroma, luminance, rgb_image=None):
    """
    Create scatter plots showing relationships between HCL dimensions.
    Uses density-based alpha values to highlight concentrations.
    Colors points by their actual RGB values from the image.

    Args:
        hue: Hue array (0-360 degrees)
        chroma: Chroma array
        luminance: Luminance array (0-100)
        rgb_image: Original RGB image (optional, for coloring points)

    Returns:
        Matplotlib figure
    """
    # Flatten arrays and sample for clarity (don't plot all pixels)
    hue_flat = hue.flatten()
    chroma_flat = chroma.flatten()
    luminance_flat = luminance.flatten()

    # Sample pixels for better performance (every 10th pixel)
    sample_idx = np.arange(0, len(hue_flat), 10)
    hue_sample = hue_flat[sample_idx]
    chroma_sample = chroma_flat[sample_idx]
    luminance_sample = luminance_flat[sample_idx]

    # Get RGB colors if image is provided
    rgb_colors = None
    if rgb_image is not None:
        rgb_flat = rgb_image.reshape(-1, 3)
        rgb_colors = rgb_flat[sample_idx] / 255.0  # Normalize to [0, 1]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Hue vs Chroma - calculate density-based alpha using histogram binning
    h_hc, xedges, yedges = np.histogram2d(hue_sample, chroma_sample, bins=20)
    x_indices = np.digitize(hue_sample, xedges) - 1
    y_indices = np.digitize(chroma_sample, yedges) - 1
    counts_hc = h_hc[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_hc = np.clip(np.sqrt(counts_hc) / np.sqrt(counts_hc.max()) * 0.7 + 0.1, 0.1, 0.8)

    # Hue vs Chroma - color by actual RGB values if available
    if rgb_colors is not None:
        axes[0].scatter(hue_sample, chroma_sample, alpha=alpha_hc, s=10, c=rgb_colors)
    else:
        scatter1 = axes[0].scatter(hue_sample, chroma_sample, alpha=alpha_hc, s=10,
                                   c=hue_sample, cmap='hsv', vmin=0, vmax=360)
        plt.colorbar(scatter1, ax=axes[0])

    axes[0].set_xlabel('Hue (degrees)')
    axes[0].set_ylabel('Chroma')
    axes[0].set_title('Hue vs Chroma')
    axes[0].set_xlim(0, 360)
    axes[0].grid(True, alpha=0.3)

    # Hue vs Luminance - calculate density-based alpha using histogram binning
    h_hl, xedges, yedges = np.histogram2d(hue_sample, luminance_sample, bins=20)
    x_indices = np.digitize(hue_sample, xedges) - 1
    y_indices = np.digitize(luminance_sample, yedges) - 1
    counts_hl = h_hl[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_hl = np.clip(np.sqrt(counts_hl) / np.sqrt(counts_hl.max()) * 0.7 + 0.1, 0.1, 0.8)

    # Hue vs Luminance - color by actual RGB values if available
    if rgb_colors is not None:
        axes[1].scatter(hue_sample, luminance_sample, alpha=alpha_hl, s=10, c=rgb_colors)
    else:
        scatter2 = axes[1].scatter(hue_sample, luminance_sample, alpha=alpha_hl, s=10,
                                   c=hue_sample, cmap='hsv', vmin=0, vmax=360)
        plt.colorbar(scatter2, ax=axes[1])

    axes[1].set_xlabel('Hue (degrees)')
    axes[1].set_ylabel('Luminance (L*)')
    axes[1].set_title('Hue vs Luminance')
    axes[1].set_xlim(0, 360)
    axes[1].grid(True, alpha=0.3)

    # Chroma vs Luminance - calculate density-based alpha using histogram binning
    h_cl, xedges, yedges = np.histogram2d(chroma_sample, luminance_sample, bins=20)
    x_indices = np.digitize(chroma_sample, xedges) - 1
    y_indices = np.digitize(luminance_sample, yedges) - 1
    counts_cl = h_cl[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_cl = np.clip(np.sqrt(counts_cl) / np.sqrt(counts_cl.max()) * 0.7 + 0.1, 0.1, 0.8)

    # Chroma vs Luminance - color by actual RGB values if available
    if rgb_colors is not None:
        axes[2].scatter(chroma_sample, luminance_sample, alpha=alpha_cl, s=10, c=rgb_colors)
    else:
        scatter3 = axes[2].scatter(chroma_sample, luminance_sample, alpha=alpha_cl, s=10,
                                   c=luminance_sample, cmap='gray')
        plt.colorbar(scatter3, ax=axes[2])

    axes[2].set_xlabel('Chroma')
    axes[2].set_ylabel('Luminance (L*)')
    axes[2].set_title('Chroma vs Luminance')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def create_xyz_visualization(xyz_image):
    """
    Create a visualization of XYZ color space components.

    XYZ is a tristimulus color space where:
    - X: Red-like component (derived from red and green cone responses)
    - Y: Luminance component (brightness)
    - Z: Blue-like component (derived from blue cone response)

    Args:
        xyz_image: XYZ image array with shape (height, width, 3)

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Extract individual components
    x_component = xyz_image[:, :, 0]
    y_component = xyz_image[:, :, 1]
    z_component = xyz_image[:, :, 2]

    # X component - Red-like (warm colors: black to red to yellow)
    im_x = axes[0].imshow(x_component, cmap='hot', vmin=0, vmax=1)
    axes[0].set_title(f'X component (Red-like)')
    axes[0].axis('off')
    plt.colorbar(im_x, ax=axes[0], fraction=0.046)

    # Y component - Luminance (grayscale: black to white)
    im_y = axes[1].imshow(y_component, cmap='gray', vmin=0, vmax=1)
    axes[1].set_title(f'Y component (Luminance)')
    axes[1].axis('off')
    plt.colorbar(im_y, ax=axes[1], fraction=0.046)

    # Z component - Blue-like (cool colors: black to blue to cyan)
    im_z = axes[2].imshow(z_component, cmap='cool', vmin=0, vmax=1)
    axes[2].set_title(f'Z component (Blue-like)')
    axes[2].axis('off')
    plt.colorbar(im_z, ax=axes[2], fraction=0.046)

    plt.tight_layout()
    return fig


def create_hsv_comparison(hsv_image):
    """
    Create a comparison plot of HSV channels.

    Args:
        hsv_image: HSV image array with shape (height, width, 3)
                   H: 0-180 (OpenCV convention)
                   S: 0-255
                   V: 0-255

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Hue channel - use hsv colormap, scale 0-180 (OpenCV convention)
    im_h = axes[0].imshow(hsv_image[:, :, 0], cmap='hsv', vmin=0, vmax=180)
    axes[0].set_title('Hue (0-180)')
    axes[0].axis('off')
    plt.colorbar(im_h, ax=axes[0], fraction=0.046)

    # Saturation channel - grayscale
    im_s = axes[1].imshow(hsv_image[:, :, 1], cmap='gray', vmin=0, vmax=255)
    axes[1].set_title('Saturation (0-255)')
    axes[1].axis('off')
    plt.colorbar(im_s, ax=axes[1], fraction=0.046)

    # Value channel - grayscale
    im_v = axes[2].imshow(hsv_image[:, :, 2], cmap='gray', vmin=0, vmax=255)
    axes[2].set_title('Value (0-255)')
    axes[2].axis('off')
    plt.colorbar(im_v, ax=axes[2], fraction=0.046)

    plt.tight_layout()
    return fig


def create_hsv_density_plots(hsv_image):
    """
    Create density plots for HSV channels.

    Args:
        hsv_image: HSV image array with shape (height, width, 3)

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Extract and flatten channels
    hue_flat = hsv_image[:, :, 0].flatten()
    saturation_flat = hsv_image[:, :, 1].flatten()
    value_flat = hsv_image[:, :, 2].flatten()

    # Hue histogram
    axes[0, 0].hist(hue_flat, bins=180, color='red', alpha=0.7, edgecolor='black')
    axes[0, 0].set_title('Hue Distribution')
    axes[0, 0].set_xlabel('Hue (0-180)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_xlim(0, 180)

    # Saturation histogram
    axes[0, 1].hist(saturation_flat, bins=256, color='green', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Saturation Distribution')
    axes[0, 1].set_xlabel('Saturation (0-255)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_xlim(0, 255)

    # Value histogram
    axes[0, 2].hist(value_flat, bins=256, color='blue', alpha=0.7, edgecolor='black')
    axes[0, 2].set_title('Value Distribution')
    axes[0, 2].set_xlabel('Value (0-255)')
    axes[0, 2].set_ylabel('Frequency')
    axes[0, 2].set_xlim(0, 255)

    # Hue KDE plot
    try:
        sns.kdeplot(hue_flat, ax=axes[1, 0], fill=True, color='red', alpha=0.6)
        axes[1, 0].set_title('Hue Density (KDE)')
        axes[1, 0].set_xlabel('Hue (0-180)')
        axes[1, 0].set_ylabel('Density')
        axes[1, 0].set_xlim(0, 180)
    except Exception:
        axes[1, 0].text(0.5, 0.5, 'KDE not available', ha='center', va='center')

    # Saturation KDE plot
    try:
        sns.kdeplot(saturation_flat, ax=axes[1, 1], fill=True, color='green', alpha=0.6)
        axes[1, 1].set_title('Saturation Density (KDE)')
        axes[1, 1].set_xlabel('Saturation (0-255)')
        axes[1, 1].set_ylabel('Density')
        axes[1, 1].set_xlim(0, 255)
    except Exception:
        axes[1, 1].text(0.5, 0.5, 'KDE not available', ha='center', va='center')

    # Value KDE plot
    try:
        sns.kdeplot(value_flat, ax=axes[1, 2], fill=True, color='blue', alpha=0.6)
        axes[1, 2].set_title('Value Density (KDE)')
        axes[1, 2].set_xlabel('Value (0-255)')
        axes[1, 2].set_ylabel('Density')
        axes[1, 2].set_xlim(0, 255)
    except Exception:
        axes[1, 2].text(0.5, 0.5, 'KDE not available', ha='center', va='center')

    plt.tight_layout()
    return fig


def create_hsv_scatter_plots(hsv_image, rgb_image=None):
    """
    Create scatter plots showing relationships between HSV dimensions.
    Uses density-based alpha values to highlight concentrations.
    Colors points by their actual RGB values from the image.

    Args:
        hsv_image: HSV image array with shape (height, width, 3)
        rgb_image: Original RGB image (optional, for coloring points)

    Returns:
        Matplotlib figure
    """
    # Flatten arrays and sample for clarity (don't plot all pixels)
    hue_flat = hsv_image[:, :, 0].flatten()
    saturation_flat = hsv_image[:, :, 1].flatten()
    value_flat = hsv_image[:, :, 2].flatten()

    # Sample pixels for better performance (every 10th pixel)
    sample_idx = np.arange(0, len(hue_flat), 10)
    hue_sample = hue_flat[sample_idx]
    saturation_sample = saturation_flat[sample_idx]
    value_sample = value_flat[sample_idx]

    # Get RGB colors if image is provided
    rgb_colors = None
    if rgb_image is not None:
        rgb_flat = rgb_image.reshape(-1, 3)
        rgb_colors = rgb_flat[sample_idx] / 255.0  # Normalize to [0, 1]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Hue vs Saturation - calculate density-based alpha using histogram binning
    h_hs, xedges, yedges = np.histogram2d(hue_sample, saturation_sample, bins=20)
    x_indices = np.digitize(hue_sample, xedges) - 1
    y_indices = np.digitize(saturation_sample, yedges) - 1
    counts_hs = h_hs[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_hs = np.clip(np.sqrt(counts_hs) / np.sqrt(counts_hs.max()) * 0.7 + 0.1, 0.1, 0.8)

    # Hue vs Saturation - color by actual RGB values if available
    if rgb_colors is not None:
        axes[0].scatter(hue_sample, saturation_sample, alpha=alpha_hs, s=10, c=rgb_colors)
    else:
        scatter1 = axes[0].scatter(hue_sample, saturation_sample, alpha=alpha_hs, s=10,
                                   c=hue_sample, cmap='hsv', vmin=0, vmax=180)
        plt.colorbar(scatter1, ax=axes[0])

    axes[0].set_xlabel('Hue (0-180)')
    axes[0].set_ylabel('Saturation (0-255)')
    axes[0].set_title('Hue vs Saturation')
    axes[0].set_xlim(0, 180)
    axes[0].set_ylim(0, 255)
    axes[0].grid(True, alpha=0.3)

    # Hue vs Value - calculate density-based alpha using histogram binning
    h_hv, xedges, yedges = np.histogram2d(hue_sample, value_sample, bins=20)
    x_indices = np.digitize(hue_sample, xedges) - 1
    y_indices = np.digitize(value_sample, yedges) - 1
    counts_hv = h_hv[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_hv = np.clip(np.sqrt(counts_hv) / np.sqrt(counts_hv.max()) * 0.7 + 0.1, 0.1, 0.8)

    # Hue vs Value - color by actual RGB values if available
    if rgb_colors is not None:
        axes[1].scatter(hue_sample, value_sample, alpha=alpha_hv, s=10, c=rgb_colors)
    else:
        scatter2 = axes[1].scatter(hue_sample, value_sample, alpha=alpha_hv, s=10,
                                   c=hue_sample, cmap='hsv', vmin=0, vmax=180)
        plt.colorbar(scatter2, ax=axes[1])

    axes[1].set_xlabel('Hue (0-180)')
    axes[1].set_ylabel('Value (0-255)')
    axes[1].set_title('Hue vs Value')
    axes[1].set_xlim(0, 180)
    axes[1].set_ylim(0, 255)
    axes[1].grid(True, alpha=0.3)

    # Saturation vs Value - calculate density-based alpha using histogram binning
    h_sv, xedges, yedges = np.histogram2d(saturation_sample, value_sample, bins=20)
    x_indices = np.digitize(saturation_sample, xedges) - 1
    y_indices = np.digitize(value_sample, yedges) - 1
    counts_sv = h_sv[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_sv = np.clip(np.sqrt(counts_sv) / np.sqrt(counts_sv.max()) * 0.7 + 0.1, 0.1, 0.8)

    # Saturation vs Value - color by actual RGB values if available
    if rgb_colors is not None:
        axes[2].scatter(saturation_sample, value_sample, alpha=alpha_sv, s=10, c=rgb_colors)
    else:
        scatter3 = axes[2].scatter(saturation_sample, value_sample, alpha=alpha_sv, s=10,
                                   c=value_sample, cmap='gray', vmin=0, vmax=255)
        plt.colorbar(scatter3, ax=axes[2])

    axes[2].set_xlabel('Saturation (0-255)')
    axes[2].set_ylabel('Value (0-255)')
    axes[2].set_title('Saturation vs Value')
    axes[2].set_xlim(0, 255)
    axes[2].set_ylim(0, 255)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def create_lab_comparison(lab_image):
    """
    Create a comparison plot of LAB channels.

    Args:
        lab_image: LAB image array with shape (height, width, 3)
                   L*: 0-100 (lightness)
                   A*: -127 to 127 (green-red)
                   B*: -127 to 127 (blue-yellow)

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # L* channel - Lightness (grayscale)
    im_l = axes[0].imshow(lab_image[:, :, 0], cmap='gray', vmin=0, vmax=100)
    axes[0].set_title('L* - Lightness (0-100)')
    axes[0].axis('off')
    plt.colorbar(im_l, ax=axes[0], fraction=0.046)

    # A* channel - Green to Red
    im_a = axes[1].imshow(lab_image[:, :, 1], cmap='RdYlGn_r', vmin=-127, vmax=127)
    axes[1].set_title('A* - Green to Red (-127 to 127)')
    axes[1].axis('off')
    plt.colorbar(im_a, ax=axes[1], fraction=0.046)

    # B* channel - Blue to Yellow
    im_b = axes[2].imshow(lab_image[:, :, 2], cmap='YlGnBu_r', vmin=-127, vmax=127)
    axes[2].set_title('B* - Blue to Yellow (-127 to 127)')
    axes[2].axis('off')
    plt.colorbar(im_b, ax=axes[2], fraction=0.046)

    plt.tight_layout()
    return fig


def create_lab_density_plots(lab_image):
    """
    Create density plots for LAB channels.

    Args:
        lab_image: LAB image array with shape (height, width, 3)

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Extract and flatten channels
    l_flat = lab_image[:, :, 0].flatten()
    a_flat = lab_image[:, :, 1].flatten()
    b_flat = lab_image[:, :, 2].flatten()

    # L* histogram
    axes[0, 0].hist(l_flat, bins=100, color='gray', alpha=0.7, edgecolor='black')
    axes[0, 0].set_title('L* (Lightness) Distribution')
    axes[0, 0].set_xlabel('L* (0-100)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_xlim(0, 100)

    # A* histogram
    axes[0, 1].hist(a_flat, bins=100, color='red', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('A* (Green-Red) Distribution')
    axes[0, 1].set_xlabel('A* (-127 to 127)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_xlim(-127, 127)

    # B* histogram
    axes[0, 2].hist(b_flat, bins=100, color='blue', alpha=0.7, edgecolor='black')
    axes[0, 2].set_title('B* (Blue-Yellow) Distribution')
    axes[0, 2].set_xlabel('B* (-127 to 127)')
    axes[0, 2].set_ylabel('Frequency')
    axes[0, 2].set_xlim(-127, 127)

    # L* KDE plot
    try:
        sns.kdeplot(l_flat, ax=axes[1, 0], fill=True, color='gray', alpha=0.6)
        axes[1, 0].set_title('L* Density (KDE)')
        axes[1, 0].set_xlabel('L* (0-100)')
        axes[1, 0].set_ylabel('Density')
        axes[1, 0].set_xlim(0, 100)
    except Exception:
        axes[1, 0].text(0.5, 0.5, 'KDE not available', ha='center', va='center')

    # A* KDE plot
    try:
        sns.kdeplot(a_flat, ax=axes[1, 1], fill=True, color='red', alpha=0.6)
        axes[1, 1].set_title('A* Density (KDE)')
        axes[1, 1].set_xlabel('A* (-127 to 127)')
        axes[1, 1].set_ylabel('Density')
        axes[1, 1].set_xlim(-127, 127)
    except Exception:
        axes[1, 1].text(0.5, 0.5, 'KDE not available', ha='center', va='center')

    # B* KDE plot
    try:
        sns.kdeplot(b_flat, ax=axes[1, 2], fill=True, color='blue', alpha=0.6)
        axes[1, 2].set_title('B* Density (KDE)')
        axes[1, 2].set_xlabel('B* (-127 to 127)')
        axes[1, 2].set_ylabel('Density')
        axes[1, 2].set_xlim(-127, 127)
    except Exception:
        axes[1, 2].text(0.5, 0.5, 'KDE not available', ha='center', va='center')

    plt.tight_layout()
    return fig


def create_lab_scatter_plots(lab_image, rgb_image=None):
    """
    Create scatter plots showing relationships between LAB dimensions.
    Uses density-based alpha values to highlight concentrations.
    Colors points by their actual RGB values from the image.

    Args:
        lab_image: LAB image array with shape (height, width, 3)
        rgb_image: Original RGB image (optional, for coloring points)

    Returns:
        Matplotlib figure
    """
    # Flatten arrays and sample for clarity (don't plot all pixels)
    l_flat = lab_image[:, :, 0].flatten()
    a_flat = lab_image[:, :, 1].flatten()
    b_flat = lab_image[:, :, 2].flatten()

    # Sample pixels for better performance (every 10th pixel)
    sample_idx = np.arange(0, len(l_flat), 10)
    l_sample = l_flat[sample_idx]
    a_sample = a_flat[sample_idx]
    b_sample = b_flat[sample_idx]

    # Get RGB colors if image is provided
    rgb_colors = None
    if rgb_image is not None:
        rgb_flat = rgb_image.reshape(-1, 3)
        rgb_colors = rgb_flat[sample_idx] / 255.0  # Normalize to [0, 1]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # A* vs B* (color space diagram) - calculate density-based alpha
    h_ab, xedges, yedges = np.histogram2d(a_sample, b_sample, bins=20)
    x_indices = np.digitize(a_sample, xedges) - 1
    y_indices = np.digitize(b_sample, yedges) - 1
    counts_ab = h_ab[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_ab = np.clip(np.sqrt(counts_ab) / np.sqrt(counts_ab.max()) * 0.7 + 0.1, 0.1, 0.8)

    # A* vs B* - color by actual RGB values if available
    if rgb_colors is not None:
        axes[0].scatter(a_sample, b_sample, alpha=alpha_ab, s=10, c=rgb_colors)
    else:
        axes[0].scatter(a_sample, b_sample, alpha=alpha_ab, s=10, c='blue')

    axes[0].set_xlabel('A* (Green ← → Red)')
    axes[0].set_ylabel('B* (Blue ← → Yellow)')
    axes[0].set_title('A* vs B* (Color Plane)')
    axes[0].set_xlim(-127, 127)
    axes[0].set_ylim(-127, 127)
    axes[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[0].axvline(x=0, color='k', linestyle='--', alpha=0.3)
    axes[0].grid(True, alpha=0.3)

    # L* vs A* - calculate density-based alpha
    h_la, xedges, yedges = np.histogram2d(l_sample, a_sample, bins=20)
    x_indices = np.digitize(l_sample, xedges) - 1
    y_indices = np.digitize(a_sample, yedges) - 1
    counts_la = h_la[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_la = np.clip(np.sqrt(counts_la) / np.sqrt(counts_la.max()) * 0.7 + 0.1, 0.1, 0.8)

    # L* vs A* - color by actual RGB values if available
    if rgb_colors is not None:
        axes[1].scatter(l_sample, a_sample, alpha=alpha_la, s=10, c=rgb_colors)
    else:
        axes[1].scatter(l_sample, a_sample, alpha=alpha_la, s=10, c='green')

    axes[1].set_xlabel('L* (Lightness)')
    axes[1].set_ylabel('A* (Green ← → Red)')
    axes[1].set_title('L* vs A*')
    axes[1].set_xlim(0, 100)
    axes[1].set_ylim(-127, 127)
    axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[1].grid(True, alpha=0.3)

    # L* vs B* - calculate density-based alpha
    h_lb, xedges, yedges = np.histogram2d(l_sample, b_sample, bins=20)
    x_indices = np.digitize(l_sample, xedges) - 1
    y_indices = np.digitize(b_sample, yedges) - 1
    counts_lb = h_lb[np.clip(x_indices, 0, 19), np.clip(y_indices, 0, 19)]
    alpha_lb = np.clip(np.sqrt(counts_lb) / np.sqrt(counts_lb.max()) * 0.7 + 0.1, 0.1, 0.8)

    # L* vs B* - color by actual RGB values if available
    if rgb_colors is not None:
        axes[2].scatter(l_sample, b_sample, alpha=alpha_lb, s=10, c=rgb_colors)
    else:
        axes[2].scatter(l_sample, b_sample, alpha=alpha_lb, s=10, c='orange')

    axes[2].set_xlabel('L* (Lightness)')
    axes[2].set_ylabel('B* (Blue ← → Yellow)')
    axes[2].set_title('L* vs B*')
    axes[2].set_xlim(0, 100)
    axes[2].set_ylim(-127, 127)
    axes[2].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

