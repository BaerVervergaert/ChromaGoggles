"""Visualization strategies and components."""
from chromagoggles.visualizations.base import VisualizationStrategy
from chromagoggles.visualizations.channels import ChannelComparisonViz
from chromagoggles.visualizations.density import DensityPlotViz
from chromagoggles.visualizations.scatter import ScatterPlotViz
from chromagoggles.visualizations.colormaps import create_lch_hue_colormap, create_oklch_hue_colormap, get_colormap
from chromagoggles.visualizations.color_transfer_viz import (
    create_color_transfer_comparison,
    create_histogram_comparison,
    create_statistics_table,
    create_difference_visualization,
)

__all__ = [
    "VisualizationStrategy",
    "ChannelComparisonViz",
    "DensityPlotViz",
    "ScatterPlotViz",
    "create_lch_hue_colormap",
    "create_oklch_hue_colormap",
    "get_colormap",
    "create_color_transfer_comparison",
    "create_histogram_comparison",
    "create_statistics_table",
    "create_difference_visualization",
]
