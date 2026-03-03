"""Visualization strategies and components."""
from artanalyzer.visualizations.base import VisualizationStrategy
from artanalyzer.visualizations.channels import ChannelComparisonViz
from artanalyzer.visualizations.density import DensityPlotViz
from artanalyzer.visualizations.scatter import ScatterPlotViz
from artanalyzer.visualizations.colormaps import create_lch_hue_colormap, get_colormap
from artanalyzer.visualizations.color_transfer_viz import (
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
    "get_colormap",
    "create_color_transfer_comparison",
    "create_histogram_comparison",
    "create_statistics_table",
    "create_difference_visualization",
]


