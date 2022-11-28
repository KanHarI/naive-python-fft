from naive_fft.ii_poly_multiplication.evaluate_poly import polynomial_to_roots
from naive_fft.ii_poly_multiplication.values_to_poly import values_to_poly


def fft(samples: list[complex]) -> list[complex]:
    return polynomial_to_roots(samples)


def ifft(frequecies: list[complex]) -> list[complex]:
    return values_to_poly(frequecies)
