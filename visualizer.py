"""
Visualization module for creating plots and displays of image analysis.
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure


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

    # Hue - use HSV colormap for better representation
    im1 = axes[0].imshow(hue, cmap='hsv', vmin=0, vmax=360)
    axes[0].set_title('Hue (0-360°)')
    axes[0].axis('off')
    plt.colorbar(im1, ax=axes[0], fraction=0.046)

    # Chroma
    im2 = axes[1].imshow(chroma, cmap='viridis')
    axes[1].set_title('Chroma')
    axes[1].axis('off')
    plt.colorbar(im2, ax=axes[1], fraction=0.046)

    # Luminance
    im3 = axes[2].imshow(luminance, cmap='gray')
    axes[2].set_title('Luminance (L*)')
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
    axes[0, 1].imshow(hsv[:, :, 0], cmap='hsv')
    axes[0, 1].set_title('HSV - Hue')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(hsv[:, :, 1], cmap='gray')
    axes[0, 2].set_title('HSV - Saturation')
    axes[0, 2].axis('off')

    axes[0, 3].imshow(hsv[:, :, 2], cmap='gray')
    axes[0, 3].set_title('HSV - Value')
    axes[0, 3].axis('off')

    # LAB channels
    axes[1, 0].imshow(lab[:, :, 0], cmap='gray')
    axes[1, 0].set_title('LAB - Lightness')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(lab[:, :, 1], cmap='RdYlGn')
    axes[1, 1].set_title('LAB - A (green-red)')
    axes[1, 1].axis('off')

    axes[1, 2].imshow(lab[:, :, 2], cmap='YlGnBu')
    axes[1, 2].set_title('LAB - B (blue-yellow)')
    axes[1, 2].axis('off')

    # YCbCr Y channel
    axes[1, 3].imshow(ycbcr[:, :, 0], cmap='gray')
    axes[1, 3].set_title('YCbCr - Luma (Y)')
    axes[1, 3].axis('off')

    plt.tight_layout()
    return fig

