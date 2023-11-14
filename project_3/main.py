import random
import matplotlib.pyplot as plt
import copy
import time


def visualize_dots(dots, accuracy):
    fig, ax = plt.subplots()

    for color in dots:
        dot_array = [list(dot) for dot in dots[color]]
        dot_array = list(zip(*dot_array))  # Transpose the dot array for plotting
        ax.scatter(dot_array[0], dot_array[1], c=color, label=color)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Dots Visualization\nAccuracy: {accuracy:.2f}%")

    plt.show()


def classify_point(point, dots, k):
    distances = []
    for color in dots:
        for dot in dots[color]:
            distance = ((point[0] - dot[0]) ** 2 + (point[1] - dot[1]) ** 2) ** 0.5
            distances.append((distance, color))

    distances.sort(key=lambda x: x[0])
    distances = distances[:k]

    colors = [x[1] for x in distances]
    return max(colors, key=colors.count)


def random_dot(color):
    borders = {
        "red": (-5000, 500, -5000, 500),
        "green": (-500, 5000, -5000, 500),
        "blue": (-5000, 500, -500, 5000),
        "purple": (-500, 5000, -500, 5000),
    }

    if random.uniform(0, 1) < 0.9:
        x = random.randint(borders[color][0], borders[color][1])
        y = random.randint(borders[color][2], borders[color][3])
    else:
        x = random.randint(-5000, 5000)
        y = random.randint(-5000, 5000)

    return (x, y)


def make_dots(num_points, dots):
    points = []
    colors = ["red", "green", "blue", "purple"]

    for _ in range(num_points):
        for color in colors:
            point = random_dot(color)
            while point in points or point in dots[color]:
                point = random_dot(color)
            points.append(point)

    return points


def main():
    k_values = [1, 3, 7, 15]
    num_points = 1000
    colors = ["red", "green", "blue", "purple"]

    dots = {
        "red": [
            (-4500, -4400),
            (-4100, -3000),
            (-1800, -2400),
            (-2500, -3400),
            (-2000, -1400),
        ],
        "green": [
            (4500, -4400),
            (4100, -3000),
            (1800, -2400),
            (2500, -3400),
            (2000, -1400),
        ],
        "blue": [
            (-4500, 4400),
            (-4100, 3000),
            (-1800, +2400),
            (-2500, +3400),
            (-2000, +1400),
        ],
        "purple": [
            (4500, 4400),
            (4100, 3000),
            (1800, 2400),
            (2500, 3400),
            (2000, 1400),
        ],
    }

    print("Welcome to the KNN Classifier!")

    for k in k_values:
        correct = 0
        print(f"\nClassifying with k = {k}...")

        dots_copy = copy.deepcopy(dots)

        start = time.time()

        for i, point in enumerate(make_dots(num_points, dots_copy)):
            color = classify_point(point, dots_copy, k)
            expected_color = colors[i % 4]
            dots_copy[color].append(point)

            if color == expected_color:
                correct += 1

        end = time.time()
        time_elapsed = end - start

        accuracy = (correct / (4 * num_points)) * 100

        print(f"Accuracy: {accuracy:.2f}%")
        print(f"Time elapsed: {time_elapsed:.2f}s")

        visualize_dots(dots_copy, accuracy)


if __name__ == "__main__":
    main()
