from naive_fft.ii_poly_multiplication.evaluate_poly import evaluate_poly
from naive_fft.ii_poly_multiplication.values_to_poly import values_to_poly


def reorder_to_fft(samples: list[complex]) -> list[complex]:
    return [samples[0]] + samples[::-1][:-1]


def fft(samples: list[complex]) -> list[complex]:
    evaluated_poly = evaluate_poly(samples)
    return reorder_to_fft(evaluated_poly)


def ifft(frequecies: list[complex]) -> list[complex]:
    return values_to_poly(reorder_to_fft(frequecies))
