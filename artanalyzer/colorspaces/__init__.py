"""Color space implementations."""
# Import all color space implementations to trigger registration
from artanalyzer.colorspaces.rgb import RGBColorSpace
from artanalyzer.colorspaces.hsv import HSVColorSpace
from artanalyzer.colorspaces.lab import LABColorSpace
from artanalyzer.colorspaces.hcl import HCLColorSpace
from artanalyzer.colorspaces.xyz import XYZColorSpace
from artanalyzer.colorspaces.luv import LUVColorSpace
from artanalyzer.colorspaces.ycbcr import YCbCrColorSpace
from artanalyzer.colorspaces.oklab import OklabColorSpace
from artanalyzer.colorspaces.oklch import OklchColorSpace
from artanalyzer.colorspaces.lms import LMSColorSpace

__all__ = [
    "RGBColorSpace",
    "HSVColorSpace",
    "LABColorSpace",
    "HCLColorSpace",
    "XYZColorSpace",
    "LUVColorSpace",
    "YCbCrColorSpace",
    "OklabColorSpace",
    "OklchColorSpace",
    "LMSColorSpace",
]
