"""
Visualization utilities for color transfer feature.
"""
import numpy as np
import matplotlib.pyplot as plt
from artanalyzer.core.color_transfer import ColorTransfer
from skimage import color
from artanalyzer.colorspaces.oklab_utils import rgb_to_oklab, oklab_to_oklch


def create_color_transfer_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray,
    title: str = "Color Transfer Comparison"
) -> plt.Figure:
    """
    Create a side-by-side comparison of source, reference, and transferred images.

    Args:
        source: Source image
        reference: Reference image
        transferred: Color-transferred image
        title: Title for the figure

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(source)
    axes[0].set_title('Source Image')
    axes[0].axis('off')

    axes[1].imshow(reference)
    axes[1].set_title('Reference Image')
    axes[1].axis('off')

    axes[2].imshow(transferred)
    axes[2].set_title('Transferred')
    axes[2].axis('off')

    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def create_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray,
    colorspace: str = 'rgb'
) -> plt.Figure:
    """
    Create histogram comparison between source, reference, and transferred.

    Args:
        source: Source image
        reference: Reference image
        transferred: Color-transferred image
        colorspace: 'rgb', 'lab', 'hsv', 'hcl', 'xyz', 'luv', or 'ycbcr'

    Returns:
        Matplotlib figure with histograms
    """
    colorspace_map = {
        'rgb': _create_rgb_histogram_comparison,
        'lab': _create_lab_histogram_comparison,
        'hsv': _create_hsv_histogram_comparison,
        'hcl': _create_hcl_histogram_comparison,
        'oklab': _create_oklab_histogram_comparison,
        'oklch': _create_oklch_histogram_comparison,
        'xyz': _create_xyz_histogram_comparison,
        'luv': _create_luv_histogram_comparison,
        'ycbcr': _create_ycbcr_histogram_comparison,
    }

    if colorspace not in colorspace_map:
        raise ValueError(f"Unknown colorspace: {colorspace}. Supported: {list(colorspace_map.keys())}")

    return colorspace_map[colorspace](source, reference, transferred)


def _create_rgb_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """Create RGB histogram comparison."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    colors_rgb = ['red', 'green', 'blue']
    channel_names = ['Red', 'Green', 'Blue']

    for i, (ax, color_name, channel_name) in enumerate(zip(axes, colors_rgb, channel_names)):
        ax.hist(source[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               color=color_name, label='Source')
        ax.hist(reference[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               color='gray', label='Reference', linestyle='--')
        ax.hist(transferred[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               color='orange', label='Transferred')

        ax.set_title(f'{channel_name} Channel')
        ax.set_xlabel('Pixel Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_xlim(0, 255)

    fig.suptitle('RGB Histogram Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def _create_lab_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """Create LAB histogram comparison."""
    # Convert to LAB
    source_lab = color.rgb2lab(source / 255.0)
    reference_lab = color.rgb2lab(reference / 255.0)
    transferred_lab = color.rgb2lab(transferred / 255.0)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    channel_names = ['L* (Lightness)', 'a* (Green-Red)', 'b* (Blue-Yellow)']
    channel_ranges = [(0, 100), (-127, 127), (-127, 127)]

    for i, (ax, channel_name, (min_val, max_val)) in enumerate(
        zip(axes, channel_names, channel_ranges)
    ):
        ax.hist(source_lab[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Source', color='blue')
        ax.hist(reference_lab[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Reference', color='gray', linestyle='--')
        ax.hist(transferred_lab[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Transferred', color='orange')

        ax.set_title(channel_name)
        ax.set_xlabel('Channel Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_xlim(min_val, max_val)

    fig.suptitle('LAB Histogram Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def _create_hsv_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """Create HSV histogram comparison."""
    import cv2

    # Convert to HSV
    source_hsv = cv2.cvtColor(source, cv2.COLOR_RGB2HSV)
    reference_hsv = cv2.cvtColor(reference, cv2.COLOR_RGB2HSV)
    transferred_hsv = cv2.cvtColor(transferred, cv2.COLOR_RGB2HSV)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    channel_names = ['Hue', 'Saturation', 'Value']
    channel_ranges = [(0, 180), (0, 255), (0, 255)]

    for i, (ax, channel_name, (min_val, max_val)) in enumerate(
        zip(axes, channel_names, channel_ranges)
    ):
        ax.hist(source_hsv[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Source', color='blue')
        ax.hist(reference_hsv[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Reference', color='gray', linestyle='--')
        ax.hist(transferred_hsv[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Transferred', color='orange')

        ax.set_title(channel_name)
        ax.set_xlabel('Channel Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_xlim(min_val, max_val)

    fig.suptitle('HSV Histogram Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def _create_hcl_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """Create HCL (LCh) histogram comparison."""
    # Convert to LAB then LCh
    source_lab = color.rgb2lab(source / 255.0)
    reference_lab = color.rgb2lab(reference / 255.0)
    transferred_lab = color.rgb2lab(transferred / 255.0)

    source_lch = color.lab2lch(source_lab)
    reference_lch = color.lab2lch(reference_lab)
    transferred_lch = color.lab2lch(transferred_lab)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    channel_names = ['Lightness (L*)', 'Chroma (C*)', 'Hue (H)']

    # For hue, convert from radians to degrees
    for i, (ax, channel_name) in enumerate(zip(axes, channel_names)):
        if i == 2:  # Hue channel in radians
            source_channel = np.degrees(source_lch[:, :, i])
            reference_channel = np.degrees(reference_lch[:, :, i])
            transferred_channel = np.degrees(transferred_lch[:, :, i])
            range_vals = (0, 360)
        elif i == 0:  # Lightness
            source_channel = source_lch[:, :, i]
            reference_channel = reference_lch[:, :, i]
            transferred_channel = transferred_lch[:, :, i]
            range_vals = (0, 100)
        else:  # Chroma
            source_channel = source_lch[:, :, i]
            reference_channel = reference_lch[:, :, i]
            transferred_channel = transferred_lch[:, :, i]
            range_vals = (0, 150)

        ax.hist(source_channel.flatten(), bins=50, alpha=0.5, density=True,
               label='Source', color='blue')
        ax.hist(reference_channel.flatten(), bins=50, alpha=0.5, density=True,
               label='Reference', color='gray', linestyle='--')
        ax.hist(transferred_channel.flatten(), bins=50, alpha=0.5, density=True,
               label='Transferred', color='orange')

        ax.set_title(channel_name)
        ax.set_xlabel('Channel Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_xlim(range_vals)

    fig.suptitle('HCL (LCh) Histogram Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def _create_xyz_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """Create XYZ histogram comparison."""
    # Convert to XYZ
    source_xyz = color.rgb2xyz(source / 255.0)
    reference_xyz = color.rgb2xyz(reference / 255.0)
    transferred_xyz = color.rgb2xyz(transferred / 255.0)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    channel_names = ['X', 'Y (Luminance)', 'Z']

    for i, (ax, channel_name) in enumerate(zip(axes, channel_names)):
        ax.hist(source_xyz[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Source', color='blue')
        ax.hist(reference_xyz[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Reference', color='gray', linestyle='--')
        ax.hist(transferred_xyz[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Transferred', color='orange')

        ax.set_title(channel_name)
        ax.set_xlabel('Channel Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_xlim(0, 1)

    fig.suptitle('XYZ Histogram Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def _create_oklab_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """Create Oklab histogram comparison."""
    source_oklab = rgb_to_oklab(source)
    reference_oklab = rgb_to_oklab(reference)
    transferred_oklab = rgb_to_oklab(transferred)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    channel_names = ['L (Lightness)', 'a (Green-Red)', 'b (Blue-Yellow)']
    channel_ranges = [(0.0, 1.0), (-0.4, 0.4), (-0.4, 0.4)]

    for i, (ax, channel_name, (min_val, max_val)) in enumerate(
        zip(axes, channel_names, channel_ranges)
    ):
        ax.hist(source_oklab[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Source', color='blue')
        ax.hist(reference_oklab[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Reference', color='gray', linestyle='--')
        ax.hist(transferred_oklab[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Transferred', color='orange')

        ax.set_title(channel_name)
        ax.set_xlabel('Channel Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_xlim(min_val, max_val)

    fig.suptitle('Oklab Histogram Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def _create_oklch_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """Create Oklch histogram comparison."""
    source_oklch = oklab_to_oklch(rgb_to_oklab(source))
    reference_oklch = oklab_to_oklch(rgb_to_oklab(reference))
    transferred_oklch = oklab_to_oklch(rgb_to_oklab(transferred))

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    channel_names = ['L (Lightness)', 'C (Chroma)', 'H (Hue)']
    channel_ranges = [(0.0, 1.0), (0.0, 0.4), (0.0, 360.0)]

    for i, (ax, channel_name, (min_val, max_val)) in enumerate(
        zip(axes, channel_names, channel_ranges)
    ):
        ax.hist(source_oklch[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Source', color='blue')
        ax.hist(reference_oklch[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Reference', color='gray', linestyle='--')
        ax.hist(transferred_oklch[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Transferred', color='orange')

        ax.set_title(channel_name)
        ax.set_xlabel('Channel Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_xlim(min_val, max_val)

    fig.suptitle('Oklch Histogram Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def _create_luv_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """Create LUV histogram comparison."""
    # Convert to LUV
    source_luv = color.rgb2luv(source / 255.0)
    reference_luv = color.rgb2luv(reference / 255.0)
    transferred_luv = color.rgb2luv(transferred / 255.0)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    channel_names = ['L* (Lightness)', 'u* (Green-Red)', 'v* (Blue-Yellow)']
    channel_ranges = [(0, 100), (-100, 100), (-100, 100)]

    for i, (ax, channel_name, (min_val, max_val)) in enumerate(
        zip(axes, channel_names, channel_ranges)
    ):
        ax.hist(source_luv[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Source', color='blue')
        ax.hist(reference_luv[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Reference', color='gray', linestyle='--')
        ax.hist(transferred_luv[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Transferred', color='orange')

        ax.set_title(channel_name)
        ax.set_xlabel('Channel Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_xlim(min_val, max_val)

    fig.suptitle('LUV Histogram Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def _create_ycbcr_histogram_comparison(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """Create YCbCr histogram comparison."""
    import cv2

    # Convert to YCrCb (OpenCV convention)
    source_ycrcb = cv2.cvtColor(source, cv2.COLOR_RGB2YCrCb)
    reference_ycrcb = cv2.cvtColor(reference, cv2.COLOR_RGB2YCrCb)
    transferred_ycrcb = cv2.cvtColor(transferred, cv2.COLOR_RGB2YCrCb)

    # Swap to YCbCr order for display
    source_ycbcr = source_ycrcb.copy()
    source_ycbcr[:, :, 1] = source_ycrcb[:, :, 2]  # Cb
    source_ycbcr[:, :, 2] = source_ycrcb[:, :, 1]  # Cr

    reference_ycbcr = reference_ycrcb.copy()
    reference_ycbcr[:, :, 1] = reference_ycrcb[:, :, 2]
    reference_ycbcr[:, :, 2] = reference_ycrcb[:, :, 1]

    transferred_ycbcr = transferred_ycrcb.copy()
    transferred_ycbcr[:, :, 1] = transferred_ycrcb[:, :, 2]
    transferred_ycbcr[:, :, 2] = transferred_ycrcb[:, :, 1]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    channel_names = ['Y (Luma)', 'Cb (Blue-difference)', 'Cr (Red-difference)']

    for i, (ax, channel_name) in enumerate(zip(axes, channel_names)):
        ax.hist(source_ycbcr[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Source', color='blue')
        ax.hist(reference_ycbcr[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Reference', color='gray', linestyle='--')
        ax.hist(transferred_ycbcr[:, :, i].flatten(), bins=50, alpha=0.5, density=True,
               label='Transferred', color='orange')

        ax.set_title(channel_name)
        ax.set_xlabel('Channel Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.set_xlim(0, 255)

    fig.suptitle('YCbCr Histogram Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def create_statistics_table(
    source: np.ndarray,
    reference: np.ndarray,
    transferred: np.ndarray
) -> str:
    """
    Create a markdown table comparing statistics.

    Args:
        source: Source image
        reference: Reference image
        transferred: Color-transferred image

    Returns:
        Markdown table string
    """
    # Compute color differences
    metrics = ColorTransfer.compute_color_difference(reference, transferred)

    lines = [
        "| Metric | Before Transfer | After Transfer | Target |",
        "|--------|-----------------|----------------|--------|"
    ]

    # RGB statistics
    for i, name in enumerate(['R', 'G', 'B']):
        source_mean = source[:, :, i].mean()
        reference_mean = reference[:, :, i].mean()
        transferred_mean = transferred[:, :, i].mean()

        lines.append(
            f"| {name} Mean | {source_mean:.1f} | {transferred_mean:.1f} | {reference_mean:.1f} |"
        )

    lines.append("|  |  |  |  |")  # Separator

    # LAB statistics
    source_lab = color.rgb2lab(source / 255.0)
    reference_lab = color.rgb2lab(reference / 255.0)
    transferred_lab = color.rgb2lab(transferred / 255.0)

    for i, name in enumerate(['L*', 'a*', 'b*']):
        source_mean = source_lab[:, :, i].mean()
        reference_mean = reference_lab[:, :, i].mean()
        transferred_mean = transferred_lab[:, :, i].mean()

        lines.append(
            f"| {name} Mean | {source_mean:.2f} | {transferred_mean:.2f} | {reference_mean:.2f} |"
        )

    return "\n".join(lines)


def create_difference_visualization(
    source: np.ndarray,
    transferred: np.ndarray
) -> plt.Figure:
    """
    Create a visualization showing pixel-wise differences.

    Args:
        source: Source image
        transferred: Color-transferred image

    Returns:
        Matplotlib figure with difference map
    """
    # Compute difference in LAB space (more perceptually meaningful)
    source_lab = color.rgb2lab(source / 255.0)
    transferred_lab = color.rgb2lab(transferred / 255.0)

    # Compute delta E (CIE76)
    delta_e = np.sqrt(
        (source_lab[:, :, 0] - transferred_lab[:, :, 0]) ** 2 +
        (source_lab[:, :, 1] - transferred_lab[:, :, 1]) ** 2 +
        (source_lab[:, :, 2] - transferred_lab[:, :, 2]) ** 2
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Show difference map
    im1 = axes[0].imshow(delta_e, cmap='hot')
    axes[0].set_title('Delta E (Color Difference)')
    axes[0].axis('off')
    plt.colorbar(im1, ax=axes[0], fraction=0.046)

    # Show distribution of differences
    axes[1].hist(delta_e.flatten(), bins=50, color='orange', alpha=0.7, edgecolor='black')
    axes[1].set_title('Distribution of Color Differences')
    axes[1].set_xlabel('Delta E (CIE76)')
    axes[1].set_ylabel('Pixel Count')
    axes[1].grid(True, alpha=0.3)

    mean_delta_e = delta_e.mean()
    axes[1].axvline(mean_delta_e, color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {mean_delta_e:.2f}')
    axes[1].legend()

    fig.suptitle('Color Difference Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

