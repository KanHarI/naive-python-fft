import math
import random
import time
from typing import Iterable, List, Tuple, cast

import matplotlib.pyplot as plt  # type: ignore
import tqdm  # type: ignore

from naive_fft.i_number_theory.number_theory import factorize
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


POINTS_TO_PLOT = 500
RANDOM_POINTS_TO_PLOT = 50
MAX_RANDOM_SIZE = 10000
# Values tuned for apple M1 Pro
N_LOG_N_CONSTANT = 350_000
N_SQUARED_CONSTANT = 2_000_000
APPROXIMATE_CONSTANT = N_SQUARED_CONSTANT


def approximate_factor(n: int) -> int:
    factorization = factorize(n)
    sum = 0
    for prime, power in factorization.items():
        sum += prime * power
        # This calculation is not really correct as the recursive steps are liekly to get larger and larger factors
        # the deaper we are into the recursion, leading to slower performance, while the analysis depends on
        # the subarray having the same asymptotical complexity; Yet - it is close enough for values up to a
        # few thousands
    return sum


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
        n_log_n = [(n, n * math.log(n) / N_LOG_N_CONSTANT) for n in tested_vals]
        x, y = zip(*n_log_n)
        ax1.plot(x, y)
        ax1.set_ylabel("n log(n)")
    if plot_n_squared:
        n_squared = [(n, n**2 / N_SQUARED_CONSTANT) for n in tested_vals]
        x, y = zip(*n_squared)
        ax1.plot(x, y)
        ax1.set_ylabel("n^2")
    if plot_approximate_factor:
        approx_factors = [
            (n, approximate_factor(n) * n / APPROXIMATE_CONSTANT) for n in tested_vals
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


def plot_numbers_generated_by_2_3_5() -> None:
    sample_sizes = [
        i for i in range(1, 1000) if set(factorize(i).keys()).issubset({2, 3, 5, 7, 11})
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


MAX_POWER_OF_2 = 14


def print_powers_of_2_times() -> None:
    sizes = list(map(lambda exp: cast(int, 2**exp), range(MAX_POWER_OF_2)))[::-1]
    for size, time in get_sample_performance(sizes[::-1]):
        print(
            f"{size}: {time}s, nlog(n) approx: {size * math.log(size) / N_LOG_N_CONSTANT}"
        )


# plot_1_to_n(POINTS_TO_PLOT)
# plot_numbers_generated_by_2_3_5()
plot_random_numbers_perf()
# print_powers_of_2_times()
