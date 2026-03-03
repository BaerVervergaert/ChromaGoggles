"""
Registry for color space implementations.
"""
from typing import Dict, Type, List, Optional
from artanalyzer.core.color_space import ColorSpace
class ColorSpaceRegistry:
    """
    Central registry for all color space implementations.
    Color spaces register themselves using the @ColorSpaceRegistry.register
    decorator. This enables automatic discovery and dynamic UI generation.
    Example:
        @ColorSpaceRegistry.register
        class RGBColorSpace(ColorSpace):
            # ... implementation ...
    """
    _colorspaces: Dict[str, Type[ColorSpace]] = {}
    _order: List[str] = []  # Track registration order
    @classmethod
    def register(cls, colorspace_class: Type[ColorSpace]) -> Type[ColorSpace]:
        """
        Register a color space class.
        Args:
            colorspace_class: The ColorSpace subclass to register
        Returns:
            The same class (for use as decorator)
        """
        # Create instance to get name
        instance = colorspace_class()
        name = instance.name
        if name in cls._colorspaces:
            print(f"Warning: ColorSpace '{name}' already registered. Overwriting.")
        cls._colorspaces[name] = colorspace_class
        if name not in cls._order:
            cls._order.append(name)
        return colorspace_class
    @classmethod
    def get(cls, name: str) -> Optional[ColorSpace]:
        """
        Get color space instance by name.
        Args:
            name: Internal name of the color space
        Returns:
            ColorSpace instance or None if not found
        """
        colorspace_class = cls._colorspaces.get(name)
        if colorspace_class:
            return colorspace_class()
        return None
    @classmethod
    def get_all(cls) -> List[ColorSpace]:
        """
        Get all registered color spaces in registration order.
        Returns:
            List of ColorSpace instances
        """
        return [cls._colorspaces[name]() for name in cls._order if name in cls._colorspaces]
    @classmethod
    def get_with_statistics(cls) -> List[ColorSpace]:
        """
        Get color spaces that support statistics tabs.
        Returns:
            List of ColorSpace instances that have statistics enabled
        """
        return [cs for cs in cls.get_all() if cs.supports_statistics_tab()]
    @classmethod
    def get_names(cls) -> List[str]:
        """
        Get all registered color space names.
        Returns:
            List of color space names
        """
        return cls._order.copy()
    @classmethod
    def clear(cls):
        """Clear all registrations (useful for testing)."""
        cls._colorspaces.clear()
        cls._order.clear()
