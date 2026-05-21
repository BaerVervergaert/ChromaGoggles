"""Color space implementations."""
# Import all color space implementations to trigger registration
from chromagoggles.colorspaces.rgb import RGBColorSpace
from chromagoggles.colorspaces.hsv import HSVColorSpace
from chromagoggles.colorspaces.lab import LABColorSpace
from chromagoggles.colorspaces.hcl import HCLColorSpace
from chromagoggles.colorspaces.xyz import XYZColorSpace
from chromagoggles.colorspaces.luv import LUVColorSpace
from chromagoggles.colorspaces.ycbcr import YCbCrColorSpace
from chromagoggles.colorspaces.oklab import OklabColorSpace
from chromagoggles.colorspaces.oklch import OklchColorSpace
from chromagoggles.colorspaces.lms import LMSColorSpace

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
