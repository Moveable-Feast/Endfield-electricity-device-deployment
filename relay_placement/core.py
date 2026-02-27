from itertools import combinations
from typing import List, Tuple
from .classes import Point, Component
from .calculations import min_distance_between, place_relay_points

def solve(n: int, m: int, l: float,
          sources: List[Tuple[float, float]],
          devices: List[Tuple[float, float]]) -> Tuple[int, List[Point]]:
    """
    Compute the minimum number of relay points needed to connect all devices to at least one source.

    Args:
        n: number of sources
        m: number of devices
        l: maximum wire length
        sources: list of (x, y) for power sources
        devices: list of (x, y) for production devices

    Returns:
        (k, relays) where k is the number of relays added, and relays is the list of Point objects.
    """
    # Build point list
    all_points = [Point(x, y, 'source') for (x, y) in sources] + \
                 [Point(x, y, 'device') for (x, y) in devices]

    # --- Union-Find to form initial components based on distance ≤ l ---
    parent = list(range(len(all_points)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i, j in combinations(range(len(all_points)), 2):
        if all_points[i].dist(all_points[j]) <= l:
            union(i, j)

    # Group points by root
    comp_map = {}
    for idx, p in enumerate(all_points):
        root = find(idx)
        comp_map.setdefault(root, []).append(p)

    components = [Component(pts) for pts in comp_map.values()]

    # If all components already have a source, we are done
    if all(c.has_source for c in components):
        return 0, []

    relay_points = []

    # Greedy merging
    while True:
        # Build list of candidate component pairs (at least one without source)
        pairs = []
        for i, j in combinations(range(len(components)), 2):
            if not components[i].has_source or not components[j].has_source:
                d, pair = min_distance_between(components[i], components[j])
                pairs.append((d, i, j, pair))

        if not pairs:  # should not happen if the loop condition is correct, but safety
            break

        # Choose the closest pair
        d, i, j, (p, q) = min(pairs, key=lambda x: x[0])

        # Place relays between p and q
        new_points = place_relay_points(p, q, l)
        relay_points.extend(new_points)

        # Merge components i, j and the new relays
        new_comp = Component(components[i].points + components[j].points + new_points)

        # Remove i and j (larger index first to avoid shifting)
        components = [comp for idx, comp in enumerate(components) if idx not in (i, j)]
        components.append(new_comp)

        # Termination condition: all components now have a source
        if all(c.has_source for c in components):
            break

    return len(relay_points), relay_points