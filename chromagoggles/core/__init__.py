"""Core abstractions and utilities."""
from chromagoggles.core.color_space import ColorSpace, ChannelMetadata
from chromagoggles.core.registry import ColorSpaceRegistry
from chromagoggles.core.statistics import StatisticsCalculator, ChannelStats
from chromagoggles.core.color_transfer import ColorTransfer

__all__ = [
    "ColorSpace",
    "ChannelMetadata",
    "ColorSpaceRegistry",
    "StatisticsCalculator",
    "ChannelStats",
    "ColorTransfer",
]

