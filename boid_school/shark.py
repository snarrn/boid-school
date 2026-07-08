# Shark
from pygame import Vector2, Surface, draw
import math, random
from .boid import Boid
from .utilities import get_arrow_at_angle

class Shark:
    """Chases boids and eats them."""

    VIEW_RANGE = 200
    EATING_RANGE = 25

    COOLDOWN_START_CHASE = 10
    SOFT_COOLDOWN_START_CHASE = 1
    CHANCE_START_CHASE = 0.2

    COOLDOWN_STOP_CHASE = 10
    SOFT_COOLDOWN_STOP_CHASE = 1
    CHANCE_STOP_CHASE = 0.2

    COOLDOWN_TURN = 1
    SOFT_COOLDOWN_TURN = 0.25
    CHANCE_TURN = 0.05
    SPEED_TURN = 0.4

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

        self._cooldown_start_chase = Shark.COOLDOWN_START_CHASE
        self._target_boid = None

        self._cooldown_stop_chase = Shark.COOLDOWN_STOP_CHASE

        self._turn_left = bool(random.random() <= 0.5)
        self._cooldown_turn = Shark.COOLDOWN_TURN

        self.__ID = Shark._id_counter
        Shark._id_counter += 1

    def set_new_target_boid(self):
        """Finds a random boid within range, if any, and sets it as the target boid."""
        self._target_boid = None
        near_boids = self.controller.get_boids_by_pos(pos=self.pos, max_dist=Shark.VIEW_RANGE)
        if len(near_boids) > 0:
            self._target_boid = random.choice(near_boids[:3])
            self._cooldown_turn = Shark.COOLDOWN_TURN
        
        self._cooldown_start_chase = self.COOLDOWN_START_CHASE

    def update_hunger(self, dt: float = 0):
        """Updates the shark's hunger and boid targeting."""
        if self._target_boid is None:
            self._cooldown_start_chase -= dt

            if self._cooldown_start_chase <= 0:
                if random.random() <= Shark.CHANCE_START_CHASE:
                    self.set_new_target_boid()
                    
                else:
                    self._cooldown_start_chase = Shark.SOFT_COOLDOWN_START_CHASE
        
        else:
            if self._target_boid.was_eaten:
                self.set_new_target_boid()

            elif math.dist(self.pos, self._target_boid.pos) <= Shark.EATING_RANGE:
                self._target_boid.was_eaten = True
                self.controller.remove_boid_by_ID(self._target_boid.ID)
                self._target_boid = None

    def update_angle(self, dt: float = 0):
        """Updates the shark's angle and turning."""

        # Ambient Behavior
        if self._target_boid is None:
            self._cooldown_turn -= dt

            if self._cooldown_turn <= 0:
                if random.random() <= Shark.CHANCE_TURN:
                    self._turn_left = not self._turn_left
                    self._cooldown_turn = Shark.COOLDOWN_TURN

                else:
                    self._cooldown_turn = Shark.SOFT_COOLDOWN_TURN
            
            self.angle += Shark.SPEED_TURN * dt * (1 if self._turn_left else -1)
        
        # Chasing Behavior
        else:
            self._cooldown_stop_chase -= dt

            if self._cooldown_stop_chase <= 0:
                if random.random() <= Shark.CHANCE_STOP_CHASE:
                    self._target_boid = None
                    self._cooldown_stop_chase = Shark.COOLDOWN_STOP_CHASE
                
                else:
                    self._cooldown_stop_chase = Shark.SOFT_COOLDOWN_STOP_CHASE
            
            else:
                self.angle = math.atan2(self._target_boid.pos.y - self.pos.y, self._target_boid.pos.x - self.pos.x)

    def update_position(self, dt: float = 0):
        """Updates the shark's position."""
        self.pos.x += math.cos(self.angle) * Shark.SPEED * dt
        self.pos.y += math.sin(self.angle) * Shark.SPEED * dt

    def update(self, dt: float = 0):
        """Updates hunger, angle, and position."""
        self.update_hunger(dt)
        self.update_angle(dt)
        self.update_position(dt)

    def draw(self, surface: Surface, draw_target_boid: bool = False):
        """Draws the shark to the surface."""
        arrow_points = get_arrow_at_angle(self.angle)
        arrow_points = tuple((point[0] * Shark.SIZE + self.pos.x, point[1] * Shark.SIZE + self.pos.y) for point in arrow_points)
        draw.polygon(surface, color=Shark.COLOR, points=arrow_points)

        if draw_target_boid and isinstance(self._target_boid, Boid):
            draw.polygon(surface, color=Shark.COLOR_OUTLINE, points=arrow_points, width=2)
            self._target_boid.draw(surface, draw_outline=True)
