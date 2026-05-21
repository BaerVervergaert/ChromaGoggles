# Copyright (c) 2026 Baer Ververgaert. All rights reserved.
"""
LUV color space implementation.
"""
import numpy as np
from skimage import color
from chromagoggles.core.color_space import ColorSpace, ChannelMetadata
from chromagoggles.core.registry import ColorSpaceRegistry


@ColorSpaceRegistry.register
class LUVColorSpace(ColorSpace):
    """
    CIELUV (L*u*v*) color space.

    A perceptually uniform color space where:
    - L*: Lightness (0-100)
    - u*: Green-Red axis (approximately -100 to 100)
    - v*: Blue-Yellow axis (approximately -100 to 100)
    """

    @property
    def name(self) -> str:
        return "luv"

    @property
    def display_name(self) -> str:
        return "LUV Color Space"

    @property
    def description(self) -> str:
        return (
            "**CIELUV (L\\*u\\*v\\*)** is another perceptually uniform color space, "
            "similar to LAB but with different chromatic components. L\\* represents "
            "lightness (0-100), u\\* represents a green-red axis, and v\\* represents "
            "a blue-yellow axis. LUV is often preferred for applications involving "
            "additive color mixing or displays."
        )

    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata(
                name="lightness",
                display_name="L* (Lightness)",
                range_min=0,
                range_max=100,
                colormap="gray",
                description="Lightness from black to white (0-100)"
            ),
            ChannelMetadata(
                name="u",
                display_name="U* (Green-Red)",
                range_min=-100,
                range_max=100,
                colormap="RdYlGn_r",
                description="Green (negative) to Red (positive) axis"
            ),
            ChannelMetadata(
                name="v",
                display_name="V* (Blue-Yellow)",
                range_min=-100,
                range_max=100,
                colormap="YlGnBu_r",
                description="Blue (negative) to Yellow (positive) axis"
            ),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """Convert RGB to LUV using scikit-image."""
        rgb_normalized = rgb_image / 255.0
        return color.rgb2luv(rgb_normalized)
