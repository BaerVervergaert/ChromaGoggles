"""
Statistics calculation for color space channels.
"""
from dataclasses import dataclass
from typing import List
import numpy as np
from chromagoggles.core.color_space import ColorSpace


@dataclass
class ChannelStats:
    """Statistics for a single channel."""
    name: str
    display_name: str
    mean: float
    std: float
    min: float
    max: float
    median: float

    def __str__(self) -> str:
        """Format statistics for display."""
        return (
            f"{self.display_name}:\n"
            f"  Mean: {self.mean:.2f}\n"
            f"  Std Dev: {self.std:.2f}\n"
            f"  Min: {self.min:.2f}\n"
            f"  Max: {self.max:.2f}\n"
            f"  Median: {self.median:.2f}"
        )


class StatisticsCalculator:
    """Calculate statistics for color space channels."""

    @staticmethod
    def calculate(colorspace: ColorSpace, rgb_image: np.ndarray) -> List[ChannelStats]:
        """
        Calculate statistics for all channels in a color space.

        Args:
            colorspace: The ColorSpace instance
            rgb_image: RGB image array with shape (height, width, 3)

        Returns:
            List of ChannelStats, one per channel
        """
        channels = colorspace.get_channels(rgb_image)
        metadata = colorspace.channels_metadata

        stats = []
        for channel, meta in zip(channels, metadata):
            flat = channel.flatten()
            # Remove NaN values if present
            flat = flat[~np.isnan(flat)]

            stats.append(ChannelStats(
                name=meta.name,
                display_name=meta.display_name,
                mean=float(np.mean(flat)),
                std=float(np.std(flat)),
                min=float(np.min(flat)),
                max=float(np.max(flat)),
                median=float(np.median(flat))
            ))

        return stats

    @staticmethod
    def format_stats_table(stats: List[ChannelStats]) -> str:
        """
        Format statistics as a markdown table.

        Args:
            stats: List of ChannelStats

        Returns:
            Markdown table string
        """
        if not stats:
            return "No statistics available."

        lines = [
            "| Channel | Mean | Std Dev | Min | Max | Median |",
            "|---------|------|---------|-----|-----|--------|"
        ]

        for stat in stats:
            lines.append(
                f"| {stat.display_name} | "
                f"{stat.mean:.2f} | "
                f"{stat.std:.2f} | "
                f"{stat.min:.2f} | "
                f"{stat.max:.2f} | "
                f"{stat.median:.2f} |"
            )

        return "\n".join(lines)

