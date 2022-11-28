import math
import random
import time
from math import e, pi

from naive_fft.evaluate_poly import polynomial_to_roots

MIN_TOLERANCE = 1e-5

LARGE_POLY_DEGREE = 10_000


def l2(p1: list[complex], p2: list[complex]) -> float:
    return math.sqrt(sum(map(lambda tpl: abs(tpl[0] - tpl[1]) ** 2, zip(p1, p2))))


def test_poly_evaluation() -> None:
    assert l2(polynomial_to_roots([]), []) < MIN_TOLERANCE
    assert l2(polynomial_to_roots([1]), [1]) < MIN_TOLERANCE
    assert l2(polynomial_to_roots([7]), [7]) < MIN_TOLERANCE
    # 0x + 1
    assert l2(polynomial_to_roots([0, 1]), [1, -1]) < MIN_TOLERANCE
    # 0x + 1
    assert l2(polynomial_to_roots([1, 0]), [1, 1]) < MIN_TOLERANCE
    assert (
        l2(
            polynomial_to_roots([0, 1, 0]),
            [e**0, e ** (2 * pi * (1j) / 3), e ** (2 * pi * (2j) / 3)],
        )
        < MIN_TOLERANCE
    )


def test_poly_performance() -> None:
    t0 = time.time()
    poly: list[complex] = []
    for _ in range(LARGE_POLY_DEGREE):
        poly.append(random.random())
    polynomial_to_roots(poly)
    t1 = time.time()
    # x15 the time on my machine
    assert t1 - t0 < 2
