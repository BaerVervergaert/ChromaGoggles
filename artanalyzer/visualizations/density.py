"""
Density plot visualization strategy.
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from artanalyzer.visualizations.base import VisualizationStrategy
from artanalyzer.core.color_space import ColorSpace


class DensityPlotViz(VisualizationStrategy):
    """
    Visualization strategy for displaying channel value distributions.

    Creates histograms and KDE plots for each channel.
    """

    def create(
        self,
        colorspace: ColorSpace,
        rgb_image: np.ndarray,
        **kwargs
    ) -> plt.Figure:
        """
        Create density plots (histograms and KDE) for all channels.

        Args:
            colorspace: ColorSpace instance
            rgb_image: Original RGB image array
            **kwargs: Additional parameters (unused)

        Returns:
            Matplotlib figure with density plots
        """
        channels = colorspace.get_channels(rgb_image)
        metadata = colorspace.channels_metadata

        n_channels = len(channels)
        fig, axes = plt.subplots(2, n_channels, figsize=(5 * n_channels, 10))

        # Handle single channel case
        if n_channels == 1:
            axes = axes.reshape(-1, 1)

        colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']

        for i, (channel, meta) in enumerate(zip(channels, metadata)):
            flat = channel.flatten()
            color = colors[i % len(colors)]

            # Histogram
            axes[0, i].hist(
                flat,
                bins=50,
                color=color,
                alpha=0.7,
                edgecolor='black'
            )
            axes[0, i].set_title(f'{meta.display_name} Distribution')
            axes[0, i].set_xlabel(meta.display_name)
            axes[0, i].set_ylabel('Frequency')
            axes[0, i].set_xlim(meta.range_min, meta.range_max)

            # KDE plot
            try:
                sns.kdeplot(flat, ax=axes[1, i], fill=True, color=color, alpha=0.6)
                axes[1, i].set_title(f'{meta.display_name} Density (KDE)')
                axes[1, i].set_xlabel(meta.display_name)
                axes[1, i].set_ylabel('Density')
                axes[1, i].set_xlim(meta.range_min, meta.range_max)
            except Exception as e:
                axes[1, i].text(
                    0.5, 0.5,
                    f'KDE not available\n({str(e)[:30]}...)',
                    ha='center',
                    va='center',
                    transform=axes[1, i].transAxes
                )
                axes[1, i].set_title(f'{meta.display_name} Density (KDE)')

        plt.tight_layout()
        return fig

