"""
Tab factory for dynamically generating Streamlit tabs.
"""
import streamlit as st
import matplotlib.pyplot as plt
from artanalyzer.core.registry import ColorSpaceRegistry
from artanalyzer.core.statistics import StatisticsCalculator
from artanalyzer.visualizations import (
    ChannelComparisonViz,
    DensityPlotViz,
    ScatterPlotViz
)


class TabFactory:
    """
    Factory for creating Streamlit tabs dynamically from registered color spaces.

    This eliminates the need for repetitive tab creation code in main.py.
    """

    @staticmethod
    def create_all_tabs(rgb_image):
        """
        Create all tabs for registered color spaces.

        Args:
            rgb_image: Original RGB image array with shape (height, width, 3)
        """
        # Get color spaces that support statistics
        colorspaces_with_stats = ColorSpaceRegistry.get_with_statistics()

        # Create tab names
        tab_names = []
        for cs in colorspaces_with_stats:
            tab_names.append(cs.display_name)
            if cs.supports_statistics_tab():
                tab_names.append(f"{cs.display_name} Statistics")

        # Create tabs
        tabs = st.tabs(tab_names)

        # Populate tabs
        tab_idx = 0
        for cs in colorspaces_with_stats:
            # Channel visualization tab
            with tabs[tab_idx]:
                TabFactory._create_channel_tab(cs, rgb_image)
            tab_idx += 1

            # Statistics tab
            if cs.supports_statistics_tab():
                with tabs[tab_idx]:
                    TabFactory._create_statistics_tab(cs, rgb_image)
                tab_idx += 1

    @staticmethod
    def _create_channel_tab(colorspace, rgb_image):
        """
        Create a channel visualization tab.

        Args:
            colorspace: ColorSpace instance
            rgb_image: Original RGB image array
        """
        st.header(colorspace.display_name)
        st.markdown(colorspace.description)

        # Create channel visualization
        viz = ChannelComparisonViz()
        fig = viz.create(colorspace, rgb_image)
        st.pyplot(fig)
        plt.close(fig)

    @staticmethod
    def _create_statistics_tab(colorspace, rgb_image):
        """
        Create a statistics tab with density plots, scatter plots, and statistics.

        Args:
            colorspace: ColorSpace instance
            rgb_image: Original RGB image array
        """
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

