# Copyright (c) 2026 Baer Ververgaert. All rights reserved.
"""
Dropdown-based factory for displaying color space analyses.
"""
import streamlit as st
import matplotlib.pyplot as plt
from chromagoggles.core.registry import ColorSpaceRegistry
from chromagoggles.core.statistics import StatisticsCalculator
from chromagoggles.visualizations import (
    ChannelComparisonViz,
    DensityPlotViz,
    ScatterPlotViz
)


class TabFactory:
    """
    Factory for displaying color space analyses via a dropdown selector.
    """

    @staticmethod
    def create_all_tabs(rgb_image):
        """
        Render a dropdown and show the selected color space's full analysis.

        Args:
            rgb_image: Original RGB image array with shape (height, width, 3)
        """
        colorspaces = ColorSpaceRegistry.get_all()

        # Build display name -> ColorSpace mapping (preserving registration order)
        cs_map = {cs.display_name: cs for cs in colorspaces}
        display_names = list(cs_map.keys())

        selected_name = st.selectbox(
            "Select color space to analyze:",
            display_names,
            key="colorspace_selector",
        )

        cs = cs_map[selected_name]

        # Channel images
        TabFactory._create_channel_tab(cs, rgb_image)

        # Statistics (density + scatter + table)
        if cs.supports_statistics_tab():
            st.divider()
            TabFactory._create_statistics_tab(cs, rgb_image)

    @staticmethod
    def _create_channel_tab(colorspace, rgb_image):
        """Render channel images for a color space."""
        st.header(colorspace.display_name)
        st.markdown(colorspace.description)

        viz = ChannelComparisonViz()
        fig = viz.create(colorspace, rgb_image)
        st.pyplot(fig)
        plt.close(fig)

    @staticmethod
    def _create_statistics_tab(colorspace, rgb_image):
        """Render density plots, scatter plots, and statistics table."""
        st.header(f"{colorspace.display_name} Statistics")

        # Density plots
        st.subheader("Value Distributions")
        viz = DensityPlotViz()
        fig = viz.create(colorspace, rgb_image)
        st.pyplot(fig)
        plt.close(fig)

        # Scatter plots
        if colorspace.supports_scatter_plots():
            st.subheader("Channel Relationships")
            st.markdown(
                "Scatter plots show relationships between channels. "
                "Points are colored by their original RGB values, and alpha is "
                "adjusted based on point density to show concentration areas."
            )
            viz = ScatterPlotViz()
            fig = viz.create(colorspace, rgb_image)
            st.pyplot(fig)
            plt.close(fig)

        # Statistics table
        st.subheader("Channel Statistics")
        stats = StatisticsCalculator.calculate(colorspace, rgb_image)
        stats_table = StatisticsCalculator.format_stats_table(stats)
        st.markdown(stats_table)
