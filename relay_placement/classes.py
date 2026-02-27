import math
from typing import List, Optional

class Point:
    """A point in 2D space, possibly with a type tag."""
    def __init__(self, x: float, y: float, typ: Optional[str] = None):
        self.x = x
        self.y = y
        self.typ = typ  # 'source', 'device', or 'relay'

    def dist(self, other: "Point") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f}, {self.typ})"

class Component:
    """A connected component of points (including relays)."""
    def __init__(self, points: List[Point]):
        self.points = points
        self.has_source = any(p.typ == 'source' for p in points)

    def add_points(self, new_points: List[Point]):
        self.points.extend(new_points)
        if not self.has_source:
            self.has_source = any(p.typ == 'source' for p in new_points)