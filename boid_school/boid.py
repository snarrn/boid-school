# Boid
from pygame import Vector2, Surface, draw
from typing import Sequence
import math

class Boid:
    """Boid that behaves based on alignment, cohesion, and separation."""

    CURRENT_ANGLE_WEIGHT = 7
    ALIGNMENT_WEIGHT = 1
    COHESION_WEIGHT = 1
    SEPARATION_WEIGHT = 1
    SPEED = 25
    SIZE = 18
    COLOR = "blue"

    _id_counter = 0

    @property
    def ID(self):
        return self.__ID

    def __init__(self, pos: Vector2, angle: float):
        self.pos = pos
        self.angle = angle

        self.__target_angle = self.angle
        self.__target_alignment_angle = self.angle
        self.__target_cohesion_angle = self.angle
        self.__target_separation_angle = self.angle

        self.__ID = Boid._id_counter
        Boid._id_counter += 1

    @staticmethod
    def get_arrow_at_angle(angle):
        return ((math.cos(angle)/2,math.sin(angle)/2),\
            (math.cos(angle+2.55)*.6,math.sin(angle+2.55)*.6),\
            (math.cos(angle-2.55)*.6,math.sin(angle-2.55)*.6))

    @staticmethod
    def get_avg_vector_angle(vectors: Sequence[Vector2], weights: Sequence[float] | None = None, normalise_vectors: bool = True):
        """Returns the [weighted] average angle of the vectors."""
        # Type Checking
        if not isinstance(vectors, (tuple, list)):
            raise TypeError(f"'vectors' must be a tuple or list, not {type(vectors)}")
        if len(vectors) <= 0:
            raise ValueError(f"'vectors' cannnot be an empty sequence.")
        if weights is not None and len(weights) != len(vectors):
            raise ValueError(f"'weights' must be the same length as 'vectors' ({len(weights)} != {len(vectors)})")

        # Normalising Vectors
        if normalise_vectors:
            vectors = tuple((vector.normalize() if vector.magnitude != 0 else vector) for vector in vectors)
        
        # Average Calculation
        total_vector = Vector2()
        if weights is None:

            for vector in vectors:
                total_vector += vector
        
        else:
            for vector, weight in zip(vectors, weights):
                total_vector += vector * weight
        
        return math.atan2(total_vector.y, total_vector.x)

    @staticmethod
    def get_avg_angle(angles: Sequence[float], weights: Sequence[float] | None = None):
        """Returns the [weighted] average angle."""
        vectors = tuple((Vector2(math.cos(angle), math.sin(angle))) for angle in angles)
        return Boid.get_avg_vector_angle(vectors, weights=weights, normalise_vectors=False)

    def get_alignment_angle(self):
        """Records and returns the alignments angle."""
        pass

    def get_cohesion_angle(self):
        """Records and returns the cohesion angle."""
        pass
    
    def get_separation_angle(self):
        """Records and returns the separation angle."""
        pass

    def update_angle(self, dt: float = 0):
        """Moves the boid's angle."""
        self.__target_angle = Boid.get_avg_angle((self.__target_alignment_angle, self.__target_cohesion_angle, self.__target_separation_angle),
                                         weights=(Boid.ALIGNMENT_WEIGHT, Boid.COHESION_WEIGHT, Boid.SEPARATION_WEIGHT))

        self.angle = Boid.get_avg_angle((self.angle, self.__target_angle), weights=(Boid.CURRENT_ANGLE_WEIGHT, 1))

    def update_position(self, dt: float = 0):
        """Moves the boid's position."""
        self.pos.x += math.cos(self.angle) * Boid.SPEED * dt
        self.pos.y += math.sin(self.angle) * Boid.SPEED * dt

    def update(self, dt: float = 0):
        """Updates the angle and position."""
        self.update_angle(dt)
        self.update_position(dt)

    def draw(self, surface: Surface, draw_target_vectors: bool = False):
        """Draws the boid to the surface."""
        arrow_points = Boid.get_arrow_at_angle(self.angle)
        arrow_points = tuple((point[0] * Boid.SIZE + self.pos.x, point[1] * Boid.SIZE + self.pos.y) for point in arrow_points)
        draw.polygon(surface, color=Boid.COLOR, points=arrow_points)

        if draw_target_vectors == True:
            draw.line(surface, "red", self.pos, (self.pos.x + Boid.SIZE * math.cos(self.__target_alignment_angle), self.pos.y + Boid.SIZE * math.sin(self.__target_alignment_angle)))
            draw.line(surface, "green", self.pos, (self.pos.x + Boid.SIZE * math.cos(self.__target_cohesion_angle), self.pos.y + Boid.SIZE * math.sin(self.__target_alignment_angle)))
            draw.line(surface, "yellow", self.pos, (self.pos.x + Boid.SIZE * math.cos(self.__target_separation_angle), self.pos.y + Boid.SIZE * math.sin(self.__target_alignment_angle)))
