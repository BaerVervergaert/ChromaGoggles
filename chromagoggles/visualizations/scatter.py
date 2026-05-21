# Copyright (c) 2026 Baer Ververgaert. All rights reserved.
"""
Scatter plot visualization strategy.
"""
import numpy as np
import matplotlib.pyplot as plt
from chromagoggles.visualizations.base import VisualizationStrategy
from chromagoggles.core.color_space import ColorSpace


class ScatterPlotViz(VisualizationStrategy):
    """
    Visualization strategy for displaying relationships between channels.

    Creates scatter plots for all pairs of channels, colored by original RGB values
    with density-based alpha for better visualization.
    """

    def create(
        self,
        colorspace: ColorSpace,
        rgb_image: np.ndarray,
        sample_rate: int = 10,
        **kwargs
    ) -> plt.Figure:
        """
        Create scatter plots showing relationships between channels.

        Args:
            colorspace: ColorSpace instance
            rgb_image: Original RGB image array
            sample_rate: Sample every Nth pixel (default: 10)
            **kwargs: Additional parameters

        Returns:
            Matplotlib figure with scatter plots
        """
        channels = colorspace.get_channels(rgb_image)
        metadata = colorspace.channels_metadata

        n_channels = len(channels)

        if n_channels < 2:
            # Can't create scatter plots with less than 2 channels
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(
                0.5, 0.5,
                'Scatter plots require at least 2 channels',
                ha='center',
                va='center',
                fontsize=14
            )
            ax.axis('off')
            return fig

        # Create scatter plots for all channel pairs
        # For 3 channels: (0,1), (0,2), (1,2)
        n_plots = n_channels * (n_channels - 1) // 2

        # Arrange plots
        if n_plots <= 3:
            fig, axes = plt.subplots(1, n_plots, figsize=(5 * n_plots, 5))
            if n_plots == 1:
                axes = [axes]
        else:
            # For more plots, use a grid
            n_cols = 3
            n_rows = (n_plots + n_cols - 1) // n_cols
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 5 * n_rows))
            axes = axes.flatten()

        # Flatten and sample channels
        flattened_channels = [ch.flatten() for ch in channels]
        sample_idx = np.arange(0, len(flattened_channels[0]), sample_rate)
        sampled_channels = [ch[sample_idx] for ch in flattened_channels]

        # Get RGB colors for points
        rgb_flat = rgb_image.reshape(-1, 3)
        rgb_colors = rgb_flat[sample_idx] / 255.0  # Normalize to [0, 1]

        # Create scatter plots for each pair
        plot_idx = 0
        for i in range(n_channels):
            for j in range(i + 1, n_channels):
                ax = axes[plot_idx]

                x_data = sampled_channels[i]
                y_data = sampled_channels[j]
                x_meta = metadata[i]
                y_meta = metadata[j]

                # Calculate density-based alpha using histogram binning
                h, xedges, yedges = np.histogram2d(x_data, y_data, bins=20)
                x_indices = np.digitize(x_data, xedges) - 1
                y_indices = np.digitize(y_data, yedges) - 1

                # Clip indices to valid range
                x_indices = np.clip(x_indices, 0, 19)
                y_indices = np.clip(y_indices, 0, 19)

                # Get counts for each point
                counts = h[x_indices, y_indices]

                # Calculate alpha: higher density = lower alpha (for overplotting)
                # Use square root for better visual distribution
                alpha_values = np.clip(
                    np.sqrt(counts) / np.sqrt(counts.max()) * 0.7 + 0.1,
                    0.1,
                    0.8
                )

                # Create scatter plot with RGB colors
                ax.scatter(
                    x_data,
                    y_data,
                    alpha=alpha_values,
                    s=10,
                    c=rgb_colors,
                    edgecolors='none'
                )

                # Labels and title
                ax.set_xlabel(x_meta.display_name)
                ax.set_ylabel(y_meta.display_name)
                ax.set_title(f'{x_meta.display_name} vs {y_meta.display_name}')

                # Set axis limits based on metadata
                ax.set_xlim(x_meta.range_min, x_meta.range_max)
                ax.set_ylim(y_meta.range_min, y_meta.range_max)

                # Add grid
                ax.grid(True, alpha=0.3)

                # Add crosshairs at origin for channels that can be negative
                if x_meta.range_min < 0:
                    ax.axvline(x=0, color='k', linestyle='--', alpha=0.3, linewidth=0.8)
                if y_meta.range_min < 0:
                    ax.axhline(y=0, color='k', linestyle='--', alpha=0.3, linewidth=0.8)

                plot_idx += 1

        # Hide unused subplots
        for idx in range(plot_idx, len(axes)):
            axes[idx].axis('off')

        plt.tight_layout()
        return fig
