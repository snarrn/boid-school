# Boid
from pygame import Vector2, Surface, draw
from typing import Sequence
import math
from .utilities import get_avg_angle, get_arrow_at_angle
from .player import Player

class Boid:
    """Boid that behaves based on alignment, cohesion, and separation."""

    CURRENT_ANGLE_WEIGHT = 40
    ALIGNMENT_WEIGHT = 2
    COHESION_WEIGHT = 4
    SEPARATION_WEIGHT = 5

    PROXIMAL_RANGE = 40
    PLAYER_INFLUENCE_RANGE = 100
    MIN_COHESION_RANGE = 15
    SEPARATION_DISTANCE = 30

    SPEED = 50
    SIZE = 18
    COLOR = "blue"

    _id_counter = 0

    @property
    def ID(self):
        return self.__ID

    def __repr__(self):
        return f"<Boid #{self.ID}>"

    def __init__(self, pos: Vector2, angle: float):
        self.pos = pos
        self.angle = angle

        self.__target_angle = self.angle
        self.__target_alignment_angle = self.angle
        self.__target_cohesion_angle = self.angle
        self.__target_separation_angle = self.angle

        self.proximal_boids: Sequence[Boid] = tuple()

        self.__ID = Boid._id_counter
        Boid._id_counter += 1

    def clear_proximal_boids(self):
        """Clears the list of proximal boids."""
        self.proximal_boids = []

    def get_alignment_angle(self, player: Player | None = None):
        """Calculates and records the alignments angle, which is the average angle of proximal boids."""
        if len(self.proximal_boids) == 0:
            if player is not None:
                if math.dist(self.pos, player.pos) <= Boid.PLAYER_INFLUENCE_RANGE:
                    return player.angle
        
        else:
            proximal_boid_angles = list((boid.angle) for boid in self.proximal_boids)

            if player is not None and math.dist(self.pos, player.pos) <= Boid.PLAYER_INFLUENCE_RANGE:
                proximal_boid_angles.append(player.angle)

            return get_avg_angle(proximal_boid_angles)

        return self.angle

    def get_cohesion_angle(self, player: Player | None = None):
        """Calculates and records the cohesion angle."""
        if len(self.proximal_boids) == 0:
            if player is not None:
                displacement = player.pos - self.pos

                if Boid.MIN_COHESION_RANGE <= displacement.magnitude() <= Boid.PLAYER_INFLUENCE_RANGE:
                    return math.atan2(displacement.y, displacement.x)

        else:
            total_x = sum((boid.pos.x) for boid in self.proximal_boids)
            total_y = sum((boid.pos.y) for boid in self.proximal_boids)

            if player is not None and (player.pos - self.pos).magnitude() <= Boid.PLAYER_INFLUENCE_RANGE:
                avg_x = (total_x + player.pos.x) / (len(self.proximal_boids) + 1)
                avg_y = (total_y + player.pos.y) / (len(self.proximal_boids) + 1)
            
            else:
                avg_x = total_x / len(self.proximal_boids)
                avg_y = total_y / len(self.proximal_boids)

            displacement = Vector2(avg_x, avg_y) - self.pos

            if displacement.magnitude() >= Boid.MIN_COHESION_RANGE:
                return math.atan2(displacement.y, displacement.x)

        return self.angle
        
    def get_separation_angle(self, player: Player | None = None):
        """Calculates and records the separation angle."""
        displacement = Vector2()

        if len(self.proximal_boids) == 0:
            if player is not None:
                displacement = self.pos - player.pos
                if 0 < displacement.magnitude() <= Boid.PLAYER_INFLUENCE_RANGE:
                    return math.atan2(displacement.y, displacement.x)
        
        else:
            min_squared_dist = float("inf")
            closest_boid = None

            for boid in self.proximal_boids:
                squared_dist = (boid.pos.x - self.pos.x)**2 + (boid.pos.y - self.pos.y)**2

                if squared_dist < Boid.SEPARATION_DISTANCE**2 and squared_dist < min_squared_dist:
                    min_squared_dist = squared_dist
                    closest_boid = boid

            if closest_boid is not None:
                displacement = self.pos - closest_boid.pos

            if player is not None:
                player_displacement = self.pos - player.pos
                if player_displacement.magnitude() < displacement.magnitude():
                    displacement = player_displacement
            
            if displacement.magnitude() > 0:
                return math.atan2(displacement.y, displacement.x)
            
        return self.angle

    def update_angle(self, dt: float = 0, player: Player | None = None):
        """Calculates and set the the boid's new angle."""
        self.__target_alignment_angle = self.get_alignment_angle(player)
        self.__target_cohesion_angle = self.get_cohesion_angle(player)
        self.__target_separation_angle = self.get_separation_angle(player)

        self.__target_angle = get_avg_angle((self.__target_alignment_angle, self.__target_cohesion_angle, self.__target_separation_angle),
                                         weights=(Boid.ALIGNMENT_WEIGHT, Boid.COHESION_WEIGHT, Boid.SEPARATION_WEIGHT))

        self.angle = get_avg_angle((self.angle, self.__target_angle), weights=(Boid.CURRENT_ANGLE_WEIGHT, 1))

    def update_position(self, dt: float = 0):
        """Moves the boid's position."""
        self.pos.x += math.cos(self.angle) * Boid.SPEED * dt
        self.pos.y += math.sin(self.angle) * Boid.SPEED * dt

    def update(self, dt: float = 0, player: Player | None = None):
        """Updates the angle and position."""
        self.update_angle(dt, player)
        self.update_position(dt)

    def draw(self, surface: Surface, draw_target_vectors: bool = False):
        """Draws the boid to the surface."""
        arrow_points = get_arrow_at_angle(self.angle)
        arrow_points = tuple((point[0] * Boid.SIZE + self.pos.x, point[1] * Boid.SIZE + self.pos.y) for point in arrow_points)
        draw.polygon(surface, color=Boid.COLOR, points=arrow_points)

        if draw_target_vectors == True:
            draw.line(surface, "red", self.pos, (self.pos.x + Boid.SIZE * math.cos(self.__target_alignment_angle), self.pos.y + Boid.SIZE * math.sin(self.__target_alignment_angle)))
            draw.line(surface, "green", self.pos, (self.pos.x + Boid.SIZE * math.cos(self.__target_cohesion_angle), self.pos.y + Boid.SIZE * math.sin(self.__target_cohesion_angle)))
            draw.line(surface, "yellow", self.pos, (self.pos.x + Boid.SIZE * math.cos(self.__target_separation_angle), self.pos.y + Boid.SIZE * math.sin(self.__target_separation_angle)))

            draw.circle(surface, (0,0,0), self.pos, Boid.PROXIMAL_RANGE, width=1)
