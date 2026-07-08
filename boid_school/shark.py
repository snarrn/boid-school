# Shark
from pygame import Vector2, Surface, draw
import math
from .boid import Boid
from .utilities import get_arrow_at_angle

class Shark:
    """Chases boids and eats them."""

    MIN_VIEW_RANGE = 80
    MAX_VIEW_RANGE = 200

    TIME_BETWEEN_MEALS = 5

    SPEED = 40
    SIZE = 24
    COLOR = (100, 100, 100)
    COLOR_OUTLINE = "red"

    _id_counter = 0

    @property
    def ID(self):
        return self.__ID

    def __repr__(self):
        return f"<Shark #{self.ID}"

    def __init__(self, pos: Vector2, angle: float, controller = None):
        self.pos = pos
        self.angle = angle
        self.controller = controller

        self._time_since_last_meal = 0
        self._target_boid = None

        self.__ID = Shark._id_counter
        Shark._id_counter += 1

    def update_angle(self, dt: float = 0):
        """Updates the shark's angle."""
        if isinstance(self._target_boid, Boid):
            self.angle = math.atan2(self._target_boid.pos.y - self.pos.y,
                                    self._target_boid.pos.x - self.pos.x)

    def update_position(self, dt: float = 0):
        """Updates the shark's position."""
        self.pos.x += math.cos(self.angle) * Shark.SPEED * dt
        self.pos.y += math.sin(self.angle) * Shark.SPEED * dt

    def update(self, dt: float = 0):
        """Updates angle, position, and hunger."""
        self.update_angle(dt)
        self.update_position(dt)

        self._time_since_last_meal += dt
        if not isinstance(self._target_boid, Boid) and self._time_since_last_meal >= Shark.TIME_BETWEEN_MEALS:
            self._target_boid = self.controller.get_random_boid()

    def draw(self, surface: Surface, draw_target_boid: bool = False):
        """Draws the shark to the surface."""
        arrow_points = get_arrow_at_angle(self.angle)
        arrow_points = tuple((point[0] * Shark.SIZE + self.pos.x, point[1] * Shark.SIZE + self.pos.y) for point in arrow_points)
        draw.polygon(surface, color=Shark.COLOR, points=arrow_points)

        if draw_target_boid and isinstance(self._target_boid, Boid):
            draw.polygon(surface, color=Shark.COLOR_OUTLINE, points=arrow_points, width=2)
            self._target_boid.draw(surface, draw_outline=True)
