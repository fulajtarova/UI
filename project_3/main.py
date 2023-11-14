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


def make_color_order(n):
    colors = ["red", "green", "blue", "purple"]

    color_order = []

    print(4 * n)

    while len(color_order) < 4 * n:
        np.random.shuffle(colors)
        color_order.extend(colors)

    return color_order


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
    num_points = 1000

    color_order = make_color_order(num_points)

    for k in k_values:
        correct = 0
        for color in color_order:
            if color == "red":
                x, y = np.random.uniform(-5000, 500, 1), np.random.uniform(
                    -5000, 500, 1
                )
                while any(
                    np.all(np.array([x[0], y[0]]) == np.array(point)) for point in red
                ):
                    x, y = np.random.uniform(-5000, 500, 1), np.random.uniform(
                        -5000, 500, 1
                    )

                correct += classify(x, y, color, k, red, green, blue, purple)
                red.append([x[0], y[0]])

            elif color == "green":
                x, y = np.random.uniform(-500, 5000, 1), np.random.uniform(
                    -5000, 500, 1
                )
                while any(
                    np.all(np.array([x[0], y[0]]) == np.array(point)) for point in green
                ):
                    x, y = np.random.uniform(-5000, 500, 1), np.random.uniform(
                        -5000, 500, 1
                    )

                correct += classify(x, y, color, k, red, green, blue, purple)
                green.append([x[0], y[0]])

            elif color == "blue":
                x, y = np.random.uniform(-5000, 500, 1), np.random.uniform(
                    -500, 5000, 1
                )
                while any(
                    np.all(np.array([x[0], y[0]]) == np.array(point)) for point in blue
                ):
                    x, y = np.random.uniform(-5000, 500, 1), np.random.uniform(
                        -5000, 500, 1
                    )

                correct += classify(x, y, color, k, red, green, blue, purple)
                blue.append([x[0], y[0]])
            elif color == "purple":
                x, y = np.random.uniform(-500, 5000, 1), np.random.uniform(
                    -500, 5000, 1
                )
                while any(
                    np.all(np.array([x[0], y[0]]) == np.array(point))
                    for point in purple
                ):
                    x, y = np.random.uniform(-5000, 500, 1), np.random.uniform(
                        -5000, 500, 1
                    )
                correct += classify(x, y, color, k, red, green, blue, purple)
                purple.append([x[0], y[0]])

        print("Correct: ", correct)

        print(f"Accuracy for k = {k}: {correct / num_points}")

        # Display the plot
        plt.xlim(-5000, 5000)
        plt.ylim(-5000, 5000)
        plt.gca().set_aspect("equal", adjustable="box")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()


if __name__ == "__main__":
    main()
