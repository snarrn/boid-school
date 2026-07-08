# Player
from pygame import Vector2, Surface, draw
from .utilities import get_avg_angle, get_arrow_at_angle
import math

class Player:
    """The avatar a player controls. Stores information such as health and dash stamina."""

    SPEED_NORMAL = 75
    SPEED_DASH = 150
    DASH_DURATION = 1
    DASH_COOLDOWN = 5
    SLOW_SPEED_RANGE = 80

    CURRENT_ANGLE_WEIGHT = 15

    SIZE = 30
    COLOR_NORMAL = "purple"
    COLOR_DASHING = "magenta"

    def __init__(self, pos: Vector2, angle: float = 0):
        self.pos = pos
        self.angle = angle

        self.speed = Player.SPEED_NORMAL

        self._dash_time_remaining = None
        self._dash_cooldown_remaining = None
        self._is_dashing = False
    
    def dash(self) -> bool:
        """Dashes the player if not in dash cooldown. Returns whether the dash occurred."""
        if self._dash_cooldown_remaining is None:
            self._dash_time_remaining = Player.DASH_DURATION
            self.speed = Player.SPEED_DASH
            self._is_dashing = True
            return True
        
        return False

    def __manage_dash_times(self, dt: float = 0):
        """Subtracts from dash time or dash cooldown times."""
        if self._dash_time_remaining is not None:
            if self._dash_time_remaining <= 0:
                self._dash_time_remaining = None
                self._dash_cooldown_remaining = Player.DASH_COOLDOWN
                self.speed = Player.SPEED_NORMAL
                self._is_dashing = False

            else:
                self._dash_time_remaining -= dt
        
        if self._dash_cooldown_remaining is not None:
            if self._dash_cooldown_remaining <= 0:
                self._dash_cooldown_remaining = None
            
            else:
                self._dash_cooldown_remaining -= dt

    def update(self, dt: float = 0, mouse_pos: Vector2 | None = None):
        """Updates the player's position and angle."""

        self.__manage_dash_times(dt)

        # Changing the Player Angle
        speed = self.speed
        if mouse_pos is not None:
            displacement = mouse_pos - self.pos

            if displacement.magnitude() > 0:
                angle_to_mouse = math.atan2(displacement.y, displacement.x)
                self.angle = get_avg_angle(angles=(self.angle, angle_to_mouse), weights=(Player.CURRENT_ANGLE_WEIGHT, dt * 200))

                # Setting Current Player Speed
                if displacement.magnitude() < Player.SLOW_SPEED_RANGE:
                    speed = self.speed * (1 - ((Player.SLOW_SPEED_RANGE - displacement.magnitude()) / Player.SLOW_SPEED_RANGE))

        # Moving the Player
        self.pos.x += math.cos(self.angle) * speed * dt
        self.pos.y += math.sin(self.angle) * speed * dt
    
    def draw(self, surface: Surface):
        """Draws the player to the surface."""
        arrow_points = get_arrow_at_angle(self.angle)
        arrow_points = tuple((point[0] * Player.SIZE + self.pos.x, point[1] * Player.SIZE + self.pos.y) for point in arrow_points)
        draw.polygon(surface, color=Player.COLOR_DASHING if self._is_dashing else Player.COLOR_NORMAL, points=arrow_points)
