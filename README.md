# ChromaGoggles 🎨

A comprehensive, modular Python-based image analysis tool that visualizes color information across multiple color spaces and transfers colors between images with a clean, extensible architecture.

## ✨ Features

### Color Analysis
- **10 Color Spaces**: RGB, HSV, LAB, HCL (CIELCh), Oklab, Oklch, LMS, XYZ, LUV, YCbCr
- **Channel Decomposition**: View individual color channels with appropriate colormaps
- **Statistical Analysis**: Histograms, KDE plots, and descriptive statistics for each channel
- **Scatter Plots**: Visualize relationships between color channels with density-based transparency
- **Interactive Web Interface**: Built with Streamlit for easy image upload and exploration

### 🎨 Color Transfer (NEW!)
- **Histogram Matching**: Transform one image to match another's color distribution
- **Statistics Matching**: Match mean and standard deviation of color channels
- **Multiple Color Spaces**: LAB (perceptually uniform), RGB, HSV
- **Blending Control**: Fine-tune the transfer effect with alpha blending
- **Visual Analysis**: Before/after comparisons, histogram analysis, color difference metrics
- **Download Results**: Save transferred images in high quality

### Color Spaces
- **RGB**: Red, Green, Blue - direct pixel values
- **HSV**: Hue, Saturation, Value - intuitive color representation
- **LAB**: L\*a\*b\* - perceptually uniform color space
- **HCL (LCh)**: Hue, Chroma, Luminance - cylindrical LAB with custom colormap
- **Oklab**: Modern perceptual lightness-opponent color space
- **Oklch**: Cylindrical Oklab with Lightness, Chroma, and Hue
- **LMS**: Long, Medium, Short cone-response space
- **XYZ**: CIE 1931 tristimulus values
- **LUV**: L\*u\*v\* - alternative perceptually uniform space
- **YCbCr**: Luma and chroma (used in JPEG/MPEG)

### Architecture Highlights
- **Modular Design**: Easy to extend with new color spaces and features
- **Plugin System**: Color spaces self-register automatically
- **Reusable Components**: Visualization strategies work with any color space
- **Type-Safe**: Full type hints for better IDE support
- **Well-Documented**: Comprehensive guides and examples

## Installation

This project uses Poetry for dependency management. Follow these steps to set up the project:

### Prerequisites

