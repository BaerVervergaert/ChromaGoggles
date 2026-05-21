"""
Channel comparison visualization strategy.
"""
import numpy as np
import matplotlib.pyplot as plt
from chromagoggles.visualizations.base import VisualizationStrategy
from chromagoggles.visualizations.colormaps import get_colormap
from chromagoggles.core.color_space import ColorSpace
class ChannelComparisonViz(VisualizationStrategy):
    """
    Visualization strategy for displaying individual color space channels side-by-side.
    """
    def create(
        self,
        colorspace: ColorSpace,
        rgb_image: np.ndarray,
        **kwargs
    ) -> plt.Figure:
        """
        Create a comparison plot of all channels in the color space.
        Args:
            colorspace: ColorSpace instance
            rgb_image: Original RGB image array
            **kwargs: Additional parameters (unused)
        Returns:
            Matplotlib figure with channel comparisons
        """
        channels = colorspace.get_channels(rgb_image)
        metadata = colorspace.channels_metadata
        n_channels = len(channels)
        fig, axes = plt.subplots(1, n_channels, figsize=(5 * n_channels, 5))
        # Handle single channel case
        if n_channels == 1:
            axes = [axes]
        for ax, channel, meta in zip(axes, channels, metadata):
            # Get colormap
            cmap = get_colormap(meta.colormap)
            # Display channel
            im = ax.imshow(
                channel,
                cmap=cmap,
                vmin=meta.range_min,
                vmax=meta.range_max
            )
            # Set title with range
            ax.set_title(f'{meta.display_name}\n({meta.range_min}-{meta.range_max})')
            ax.axis('off')
            # Add colorbar
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        plt.tight_layout()
        return fig
