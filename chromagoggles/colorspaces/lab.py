# Copyright (c) 2026 Baer Ververgaert. All rights reserved.
"""
LAB color space implementation.
"""
import numpy as np
from skimage import color
from chromagoggles.core.color_space import ColorSpace, ChannelMetadata
from chromagoggles.core.registry import ColorSpaceRegistry


@ColorSpaceRegistry.register
class LABColorSpace(ColorSpace):
    """
    CIELAB (L*a*b*) color space.

    A perceptually uniform color space where:
    - L*: Lightness (0-100)
    - a*: Green-Red axis (-127 to 127)
    - b*: Blue-Yellow axis (-127 to 127)
    """

    @property
    def name(self) -> str:
        return "lab"

    @property
    def display_name(self) -> str:
        return "LAB Color Space"

    @property
    def description(self) -> str:
        return (
            "**CIELAB (L\\*a\\*b\\*)** is a perceptually uniform color space designed "
            "to approximate human vision. L\\* represents lightness (0-100), a\\* "
            "represents the green-red axis (negative = green, positive = red), and "
            "b\\* represents the blue-yellow axis (negative = blue, positive = yellow). "
            "Equal distances in LAB space correspond to roughly equal perceived color differences."
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
                name="a",
                display_name="A* (Green-Red)",
                range_min=-127,
                range_max=127,
                colormap="RdYlGn_r",
                description="Green (negative) to Red (positive) axis"
            ),
            ChannelMetadata(
                name="b",
                display_name="B* (Blue-Yellow)",
                range_min=-127,
                range_max=127,
                colormap="YlGnBu_r",
                description="Blue (negative) to Yellow (positive) axis"
            ),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """Convert RGB to LAB using scikit-image."""
        rgb_normalized = rgb_image / 255.0
        return color.rgb2lab(rgb_normalized)