- Python 3.10 or higher
- Poetry (install from https://python-poetry.org/)

### Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd ChromaGoggles
```

2. Install dependencies using Poetry:
```bash
poetry install
```

This will create a virtual environment and install all required packages including:
- numpy
- colour-science
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

This will open a browser window with the ChromaGoggles interface.

### Using the Interface

1. **Upload an Image**: Click the "Browse files" button to upload an image (PNG, JPG, JPEG, BMP, TIFF, or WebP)
2. **Explore Tabs**: Navigate through automatically generated tabs for each color space:
   - Each color space has a channel visualization tab
   - Color spaces with statistics also have a statistics tab with:
     - Histograms and KDE density plots
     - Scatter plots showing channel relationships
     - Descriptive statistics (mean, std, min, max, median)

## 📁 Project Structure

```
ChromaGoggles/
├── chromagoggles/                   # Main package
│   ├── core/                      # Core abstractions
│   │   ├── color_space.py         # ColorSpace base class
│   │   ├── registry.py            # ColorSpaceRegistry
│   │   └── statistics.py          # StatisticsCalculator
│   ├── colorspaces/               # Color space implementations
│   │   ├── rgb.py                 # RGB color space
│   │   ├── hsv.py                 # HSV color space
│   │   ├── lab.py                 # LAB color space
│   │   ├── hcl.py                 # HCL (LCh) color space
│   │   ├── oklab.py               # Oklab color space
│   │   ├── oklch.py               # Oklch color space
│   │   ├── lms.py                 # LMS color space
│   │   ├── xyz.py                 # XYZ color space
│   │   ├── luv.py                 # LUV color space
│   │   └── ycbcr.py               # YCbCr color space
│   ├── visualizations/            # Visualization strategies
│   │   ├── base.py                # VisualizationStrategy base
│   │   ├── channels.py            # Channel comparison viz
│   │   ├── density.py             # Density plot viz
│   │   ├── scatter.py             # Scatter plot viz
│   │   └── colormaps.py           # Custom colormaps (LCh hue)
│   └── ui/                        # UI components
│       └── tab_factory.py         # Dynamic tab generation
├── main.py                        # Streamlit application (96 lines!)
├── image_processor.py             # Legacy (preserved for reference)
├── visualizer.py                  # Legacy (preserved for reference)
├── test_refactored.py             # Comprehensive test suite
├── pyproject.toml                 # Poetry configuration
└── README.md                      # This file
```

## 🏗️ Architecture

### ColorSpace Abstraction

Each color space is a self-contained class that inherits from `ColorSpace`:

```python
@ColorSpaceRegistry.register
class RGBColorSpace(ColorSpace):
    @property
    def name(self) -> str: ...
    
    @property
    def channels_metadata(self) -> list[ChannelMetadata]: ...
    
    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray: ...
```

Benefits:
- **Self-documenting**: Metadata describes each channel
- **Automatic UI**: Tabs generate automatically
- **Reusable**: Visualizations work with any ColorSpace

### Visualization Strategies

Visualization strategies work generically with any ColorSpace:

```python
viz = ChannelComparisonViz()
fig = viz.create(colorspace, rgb_image)
```

Strategies:
- `ChannelComparisonViz`: Side-by-side channel display
- `DensityPlotViz`: Histograms and KDE plots
- `ScatterPlotViz`: Channel relationships with RGB coloring

### Registry Pattern

Color spaces self-register using a decorator:

```python
@ColorSpaceRegistry.register
class MyColorSpace(ColorSpace):
    # ... implementation ...
```

No manual tracking needed - the UI discovers them automatically!

## 🎓 Key Components

### Core Module (`chromagoggles/core/`)

**ColorSpace Base Class**
- Abstract base for all color space implementations
- Defines conversion interface and metadata structure
- Provides default implementations for common operations

**ColorSpaceRegistry**
- Manages registration of color spaces
- Enables automatic discovery
- Supports filtering (e.g., get all with statistics)

**StatisticsCalculator**
- Computes descriptive statistics for channels
- Formats results as markdown tables
- Works with any ColorSpace

### Color Spaces (`chromagoggles/colorspaces/`)

Each file implements a complete color space:
- Metadata (name, display name, description)
- Channel information (ranges, colormaps)
- Conversion from RGB
- Optional: custom behaviors

### Visualizations (`chromagoggles/visualizations/`)

**ChannelComparisonViz**
- Displays channels side-by-side
- Uses metadata-defined colormaps
- Automatic scaling to correct ranges

**DensityPlotViz**
- Creates histograms for each channel
- Adds KDE (Kernel Density Estimation) plots
- Handles edge cases gracefully

**ScatterPlotViz**
- Shows relationships between channels
- Colors points by original RGB values
- Uses density-based alpha for overplotting

**Custom Colormaps**
- LCh hue colormap (perceptually accurate)
- Easily extensible for new colormaps

## 🚀 Extending ChromaGoggles

### Adding a New Color Space

Create a new file in `chromagoggles/colorspaces/`:

```python
from chromagoggles.core.color_space import ColorSpace, ChannelMetadata
from chromagoggles.core.registry import ColorSpaceRegistry
import numpy as np

@ColorSpaceRegistry.register
class MyColorSpace(ColorSpace):
    @property
    def name(self) -> str:
        return "myspace"
    
    @property
    def display_name(self) -> str:
        return "My Color Space"
    
    @property
    def description(self) -> str:
        return "Description of your color space..."
    
    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        return [
            ChannelMetadata(
                name="channel1",
                display_name="Channel 1",
                range_min=0,
                range_max=100,
                colormap="viridis",
                description="First channel"
            ),
            # ... more channels ...
        ]
    
    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        # Your conversion logic here
        pass
```

Then import it in `chromagoggles/colorspaces/__init__.py`:
```python
from chromagoggles.colorspaces.myspace import MyColorSpace
```

That's it! The UI will automatically generate tabs for your color space.

### Adding a New Visualization

Create a strategy class in `chromagoggles/visualizations/`:

```python
from chromagoggles.visualizations.base import VisualizationStrategy
import matplotlib.pyplot as plt

class MyViz(VisualizationStrategy):
    def create(self, colorspace, rgb_image, **kwargs):
        # Create your visualization
        fig, ax = plt.subplots()
        # ... your plotting code ...
        return fig
```

Use it in the TabFactory or anywhere else:
```python
viz = MyViz()
fig = viz.create(colorspace, image)
```

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

### Oklab / Oklch
Modern perceptual spaces designed for robust image manipulation:
- **Oklab**: Cartesian channels `L`, `a`, `b`
- **Oklch**: Cylindrical channels `L`, `C`, `H`

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

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_refactored.py example_gradient.png
```

This tests:
- All color space conversions
- All visualizations
- Statistics calculations
- Error handling

## 📊 Performance

The refactored architecture:
- Maintains same performance as original
- Enables future caching optimizations
- Reduces memory by eliminating duplicate code
- More efficient imports (load only what you need)

## 🔄 Migration from v0.1

The old files are preserved as backups:
- `main_old.py` (original main.py)
- `image_processor.py` (still functional)
- `visualizer.py` (still functional)

New code uses the `chromagoggles` package exclusively.

## Contributing

- **numpy**: Numerical operations on image arrays
- **colour-science**: Oklab and Oklch color encoding conversions
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

