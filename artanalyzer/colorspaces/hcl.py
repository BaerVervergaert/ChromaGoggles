"""
HCL (CIELCh) color space implementation.
"""
import numpy as np
from skimage import color
from artanalyzer.core.color_space import ColorSpace, ChannelMetadata
from artanalyzer.core.registry import ColorSpaceRegistry


@ColorSpaceRegistry.register
class HCLColorSpace(ColorSpace):
    """
    HCL (CIELCh) color space - cylindrical representation of LAB.

    A perceptually uniform cylindrical color space where:
    - L*: Lightness (0-100)
    - C*: Chroma/saturation (0-100+)
    - H: Hue angle (0-360°)
    """

    @property
    def name(self) -> str:
        return "hcl"

    @property
    def display_name(self) -> str:
        return "HCL (CIELCh)"

    @property
    def description(self) -> str:
        return (
            "**HCL (CIELCh)** is the cylindrical representation of the CIELAB color space. "
            "It uses Hue (color type, 0-360°), Chroma (color saturation/purity), and "
            "Luminance (brightness, 0-100). This representation is often more intuitive "
            "than LAB's Cartesian coordinates while maintaining perceptual uniformity."
        )

    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata(
                name="hue",
                display_name="Hue",
                range_min=0,
                range_max=360,
                colormap="lch_hue",  # Custom colormap
                description="Hue angle in perceptual color wheel (0-360°)"
            ),
            ChannelMetadata(
                name="chroma",
                display_name="Chroma",
                range_min=0,
                range_max=100,
                colormap="gray",
                description="Color saturation/purity (0-100+)"
            ),
            ChannelMetadata(
                name="luminance",
                display_name="Luminance",
                range_min=0,
                range_max=100,
                colormap="gray",
                description="Perceptual lightness (0-100)"
            ),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """
        Convert RGB to LCh (HCL) using scikit-image.

        Returns array with channels in order: [H, C, L]
        """
        # Convert RGB to LAB first
        rgb_normalized = rgb_image / 255.0
        lab_image = color.rgb2lab(rgb_normalized)

        # Convert LAB to LCH
        lch_image = color.lab2lch(lab_image)

        # lch_image has channels as [L, C, H] where H is in radians
        # We need [H, C, L] with H in degrees
        h, w = lch_image.shape[:2]
        hcl_image = np.zeros((h, w, 3), dtype=np.float64)

        # Hue: convert from radians to degrees
        hcl_image[:, :, 0] = np.degrees(lch_image[:, :, 2])  # H (0-360°)
        hcl_image[:, :, 1] = lch_image[:, :, 1]  # C
        hcl_image[:, :, 2] = lch_image[:, :, 0]  # L

        return hcl_image

