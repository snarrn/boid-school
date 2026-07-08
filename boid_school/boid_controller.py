# Boid Controller
from pygame import Rect, Vector2, Surface
from typing import Sequence
import random, math
from .boid import Boid
from .shark import Shark
from .player import Player

class BoidController:
    def __init__(self, num_init_boids: int = 50, num_init_sharks: int = 0, spawn_range: Rect = Rect(0,0,100,100)):
        """Manages and updates boids."""
        self._boids: Sequence[Boid] = []
        for _ in range(num_init_boids):
            x, y = random.randint(spawn_range.left, spawn_range.right), random.randint(spawn_range.top, spawn_range.bottom)
            self._boids.append(Boid(Vector2(x, y), random.random() * 2 * math.pi))
        
        self._sharks: Sequence[Shark] = []
        for _ in range(num_init_sharks):
            x, y = random.randint(spawn_range.left, spawn_range.right), random.randint(spawn_range.top, spawn_range.bottom)
            self._sharks.append(Shark(Vector2(x, y), random.random() * 2 * math.pi, controller=self))
        
        self.spawn_range = spawn_range

    def add_boid(self, position: Vector2 | None = None, angle: float | None = None) -> int:
        """Adds a boid to the controller and returns its ID. A random position and angle are assigned if none are given."""

        position = position or Vector2(random.randint(self.spawn_range.left, self.spawn_range.right), random.randint(self.spawn_range.top, self.spawn_range.bottom))
        angle = angle if isinstance(angle, (float, int)) else random.random() * 2 * math.pi
        
        boid = Boid(position, angle)
        self._boids.append(boid)

        return boid.ID

    def add_boids(self, count: int = 1, positions: Sequence[Vector2] | Vector2 | None = None, angles: Sequence[float] | float | None = None) -> Sequence[int]:
        """Adds boids to the controller and returns their IDs. Random positions and angles are assigned if none are given or if their lengths are less than 'count'. If more positions or angles are given than 'count', then the extras are ignored. If a single position or angle is given not in a sequence, then it will be applied to every boid."""
        
        IDs = []

        if isinstance(positions, Vector2):
            positions = tuple(positions.copy() for _ in range(count))
        else:
            positions = positions or []
        
        if isinstance(angles, (float, int)):
            angles = tuple(angles for _ in range(count))
        else:
            angles = angles or []

        for i in range(count):
            pos = positions[i] if i < len(positions) else None
            ang = angles[i] if i < len(angles) else None
            IDs.append(self.add_boid(pos, ang))

        return IDs

    def remove_boid_by_ID(self, ID: int | None = None) -> Boid | None:
        """Removes and returns a boid from the controller given a boid ID. Returns None if no boid has that ID."""
        if len(self._boids) == 0:
            return None
        
        for boid in self._boids:
            if boid.ID == ID:
                self._boids.remove(boid)
                return boid
        
        return None

    def remove_boid_by_pos(self, pos: Vector2, max_dist: float | None = None) -> Boid | None:
        """Removes a boid with the given position. If 'max_dist' is given, removes the closest boid to 'pos' if there are any within that range."""
        if len(self._boids) == 0:
            return None
        
        if max_dist is None or max_dist == 0:
            for boid in self._boids:
                if boid.pos == pos:
                    self._boids.remove(boid)
                    return boid
        
        else:
            nearest_boid = sorted(self._boids, key=lambda x: ((x.pos.x - pos.x)**2 + (x.pos.y - pos.y)**2))[0]
            if math.dist(nearest_boid.pos, pos) <= max_dist:
                self._boids.remove(nearest_boid)
                return nearest_boid
        
        return None

    def get_random_boid(self) -> Boid | None:
        """Returns a random boid or None if there are no boids."""
        return random.choice(self._boids)

    def update(self, dt: float = 0, player: Player | None = None):
        """Updates all boids and sharks."""

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
        
        # Update Sharks
        for shark in self._sharks:
            shark.update(dt)

    def draw(self, surface: Surface, do_debug_view: bool = False):
        """Draws boids and sharks to the surface."""
        for boid in self._boids:
            boid.draw(surface, do_debug_view)

        for shark in self._sharks:
            shark.draw(surface, do_debug_view)