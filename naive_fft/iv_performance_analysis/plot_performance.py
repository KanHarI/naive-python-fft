import math
import random
import time
from typing import Iterable, List, Tuple, cast

import matplotlib.pyplot as plt  # type: ignore
import tqdm  # type: ignore

from naive_fft.i_number_theory.number_theory import (
    GLOBAL_PRIMES_LIST,
    factorial,
    factorize,
    first_prime_after,
    populate_primes_up_to,
    reset_primes,
)
from naive_fft.ii_poly_multiplication.evaluate_poly import evaluate_poly
from naive_fft.ii_poly_multiplication.values_to_poly import values_to_poly

MIN_TIME_FOR_ANALYSIS = 0.02  # 0.02 second per tested size


def get_sample_performance(sample_sizes: Iterable[int]) -> List[Tuple[int, float]]:
    samples: List[Tuple[int, float]] = []
    for size in tqdm.tqdm(sample_sizes):
        random_poly: List[complex] = []
        for _ in range(size):
            random_poly.append(random.random() * 2 - 1 + 1j * (random.random() * 2 - 1))
        t_0 = time.time()
        t_1 = time.time()
        i = 0
        while t_1 - t_0 < MIN_TIME_FOR_ANALYSIS:
            values_to_poly(evaluate_poly(random_poly))
            i += 1
            t_1 = time.time()
        average_time = (t_1 - t_0) / i
        samples.append((size, average_time))
    return samples


POINTS_TO_PLOT = 200
RANDOM_POINTS_TO_PLOT = 60
MAX_RANDOM_SIZE = 3000
MAX_NUMBER_GENERATED_BY_PRIMES = 3000

# Values tuned for apple M1 Pro
N_LOG_N_CONSTANT = 1.889597219190644e-06
N_SQUARED_CONSTANT = 2.6172736330578685e-07
APPROXIMATE_CONSTANT = 5.032931188659143e-07


def calibrate() -> None:
    global MIN_TIME_FOR_ANALYSIS
    global N_SQUARED_CONSTANT
    global APPROXIMATE_CONSTANT
    global N_LOG_N_CONSTANT

    large_prime = first_prime_after(1000)
    power_of_2 = 2**14
    # Caches warmup - dont count first run of each
    get_sample_performance([large_prime])
    prime_performances = get_sample_performance(
        [large_prime, large_prime, large_prime, large_prime, large_prime]
    )
    average_prime_runtime = sum(
        map(lambda sample: sample[1], prime_performances)
    ) / len(prime_performances)
    print(f"Prime runtime: {average_prime_runtime}s, prime: {large_prime}")
    old_min_time_for_analysis = MIN_TIME_FOR_ANALYSIS
    MIN_TIME_FOR_ANALYSIS = 1
    get_sample_performance([power_of_2])
    power_of_2_performances = get_sample_performance(
        [power_of_2, power_of_2, power_of_2, power_of_2, power_of_2]
    )
    average_power_of_2_runtime = sum(
        map(lambda sample: sample[1], power_of_2_performances)
    ) / len(power_of_2_performances)
    print(
        f"Power of 2 runtime: {average_power_of_2_runtime}s, power of 2: {power_of_2}"
    )

    tested_composite = factorial(7)
    get_sample_performance([tested_composite])
    composite_performances = get_sample_performance(
        [
            tested_composite,
            tested_composite,
            tested_composite,
            tested_composite,
            tested_composite,
        ]
    )
    average_composite_time = sum(
        map(lambda sample: sample[1], composite_performances)
    ) / len(composite_performances)
    print(
        f"Composite runtime: {average_composite_time}s, power of 2: {tested_composite}"
    )

    N_SQUARED_CONSTANT = average_prime_runtime / large_prime**2
    print("N_SQUARED_CONSTANT", N_SQUARED_CONSTANT)
    N_LOG_N_CONSTANT = average_power_of_2_runtime / (power_of_2 * math.log(power_of_2))
    print("N_LOG_N_CONSTANT", N_LOG_N_CONSTANT)
    candidate_1_approximate = average_prime_runtime / (
        approximate_factor(large_prime) * large_prime
    )
    candidate_2_approximate = average_power_of_2_runtime / (
        approximate_factor(power_of_2) * power_of_2
    )
    candidate_3_approximate = average_composite_time / (
        approximate_factor(tested_composite) * tested_composite
    )
    APPROXIMATE_CONSTANT = (
        candidate_1_approximate + candidate_2_approximate + candidate_3_approximate
    ) / 3
    print("APPROXIMATE_CONSTANT", APPROXIMATE_CONSTANT)
    MIN_TIME_FOR_ANALYSIS = old_min_time_for_analysis


