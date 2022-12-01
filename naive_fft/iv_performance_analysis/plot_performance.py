import math
import random
import time
from typing import Iterable

import matplotlib.pyplot as plt  # type:ignore

from naive_fft.i_number_theory.number_theory import factorize
from naive_fft.ii_poly_multiplication.evaluate_poly import evaluate_poly
from naive_fft.ii_poly_multiplication.values_to_poly import values_to_poly

MIN_TIME_FOR_ANALYSIS = 0.02  # 0.02 second per tested size


def get_sample_performance(sample_sizes: Iterable[int]) -> list[tuple[int, float]]:
    samples: list[tuple[int, float]] = []
    for size in sample_sizes:
        random_poly: list[complex] = []
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


RANGE_TO_PLOT = 200
# Values tuned for apple M1 Pro
N_LOG_N_CONSTANT = 450_000
N_SQUARED_CONSTANT = 2_900_000
APPROXIMATE_CONSTANT = N_SQUARED_CONSTANT


def approximate_factor(n: int) -> int:
    factorization = factorize(n)
    sum = 0
    for prime, power in factorization.items():
        sum += prime * power
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


def plot_1_to_200() -> None:
    plot_for_ranges(range(1, 1 + RANGE_TO_PLOT), plot_n_log_n=True, plot_n_squared=True, plot_approximate_factor=True)


plot_1_to_200()
