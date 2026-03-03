"""
YCbCr color space implementation.
"""
import numpy as np
import cv2
from artanalyzer.core.color_space import ColorSpace, ChannelMetadata
from artanalyzer.core.registry import ColorSpaceRegistry


@ColorSpaceRegistry.register
class YCbCrColorSpace(ColorSpace):
    """
    YCbCr color space.

    A color space used in video and image compression where:
    - Y: Luma (brightness)
    - Cb: Blue-difference chroma
    - Cr: Red-difference chroma
    """

    @property
    def name(self) -> str:
        return "ycbcr"

    @property
    def display_name(self) -> str:
        return "YCbCr Color Space"

    @property
    def description(self) -> str:
        return (
            "**YCbCr** is a color space commonly used in video and image compression "
            "(e.g., JPEG, MPEG). Y represents luma (brightness), Cb represents the "
            "blue-difference chroma component, and Cr represents the red-difference "
            "chroma component. This separation allows for efficient compression by "
            "exploiting the human visual system's greater sensitivity to luminance."
        )

    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata(
                name="y",
                display_name="Y (Luma)",
                range_min=0,
                range_max=255,
                colormap="gray",
                description="Luma/brightness component (0-255)"
            ),
            ChannelMetadata(
                name="cb",
                display_name="Cb (Blue-difference)",
                range_min=0,
                range_max=255,
                colormap="RdBu_r",
                description="Blue-difference chroma (0-255)"
            ),
            ChannelMetadata(
                name="cr",
                display_name="Cr (Red-difference)",
                range_min=0,
                range_max=255,
                colormap="RdYlGn_r",
                description="Red-difference chroma (0-255)"
            ),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """Convert RGB to YCbCr using OpenCV."""
        # OpenCV converts to YCrCb, so we need to swap the channels
        ycrcb = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2YCrCb)
        # Swap Cr and Cb to get YCbCr
        ycbcr = ycrcb.copy()
        ycbcr[:, :, 1] = ycrcb[:, :, 2]  # Cb
        ycbcr[:, :, 2] = ycrcb[:, :, 1]  # Cr
        return ycbcr

    def supports_statistics_tab(self) -> bool:
        """YCbCr doesn't need a statistics tab in the current UI."""
        return False

