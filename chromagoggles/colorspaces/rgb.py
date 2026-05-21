"""
RGB color space implementation.
"""
import numpy as np
from chromagoggles.core.color_space import ColorSpace, ChannelMetadata
from chromagoggles.core.registry import ColorSpaceRegistry


@ColorSpaceRegistry.register
class RGBColorSpace(ColorSpace):
    """
    RGB (Red, Green, Blue) color space.

    An additive color model where colors are created by combining
    red, green, and blue light. This is the native color space for
    most digital images.
    """

    @property
    def name(self) -> str:
        return "rgb"

    @property
    def display_name(self) -> str:
        return "RGB Channels"

    @property
    def description(self) -> str:
        return (
            "**RGB (Red, Green, Blue)** is an additive color model where colors are "
            "created by combining different intensities of red, green, and blue light. "
            "Each channel represents the intensity of one primary color, ranging from "
            "0 (no intensity) to 255 (full intensity)."
        )

    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata(
                name="red",
                display_name="Red Channel",
                range_min=0,
                range_max=255,
                colormap="Reds",
                description="Red component intensity (0-255)"
            ),
            ChannelMetadata(
                name="green",
                display_name="Green Channel",
                range_min=0,
                range_max=255,
                colormap="Greens",
                description="Green component intensity (0-255)"
            ),
            ChannelMetadata(
                name="blue",
                display_name="Blue Channel",
                range_min=0,
                range_max=255,
                colormap="Blues",
                description="Blue component intensity (0-255)"
            ),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """RGB to RGB is identity transform."""
        return rgb_image.copy()

