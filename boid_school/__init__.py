"""
Boid School

A boid herding game built around Pygame.
"""

from .utilities import *
from .boid import Boid
from .boid_controller import BoidController
from .player import Player

__all__ = ["utilities",
           "Boid",
           "BoidController",
           "Player",
           "__version__"]

__version__ = "0.1"