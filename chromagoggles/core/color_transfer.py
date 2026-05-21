# Copyright (c) 2026 Baer Ververgaert. All rights reserved.
"""
Color transfer module for matching color distributions between images.

This module provides algorithms to transform image A to match the color
distribution of image B (reference image).
"""
import numpy as np
from skimage import color
from chromagoggles.colorspaces.oklab_utils import (
    rgb_to_oklab,
    oklab_to_rgb,
    oklab_to_oklch,
    oklch_to_oklab,
)


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
            'oklab': ColorTransfer._match_histograms_oklab,
            'oklch': ColorTransfer._match_histograms_oklch,
            'xyz': ColorTransfer._match_histograms_xyz,
            'luv': ColorTransfer._match_histograms_luv,
            'ycbcr': ColorTransfer._match_histograms_ycbcr,
        }

        if colorspace not in colorspace_map:
            raise ValueError(f"Unknown colorspace: {colorspace}. Supported: {list(colorspace_map.keys())}")

        return colorspace_map[colorspace](source, reference)

    @staticmethod
    def match_correlation_preserving(
        source: np.ndarray,
        reference: np.ndarray,
        colorspace: str = 'lab'
    ) -> np.ndarray:
        """
        Match color distribution while preserving correlations between channels.

        Uses the Monge-Kantorovich linear color transfer method which preserves
        the correlation structure between color dimensions. This is based on
        optimal transport theory and produces more natural-looking results than
        independent channel matching.

        Reference: "Color Transfer between Images" by Reinhard et al. (2001)
        and improvements from "N-Dimensional Probability Density Function Transfer"

        Args:
            source: Source image (height, width, 3), uint8 [0, 255]
            reference: Reference image (height, width, 3), uint8 [0, 255]
            colorspace: Color space for matching ('lab', 'rgb', 'hsv', 'hcl', 'xyz', 'luv', 'ycbcr')

        Returns:
            Transformed image with matched distribution and preserved correlations
        """
        colorspace_map = {
            'lab': ColorTransfer._match_correlation_preserving_lab,
            'rgb': ColorTransfer._match_correlation_preserving_rgb,
            'hsv': ColorTransfer._match_correlation_preserving_hsv,
            'hcl': ColorTransfer._match_correlation_preserving_hcl,
            'oklab': ColorTransfer._match_correlation_preserving_oklab,
            'oklch': ColorTransfer._match_correlation_preserving_oklch,
            'xyz': ColorTransfer._match_correlation_preserving_xyz,
            'luv': ColorTransfer._match_correlation_preserving_luv,
            'ycbcr': ColorTransfer._match_correlation_preserving_ycbcr,
        }

        if colorspace not in colorspace_map:
            raise ValueError(f"Unknown colorspace: {colorspace}. Supported: {list(colorspace_map.keys())}")

        return colorspace_map[colorspace](source, reference)

    @staticmethod
    def _apply_monge_kantorovich_transform(
        source_data: np.ndarray,
        reference_data: np.ndarray
    ) -> np.ndarray:
        """
        Apply Monge-Kantorovich linear color transfer.

        This preserves the correlation structure by using the full covariance matrix.

        Args:
            source_data: Source data as (n_pixels, n_channels)
            reference_data: Reference data as (m_pixels, n_channels)

        Returns:
            Transformed data as (n_pixels, n_channels)
        """
        # Compute means
        source_mean = source_data.mean(axis=0)
        reference_mean = reference_data.mean(axis=0)

        # Center the data
        source_centered = source_data - source_mean
        reference_centered = reference_data - reference_mean

        # Compute covariance matrices
        n_source = source_data.shape[0]
        n_reference = reference_data.shape[0]

        cov_source = (source_centered.T @ source_centered) / (n_source - 1)
        cov_reference = (reference_centered.T @ reference_centered) / (n_reference - 1)

        # Add small regularization to avoid singular matrices
        eps = 1e-6
        cov_source += eps * np.eye(cov_source.shape[0])
        cov_reference += eps * np.eye(cov_reference.shape[0])

        # Compute the transformation using Cholesky decomposition
        # T = L_ref @ L_source^(-1)
        try:
            L_source = np.linalg.cholesky(cov_source)
            L_reference = np.linalg.cholesky(cov_reference)

            # Transformation matrix
            L_source_inv = np.linalg.inv(L_source)
            T = L_reference @ L_source_inv

        except np.linalg.LinAlgError:
            # Fallback to SVD if Cholesky fails
            U_s, S_s, Vt_s = np.linalg.svd(cov_source)
            U_r, S_r, Vt_r = np.linalg.svd(cov_reference)

            # Regularize singular values
            S_s = np.maximum(S_s, eps)

            # Transform: sqrt(Sigma_ref) @ sqrt(Sigma_source)^(-1)
            sqrt_S_source_inv = np.diag(1.0 / np.sqrt(S_s))
            sqrt_S_reference = np.diag(np.sqrt(S_r))

            T = U_r @ sqrt_S_reference @ sqrt_S_source_inv @ Vt_s

        # Apply transformation
        result = source_centered @ T.T + reference_mean

        return result

    @staticmethod
    def _match_correlation_preserving_lab(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match LAB with correlation preservation."""
        # Convert to LAB
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_lab = color.rgb2lab(source_norm)
        reference_lab = color.rgb2lab(reference_norm)

        # Reshape to (n_pixels, 3)
        h, w = source_lab.shape[:2]
        source_flat = source_lab.reshape(-1, 3)
        reference_flat = reference_lab.reshape(-1, 3)

        # Apply correlation-preserving transform
        result_flat = ColorTransfer._apply_monge_kantorovich_transform(
            source_flat, reference_flat
        )

        # Reshape back
        result_lab = result_flat.reshape(h, w, 3)

        # Convert back to RGB
        result_rgb_norm = color.lab2rgb(result_lab)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_correlation_preserving_rgb(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match RGB with correlation preservation."""
        # Reshape to (n_pixels, 3)
        h, w = source.shape[:2]
        source_flat = source.reshape(-1, 3).astype(np.float64)
        reference_flat = reference.reshape(-1, 3).astype(np.float64)

        # Apply correlation-preserving transform
        result_flat = ColorTransfer._apply_monge_kantorovich_transform(
            source_flat, reference_flat
        )

        # Reshape back and clip
        result = result_flat.reshape(h, w, 3)
        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_correlation_preserving_hsv(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match HSV with correlation preservation."""
        import cv2

        source_hsv = cv2.cvtColor(source, cv2.COLOR_RGB2HSV).astype(np.float64)
        reference_hsv = cv2.cvtColor(reference, cv2.COLOR_RGB2HSV).astype(np.float64)

        h, w = source_hsv.shape[:2]
        source_flat = source_hsv.reshape(-1, 3)
        reference_flat = reference_hsv.reshape(-1, 3)

        result_flat = ColorTransfer._apply_monge_kantorovich_transform(
            source_flat, reference_flat
        )

        result_hsv = result_flat.reshape(h, w, 3)

        # Clip to valid ranges
        result_hsv[:, :, 0] = np.clip(result_hsv[:, :, 0], 0, 180)
        result_hsv[:, :, 1] = np.clip(result_hsv[:, :, 1], 0, 255)
        result_hsv[:, :, 2] = np.clip(result_hsv[:, :, 2], 0, 255)

        result_hsv = result_hsv.astype(np.uint8)
        result_rgb = cv2.cvtColor(result_hsv, cv2.COLOR_HSV2RGB)

        return result_rgb

    @staticmethod
    def _match_correlation_preserving_hcl(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match HCL with correlation preservation."""
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_lab = color.rgb2lab(source_norm)
        reference_lab = color.rgb2lab(reference_norm)

        source_lch = color.lab2lch(source_lab)
        reference_lch = color.lab2lch(reference_lab)

        h, w = source_lch.shape[:2]
        source_flat = source_lch.reshape(-1, 3)
        reference_flat = reference_lch.reshape(-1, 3)

        result_flat = ColorTransfer._apply_monge_kantorovich_transform(
            source_flat, reference_flat
        )

        result_lch = result_flat.reshape(h, w, 3)

        # Clip to valid ranges
        result_lch[:, :, 0] = np.clip(result_lch[:, :, 0], 0, 100)
        result_lch[:, :, 1] = np.maximum(result_lch[:, :, 1], 0)
        result_lch[:, :, 2] = result_lch[:, :, 2] % (2 * np.pi)

        result_lab = color.lch2lab(result_lch)
        result_rgb_norm = color.lab2rgb(result_lab)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_correlation_preserving_oklab(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match Oklab with correlation preservation."""
        source_oklab = rgb_to_oklab(source)
        reference_oklab = rgb_to_oklab(reference)

        h, w = source_oklab.shape[:2]
        source_flat = source_oklab.reshape(-1, 3)
        reference_flat = reference_oklab.reshape(-1, 3)

        result_flat = ColorTransfer._apply_monge_kantorovich_transform(
            source_flat, reference_flat
        )
        result_oklab = result_flat.reshape(h, w, 3)

        result_oklab[:, :, 0] = np.clip(result_oklab[:, :, 0], 0.0, 1.0)
        result_oklab[:, :, 1:] = np.clip(result_oklab[:, :, 1:], -0.5, 0.5)
        return oklab_to_rgb(result_oklab)

    @staticmethod
    def _match_correlation_preserving_oklch(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match Oklch with correlation preservation."""
        source_oklch = oklab_to_oklch(rgb_to_oklab(source))
        reference_oklch = oklab_to_oklch(rgb_to_oklab(reference))

        h, w = source_oklch.shape[:2]
        source_flat = source_oklch.reshape(-1, 3)
        reference_flat = reference_oklch.reshape(-1, 3)

        result_flat = ColorTransfer._apply_monge_kantorovich_transform(
            source_flat, reference_flat
        )
        result_oklch = result_flat.reshape(h, w, 3)

        result_oklch[:, :, 0] = np.clip(result_oklch[:, :, 0], 0.0, 1.0)
        result_oklch[:, :, 1] = np.clip(result_oklch[:, :, 1], 0.0, 0.5)
        result_oklch[:, :, 2] = result_oklch[:, :, 2] % 360.0

        result_oklab = oklch_to_oklab(result_oklch)
        return oklab_to_rgb(result_oklab)

    @staticmethod
    def _match_correlation_preserving_xyz(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match XYZ with correlation preservation."""
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_xyz = color.rgb2xyz(source_norm)
        reference_xyz = color.rgb2xyz(reference_norm)

        h, w = source_xyz.shape[:2]
        source_flat = source_xyz.reshape(-1, 3)
        reference_flat = reference_xyz.reshape(-1, 3)

        result_flat = ColorTransfer._apply_monge_kantorovich_transform(
            source_flat, reference_flat
        )

        result_xyz = result_flat.reshape(h, w, 3)
        result_xyz = np.maximum(result_xyz, 0)

        result_rgb_norm = color.xyz2rgb(result_xyz)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_correlation_preserving_luv(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match LUV with correlation preservation."""
        source_norm = source / 255.0
        reference_norm = reference / 255.0

        source_luv = color.rgb2luv(source_norm)
        reference_luv = color.rgb2luv(reference_norm)

        h, w = source_luv.shape[:2]
        source_flat = source_luv.reshape(-1, 3)
        reference_flat = reference_luv.reshape(-1, 3)

        result_flat = ColorTransfer._apply_monge_kantorovich_transform(
            source_flat, reference_flat
        )

        result_luv = result_flat.reshape(h, w, 3)

        result_rgb_norm = color.luv2rgb(result_luv)
        return np.clip(result_rgb_norm * 255, 0, 255).astype(np.uint8)

    @staticmethod
    def _match_correlation_preserving_ycbcr(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match YCbCr with correlation preservation."""
        import cv2

        source_ycrcb = cv2.cvtColor(source, cv2.COLOR_RGB2YCrCb).astype(np.float64)
        reference_ycrcb = cv2.cvtColor(reference, cv2.COLOR_RGB2YCrCb).astype(np.float64)

        h, w = source_ycrcb.shape[:2]
        source_flat = source_ycrcb.reshape(-1, 3)
        reference_flat = reference_ycrcb.reshape(-1, 3)

        result_flat = ColorTransfer._apply_monge_kantorovich_transform(
            source_flat, reference_flat
        )

        result_ycrcb = result_flat.reshape(h, w, 3)
        result_ycrcb = np.clip(result_ycrcb, 0, 255).astype(np.uint8)

        result_rgb = cv2.cvtColor(result_ycrcb, cv2.COLOR_YCrCb2RGB)
        return result_rgb
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
    def _match_histograms_oklab(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match histograms in Oklab color space."""
        source_oklab = rgb_to_oklab(source)
        reference_oklab = rgb_to_oklab(reference)
        result_oklab = source_oklab.copy()

        oklab_ranges = [(0.0, 1.0), (-0.5, 0.5), (-0.5, 0.5)]

        for i, (min_val, max_val) in enumerate(oklab_ranges):
            source_channel = ((source_oklab[:, :, i] - min_val) / (max_val - min_val) * 255).astype(np.uint8)
            reference_channel = ((reference_oklab[:, :, i] - min_val) / (max_val - min_val) * 255).astype(np.uint8)

            source_hist, _ = np.histogram(source_channel.flatten(), bins=256, range=(0, 256))
            reference_hist, _ = np.histogram(reference_channel.flatten(), bins=256, range=(0, 256))

            source_cdf = np.cumsum(source_hist) / (source_hist.sum() + 1e-10)
            reference_cdf = np.cumsum(reference_hist) / (reference_hist.sum() + 1e-10)

            mapping = np.zeros(256, dtype=np.uint8)
            for j in range(256):
                idx = np.argmin(np.abs(reference_cdf - source_cdf[j]))
                mapping[j] = idx

            mapped_channel = mapping[source_channel]
            result_oklab[:, :, i] = (mapped_channel / 255.0 * (max_val - min_val) + min_val)

        result_oklab[:, :, 0] = np.clip(result_oklab[:, :, 0], 0.0, 1.0)
        result_oklab[:, :, 1:] = np.clip(result_oklab[:, :, 1:], -0.5, 0.5)
        return oklab_to_rgb(result_oklab)

    @staticmethod
    def _match_histograms_oklch(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match histograms in Oklch color space."""
        source_oklch = oklab_to_oklch(rgb_to_oklab(source))
        reference_oklch = oklab_to_oklch(rgb_to_oklab(reference))
        result_oklch = source_oklch.copy()

        oklch_ranges = [(0.0, 1.0), (0.0, 0.5), (0.0, 360.0)]

        for i, (min_val, max_val) in enumerate(oklch_ranges):
            source_channel = source_oklch[:, :, i]
            reference_channel = reference_oklch[:, :, i]

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
            result_oklch[:, :, i] = (mapped_channel / 255.0 * (max_val - min_val) + min_val)

        result_oklch[:, :, 0] = np.clip(result_oklch[:, :, 0], 0.0, 1.0)
        result_oklch[:, :, 1] = np.clip(result_oklch[:, :, 1], 0.0, 0.5)
        result_oklch[:, :, 2] = result_oklch[:, :, 2] % 360.0

        result_oklab = oklch_to_oklab(result_oklch)
        return oklab_to_rgb(result_oklab)

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
            'oklab': ColorTransfer._match_statistics_oklab,
            'oklch': ColorTransfer._match_statistics_oklch,
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
    def _match_statistics_oklab(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match Oklab statistics (mean and std)."""
        source_oklab = rgb_to_oklab(source)
        reference_oklab = rgb_to_oklab(reference)
        result_oklab = source_oklab.copy()

        for i in range(3):
            source_mean = source_oklab[:, :, i].mean()
            source_std = source_oklab[:, :, i].std()
            reference_mean = reference_oklab[:, :, i].mean()
            reference_std = reference_oklab[:, :, i].std()

            if source_std < 1e-6:
                source_std = 1e-6

            result_oklab[:, :, i] = ((source_oklab[:, :, i] - source_mean) /
                                     source_std * reference_std + reference_mean)

        result_oklab[:, :, 0] = np.clip(result_oklab[:, :, 0], 0.0, 1.0)
        result_oklab[:, :, 1:] = np.clip(result_oklab[:, :, 1:], -0.5, 0.5)
        return oklab_to_rgb(result_oklab)

    @staticmethod
    def _match_statistics_oklch(
        source: np.ndarray,
        reference: np.ndarray
    ) -> np.ndarray:
        """Match Oklch statistics (mean and std)."""
        source_oklch = oklab_to_oklch(rgb_to_oklab(source))
        reference_oklch = oklab_to_oklch(rgb_to_oklab(reference))
        result_oklch = source_oklch.copy()

        for i in range(3):
            source_mean = source_oklch[:, :, i].mean()
            source_std = source_oklch[:, :, i].std()
            reference_mean = reference_oklch[:, :, i].mean()
            reference_std = reference_oklch[:, :, i].std()

            if source_std < 1e-6:
                source_std = 1e-6

            result_oklch[:, :, i] = ((source_oklch[:, :, i] - source_mean) /
                                     source_std * reference_std + reference_mean)

        result_oklch[:, :, 0] = np.clip(result_oklch[:, :, 0], 0.0, 1.0)
        result_oklch[:, :, 1] = np.clip(result_oklch[:, :, 1], 0.0, 0.5)
        result_oklch[:, :, 2] = result_oklch[:, :, 2] % 360.0

        result_oklab = oklch_to_oklab(result_oklch)
        return oklab_to_rgb(result_oklab)

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

    @staticmethod
    def match_nearest_reference_pixels(
        source: np.ndarray,
        reference: np.ndarray,
        colorspace: str = 'lab',
        working_size: int = 160
    ) -> np.ndarray:
        """
        Replace each pixel in a scaled source image with the closest pixel from
        a scaled reference image.

        Steps:
        1) Scale source and reference to the same working shape.
        2) Build a nearest-neighbor index over reference pixels in the chosen color space.
        3) Replace every source pixel by its closest reference pixel.
        4) Resize result back to source shape for consistent app output.

        Args:
            source: Source RGB image, uint8 [0, 255]
            reference: Reference RGB image, uint8 [0, 255]
            colorspace: One of 'rgb', 'lab', 'hsv', 'hcl', 'xyz', 'luv', 'ycbcr'
            working_size: Common square working resolution used for matching

        Returns:
            RGB uint8 image with source shape
        """
        import cv2
        from scipy.spatial import cKDTree

        if working_size < 8:
            raise ValueError("working_size must be >= 8")

        target_hw = (working_size, working_size)
        # cv2.resize expects (width, height)
        source_scaled = cv2.resize(source, (target_hw[1], target_hw[0]), interpolation=cv2.INTER_AREA)
        reference_scaled = cv2.resize(reference, (target_hw[1], target_hw[0]), interpolation=cv2.INTER_AREA)

        source_feat = ColorTransfer._to_matching_features(source_scaled, colorspace)
        reference_feat = ColorTransfer._to_matching_features(reference_scaled, colorspace)

        source_flat = source_feat.reshape(-1, source_feat.shape[-1])
        reference_flat = reference_feat.reshape(-1, reference_feat.shape[-1])
        reference_rgb_flat = reference_scaled.reshape(-1, 3)

        tree = cKDTree(reference_flat)
        _, nn_idx = tree.query(source_flat, k=1)

        matched_scaled = reference_rgb_flat[nn_idx].reshape(source_scaled.shape)

        # Keep app behavior consistent: output uses original source shape.
        result = cv2.resize(matched_scaled, (source.shape[1], source.shape[0]), interpolation=cv2.INTER_NEAREST)
        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def _to_matching_features(image_rgb: np.ndarray, colorspace: str) -> np.ndarray:
        """Convert RGB image to nearest-neighbor feature vectors for a color space."""
        import cv2

        if colorspace == 'rgb':
            return image_rgb.astype(np.float32) / 255.0

        if colorspace == 'lab':
            return color.rgb2lab(image_rgb / 255.0).astype(np.float32)

        if colorspace == 'hsv':
            hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
            h = hsv[:, :, 0] / 180.0 * (2.0 * np.pi)
            s = hsv[:, :, 1] / 255.0
            v = hsv[:, :, 2] / 255.0
            # Circular hue embedding avoids 0/360 discontinuity.
            return np.stack([np.cos(h) * s, np.sin(h) * s, v], axis=-1).astype(np.float32)

        if colorspace == 'hcl':
            lab = color.rgb2lab(image_rgb / 255.0)
            lch = color.lab2lch(lab).astype(np.float32)
            l = lch[:, :, 0] / 100.0
            c = lch[:, :, 1] / 150.0
            h = lch[:, :, 2]
            return np.stack([np.cos(h) * c, np.sin(h) * c, l], axis=-1).astype(np.float32)

        if colorspace == 'oklab':
            return rgb_to_oklab(image_rgb).astype(np.float32)

        if colorspace == 'oklch':
            oklch = oklab_to_oklch(rgb_to_oklab(image_rgb)).astype(np.float32)
            l = oklch[:, :, 0]
            c = oklch[:, :, 1] / 0.5
            h = np.radians(oklch[:, :, 2])
            return np.stack([np.cos(h) * c, np.sin(h) * c, l], axis=-1).astype(np.float32)

        if colorspace == 'xyz':
            return color.rgb2xyz(image_rgb / 255.0).astype(np.float32)

        if colorspace == 'luv':
            luv = color.rgb2luv(image_rgb / 255.0).astype(np.float32)
            luv[:, :, 0] /= 100.0
            luv[:, :, 1] /= 100.0
            luv[:, :, 2] /= 100.0
            return luv

        if colorspace == 'ycbcr':
            ycrcb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2YCrCb).astype(np.float32)
            ycbcr = ycrcb.copy()
            ycbcr[:, :, 1] = ycrcb[:, :, 2]  # Cb
            ycbcr[:, :, 2] = ycrcb[:, :, 1]  # Cr
            return ycbcr / 255.0

        raise ValueError(f"Unknown colorspace: {colorspace}")
