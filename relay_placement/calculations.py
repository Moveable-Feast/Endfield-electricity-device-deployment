import math
from typing import List, Tuple
from .classes import Point, Component

def min_distance_between(comp_a: Component, comp_b: Component) -> Tuple[float, Tuple[Point, Point]]:
    """Return the smallest distance between any point of comp_a and any point of comp_b,
       and the pair of points that achieve it."""
    min_d = float('inf')
    best_pair = None
    for p in comp_a.points:
        for q in comp_b.points:
            d = p.dist(q)
            if d < min_d:
                min_d = d
                best_pair = (p, q)
    return min_d, best_pair

def place_relay_points(p: Point, q: Point, l: float) -> List[Point]:
    """Place relays along the straight line from p to q so that consecutive points are ≤ l apart.
       Returns a list of new relay points (excluding p and q)."""
    d = p.dist(q)
    if d <= l:
        return []
    k = math.ceil(d / l) - 1
    points = []
    dx = (q.x - p.x) / d
    dy = (q.y - p.y) / d
    for i in range(1, k + 1):
        xi = p.x + i * l * dx
        yi = p.y + i * l * dy
        points.append(Point(xi, yi, typ='relay'))
    return points