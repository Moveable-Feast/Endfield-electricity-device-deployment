import os
import matplotlib.pyplot as plt
from typing import List, Tuple
from .classes import Point

def plot_solution(sources: List[Tuple[float, float]],
                  devices: List[Tuple[float, float]],
                  relays: List[Point],
                  l: float,
                  show_connections: bool = True,
                  save_path='reports/figures/all_points.png'):
    """
    Plot the points and optionally draw circles of radius l around sources/devices/relays
    to illustrate connectivity.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    fig, ax = plt.subplots()

    # Plot sources
    if sources:
        sx, sy = zip(*sources)
        ax.scatter(sx, sy, c='green', marker='s', s=100, label='Sources')

    # Plot devices
    if devices:
        dx, dy = zip(*devices)
        ax.scatter(dx, dy, c='red', marker='o', s=100, label='Devices')

    # Plot relays
    if relays:
        rx = [r.x for r in relays]
        ry = [r.y for r in relays]
        ax.scatter(rx, ry, c='blue', marker='^', s=80, label='Relays')

    # Draw circles of radius l around each point (optional, can be slow for many points)
    if show_connections:
        all_pts = sources + devices + [(r.x, r.y) for r in relays]
        for (x, y) in all_pts:
            circle = plt.Circle((x, y), l, fill=False, edgecolor='gray', linestyle='--', alpha=0.5)
            ax.add_patch(circle)

    ax.set_aspect('equal')
    ax.legend()
    ax.set_title(f"Relay placement (max wire length = {l})")
    plt.savefig(save_path)
    plt.show()