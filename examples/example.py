import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from relay_placement.core import solve

def main():
    n, m, l = 2, 3, 10
    sources = [(0, 0), (100, 0)]
    devices = [(50, 30), (60, 40), (70, 50)]

    k, relays = solve(n, m, l, sources, devices)
    print(f"Need {k} relay points")
    for r in relays:
        print(f"({r.x:.2f}, {r.y:.2f})")

    # Optional: visualize
    try:
        from relay_placement.visualization import plot_solution
        plot_solution(sources, devices, relays, l)
    except ImportError:
        print("matplotlib not installed, skipping visualization.")

if __name__ == "__main__":
    main()