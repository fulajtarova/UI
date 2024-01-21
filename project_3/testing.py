import main
import matplotlib.pyplot as plt


def make_graphs(whole_results, k_values, color_count):
    # Extract results for accuracy and time for each run
    accuracies = [[result[1] for result in run] for run in whole_results]
    times = [[result[2] for result in run] for run in whole_results]

    # Plot Accuracy
    plt.figure(figsize=(10, 5))
    for i, run in enumerate(accuracies):
        plt.plot(k_values, run, marker="o", label=f"Run {i+1}")

    plt.title("Accuracy vs. k\nDots count: " + str(color_count))
    plt.xlabel("k")
    plt.ylabel("Accuracy")
    plt.legend(
        loc="upper right",
        fontsize="xx-small",
    )
    plt.show()

    # Plot Time
    plt.figure(figsize=(10, 5))
    for i, run in enumerate(times):
        plt.plot(k_values, run, marker="o", label=f"Run {i+1}")

    plt.title("Time vs. k\nDots count: " + str(color_count))
    plt.xlabel("k")
    plt.ylabel("Time (seconds)")
    plt.legend(
        loc="upper right",
        fontsize="xx-small",
    )
    plt.show()


def start():
    run_count = 5
    color_count = 10000

    k_values = [1, 3, 7, 15]
    whole_results = []

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

    for _ in range(run_count):
        generated_dots = main.make_dots(
            color_count, dots, ["red", "green", "blue", "purple"]
        )
        results = main.main(color_count, k_values, False, generated_dots, dots)
        whole_results.append(results)

    make_graphs(whole_results, k_values, color_count * 4)


start()
