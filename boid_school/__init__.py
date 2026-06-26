"""
Boid School

A boid herding game built around Pygame.
"""

from .boid import Boid
from .boid_controller import BoidController

__all__ = ["Boid",
           "BoidController",
           "__version__"]

__version__ = "0.1"