def approximate_factor(n: int) -> float:
    factorization = factorize(n)
    result = 0
    for prime, power in factorization.items():
        result += prime * power
    return max(result, 1)


def plot_for_ranges(
    tested_vals: Iterable[int],
    *,
    plot_n_log_n: bool = False,
    plot_n_squared: bool = False,
    plot_approximate_factor: bool = False,
) -> None:
    fig = plt.figure()
    ax1 = fig.add_subplot()
    if plot_n_log_n:
        n_log_n = [(n, n * math.log(n) * N_LOG_N_CONSTANT) for n in tested_vals]
        x, y = zip(*n_log_n)
        ax1.plot(x, y)
        ax1.set_ylabel("n log(n)")
    if plot_n_squared:
        n_squared = [(n, n**2 * N_SQUARED_CONSTANT) for n in tested_vals]
        x, y = zip(*n_squared)
        ax1.plot(x, y)
        ax1.set_ylabel("n^2")
    if plot_approximate_factor:
        approx_factors = [
            (n, approximate_factor(n) * n * APPROXIMATE_CONSTANT) for n in tested_vals
        ]
        x, y = zip(*approx_factors)
        ax1.plot(x, y)
        ax1.set_ylabel("Approx")
    samples = get_sample_performance(tested_vals)
    x, y = zip(*samples)
    ax1.plot(x, y)
    ax1.set_ylabel("Runtime")
    plt.show()


def plot_1_to_n(n: int) -> None:
    plot_for_ranges(
        list(range(1, 1 + n))[::-1],
        plot_n_log_n=True,
        plot_n_squared=True,
        plot_approximate_factor=True,
    )


def plot_numbers_generated_by_primes(primes_list: List[int]) -> None:
    primes_set = set(primes_list)
    sample_sizes = [
        i
        for i in range(1, MAX_NUMBER_GENERATED_BY_PRIMES)
        if set(factorize(i).keys()).issubset(primes_set)
    ][::-1]
    plot_for_ranges(
        sample_sizes,
        plot_approximate_factor=True,
        plot_n_log_n=True,
    )


def plot_random_numbers_perf() -> None:
    sample_sizes = []
    for _ in range(RANDOM_POINTS_TO_PLOT):
        sample_sizes.append(math.ceil(random.random() * MAX_RANDOM_SIZE))
    sample_sizes = sorted(list(set(sample_sizes)))[::-1]
    plot_for_ranges(
        sample_sizes,
        plot_approximate_factor=True,
        plot_n_squared=True,
        plot_n_log_n=True,
    )


MAX_POWER_OF_2 = 16


def print_powers_of_2_times() -> None:
    sizes = list(map(lambda exp: cast(int, 2**exp), range(MAX_POWER_OF_2)))[::-1]
    for size, time in get_sample_performance(sizes[::-1]):
        print(
            f"{size}: {time}s, n log(n) approx: {size * math.log(size) * N_LOG_N_CONSTANT}"
        )


if __name__ == "__main__":
    calibrate()
    print_powers_of_2_times()
    plot_1_to_n(POINTS_TO_PLOT)
    plot_numbers_generated_by_primes([3, 7, 13, 17, 23])
    plot_random_numbers_perf()
