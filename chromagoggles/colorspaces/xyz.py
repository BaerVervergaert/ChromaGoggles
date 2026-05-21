"""
XYZ color space implementation.
"""
import numpy as np
from skimage import color
from chromagoggles.core.color_space import ColorSpace, ChannelMetadata
from chromagoggles.core.registry import ColorSpaceRegistry


@ColorSpaceRegistry.register
class XYZColorSpace(ColorSpace):
    """
    CIE XYZ color space.

    A tristimulus color space based on human color perception:
    - X: Red-like component (mix of cone responses)
    - Y: Luminance (brightness)
    - Z: Blue-like component (mostly blue cone response)
    """

    @property
    def name(self) -> str:
        return "xyz"

    @property
    def display_name(self) -> str:
        return "XYZ Color Space"

    @property
    def description(self) -> str:
        return (
            "**CIE XYZ** is a tristimulus color space based on human color perception. "
            "X represents a red-like component (derived from red and green cone responses), "
            "Y represents luminance (brightness), and Z represents a blue-like component "
            "(primarily blue cone response). This is the foundation for many other color spaces."
        )

    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata(
                name="x",
                display_name="X (Red-like)",
                range_min=0,
                range_max=1,
                colormap="hot",  # Warm colors for red-like component
                description="Red-like tristimulus value (0-1)"
            ),
            ChannelMetadata(
                name="y",
                display_name="Y (Luminance)",
                range_min=0,
                range_max=1,
                colormap="gray",  # Grayscale for luminance
                description="Luminance/brightness (0-1)"
            ),
            ChannelMetadata(
                name="z",
                display_name="Z (Blue-like)",
                range_min=0,
                range_max=1,
                colormap="cool",  # Cool colors for blue-like component
                description="Blue-like tristimulus value (0-1)"
            ),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """Convert RGB to XYZ using scikit-image."""
        rgb_normalized = rgb_image / 255.0
        return color.rgb2xyz(rgb_normalized)

