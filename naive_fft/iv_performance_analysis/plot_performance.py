import random
import time

import matplotlib.pyplot as plt  # type:ignore

from naive_fft.ii_poly_multiplication.evaluate_poly import evaluate_poly
from naive_fft.ii_poly_multiplication.values_to_poly import values_to_poly

MIN_TIME_FOR_ANALYSIS = 0.01  # 0.01 second per tested size


def get_sample_performance(
    start_size: int, end_size: int, step_size: int
) -> list[tuple[int, float]]:
    samples: list[tuple[int, float]] = []
    size = start_size
    while size < end_size:
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
        size += step_size
    return samples


def plot_1_to_100() -> None:
    samples = get_sample_performance(1, 201, 1)
    x, y = zip(*samples)
    plt.plot(x, y)
    plt.show()
