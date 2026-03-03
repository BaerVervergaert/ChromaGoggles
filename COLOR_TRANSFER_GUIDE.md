# Color Transfer Feature - Documentation

## Overview

The **Color Transfer** feature allows you to transform the colors of one image (source) to match the color palette of another image (reference). This is useful for:

- **Artistic stylization**: Apply one image's color scheme to another
- **Color grading**: Quickly match the colors of one shot to another
- **Image harmonization**: Make multiple images have a consistent color tone
- **Color correction**: Transfer color profiles between similar images

## How It Works

### Two Transfer Methods

#### 1. Histogram Matching
Transforms the pixel value distributions of the source image to match the reference image's distribution.

**How it works:**
1. Compute histograms for each channel
2. Calculate cumulative distribution functions (CDFs)
3. Map source pixel values to reference values based on CDF matching

**Best for:**
- Subtle, natural-looking color adjustments
- When you want to preserve original image structure
- Fine-tuning color intensity matches

**Pros:**
- Produces natural results
- Preserves image details
- Works in multiple color spaces

**Cons:**
- May not fully match if distributions are very different
- Requires reasonable similarity between images

#### 2. Statistics Matching
Directly adjusts the mean and standard deviation of each channel to match the reference image.

**How it works:**
1. Calculate mean and std for each channel
2. Transform source channel: `(x - source_mean) / source_std * reference_std + reference_mean`

**Best for:**
- Aggressive color transformation
- Quick color matching
- When fine details are less important

**Pros:**
- Fast computation
- Complete color matching
- Mathematically precise

**Cons:**
- Can sometimes produce less natural results
- May lose some color nuance
- Less controllable

### Color Spaces

The feature supports three color spaces for transformation:

#### LAB (Recommended ⭐)
- **Perceptually uniform**: Equal distances in LAB correspond to equal perceived color differences
- **Best quality**: Usually produces the most natural-looking results
- **Channels**:
  - L* (0-100): Lightness
  - a* (-127 to 127): Green-Red axis
  - b* (-127 to 127): Blue-Yellow axis

