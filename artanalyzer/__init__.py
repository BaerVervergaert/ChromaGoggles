"""
ArtAnalyzer - A modular image color analysis toolkit.
"""
from artanalyzer.core.color_space import ColorSpace, ChannelMetadata
from artanalyzer.core.registry import ColorSpaceRegistry

__version__ = "0.2.0"
__all__ = ["ColorSpace", "ChannelMetadata", "ColorSpaceRegistry"]

