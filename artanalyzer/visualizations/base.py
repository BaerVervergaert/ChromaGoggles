"""
Base class for visualization strategies.
"""
from abc import ABC, abstractmethod
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
from artanalyzer.core.color_space import ColorSpace


class VisualizationStrategy(ABC):
    """
    Base class for visualization strategies.

    Visualization strategies create matplotlib figures from color space data.
    They work generically with any ColorSpace implementation.
    """

    @abstractmethod
    def create(
        self,
        colorspace: ColorSpace,
        rgb_image: np.ndarray,
        **kwargs
    ) -> plt.Figure:
        """
        Create visualization figure.

        Args:
            colorspace: ColorSpace instance
            rgb_image: Original RGB image array
            **kwargs: Additional visualization-specific parameters

        Returns:
            Matplotlib figure
        """
        pass

