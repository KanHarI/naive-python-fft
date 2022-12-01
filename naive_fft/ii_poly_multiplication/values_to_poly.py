from typing import List

from naive_fft.ii_poly_multiplication.evaluate_poly import evaluate_poly


def values_to_poly(values: List[complex]) -> List[complex]:
    """Convert an array of values at roots of unity of a polynomial into the
    coefficients of the polynomial"""

    # We will not prove this equivalence today
    n = len(values)
    return list(
        map(
            lambda x: x.conjugate(),
            evaluate_poly([value.conjugate() / n for value in values]),
        )
    )
