import game
import math
import matplotlib.pyplot as plt
import time


def graph(generation_num_list, name):
    x = range(1, len(generation_num_list) + 1)

    colors = ["red" if value == 1000 else "green" for value in generation_num_list]

    plt.bar(x, generation_num_list, color=colors)

    plt.xlabel("Run number")
    plt.ylabel("Number of generations")

    plt.title(name)

    sum_value = sum(generation_num_list)
    average_value = sum_value / len(generation_num_list)

    plt.text(
        len(generation_num_list) / 2,
        max(generation_num_list),
        f"Average: {int(average_value)}",
        horizontalalignment="center",
        va="bottom",
        color="black",
    )

    plt.show()


def testing():
    treasure_count = 5
    board_size = 7
    board = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2,
        0,
        0,
        0,
        0,
        2,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2,
        0,
        0,
        2,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
    ]

    individual_count = 40
    mutation_probability = int(10 / 100 * 64)
    mutation_probability = math.ceil(mutation_probability)
    if mutation_probability == 0:
        mutation_probability = 1
    max_generations = 1000
    random_values_for_individuals = 60
    elitism_count_percentage = 10 / 100
    elite_individual_count = int(individual_count * elitism_count_percentage)
    selection_type = 1
    animation = 2

    roulette_evolutions = []

    t11 = time.time()
    for x in range(50):
        print(x)
        gen_num = game.play_game(
            board,
            board_size,
            individual_count,
            mutation_probability,
            max_generations,
            treasure_count,
            random_values_for_individuals,
            elite_individual_count,
            selection_type,
            animation,
            graph=False,
        )
        roulette_evolutions.append(gen_num)

    t12 = time.time()
    t1f = t12 - t11

    selection_type = 2

    graph(roulette_evolutions, name="Roulette Wheel")

    tournament_evolutions = []

    t21 = time.time()
    for x in range(50):
        print(x)
        gen_num = game.play_game(
            board,
            board_size,
            individual_count,
            mutation_probability,
            max_generations,
            treasure_count,
            random_values_for_individuals,
            elite_individual_count,
            selection_type,
            animation,
            graph=False,
        )
        tournament_evolutions.append(gen_num)

    graph(tournament_evolutions, name="Tournament")

    t22 = time.time()
    t2f = t22 - t21

    print("Roulette Wheel")
    print("Time:", t1f)
    print("\nTournament")
    print("Time:", t2f)


testing()