#### RGB
- **Direct channel matching**: Matches red, green, blue channels independently
- **Fast**: Simplest computation
- **Predictable**: Direct correspondence to monitor colors
- **Downside**: May produce color casts (doesn't account for human perception)

#### HSV (Histogram only)
- **Intuitive**: Separates color appearance
- **Channels**:
  - H (0-180): Hue
  - S (0-255): Saturation
  - V (0-255): Value (brightness)
- **Best for**: Color-aware transformations

## Step-by-Step Guide

### 1. Upload Images
- **Source Image**: The image you want to transform
- **Reference Image**: The image whose colors you want to match

### 2. Select Transfer Method
- **Histogram Matching**: For subtle, natural adjustments
- **Statistics Matching**: For aggressive color transformation

### 3. Choose Color Space
- **LAB**: Best for photorealistic results (recommended)
- **RGB**: Fast, direct channel matching
- **HSV**: For color-aware transformations (histogram only)

### 4. Review Results
The app shows:
- **Before/After Comparison**: Side-by-side preview
- **Histogram Comparison**: Shows how distributions changed
- **Color Difference Analysis**: Visualizes pixel-level changes
- **Statistics Table**: Detailed metrics

### 5. Fine-tune with Blending
Use the **Blend** slider to mix between:
- **0.0**: Original source (no transfer)
- **0.5**: 50/50 blend (subtle effect)
- **1.0**: Full color transfer (maximum effect)

### 6. Download Result
- Download the full transfer
- Download the blended result (if using blend)

## Technical Details

### Algorithm: Histogram Matching

For each color channel:
1. Compute histogram: counts of each pixel value
2. Normalize to get probability distribution
3. Compute CDF: cumulative sum of normalized histogram
4. For each source pixel value, find the reference value with closest CDF value
5. Apply this mapping to transform the image

```
Source CDF: [0.0, 0.1, 0.2, ..., 1.0]
Reference CDF: [0.0, 0.05, 0.15, ..., 1.0]

For source value 100 with CDF 0.45:
Find reference value where CDF ≈ 0.45
Map source 100 → reference 125
```

### Algorithm: Statistics Matching

For each color channel:
```
transformed[i,j,k] = (source[i,j,k] - source_mean) / source_std 
                    * reference_std + reference_mean
```

This is a linear transformation that:
- Centers source values (subtract mean)
- Rescales to reference variance (divide by source_std, multiply by reference_std)
- Shifts to reference mean (add reference_mean)

### Color Difference Metric: Delta E (CIE76)

Measures perceptual color difference between images:
```
ΔE = sqrt((ΔL*)² + (Δa*)² + (Δb*)²)
```

Where L*, a*, b* are LAB color space coordinates.

**Interpretation:**
- ΔE < 1: Not perceptibly different
- ΔE 1-2: Just noticeable difference
- ΔE 2-10: Noticeable difference
- ΔE > 10: Large difference

## Advanced Usage

### Matching Multiple Images
To color-match multiple images to one reference:
1. Use reference image as the "Reference"
2. Upload each image as "Source" sequentially
3. Download each result

### Combining with Analysis
1. Use the **Color Analysis** tab to examine color distributions
2. Switch to **Color Transfer** tab with same reference
3. See how the transfer affects different color spaces

### Iterative Refinement
1. Apply color transfer
2. Check results in Color Analysis tab
3. Adjust blend factor if needed
4. Download final result

## Tips and Best Practices

### For Best Results

1. **Use LAB color space**: It's perceptually uniform and usually gives best results

2. **Start with Histogram Matching**: Try this first for natural-looking results

3. **Compare histogram distributions**: Look at the histogram comparison to verify the transfer worked

4. **Use blending for subtlety**: A blend factor of 0.7-0.9 often produces more natural results than 1.0

5. **Ensure image compatibility**: Works best when images are similar in content (e.g., both outdoor photos)

### Common Issues and Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| Unnatural colors | LAB doesn't work well for very different images | Try RGB or HSV, use lower blend factor |
| Not enough color change | Histogram matching too subtle | Use Statistics Matching |
| Too much change | Statistics Matching too aggressive | Use Histogram Matching, or reduce blend factor |
| Color cast | Statistics Matching in RGB | Use LAB color space |
| Lost details | Transfer too strong | Use blending (α < 1.0) |

## Examples

### Example 1: Indoor to Outdoor
- **Source**: Indoor photo (warm tungsten lighting)
- **Reference**: Outdoor photo (cool daylight)
- **Method**: Histogram Matching, LAB
- **Result**: Transforms indoor warm tones to outdoor cool tones

### Example 2: Artistic Style Transfer
- **Source**: Photo you want to style
- **Reference**: Reference artwork or photo with desired color palette
- **Method**: Statistics Matching, LAB
- **Result**: Matches color distribution to create artistic effect

### Example 3: Color Correction
- **Source**: Incorrectly white-balanced photo
- **Reference**: Correctly white-balanced photo from same scene
- **Method**: Histogram Matching, RGB
- **Result**: Corrects color balance

## Limitations

1. **Not content-aware**: Matches distributions, not semantic content
2. **Requires similar images**: Works best when images have similar structure
3. **No spatial matching**: Doesn't match colors at specific locations
4. **All channels treated equally**: Doesn't weight channels by importance

## Future Enhancements

Possible improvements to the color transfer feature:

- **Local color transfer**: Match colors in specific regions
- **Channel weighting**: Give more importance to certain channels
- **Multi-scale transfer**: Match at multiple scales
- **Deep learning methods**: Use neural networks for better quality
- **Interactive masks**: Select regions to apply transfer

## Mathematical Background

### Histogram Equalization & Matching

**Histogram Equalization** makes a single image have uniform pixel distribution.

**Histogram Matching** (our method) makes one image's distribution match another's using CDF matching.

**Reference**: Gonzalez & Woods, "Digital Image Processing"

### Perceptual Color Spaces

LAB space was designed to be "perceptually uniform" - equal distances correspond to equal perceived differences. This is why it produces better visual results than RGB.

**Reference**: CIE Color Science Technical Documentation

## Related Features

- **Color Analysis Tab**: Examine color distributions before/after transfer
- **Color Space Visualizations**: Understand how colors are represented
- **Histogram Plots**: Detailed distribution analysis

## Support & Feedback

For issues or feature requests related to color transfer:
1. Check the troubleshooting section above
2. Experiment with different methods and color spaces
3. Open an issue on GitHub with example images

---

## Quick Reference

| Feature | Best For | Color Space | Method |
|---------|----------|-------------|--------|
| Natural results | Photo recoloring | LAB | Histogram |
| Artistic style | Style transfer | LAB | Statistics |
| Color correction | White balance | RGB | Histogram |
| Fast matching | Quick tests | RGB | Statistics |
| Color-aware | Hue preservation | HSV | Histogram |

---

*Last updated: March 2026*

