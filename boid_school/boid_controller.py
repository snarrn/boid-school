# Boid Controller
from pygame import Rect, Vector2, Surface
from typing import Sequence
import random, math
from .boid import Boid

class BoidController:
    def __init__(self, num_init_boids: int = 50, spawn_range: Rect = Rect(0,0,100,100)):
        """Manages and updates boids."""
        self._boids: Sequence[Boid] = []
        for _ in range(num_init_boids):
            x, y = random.randint(spawn_range.left, spawn_range.right), random.randint(spawn_range.top, spawn_range.bottom)
            self._boids.append(Boid(Vector2(x, y), random.random() * 2 * math.pi))
        
        self.spawn_range = spawn_range

    def update(self, dt: float = 0):
        """Updates all boid positions and angles."""
        for boid in self._boids:
            boid.update(dt)

    def draw(self, surface: Surface, do_debug_view: bool = False):
        """Draws boids to the surface."""
        for boid in self._boids:
            boid.draw(surface, do_debug_view)
