"""
HSV color space implementation.
"""
import numpy as np
import cv2
from artanalyzer.core.color_space import ColorSpace, ChannelMetadata
from artanalyzer.core.registry import ColorSpaceRegistry


@ColorSpaceRegistry.register
class HSVColorSpace(ColorSpace):
    """
    HSV (Hue, Saturation, Value) color space.

    A cylindrical color model that represents colors in terms of:
    - Hue: The color type (0-180° in OpenCV)
    - Saturation: Color purity (0-255)
    - Value: Brightness (0-255)
    """

    @property
    def name(self) -> str:
        return "hsv"

    @property
    def display_name(self) -> str:
        return "HSV Color Space"

    @property
    def description(self) -> str:
        return (
            "**HSV (Hue, Saturation, Value)** is a cylindrical color model that "
            "represents colors more intuitively than RGB. Hue determines the color "
            "type (0-180°), Saturation controls color purity (0-255), and Value "
            "represents brightness (0-255). Note: OpenCV uses 0-180° for hue instead "
            "of the standard 0-360° to fit in an 8-bit value."
        )

    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata(
                name="hue",
                display_name="Hue",
                range_min=0,
                range_max=180,
                colormap="hsv",
                description="Color type (0-180°, OpenCV convention)"
            ),
            ChannelMetadata(
                name="saturation",
                display_name="Saturation",
                range_min=0,
                range_max=255,
                colormap="gray",
                description="Color purity/intensity (0-255)"
            ),
            ChannelMetadata(
                name="value",
                display_name="Value",
                range_min=0,
                range_max=255,
                colormap="gray",
                description="Brightness (0-255)"
            ),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """Convert RGB to HSV using OpenCV."""
        return cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)

