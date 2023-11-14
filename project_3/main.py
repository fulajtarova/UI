import numpy as np
import matplotlib.pyplot as plt


def k_nearest_neighbors(x, y, k, red, green, blue, purple):
    all_points = np.array(red + green + blue + purple)
    distances = np.sqrt((all_points[:, 0] - x) ** 2 + (all_points[:, 1] - y) ** 2)

    # Combine distances with corresponding points
    nearest_neighbors = np.column_stack((distances, all_points))

    # Sort based on distances
    nearest_neighbors = nearest_neighbors[np.argsort(nearest_neighbors[:, 0])]

    # Get the k nearest neighbors
    nearest_neighbors = nearest_neighbors[:k, 1:]

    return nearest_neighbors


def classify(x, y, color, k, red, green, blue, purple):
    neighbors = k_nearest_neighbors(x, y, k, red, green, blue, purple)

    colors = []

    for i in range(len(neighbors)):
        neighbor_list = neighbors[i].tolist()  # Convert array to list
        if neighbor_list in red:
            colors.append("red")
        elif neighbor_list in green:
            colors.append("green")
        elif neighbor_list in blue:
            colors.append("blue")
        elif neighbor_list in purple:
            colors.append("purple")

    # Find the majority color
    majority_color = max(set(colors), key=colors.count)

    # Visualization
    # Manually plot points with the majority color
    plt.plot(x, y, color=majority_color, marker=".", markersize=5)

    return 1 if majority_color == color else 0


def main():
    red = [
        [-4500, -4400],
        [-4100, -3000],
        [-1800, -2400],
        [-2500, -3400],
        [-2000, -1400],
    ]
    green = [
        [+4500, -4400],
        [+4100, -3000],
        [+1800, -2400],
        [+2500, -3400],
        [+2000, -1400],
    ]
    blue = [
        [-4500, +4400],
        [-4100, +3000],
        [-1800, +2400],
        [-2500, +3400],
        [-2000, +1400],
    ]
    purple = [
        [+4500, +4400],
        [+4100, +3000],
        [+1800, +2400],
        [+2500, +3400],
        [+2000, +1400],
    ]

    k_values = [1, 3, 7, 15]
    num_points = 100

    for k in k_values:
        stats = 0
        red = 0
        green = 0
        blue = 0
        purple = 0

        for _ in range(4 * num_points):
            xr, yr = np.random.uniform(-5000, 500, 1), np.random.uniform(-5000, 500, 1)
            while any(
                np.all(np.array([xr[0], yr[0]]) == np.array(point)) for point in red
            ):
                xr, yr = np.random.uniform(-5000, 500, 1), np.random.uniform(
                    -5000, 500, 1
                )

            xg, yg = np.random.uniform(-500, 5000, 1), np.random.uniform(-5000, 500, 1)
            while any(
                np.all(np.array([xg[0], yg[0]]) == np.array(point)) for point in green
            ):
                xg, yg = np.random.uniform(-5000, 500, 1), np.random.uniform(
                    -5000, 500, 1
                )

            xb, yb = np.random.uniform(-5000, 500, 1), np.random.uniform(-500, 5000, 1)
            while any(
                np.all(np.array([xb[0], yb[0]]) == np.array(point)) for point in blue
            ):
                xb, yb = np.random.uniform(-5000, 500, 1), np.random.uniform(
                    -5000, 500, 1
                )

            xp, yp = np.random.uniform(-500, 5000, 1), np.random.uniform(-500, 5000, 1)
            while any(
                np.all(np.array([xp[0], yp[0]]) == np.array(point)) for point in purple
            ):
                xp, yp = np.random.uniform(-5000, 500, 1), np.random.uniform(
                    -5000, 500, 1
                )

            correctr = classify(xr[0], yr[0], "red", k, red, green, blue, purple)
            correctg = classify(xg[0], yg[0], "green", k, red, green, blue, purple)
            correctb = classify(xb[0], yb[0], "blue", k, red, green, blue, purple)
            correctp = classify(xp[0], yp[0], "purple", k, red, green, blue, purple)

            red.append([xr[0], yr[0]])
            green.append([xg[0], yg[0]])
            blue.append([xb[0], yb[0]])
            purple.append([xp[0], yp[0]])

            stats += correctr + correctg + correctb + correctp

        accuracy = stats / (len(k_values) * num_points)
        print(f"Accuracy for k = {k}: {accuracy:.2%}")

        # Display the plot
        plt.xlim(-5000, 5000)
        plt.ylim(-5000, 5000)
        plt.gca().set_aspect("equal", adjustable="box")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()


if __name__ == "__main__":
    main()
