"""
LMS color space implementation.
"""
import numpy as np
import colour
from chromagoggles.core.color_space import ColorSpace, ChannelMetadata
from chromagoggles.core.registry import ColorSpaceRegistry


@ColorSpaceRegistry.register
class LMSColorSpace(ColorSpace):
    """
    LMS cone-response color space.

    This space models approximate responses of the human eye cone cells:
    - L: Long-wavelength cone response (red-sensitive)
    - M: Medium-wavelength cone response (green-sensitive)
    - S: Short-wavelength cone response (blue-sensitive)
    """

    @property
    def name(self) -> str:
        return "lms"

    @property
    def display_name(self) -> str:
        return "LMS Color Space"

    @property
    def description(self) -> str:
        return (
            "**LMS** approximates human cone responses. L corresponds to long-wave "
            "(red-sensitive), M to medium-wave (green-sensitive), and S to short-wave "
            "(blue-sensitive) cone channels."
        )

    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata(
                name="l",
                display_name="L (Long-wave)",
                range_min=-0.1,
                range_max=1.2,
                colormap="Reds",
                description="Long-wavelength cone response",
            ),
            ChannelMetadata(
                name="m",
                display_name="M (Medium-wave)",
                range_min=-0.1,
                range_max=1.2,
                colormap="Greens",
                description="Medium-wavelength cone response",
            ),
            ChannelMetadata(
                name="s",
                display_name="S (Short-wave)",
                range_min=-0.1,
                range_max=1.2,
                colormap="Blues",
                description="Short-wavelength cone response",
            ),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """Convert RGB to LMS using sRGB -> XYZ -> CAT02 LMS."""
        rgb = np.clip(rgb_image.astype(np.float64) / 255.0, 0.0, 1.0)
        xyz = colour.models.RGB_to_XYZ(rgb, "sRGB", apply_cctf_decoding=True)
        return xyz @ colour.adaptation.CAT_CAT02.T

