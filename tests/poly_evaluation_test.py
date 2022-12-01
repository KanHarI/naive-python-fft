import math
import random
import time
from math import e, pi
from typing import List

from naive_fft.ii_poly_multiplication.evaluate_poly import evaluate_poly
from naive_fft.ii_poly_multiplication.values_to_poly import values_to_poly
from naive_fft.utils import l2

MAX_TOLERANCE = 1e-5

LARGE_POLY_DEGREE = 10_000
INVERTIBLE_POLYS_TO_TEST = 100
INVERTIBLE_POLY_MAX_DEGREE = 100


def test_poly_evaluation() -> None:
    assert l2(evaluate_poly([]), []) < MAX_TOLERANCE
    assert l2(evaluate_poly([1]), [1]) < MAX_TOLERANCE
    assert l2(evaluate_poly([7]), [7]) < MAX_TOLERANCE
    # 0x + 1
    assert l2(evaluate_poly([0, 1]), [1, -1]) < MAX_TOLERANCE
    # 0x + 1
    assert l2(evaluate_poly([1, 0]), [1, 1]) < MAX_TOLERANCE
    assert (
        l2(
            evaluate_poly([0, 1, 0]),
            [e**0, e ** (2 * pi * (1j) / 3), e ** (2 * pi * (2j) / 3)],
        )
        < MAX_TOLERANCE
    )


def test_poly_performance() -> None:
    t0 = time.time()
    poly: List[complex] = []
    for _ in range(LARGE_POLY_DEGREE):
        poly.append((random.random() * 2 - 1) + 1j * (random.random() * 2 - 1))
    evaluate_poly(poly)
    t1 = time.time()
    # x15 the time on my machine
    assert t1 - t0 < 2


def test_poly_invertability() -> None:
    for _ in range(INVERTIBLE_POLYS_TO_TEST):
        poly: List[complex] = []
        degree = math.ceil(random.random() * INVERTIBLE_POLY_MAX_DEGREE)
        for _ in range(degree):
            poly.append((random.random() * 2 - 1) + 1j * (random.random() * 2 - 1))
        values = evaluate_poly(poly)
        reconstructed_poly = values_to_poly(values)
        assert l2(poly, reconstructed_poly) < MAX_TOLERANCE
