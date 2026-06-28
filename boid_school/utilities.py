# Utilities
import math
from typing import Sequence
from pygame import Vector2

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
    return get_avg_vector_angle(vectors, weights=weights, normalise_vectors=False)

@staticmethod
def get_arrow_at_angle(angle):
    return ((math.cos(angle)/2,math.sin(angle)/2),\
        (math.cos(angle+2.55)*.6,math.sin(angle+2.55)*.6),\
        (math.cos(angle-2.55)*.6,math.sin(angle-2.55)*.6))
