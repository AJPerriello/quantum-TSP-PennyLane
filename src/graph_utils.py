"""
graph_utils.py

Utility functions for generating graph representations, 2D city coordinates,
and distance matrices for the Travelling Salesperson Problem (TSP) using NumPy.
"""

from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np


def generate_tsp_graph(
    num_cities: int, seed: int = None, bbox: Tuple[float, float] = (0.0, 100.0)
) -> Tuple[np.ndarray, np.ndarray]:
    """Generates random 2D coordinates for N cities and calculates the Euclidean

    distance matrix.

    Args:
        num_cities (int): The number of cities (nodes) in the TSP graph.
        seed (int, optional): Seed for reproducible random coordinate generation.
        bbox (Tuple[float, float]): The (min, max) range for generating x and y coordinates.

    Returns:
        Tuple[np.ndarray, np.ndarray]:
            - coordinates: An (N, 2) NumPy array of (x, y) coordinates.
            - distance_matrix: An (N, N) symmetric NumPy array of pairwise distances.
    """
    if num_cities < 2:
        raise ValueError("Number of cities must be at least 2.")

    if seed is not None:
        np.random.seed(seed)

    # 1. Generate random 2D spatial coordinates for N cities
    low, high = bbox
    coordinates = np.random.uniform(low, high, size=(num_cities, 2))

    # 2. Compute pairwise Euclidean distances using vectorized NumPy broadcasting
    # diff shape: (N, N, 2) where diff[i, j] = coord[i] - coord[j]
    diff = coordinates[:, np.newaxis, :] - coordinates[np.newaxis, :, :]

    # distance_matrix shape: (N, N)
    distance_matrix = np.linalg.norm(diff, axis=-1)

    return coordinates, distance_matrix


def calculate_route_distance(
    route: List[int], distance_matrix: np.ndarray
) -> float:
    """Calculates the total tour distance for a given sequence of visited cities.

    Args:
        route (List[int]): Ordered list of city indices representing the tour.
                           e.g., [0, 2, 1, 3]
        distance_matrix (np.ndarray): The (N, N) distance matrix.

    Returns:
        float: Total Euclidean distance of the closed tour.
    """
    num_cities = len(route)
    total_distance = 0.0

    for i in range(num_cities):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]  # Wraps around to starting city
        total_distance += distance_matrix[from_city, to_city]

    return total_distance


def plot_tsp_tour(
    coordinates: np.ndarray,
    route: List[int] = None,
    title: str = "TSP City Layout",
    filename: str = None,
) -> None:
    """Plots city coordinates and an optional TSP route using Matplotlib.

    Args:
        coordinates (np.ndarray): (N, 2) array of city coordinates.
        route (List[int], optional): Sequence of city indices forming a tour.
        title (str): Title for the plot.
        filename (str, optional): File path to save the plot. Displays interactive plot if None.
    """
    plt.figure(figsize=(7, 6))

    # Plot city nodes
    plt.scatter(
        coordinates[:, 0],
        coordinates[:, 1],
        color="crimson",
        s=120,
        zorder=3,
        label="Cities",
    )

    # Label city indices
    for idx, (x, y) in enumerate(coordinates):
        plt.annotate(
            f"City {idx}",
            (x, y),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=10,
            weight="bold",
        )

    # Plot tour connections if route is provided
    if route is not None:
        num_cities = len(route)
        for i in range(num_cities):
            start_idx = route[i]
            end_idx = route[(i + 1) % num_cities]
            p1 = coordinates[start_idx]
            p2 = coordinates[end_idx]

            plt.plot(
                [p1[0], p2[0]],
                [p1[1], p2[1]],
                "b--",
                alpha=0.7,
                linewidth=1.5,
                zorder=2,
            )

    plt.title(title, fontsize=12)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()

    if filename:
        plt.savefig(filename, dpi=300)
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    # --- Example Usage ---
    NUM_CITIES = 4
    SEED = 42

    coords, dist_matrix = generate_tsp_graph(num_cities=NUM_CITIES, seed=SEED)

    print("=== Generated TSP Coordinates (N=4) ===")
    print(np.round(coords, 2))

    print("\n=== Pairwise Distance Matrix ===")
    print(np.round(dist_matrix, 2))

    # Example route: City 0 -> City 1 -> City 2 -> City 3 -> City 0
    sample_route = [0, 1, 2, 3]
    tour_dist = calculate_route_distance(sample_route, dist_matrix)
    print(f"\nSample Route {sample_route} Total Distance: {tour_dist:.2f}")