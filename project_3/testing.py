import main


def start():
    run_count = 10
    color_count = 1000
    k_values = [1, 3, 7, 15]
    whole_results = []

    for _ in range(run_count):
        results = main.main(color_count, k_values, visualize=False)
        whole_results.append(results)

    print(whole_results)


start()
