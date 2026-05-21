# Copyright (c) 2026 Baer Ververgaert. All rights reserved.
"""
Utilities for converting between RGB, Oklab, and Oklch color spaces.
"""
import numpy as np
import colour


def rgb_to_oklab(rgb_image: np.ndarray) -> np.ndarray:
    """
    Convert RGB uint8 image to Oklab.

    Returns array with channels [L, a, b].
    """
    rgb = np.clip(rgb_image.astype(np.float64) / 255.0, 0.0, 1.0)
    xyz = colour.models.RGB_to_XYZ(rgb, "sRGB", apply_cctf_decoding=True)
    return colour.models.XYZ_to_Oklab(xyz)


def oklab_to_rgb(oklab_image: np.ndarray) -> np.ndarray:
    """
    Convert Oklab image [L, a, b] to RGB uint8.
    """
    xyz = colour.models.Oklab_to_XYZ(oklab_image.astype(np.float64))
    rgb = colour.models.XYZ_to_RGB(xyz, "sRGB", apply_cctf_encoding=True)
    return np.clip(rgb * 255.0, 0, 255).astype(np.uint8)


def oklab_to_oklch(oklab_image: np.ndarray) -> np.ndarray:
    """
    Convert Oklab [L, a, b] to Oklch [L, C, H] where H is in degrees.
    """
    return colour.models.Oklab_to_Oklch(oklab_image.astype(np.float64))


def oklch_to_oklab(oklch_image: np.ndarray) -> np.ndarray:
    """
    Convert Oklch [L, C, H] with H in degrees to Oklab [L, a, b].
    """
    return colour.models.Oklch_to_Oklab(oklch_image.astype(np.float64))
