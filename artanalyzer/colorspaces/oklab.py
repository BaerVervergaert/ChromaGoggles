"""Oklab color space implementation."""
import numpy as np
from artanalyzer.core.color_space import ColorSpace, ChannelMetadata
from artanalyzer.core.registry import ColorSpaceRegistry
from artanalyzer.colorspaces.oklab_utils import rgb_to_oklab


@ColorSpaceRegistry.register
class OklabColorSpace(ColorSpace):
    @property
    def name(self) -> str:
        return "oklab"

    @property
    def display_name(self) -> str:
        return "Oklab Color Space"

    @property
    def description(self) -> str:
        return (
            "**Oklab** is a modern perceptually uniform color space designed for image "
            "processing. L is lightness, a is green-red, and b is blue-yellow."
        )

    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata("lightness", "L (Lightness)", 0.0, 1.0, "gray", "Perceived lightness (0-1)"),
            ChannelMetadata("a", "a (Green-Red)", -0.4, 0.4, "RdYlGn_r", "Green (negative) to Red (positive) axis"),
            ChannelMetadata("b", "b (Blue-Yellow)", -0.4, 0.4, "YlGnBu_r", "Blue (negative) to Yellow (positive) axis"),
        ]

    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        return rgb_to_oklab(rgb_image)

