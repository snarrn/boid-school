# Boid Controller
from pygame import Rect, Vector2, Surface
from typing import Sequence
import random, math
from .boid import Boid
from .player import Player

class BoidController:
    def __init__(self, num_init_boids: int = 50, spawn_range: Rect = Rect(0,0,100,100)):
        """Manages and updates boids."""
        self._boids: Sequence[Boid] = []
        for _ in range(num_init_boids):
            x, y = random.randint(spawn_range.left, spawn_range.right), random.randint(spawn_range.top, spawn_range.bottom)
            self._boids.append(Boid(Vector2(x, y), random.random() * 2 * math.pi))
        
        self.spawn_range = spawn_range

    def update(self, dt: float = 0, player: Player | None = None):
        """Updates all boid positions and angles."""

        # Determining Proximal Boids
        for boid in self._boids:
            boid.proximal_boids = []
        
        for i in range(len(self._boids)-1):
            boid_1 = self._boids[i]

            for j in range(i+1, len(self._boids)):
                boid_2 = self._boids[j]

                square_dist = (boid_2.pos.x - boid_1.pos.x)**2 + (boid_2.pos.y - boid_1.pos.y)**2

                if square_dist <= Boid.PROXIMAL_RANGE**2:
                    boid_1.proximal_boids.append(boid_2)
                    boid_2.proximal_boids.append(boid_1)

        # Update Boid Positions and Angles
        for boid in self._boids:
            boid.update(dt, player)

    def draw(self, surface: Surface, do_debug_view: bool = False):
        """Draws boids to the surface."""
        for boid in self._boids:
            boid.draw(surface, do_debug_view)
