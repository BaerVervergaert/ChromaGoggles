"""
Image processing module for analyzing and extracting color information from images.
"""
import numpy as np
import cv2
from PIL import Image
from skimage import color


class ImageAnalyzer:
    """Handles image loading and color space analysis."""

    def __init__(self, image_path):
        """
        Initialize the analyzer with an image.

        Args:
            image_path: Path to the image file or PIL Image object
        """
        if isinstance(image_path, str):
            self.original_image = cv2.imread(image_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        elif isinstance(image_path, Image.Image):
            self.original_image = np.array(image_path)
        else:
            self.original_image = image_path

        self.height, self.width = self.original_image.shape[:2]

    def get_rgb_channels(self):
        """
        Extract individual RGB channels.

        Returns:
            Tuple of (red_channel, green_channel, blue_channel) as grayscale images
        """
        r_channel = self.original_image[:, :, 0]
        g_channel = self.original_image[:, :, 1]
        b_channel = self.original_image[:, :, 2]

        return r_channel, g_channel, b_channel

    def get_rgb_channel_images(self):
        """
        Get RGB channels as colored images (with other channels zeroed).

        Returns:
            Tuple of (red_image, green_image, blue_image) as RGB images
        """
        red_image = np.zeros_like(self.original_image)
        red_image[:, :, 0] = self.original_image[:, :, 0]

        green_image = np.zeros_like(self.original_image)
        green_image[:, :, 1] = self.original_image[:, :, 1]

        blue_image = np.zeros_like(self.original_image)
        blue_image[:, :, 2] = self.original_image[:, :, 2]

        return red_image, green_image, blue_image

    def get_hsv(self):
        """
        Convert image to HSV color space.

        Returns:
            HSV image array
        """
        hsv_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2HSV)
        return hsv_image

    def get_hcl(self):
        """
        Extract Hue, Chroma, and Luminance values.
        Uses the LCh (CIELCh) color space (cylindrical representation of LAB).

        Returns:
            Tuple of (hue, chroma, luminance) arrays
        """
        # Convert RGB to LAB first
        rgb_normalized = self.original_image / 255.0
        lab_image = color.rgb2lab(rgb_normalized)

        # Convert LAB to LCH using scikit-image
        lch_image = color.lab2lch(lab_image)

        # Extract individual channels
        luminance = lch_image[:, :, 0]
        chroma = lch_image[:, :, 1]
        hue = lch_image[:, :, 2]
        # Hue is returned in radians [0, 2π], convert to degrees [0, 360]
        hue = np.degrees(hue)

        return hue, chroma, luminance

    def get_lab(self):
        """
        Convert image to LAB color space.

        Returns:
            LAB image array
        """
        rgb_normalized = self.original_image / 255.0
        lab_image = color.rgb2lab(rgb_normalized)
        return lab_image

    def get_ycbcr(self):
        """
        Convert image to YCbCr color space.

        Returns:
            YCbCr image array
        """
        ycbcr_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2YCrCb)
        return ycbcr_image

    def get_luv(self):
        """
        Convert image to LUV color space.

        Returns:
            LUV image array
        """
        rgb_normalized = self.original_image / 255.0
        luv_image = color.rgb2luv(rgb_normalized)
        return luv_image

    def get_xyz(self):
        """
        Convert image to XYZ color space.

        Returns:
            XYZ image array
        """
        rgb_normalized = self.original_image / 255.0
        xyz_image = color.rgb2xyz(rgb_normalized)
        return xyz_image

    def get_grayscale(self):
        """
        Convert image to grayscale.

        Returns:
            Grayscale image array
        """
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        return gray_image

