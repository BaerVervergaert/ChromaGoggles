# ArtAnalyzer 🎨

A comprehensive Python-based image analysis tool that visualizes color information across multiple color spaces, including RGB channel decomposition, Hue-Chroma-Luminance analysis, and statistical distributions.

## Features

- **RGB Channel Analysis**: View individual red, green, and blue channels in both grayscale and colored representations
- **Statistical Distributions**: Interactive histograms and kernel density estimation (KDE) plots for each color channel
- **HCL Analysis**: Extract and visualize Hue, Chroma, and Luminance values using the CIELCh color space
- **Multiple Color Spaces**: 
  - HSV (Hue, Saturation, Value)
  - LAB (CIELAB color space)
  - YCbCr (Luma and chroma components)
  - LUV (CIELUV color space)
  - XYZ (CIE 1931 color space)
- **Interactive Web Interface**: Built with Streamlit for easy image upload and exploration
- **Comprehensive Visualizations**: Side-by-side comparisons and detailed statistical metrics

## Installation

This project uses Poetry for dependency management. Follow these steps to set up the project:

### Prerequisites

- Python 3.10 or higher
- Poetry (install from https://python-poetry.org/)

### Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd ArtAnalyzer
```

2. Install dependencies using Poetry:
```bash
poetry install
```

This will create a virtual environment and install all required packages including:
- numpy
- pillow
- opencv-python
- matplotlib
- seaborn
- scikit-image
- streamlit
- pandas

## Usage

### Running the Application

To start the web-based interface:

```bash
poetry run streamlit run main.py
```

This will open a browser window with the ArtAnalyzer interface.

### Using the Interface

1. **Upload an Image**: Click the "Browse files" button to upload an image (PNG, JPG, JPEG, BMP, or TIFF)
2. **Explore Tabs**: Navigate through the different analysis tabs:
   - **RGB Channels**: View color channel decomposition
   - **RGB Statistics**: See histograms and statistics for each RGB channel
   - **Hue-Chroma-Luminance**: Visualize HCL color space representation
   - **HCL Statistics**: View distribution plots and metrics for HCL values
   - **Color Spaces**: Compare different color space representations
   - **Advanced Analysis**: Explore LUV, XYZ, and grayscale conversions

## Project Structure

```
ArtAnalyzer/
├── main.py                 # Streamlit web application
├── image_processor.py      # Image analysis and color space conversion
├── visualizer.py           # Plotting and visualization functions
├── pyproject.toml          # Poetry configuration and dependencies
├── poetry.lock             # Locked dependency versions
└── README.md               # This file
```

## Modules

### image_processor.py

The `ImageAnalyzer` class provides methods for:
- Loading and processing images
- Extracting RGB channels
- Converting to various color spaces (HSV, LAB, YCbCr, LUV, XYZ)
- Computing Hue, Chroma, and Luminance values

### visualizer.py

Functions for creating matplotlib figures:
- `create_channel_comparison()`: RGB channel visualization
- `create_hcl_comparison()`: HCL value visualization
- `create_density_plots()`: Statistical distribution plots
- `create_colorspace_comparison()`: Multi-space comparison
- And more...

## Color Spaces Explained

### RGB (Red, Green, Blue)
The standard color space for digital images. Each pixel has three values (0-255) representing red, green, and blue intensities.

### HCL (Hue, Chroma, Luminance)
Also known as CIELCh, this perceptually uniform color space represents:
- **Hue**: The color angle (0-360°)
- **Chroma**: Color intensity/saturation
- **Luminance**: Perceived brightness (L* from CIELAB)

### HSV (Hue, Saturation, Value)
A cylindrical color space useful for color selection:
- **Hue**: Color type (0-360°)
- **Saturation**: Color purity (0-100%)
- **Value**: Brightness (0-100%)

### LAB (CIELAB)
A perceptually uniform color space:
- **L***: Lightness (0-100)
- **A***: Green to Red axis
- **B***: Blue to Yellow axis

### YCbCr
Used in video compression:
- **Y**: Luma (brightness)
- **Cb**: Blue-difference chroma
- **Cr**: Red-difference chroma

## Examples

After uploading an image, you can:
- Compare how different channels contribute to the final image
- Identify dominant colors through hue distribution analysis
- Analyze color saturation using chroma values
- Examine brightness distribution with luminance plots
- Compare the same image across different color space representations

## Development

### Adding New Features

To add new analysis features:

1. Add processing methods to `ImageAnalyzer` class in `image_processor.py`
2. Create visualization functions in `visualizer.py`
3. Update the Streamlit interface in `main.py` to display new analyses

### Running Tests

(To be implemented)

## Dependencies

- **numpy**: Numerical operations on image arrays
- **pillow**: Image loading and basic manipulation
- **opencv-python**: Advanced image processing and color space conversions
- **matplotlib**: Creating plots and visualizations
- **seaborn**: Statistical data visualization
- **scikit-image**: Additional color space conversions (LAB, LUV, XYZ)
- **streamlit**: Web-based interactive interface
- **pandas**: Data manipulation (used by visualizations)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

(Add your license here)

## Author

BaerVervergaert

## Acknowledgments

- Color space conversion algorithms based on CIE standards
- Built with Streamlit for rapid prototyping and deployment


