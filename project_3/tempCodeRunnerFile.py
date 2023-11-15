import random
import matplotlib.pyplot as plt
import copy
import time
from collections import Counter
import itertools
import numpy as np


from scipy.spatial import ConvexHull


def visualize_dots(dots, accuracy, filler_dots):
    fig, ax = plt.subplots()

    for color in filler_dots:
        if filler_dots[color]:
            dot_array = np.array(filler_dots[color])
            ax.scatter(dot_array[:, 0], dot_array[:, 1], c=color, alpha=0.3, s=100)

    for color in dots:
        dot_array = np.array(dots[color])
        ax.scatter(dot_array[:, 0], dot_array[:, 1], c=color, label=color, marker="o")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Dots Visualization\nAccuracy: {accuracy:.2f}%")

    plt.show()


def make_filler_dots(dots, k):
    total_range = 5000
    interval = int(total_range / 25)
    filler_dots = {
        "red": [],
        "green": [],
        "blue": [],
        "purple": [],
    }

    for x in range(-5000, 5000, interval):
        for y in range(-5000, 5000, interval):
            point = (x, y)
            color = classify(point, dots, k)
            filler_dots[color].append(point)

    return filler_dots


def classify(point, dots, k):
    distances = [
        (color, ((point[0] - dot[0]) ** 2 + (point[1] - dot[1]) ** 2) ** 0.5)
        for color in dots
        for dot in dots[color]
    ]
    distances.sort(key=lambda x: x[1])

    top_k_colors = [color for color, _ in distances[:k]]
    return Counter(top_k_colors).most_common(1)[0][0]


def random_dot(color):
    borders = {
        "red": (-5000, 500, -5000, 500),
        "green": (-500, 5000, -5000, 500),
        "blue": (-5000, 500, -500, 5000),
        "purple": (-500, 5000, -500, 5000),
    }

    if random.uniform(0, 1) < 0.99:
        x = random.randint(borders[color][0], borders[color][1])
        y = random.randint(borders[color][2], borders[color][3])
    else:
        x = random.randint(-5000, 5000)
        y = random.randint(-5000, 5000)

    return (x, y)


def make_dots(individual_color_num, dots, colors):
    colors = itertools.cycle(colors)
    new_points = []

    for _ in range(4 * individual_color_num):
        color = next(colors)
        point = random_dot(color)

        while point in new_points or point in dots[color]:
            point = random_dot(color)

        new_points.append(point)

    return new_points


def main():
    # k_values = [1, 3, 7, 15]
    k_values = [3]

    individual_color_num = 1000
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

        for i, point in enumerate(make_dots(individual_color_num, dots_copy, colors)):
            color = classify(point, dots_copy, k)
            expected_color = colors[i % 4]
            dots_copy[color].append(point)

            if color == expected_color:
                correct += 1

        end = time.time()
        time_elapsed = end - start

        accuracy = (correct / (4 * individual_color_num)) * 100

        print(f"Accuracy: {accuracy:.2f}%")
        print(f"Time elapsed: {time_elapsed:.2f}s")

        filler_dots = make_filler_dots(dots_copy, k)

        print("Visualizing...")

        visualize_dots(dots_copy, accuracy, filler_dots)


if __name__ == "__main__":
    for _ in range(1):
        main()
