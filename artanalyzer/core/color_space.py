"""
Base class and abstractions for color space implementations.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
import numpy as np


@dataclass
class ChannelMetadata:
    """Metadata describing a color channel."""
    name: str  # Internal name (e.g., 'red', 'hue')
    display_name: str  # Display name for UI (e.g., 'Red Channel', 'Hue')
    range_min: float  # Minimum value in the channel
    range_max: float  # Maximum value in the channel
    colormap: str  # Matplotlib colormap name
    description: str  # Description of what this channel represents


class ColorSpace(ABC):
    """
    Base class for all color space implementations.

    Subclasses must implement the abstract methods to define:
    - Color space name and metadata
    - Conversion from RGB
    - Channel information

    This abstraction enables:
    - Automatic UI generation
    - Reusable visualization strategies
    - Easy addition of new color spaces
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Internal name for the color space (lowercase, no spaces).

        Example: 'rgb', 'hsv', 'lab'
        """
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """
        Human-readable display name for the UI.

        Example: 'RGB Channels', 'HSV Color Space'
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Brief description of the color space for the UI.

        Example: 'RGB (Red, Green, Blue) is an additive color model...'
        """
        pass

    @property
    @abstractmethod
    def channels_metadata(self) -> List[ChannelMetadata]:
        """
        Metadata for each channel in this color space.

        Returns a list of ChannelMetadata objects describing each channel.
        The order must match the channel order in the converted image.
        """
        pass

    @abstractmethod
    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """
        Convert an RGB image to this color space.

        Args:
            rgb_image: RGB image array with shape (height, width, 3)
                      and values in range [0, 255]

        Returns:
            Converted image array with shape (height, width, n_channels)
            where n_channels matches len(channels_metadata)
        """
        pass

    def get_channels(self, rgb_image: np.ndarray) -> List[np.ndarray]:
        """
        Get individual channels as separate 2D arrays.

        Args:
            rgb_image: RGB image array with shape (height, width, 3)

        Returns:
            List of 2D arrays, one per channel
        """
        converted = self.convert_from_rgb(rgb_image)
        if len(converted.shape) == 2:
            # Grayscale or single-channel
            return [converted]
        return [converted[:, :, i] for i in range(converted.shape[2])]

    def supports_statistics_tab(self) -> bool:
        """
        Whether this color space should have a statistics tab.

        Override to return False for color spaces that don't need statistics.
        """
        return True

    def supports_scatter_plots(self) -> bool:
        """
        Whether scatter plots make sense for this color space.

        Override to return False for color spaces where scatter plots
        are not meaningful (e.g., single-channel images).
        """
        return len(self.channels_metadata) >= 2

    def get_converted_image(self, rgb_image: np.ndarray) -> np.ndarray:
        """
        Get the full converted image array.

        Convenience method that returns the converted image.

        Args:
            rgb_image: RGB image array with shape (height, width, 3)

        Returns:
            Converted image array
        """
        return self.convert_from_rgb(rgb_image)

