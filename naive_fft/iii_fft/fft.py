from naive_fft.ii_poly_multiplication.evaluate_poly import evaluate_poly
from naive_fft.ii_poly_multiplication.values_to_poly import values_to_poly


def fft(samples: list[complex]) -> list[complex]:
    return evaluate_poly(samples)


def ifft(frequecies: list[complex]) -> list[complex]:
    return values_to_poly(frequecies)
