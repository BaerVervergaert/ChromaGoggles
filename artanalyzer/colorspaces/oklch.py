"""Oklch color space implementation."""
import numpy as np
from artanalyzer.core.color_space import ColorSpace, ChannelMetadata
from artanalyzer.core.registry import ColorSpaceRegistry
from artanalyzer.colorspaces.oklab_utils import rgb_to_oklab, oklab_to_oklch


@ColorSpaceRegistry.register
class OklchColorSpace(ColorSpace):
    @property
    def name(self) -> str:
        return "oklch"

    @property
    def display_name(self) -> str:
        return "Oklch Color Space"

    @property
    def description(self) -> str:
        return (
            "**Oklch** is the cylindrical representation of Oklab. This view uses "
            "Hue, Chroma, and Lightness ordering for consistency with HSV/HCL tabs."
        )

    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata("hue", "H (Hue)", 0.0, 360.0, "oklch_hue", "Hue angle in degrees"),
            ChannelMetadata("chroma", "C (Chroma)", 0.0, 0.4, "gray", "Colorfulness/chroma"),
            ChannelMetadata("lightness", "L (Lightness)", 0.0, 1.0, "gray", "Perceived lightness (0-1)"),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        # oklab_to_oklch returns channels as [L, C, H]; reorder to [H, C, L].
        oklch = oklab_to_oklch(rgb_to_oklab(rgb_image))
        return np.stack([oklch[:, :, 2], oklch[:, :, 1], oklch[:, :, 0]], axis=-1)
