"""
Color transfer module for matching color distributions between images.

This module provides algorithms to transform image A to match the color
distribution of image B (reference image).
"""
import numpy as np
from skimage import color


class ColorTransfer:
    """
    Implements color transfer algorithms to match color distributions
    between a source and reference image.
    """

    @staticmethod
    def match_histograms(
        source: np.ndarray,
        reference: np.ndarray,
        colorspace: str = 'rgb'
    ) -> np.ndarray:
        """
        Match the histogram of source image to reference image.

        Supports multiple color spaces for histogram matching.

        Args:
            source: Source image (height, width, 3), uint8 [0, 255]
            reference: Reference image (height, width, 3), uint8 [0, 255]
            colorspace: Color space for matching ('rgb', 'lab', 'hsv', 'hcl', 'xyz', 'luv', 'ycbcr')

        Returns:
            Transformed image with matched color distribution
        """
        colorspace_map = {
            'rgb': ColorTransfer._match_histograms_rgb,
            'lab': ColorTransfer._match_histograms_lab,
            'hsv': ColorTransfer._match_histograms_hsv,
            'hcl': ColorTransfer._match_histograms_hcl,
            'xyz': ColorTransfer._match_histograms_xyz,
            'luv': ColorTransfer._match_histograms_luv,
            'ycbcr': ColorTransfer._match_histograms_ycbcr,
        }

        if colorspace not in colorspace_map:
            raise ValueError(f"Unknown colorspace: {colorspace}. Supported: {list(colorspace_map.keys())}")

        return colorspace_map[colorspace](source, reference)

    @staticmethod
    def _match_histograms_rgb(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match histograms in RGB color space."""
        result = source.copy().astype(np.float32)

        # Process each RGB channel independently
        for i in range(3):
            source_hist, bins = np.histogram(
                source[:, :, i].flatten(),
                bins=256,
                range=(0, 256)
            )
            reference_hist, _ = np.histogram(
                reference[:, :, i].flatten(),
                bins=256,
                range=(0, 256)
            )

            # Compute cumulative sums (CDFs)
            source_cdf = np.cumsum(source_hist) / source_hist.sum()
            reference_cdf = np.cumsum(reference_hist) / reference_hist.sum()

            # Create mapping
            mapping = np.zeros(256, dtype=np.uint8)
            for j in range(256):
                # Find closest value in reference CDF
                idx = np.argmin(np.abs(reference_cdf - source_cdf[j]))
                mapping[j] = idx

            # Apply mapping
            result[:, :, i] = mapping[source[:, :, i]]

        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_histograms_lab(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """
        Match histograms in LAB color space.

        This is more perceptually meaningful than RGB.
        """
        # Convert to LAB
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_lab = color.rgb2lab(source_norm)
        reference_lab = color.rgb2lab(reference_norm)

        result_lab = source_lab.copy()

        # Match each LAB channel
        # L* range is 0-100
        lab_ranges = [(0, 100), (-127, 127), (-127, 127)]

        for i, (min_val, max_val) in enumerate(lab_ranges):
            # Normalize to 0-255 range for histogram computation
            source_channel = ((source_lab[:, :, i] - min_val) /
                            (max_val - min_val) * 255).astype(np.uint8)
            reference_channel = ((reference_lab[:, :, i] - min_val) /
                               (max_val - min_val) * 255).astype(np.uint8)

            # Compute histograms
            source_hist, bins = np.histogram(
                source_channel.flatten(),
                bins=256,
                range=(0, 256)
            )
            reference_hist, _ = np.histogram(
                reference_channel.flatten(),
                bins=256,
                range=(0, 256)
            )

            # Compute CDFs
            source_cdf = np.cumsum(source_hist) / (source_hist.sum() + 1e-10)
            reference_cdf = np.cumsum(reference_hist) / (reference_hist.sum() + 1e-10)

            # Create mapping
            mapping = np.zeros(256, dtype=np.uint8)
            for j in range(256):
                idx = np.argmin(np.abs(reference_cdf - source_cdf[j]))
                mapping[j] = idx

            # Apply mapping
            mapped_channel = mapping[source_channel]

            # Convert back to original range
            result_lab[:, :, i] = (mapped_channel / 255.0 *
                                  (max_val - min_val) + min_val)

        # Convert back to RGB
        result_rgb_norm = color.lab2rgb(result_lab)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_histograms_hsv(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """
        Match histograms in HSV color space.

        Useful for matching color appearance while preserving intensity.
        """
        import cv2

        # Convert to HSV
        source_hsv = cv2.cvtColor(source, cv2.COLOR_RGB2HSV)
        reference_hsv = cv2.cvtColor(reference, cv2.COLOR_RGB2HSV)

        result_hsv = source_hsv.copy().astype(np.float32)

        # Match each HSV channel
        # H: 0-180, S: 0-255, V: 0-255 (in OpenCV)
        hsv_ranges = [(0, 180), (0, 255), (0, 255)]

        for i, (min_val, max_val) in enumerate(hsv_ranges):
            source_hist, bins = np.histogram(
                source_hsv[:, :, i].flatten(),
                bins=256,
                range=(0, 256)
            )
            reference_hist, _ = np.histogram(
                reference_hsv[:, :, i].flatten(),
                bins=256,
                range=(0, 256)
            )

            # Compute CDFs
            source_cdf = np.cumsum(source_hist) / (source_hist.sum() + 1e-10)
            reference_cdf = np.cumsum(reference_hist) / (reference_hist.sum() + 1e-10)

            # Create mapping
            mapping = np.zeros(256, dtype=np.uint8)
            for j in range(256):
                idx = np.argmin(np.abs(reference_cdf - source_cdf[j]))
                mapping[j] = idx

            # Apply mapping
            result_hsv[:, :, i] = mapping[source_hsv[:, :, i]]

        # Convert back to RGB
        result_hsv = np.clip(result_hsv, 0, 255).astype(np.uint8)
        result_rgb = cv2.cvtColor(result_hsv, cv2.COLOR_HSV2RGB)

        return result_rgb

    @staticmethod
    def _match_histograms_hcl(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """
        Match histograms in HCL (CIELCh) color space.

        Perceptually uniform cylindrical color space.
        """
        # Convert to LAB first, then to LCH
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_lab = color.rgb2lab(source_norm)
        reference_lab = color.rgb2lab(reference_norm)

        source_lch = color.lab2lch(source_lab)
        reference_lch = color.lab2lch(reference_lab)

        result_lch = source_lch.copy()

        # LCH channels: L (0-100), C (0-100+), H (0-2π radians)
        # For histogram matching, convert H to degrees for better binning
        lch_ranges = [(0, 100), (0, 150), (0, 360)]

        for i in range(3):
            # For hue channel, convert from radians to degrees
            if i == 2:
                source_channel = np.degrees(source_lch[:, :, i])
                reference_channel = np.degrees(reference_lch[:, :, i])
            else:
                source_channel = source_lch[:, :, i]
                reference_channel = reference_lch[:, :, i]

            min_val, max_val = lch_ranges[i]

            # Normalize to 0-255 for histogram computation
            source_norm_ch = ((source_channel - min_val) / (max_val - min_val) * 255).astype(np.uint8)
            reference_norm_ch = ((reference_channel - min_val) / (max_val - min_val) * 255).astype(np.uint8)

            source_hist, _ = np.histogram(source_norm_ch.flatten(), bins=256, range=(0, 256))
            reference_hist, _ = np.histogram(reference_norm_ch.flatten(), bins=256, range=(0, 256))

            source_cdf = np.cumsum(source_hist) / (source_hist.sum() + 1e-10)
            reference_cdf = np.cumsum(reference_hist) / (reference_hist.sum() + 1e-10)

            mapping = np.zeros(256, dtype=np.uint8)
            for j in range(256):
                idx = np.argmin(np.abs(reference_cdf - source_cdf[j]))
                mapping[j] = idx

            mapped_channel = mapping[source_norm_ch]

            # Convert back to original range
            result_channel = (mapped_channel / 255.0 * (max_val - min_val) + min_val)

            # For hue channel, convert back to radians
            if i == 2:
                result_lch[:, :, i] = np.radians(result_channel)
            else:
                result_lch[:, :, i] = result_channel

        # Convert back to RGB
        result_lab = color.lch2lab(result_lch)
        result_rgb_norm = color.lab2rgb(result_lab)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_histograms_xyz(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """
        Match histograms in XYZ color space.

        CIE XYZ tristimulus color space.
        """
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_xyz = color.rgb2xyz(source_norm)
        reference_xyz = color.rgb2xyz(reference_norm)

        result_xyz = source_xyz.copy()

        # XYZ ranges are typically 0-1
        for i in range(3):
            # Normalize to 0-255 for histogram
            source_channel = (source_xyz[:, :, i] * 255).astype(np.uint8)
            reference_channel = (reference_xyz[:, :, i] * 255).astype(np.uint8)

            source_hist, _ = np.histogram(source_channel.flatten(), bins=256, range=(0, 256))
            reference_hist, _ = np.histogram(reference_channel.flatten(), bins=256, range=(0, 256))

            source_cdf = np.cumsum(source_hist) / (source_hist.sum() + 1e-10)
            reference_cdf = np.cumsum(reference_hist) / (reference_hist.sum() + 1e-10)

            mapping = np.zeros(256, dtype=np.uint8)
            for j in range(256):
                idx = np.argmin(np.abs(reference_cdf - source_cdf[j]))
                mapping[j] = idx

            mapped_channel = mapping[source_channel]
            result_xyz[:, :, i] = mapped_channel / 255.0

        # Convert back to RGB
        result_rgb_norm = color.xyz2rgb(result_xyz)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_histograms_luv(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """
        Match histograms in LUV color space.

        CIELUV perceptually uniform color space.
        """
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_luv = color.rgb2luv(source_norm)
        reference_luv = color.rgb2luv(reference_norm)

        result_luv = source_luv.copy()

        # LUV ranges: L (0-100), u* (~-100 to 100), v* (~-100 to 100)
        luv_ranges = [(0, 100), (-100, 100), (-100, 100)]

        for i, (min_val, max_val) in enumerate(luv_ranges):
            # Normalize to 0-255 for histogram
            source_channel = ((source_luv[:, :, i] - min_val) / (max_val - min_val) * 255).astype(np.uint8)
            reference_channel = ((reference_luv[:, :, i] - min_val) / (max_val - min_val) * 255).astype(np.uint8)

            source_hist, _ = np.histogram(source_channel.flatten(), bins=256, range=(0, 256))
            reference_hist, _ = np.histogram(reference_channel.flatten(), bins=256, range=(0, 256))

            source_cdf = np.cumsum(source_hist) / (source_hist.sum() + 1e-10)
            reference_cdf = np.cumsum(reference_hist) / (reference_hist.sum() + 1e-10)

            mapping = np.zeros(256, dtype=np.uint8)
            for j in range(256):
                idx = np.argmin(np.abs(reference_cdf - source_cdf[j]))
                mapping[j] = idx

            mapped_channel = mapping[source_channel]
            result_luv[:, :, i] = (mapped_channel / 255.0 * (max_val - min_val) + min_val)

        # Convert back to RGB
        result_rgb_norm = color.luv2rgb(result_luv)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_histograms_ycbcr(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """
        Match histograms in YCbCr color space.

        Luma and chroma components used in video compression.
        """
        import cv2

        # Convert to YCbCr (OpenCV uses YCrCb, so we swap channels)
        source_ycrcb = cv2.cvtColor(source, cv2.COLOR_RGB2YCrCb)
        reference_ycrcb = cv2.cvtColor(reference, cv2.COLOR_RGB2YCrCb)

        # Swap to YCbCr order
        source_ycbcr = source_ycrcb.copy()
        source_ycbcr[:, :, 1] = source_ycrcb[:, :, 2]  # Cb
        source_ycbcr[:, :, 2] = source_ycrcb[:, :, 1]  # Cr

        reference_ycbcr = reference_ycrcb.copy()
        reference_ycbcr[:, :, 1] = reference_ycrcb[:, :, 2]  # Cb
        reference_ycbcr[:, :, 2] = reference_ycrcb[:, :, 1]  # Cr

        result_ycbcr = source_ycbcr.copy().astype(np.float32)

        # Match each channel (all are 0-255)
        for i in range(3):
            source_hist, _ = np.histogram(source_ycbcr[:, :, i].flatten(), bins=256, range=(0, 256))
            reference_hist, _ = np.histogram(reference_ycbcr[:, :, i].flatten(), bins=256, range=(0, 256))

            source_cdf = np.cumsum(source_hist) / (source_hist.sum() + 1e-10)
            reference_cdf = np.cumsum(reference_hist) / (reference_hist.sum() + 1e-10)

            mapping = np.zeros(256, dtype=np.uint8)
            for j in range(256):
                idx = np.argmin(np.abs(reference_cdf - source_cdf[j]))
                mapping[j] = idx

            result_ycbcr[:, :, i] = mapping[source_ycbcr[:, :, i]]

        # Convert back to YCrCb for OpenCV
        result_ycrcb = result_ycbcr.copy()
        result_ycrcb[:, :, 1] = result_ycbcr[:, :, 2]  # Cr
        result_ycrcb[:, :, 2] = result_ycbcr[:, :, 1]  # Cb

        result_ycrcb = np.clip(result_ycrcb, 0, 255).astype(np.uint8)
        result_rgb = cv2.cvtColor(result_ycrcb, cv2.COLOR_YCrCb2RGB)

        return result_rgb

    @staticmethod
    def match_statistics(
        source: np.ndarray,
        reference: np.ndarray,
        colorspace: str = 'lab'
    ) -> np.ndarray:
        """
        Match color statistics (mean and std) between images.

        More aggressive color transfer that matches both mean and standard deviation.

        Args:
            source: Source image (height, width, 3), uint8 [0, 255]
            reference: Reference image (height, width, 3), uint8 [0, 255]
            colorspace: Color space for matching ('lab', 'rgb', 'hsv', 'hcl', 'xyz', 'luv', 'ycbcr')

        Returns:
            Transformed image with matched statistics
        """
        colorspace_map = {
            'lab': ColorTransfer._match_statistics_lab,
            'rgb': ColorTransfer._match_statistics_rgb,
            'hsv': ColorTransfer._match_statistics_hsv,
            'hcl': ColorTransfer._match_statistics_hcl,
            'xyz': ColorTransfer._match_statistics_xyz,
            'luv': ColorTransfer._match_statistics_luv,
            'ycbcr': ColorTransfer._match_statistics_ycbcr,
        }

        if colorspace not in colorspace_map:
            raise ValueError(f"Unknown colorspace: {colorspace}. Supported: {list(colorspace_map.keys())}")

        return colorspace_map[colorspace](source, reference)

    @staticmethod
    def _match_statistics_lab(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """
        Match LAB statistics (mean and std).

        This is the most perceptually meaningful color transfer.
        """
        # Convert to LAB
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_lab = color.rgb2lab(source_norm)
        reference_lab = color.rgb2lab(reference_norm)

        result_lab = source_lab.copy()

        # Match statistics for each LAB channel
        for i in range(3):
            source_mean = source_lab[:, :, i].mean()
            source_std = source_lab[:, :, i].std()

            reference_mean = reference_lab[:, :, i].mean()
            reference_std = reference_lab[:, :, i].std()

            # Avoid division by zero
            if source_std < 1e-6:
                source_std = 1e-6

            # Transform: (x - mean_src) / std_src * std_ref + mean_ref
            result_lab[:, :, i] = ((source_lab[:, :, i] - source_mean) /
                                   source_std * reference_std + reference_mean)

        # Convert back to RGB
        result_rgb_norm = color.lab2rgb(result_lab)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_statistics_rgb(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match RGB statistics (mean and std)."""
        result = source.copy().astype(np.float32)

        for i in range(3):
            source_mean = source[:, :, i].mean()
            source_std = source[:, :, i].std()

            reference_mean = reference[:, :, i].mean()
            reference_std = reference[:, :, i].std()

            if source_std < 1e-6:
                source_std = 1e-6

            result[:, :, i] = ((source[:, :, i] - source_mean) /
                              source_std * reference_std + reference_mean)

        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_statistics_hsv(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match HSV statistics (mean and std)."""
        import cv2

        source_hsv = cv2.cvtColor(source, cv2.COLOR_RGB2HSV).astype(np.float32)
        reference_hsv = cv2.cvtColor(reference, cv2.COLOR_RGB2HSV).astype(np.float32)

        result_hsv = source_hsv.copy()

        for i in range(3):
            source_mean = source_hsv[:, :, i].mean()
            source_std = source_hsv[:, :, i].std()

            reference_mean = reference_hsv[:, :, i].mean()
            reference_std = reference_hsv[:, :, i].std()

            if source_std < 1e-6:
                source_std = 1e-6

            result_hsv[:, :, i] = ((source_hsv[:, :, i] - source_mean) /
                                   source_std * reference_std + reference_mean)

        # Clip to valid ranges
        result_hsv[:, :, 0] = np.clip(result_hsv[:, :, 0], 0, 180)  # Hue
        result_hsv[:, :, 1] = np.clip(result_hsv[:, :, 1], 0, 255)  # Saturation
        result_hsv[:, :, 2] = np.clip(result_hsv[:, :, 2], 0, 255)  # Value

        result_hsv = result_hsv.astype(np.uint8)
        result_rgb = cv2.cvtColor(result_hsv, cv2.COLOR_HSV2RGB)

        return result_rgb

    @staticmethod
    def _match_statistics_hcl(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match HCL (LCh) statistics (mean and std)."""
        # Convert to LAB then LCh
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_lab = color.rgb2lab(source_norm)
        reference_lab = color.rgb2lab(reference_norm)

        source_lch = color.lab2lch(source_lab)
        reference_lch = color.lab2lch(reference_lab)

        result_lch = source_lch.copy()

        for i in range(3):
            source_mean = source_lch[:, :, i].mean()
            source_std = source_lch[:, :, i].std()

            reference_mean = reference_lch[:, :, i].mean()
            reference_std = reference_lch[:, :, i].std()

            if source_std < 1e-6:
                source_std = 1e-6

            result_lch[:, :, i] = ((source_lch[:, :, i] - source_mean) /
                                   source_std * reference_std + reference_mean)

        # Clip to valid ranges
        result_lch[:, :, 0] = np.clip(result_lch[:, :, 0], 0, 100)  # Lightness
        result_lch[:, :, 1] = np.maximum(result_lch[:, :, 1], 0)    # Chroma (non-negative)
        # Hue wraps around, so use modulo
        result_lch[:, :, 2] = result_lch[:, :, 2] % (2 * np.pi)

        # Convert back to RGB
        result_lab = color.lch2lab(result_lch)
        result_rgb_norm = color.lab2rgb(result_lab)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_statistics_xyz(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match XYZ statistics (mean and std)."""
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_xyz = color.rgb2xyz(source_norm)
        reference_xyz = color.rgb2xyz(reference_norm)

        result_xyz = source_xyz.copy()

        for i in range(3):
            source_mean = source_xyz[:, :, i].mean()
            source_std = source_xyz[:, :, i].std()

            reference_mean = reference_xyz[:, :, i].mean()
            reference_std = reference_xyz[:, :, i].std()

            if source_std < 1e-6:
                source_std = 1e-6

            result_xyz[:, :, i] = ((source_xyz[:, :, i] - source_mean) /
                                   source_std * reference_std + reference_mean)

        # XYZ values should be non-negative
        result_xyz = np.maximum(result_xyz, 0)

        # Convert back to RGB
        result_rgb_norm = color.xyz2rgb(result_xyz)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_statistics_luv(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match LUV statistics (mean and std)."""
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_luv = color.rgb2luv(source_norm)
        reference_luv = color.rgb2luv(reference_norm)

        result_luv = source_luv.copy()

        for i in range(3):
            source_mean = source_luv[:, :, i].mean()
            source_std = source_luv[:, :, i].std()

            reference_mean = reference_luv[:, :, i].mean()
            reference_std = reference_luv[:, :, i].std()

            if source_std < 1e-6:
                source_std = 1e-6

            result_luv[:, :, i] = ((source_luv[:, :, i] - source_mean) /
                                   source_std * reference_std + reference_mean)

        # Convert back to RGB
        result_rgb_norm = color.luv2rgb(result_luv)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_statistics_ycbcr(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match YCbCr statistics (mean and std)."""
        import cv2

        # Convert to YCrCb (OpenCV convention)
        source_ycrcb = cv2.cvtColor(source, cv2.COLOR_RGB2YCrCb).astype(np.float32)
        reference_ycrcb = cv2.cvtColor(reference, cv2.COLOR_RGB2YCrCb).astype(np.float32)

        result_ycrcb = source_ycrcb.copy()

        for i in range(3):
            source_mean = source_ycrcb[:, :, i].mean()
            source_std = source_ycrcb[:, :, i].std()

            reference_mean = reference_ycrcb[:, :, i].mean()
            reference_std = reference_ycrcb[:, :, i].std()

            if source_std < 1e-6:
                source_std = 1e-6

            result_ycrcb[:, :, i] = ((source_ycrcb[:, :, i] - source_mean) /
                                     source_std * reference_std + reference_mean)

        # Clip to valid range
        result_ycrcb = np.clip(result_ycrcb, 0, 255).astype(np.uint8)
        result_rgb = cv2.cvtColor(result_ycrcb, cv2.COLOR_YCrCb2RGB)

        return result_rgb

    @staticmethod
    def blend(
        source: np.ndarray,
        transferred: np.ndarray,
        alpha: float = 0.5
    ) -> np.ndarray:
        """
        Blend between source and transferred image.

        Args:
            source: Original source image
            transferred: Color-transferred image
            alpha: Blend factor (0 = source, 1 = transferred, 0.5 = equal blend)

        Returns:
            Blended image
        """
        return (source * (1 - alpha) + transferred * alpha).astype(np.uint8)

    @staticmethod
    def compute_color_difference(
        image1: np.ndarray,
        image2: np.ndarray
    ) -> dict:
        """
        Compute color differences between two images.

        Args:
            image1: First image
            image2: Second image

        Returns:
            Dictionary with difference metrics
        """
        metrics = {}

        # RGB statistics difference
        for i, name in enumerate(['R', 'G', 'B']):
            metrics[f'{name}_mean_diff'] = (
                image1[:, :, i].mean() - image2[:, :, i].mean()
            )
            metrics[f'{name}_std_diff'] = (
                image1[:, :, i].std() - image2[:, :, i].std()
            )

        # LAB statistics difference
        image1_lab = color.rgb2lab(image1 / 255.0)
        image2_lab = color.rgb2lab(image2 / 255.0)

        for i, name in enumerate(['L', 'a', 'b']):
            metrics[f'{name}_mean_diff'] = (
                image1_lab[:, :, i].mean() - image2_lab[:, :, i].mean()
            )
            metrics[f'{name}_std_diff'] = (
                image1_lab[:, :, i].std() - image2_lab[:, :, i].std()
            )

        return metrics


