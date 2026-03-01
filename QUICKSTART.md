# Quick Start Guide

## Installation

1. Ensure you have Python 3.10+ and Poetry installed
2. Install dependencies:
   ```bash
   poetry install
   ```

## Running the Application

### Option 1: Using the run script
```bash
./run.sh
```

### Option 2: Using Poetry directly
```bash
poetry run streamlit run main.py
```

### Option 3: Activate the virtual environment
```bash
poetry shell
streamlit run main.py
```

## Using the Application

1. The application will open in your default web browser at http://localhost:8501
2. Click "Browse files" to upload an image
3. Explore the different tabs to view various analyses:
   - **RGB Channels**: See how the image is composed of red, green, and blue
   - **RGB Statistics**: View histograms and statistical metrics for each channel
   - **Hue-Chroma-Luminance**: Explore the perceptual color properties
   - **HCL Statistics**: See distribution plots for hue, chroma, and luminance
   - **Color Spaces**: Compare HSV, LAB, and YCbCr representations
   - **Advanced Analysis**: View LUV, XYZ, and grayscale conversions

## Supported Image Formats

- PNG
- JPG/JPEG
- BMP
- TIFF

## Tips

- Larger images will take longer to process
- Use images with diverse colors for more interesting analyses
- The density plots show how color values are distributed across the image
- Hue values range from 0-360° and represent the color wheel
- Chroma represents color intensity (higher = more saturated)
- Luminance represents perceived brightness

## Troubleshooting

### Packages not found
Make sure you've installed dependencies:
```bash
poetry install
```

### Application won't start
Try updating Streamlit:
```bash
poetry update streamlit
```

### IDE doesn't recognize imports
Configure your IDE to use the Poetry virtual environment:
```bash
poetry env info
```
Then point your IDE to the path shown.

## Examples of Analysis

### RGB Channels
Shows how combining red, green, and blue light creates the full color image.
Useful for understanding color composition.

### HCL Analysis
Hue-Chroma-Luminance provides a more perceptually uniform color space.
This makes it easier to analyze colors as humans perceive them.

### Density Plots
Show the distribution of color values across the image.
Peaks indicate dominant colors or brightness levels.

## Exporting Results

Currently, the application displays results interactively. To save visualizations:
1. Right-click on any plot
2. Select "Save image as..."
3. Choose your desired location and format

## Further Reading

- [CIELAB Color Space](https://en.wikipedia.org/wiki/CIELAB_color_space)
- [HSV Color Space](https://en.wikipedia.org/wiki/HSL_and_HSV)
- [RGB Color Model](https://en.wikipedia.org/wiki/RGB_color_model)
- [Streamlit Documentation](https://docs.streamlit.io)

