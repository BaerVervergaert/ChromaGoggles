# Developer Guide - ChromaGoggles

This guide explains how to work with the refactored ChromaGoggles architecture.

## 📚 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Adding a New Color Space](#adding-a-new-color-space)
3. [Adding a New Visualization](#adding-a-new-visualization)
4. [Modifying the UI](#modifying-the-ui)
5. [Testing](#testing)
6. [Best Practices](#best-practices)

---

## Architecture Overview

### Core Concepts

**ColorSpace**: Abstract base class that defines a color space
- Metadata (name, description)
- Channel information (names, ranges, colormaps)
- Conversion from RGB
- Support flags (statistics, scatter plots)

**Registry**: Central registry that tracks all ColorSpace implementations
- Color spaces self-register via decorator
- Supports querying and filtering

**Visualization Strategies**: Reusable visualization patterns
- Work with any ColorSpace
- Metadata-driven rendering
- Consistent styling

**TabFactory**: Dynamic UI generator
- Creates Streamlit tabs from registered ColorSpaces
- No hardcoding needed

### Data Flow

```
User uploads image
    ↓
PIL Image → NumPy array (RGB)
    ↓
ColorSpace.convert_from_rgb() → Converted image
    ↓
ColorSpace.get_channels() → Individual channels
    ↓
VisualizationStrategy.create() → Matplotlib figure
    ↓
Streamlit displays figure
```

---

## Adding a New Color Space

### Step 1: Create the File

Create `chromagoggles/colorspaces/your_space.py`:

```python
"""
Your color space implementation.
"""
import numpy as np
from chromagoggles.core.color_space import ColorSpace, ChannelMetadata
from chromagoggles.core.registry import ColorSpaceRegistry


@ColorSpaceRegistry.register
class YourColorSpace(ColorSpace):
    """
    Brief description of your color space.
    
    More detailed explanation...
    """
    
    @property
    def name(self) -> str:
        """Internal name (lowercase, no spaces)."""
        return "yourspace"
    
    @property
    def display_name(self) -> str:
        """Human-readable name for UI."""
        return "Your Color Space"
    
    @property
    def description(self) -> str:
        """Markdown description shown in UI."""
        return (
            "**Your Color Space** description here. "
            "Explain what each channel represents."
        )
    
    @property
    def channels_metadata(self) -> list[ChannelMetadata]:
        """Define each channel."""
        return [
            ChannelMetadata(
                name="channel1",  # Internal name
                display_name="Channel 1",  # UI display
                range_min=0,  # Minimum value
                range_max=100,  # Maximum value
                colormap="viridis",  # Matplotlib colormap
                description="What this channel represents"
            ),
            # Add more channels...
        ]
    
    def convert_from_rgb(self, rgb_image: np.ndarray) -> np.ndarray:
        """
        Convert RGB image to this color space.
        
        Args:
            rgb_image: NumPy array with shape (height, width, 3)
                      Values are uint8 in range [0, 255]
        
        Returns:
            Converted image with shape (height, width, n_channels)
        """
        # Your conversion logic here
        # Example using opencv:
        # import cv2
        # return cv2.cvtColor(rgb_image, cv2.COLOR_RGB2...)
        
        # Or using scikit-image:
        # from skimage import color
        # rgb_normalized = rgb_image / 255.0
        # return color.rgb2....(rgb_normalized)
        
        pass
    
    def supports_statistics_tab(self) -> bool:
        """Override to False if statistics don't make sense."""
        return True
    
    def supports_scatter_plots(self) -> bool:
        """Override to False if scatter plots aren't meaningful."""
        return True
```

### Step 2: Register in __init__.py

Add to `chromagoggles/colorspaces/__init__.py`:

```python
from chromagoggles.colorspaces.your_space import YourColorSpace

__all__ = [
    # ... existing ...
    "YourColorSpace",
]
```

### Step 3: Test

```python
from chromagoggles.colorspaces import YourColorSpace
import numpy as np

# Create test image
test_img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

# Test conversion
cs = YourColorSpace()
converted = cs.convert_from_rgb(test_img)
print(f"Converted shape: {converted.shape}")

# Test channels
channels = cs.get_channels(test_img)
print(f"Channels: {len(channels)}")
```

That's it! Your color space will now appear in the UI automatically.

---

## Adding a New Visualization

### Step 1: Create Strategy Class

Create `chromagoggles/visualizations/my_viz.py`:

```python
"""
My custom visualization strategy.
"""
import numpy as np
import matplotlib.pyplot as plt
from chromagoggles.visualizations.base import VisualizationStrategy
from chromagoggles.core.color_space import ColorSpace


class MyViz(VisualizationStrategy):
    """
    Description of what this visualization shows.
    """
    
    def create(
        self,
        colorspace: ColorSpace,
        rgb_image: np.ndarray,
        **kwargs
    ) -> plt.Figure:
        """
        Create the visualization.
        
        Args:
            colorspace: ColorSpace instance
            rgb_image: Original RGB image
            **kwargs: Additional parameters
        
        Returns:
            Matplotlib figure
        """
        # Get data from colorspace
        channels = colorspace.get_channels(rgb_image)
        metadata = colorspace.channels_metadata
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Your plotting code here
        # ...
        
        plt.tight_layout()
        return fig
```

### Step 2: Use in TabFactory or Elsewhere

```python
from chromagoggles.visualizations.my_viz import MyViz

viz = MyViz()
fig = viz.create(colorspace, rgb_image)
st.pyplot(fig)
plt.close(fig)
```

### Tips for Visualizations

- Always use `plt.tight_layout()` before returning
- Use metadata for colormaps and ranges: `meta.colormap`, `meta.range_min`
- Close figures after displaying: `plt.close(fig)`
- Handle edge cases (single channel, etc.)

---

## Modifying the UI

### Adding a Tab Section

Edit `chromagoggles/ui/tab_factory.py`:

```python
@staticmethod
def _create_statistics_tab(colorspace, rgb_image):
    st.header(f"{colorspace.display_name} Statistics")
    
    # Existing sections...
    
    # Add your new section
    st.subheader("My New Section")
    viz = MyViz()
    fig = viz.create(colorspace, rgb_image)
    st.pyplot(fig)
    plt.close(fig)
```

### Adding a Global Tab

Modify `TabFactory.create_all_tabs()` to add tabs that aren't color-space-specific:

```python
@staticmethod
def create_all_tabs(rgb_image):
    # Existing color space tabs
    colorspaces_with_stats = ColorSpaceRegistry.get_with_statistics()
    
    tab_names = [...]  # Existing tabs
    tab_names.append("My Global Tab")  # Add yours
    
    tabs = st.tabs(tab_names)
    
    # ... existing tab population ...
    
    # Your global tab
    with tabs[-1]:
        st.header("My Global Analysis")
        # Your content here
```

---

## Testing

### Unit Tests

Test individual components:

```python
# test_colorspaces.py
def test_rgb_conversion():
    from chromagoggles.colorspaces import RGBColorSpace
    import numpy as np
    
    cs = RGBColorSpace()
    test_img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    
    converted = cs.convert_from_rgb(test_img)
    assert converted.shape == test_img.shape
    assert np.array_equal(converted, test_img)  # RGB is identity
```

### Integration Tests

Test full workflow:

```python
# test_integration.py
def test_full_workflow():
    from chromagoggles.core.registry import ColorSpaceRegistry
    from chromagoggles.visualizations import ChannelComparisonViz
    import chromagoggles.colorspaces
    import numpy as np
    
    # Create test image
    img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    
    # Test each color space
    for cs in ColorSpaceRegistry.get_all():
        viz = ChannelComparisonViz()
        fig = viz.create(cs, img)
        assert fig is not None
```

### Visual Tests

Use `test_refactored.py` for visual verification:

```bash
python test_refactored.py example_gradient.png
```

---

## Best Practices

### ColorSpace Implementation

1. **Validate inputs**: Check shape and dtype of rgb_image
2. **Handle edge cases**: NaN values, invalid ranges
3. **Use established libraries**: OpenCV, scikit-image for conversions
4. **Document ranges**: Be explicit about min/max values
5. **Choose appropriate colormaps**: Match the channel's meaning

### Visualization Strategies

1. **Be generic**: Work with any ColorSpace
2. **Use metadata**: Don't hardcode ranges or colormaps
3. **Sample large images**: Use every Nth pixel for scatter plots
4. **Close figures**: Always close after displaying
5. **Handle errors gracefully**: Wrap risky operations in try-except

### UI Components

1. **Keep TabFactory simple**: Complex logic belongs elsewhere
2. **Use markdown**: For rich descriptions and formatting
3. **Add loading indicators**: For slow operations
4. **Provide context**: Explain what users are seeing

### Code Organization

1. **One class per file**: Except very small utilities
2. **Import at module level**: Not inside functions
3. **Use type hints**: For all public APIs
4. **Document everything**: Classes, methods, parameters
5. **Follow existing patterns**: Consistency matters

---

## Common Patterns

### Getting Color Space Data

```python
from chromagoggles.core.registry import ColorSpaceRegistry

# Get by name
rgb = ColorSpaceRegistry.get("rgb")

# Get all
all_cs = ColorSpaceRegistry.get_all()

# Get with statistics
stats_cs = ColorSpaceRegistry.get_with_statistics()
```

### Working with Channels

```python
# Get individual channels
channels = colorspace.get_channels(rgb_image)

# Get full converted image
converted = colorspace.convert_from_rgb(rgb_image)

# Access metadata
for channel, meta in zip(channels, colorspace.channels_metadata):
    print(f"{meta.display_name}: range {meta.range_min}-{meta.range_max}")
```

### Creating Visualizations

```python
from chromagoggles.visualizations import ChannelComparisonViz
import matplotlib.pyplot as plt

viz = ChannelComparisonViz()
fig = viz.create(colorspace, rgb_image)

# Display in Streamlit
import streamlit as st
st.pyplot(fig)
plt.close(fig)

# Or save to file
fig.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close(fig)
```

---

## Troubleshooting

### ColorSpace not appearing in UI

- Check that `@ColorSpaceRegistry.register` decorator is present
- Verify import in `chromagoggles/colorspaces/__init__.py`
- Ensure no syntax errors in the file

### Visualization not working

- Check that `create()` returns a matplotlib Figure
- Verify that `plt.tight_layout()` is called
- Ensure metadata ranges are correct

### ImportError

- Check for circular imports
- Verify all dependencies are installed
- Make sure you're in the right directory

---

## Resources

### Key Files to Reference

- `chromagoggles/core/color_space.py` - ColorSpace base class
- `chromagoggles/colorspaces/rgb.py` - Simplest example
- `chromagoggles/colorspaces/hcl.py` - Complex example with custom colormap
- `chromagoggles/visualizations/scatter.py` - Advanced visualization

### External Resources

- [Matplotlib Colormaps](https://matplotlib.org/stable/tutorials/colors/colormaps.html)
- [scikit-image Color Conversions](https://scikit-image.org/docs/stable/api/skimage.color.html)
- [OpenCV Color Conversions](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## Questions?

Check the main codebase for examples, or open an issue on GitHub.

Happy coding! 🎨

