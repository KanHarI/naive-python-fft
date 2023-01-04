import cmath
import math
from typing import List

from numpy.fft import fft as numpy_fft


def dft_trig(array: List[complex]) -> List[complex]:
    result: List[complex] = []
    total_length = len(array)
    for i in range(total_length):
        accumulator = 0 + 0j
        for n in range(total_length):
            angle = -math.pi * 2 * n * i / total_length
            accumulator += array[n] * (math.cos(angle) + (0 + 1j) * math.sin(angle))
        result.append(accumulator)
    return result


def dft_exp(array: List[complex]) -> List[complex]:
    result: List[complex] = []
    total_length = len(array)
    for i in range(total_length):
        accumulator = 0 + 0j
        for n in range(total_length):
            angle = -math.pi * 2 * n * i / total_length
            accumulator += array[n] * cmath.exp((0 + 1j) * angle)
        result.append(accumulator)
    return result


def dft_poly(array: List[complex]) -> List[complex]:
    result: List[complex] = []
    total_length = len(array)
    root_of_unity = cmath.exp(-(0 + 1j) * 2 * math.pi / total_length)
    # We use the conjugate instead of root of unity to use the same convention as numpy
    # Use the following to get the root of unity instead:
    # root_of_unity = cmath.exp((0 + 1j) * 2 * math.pi / total_length)
    for i in range(total_length):
        accumulator = 0 + 0j
        root_of_unity_power = root_of_unity ** i
        for n in range(total_length):
            accumulator += array[n] * root_of_unity_power ** n
        result.append(accumulator)
    return result


def main() -> None:
    sample_input = [1 + 0j, 1 + 0j, 0 + 0j, 0 + 0j]
    trig_dft_result = dft_trig(sample_input)
    exp_dft_result = dft_exp(sample_input)
    numpy_fft_result = list(numpy_fft(sample_input))
    poly_dft_result = dft_poly(sample_input)
    print(f"Trig DFT: {trig_dft_result}")
    print(f"Exp DFT: {exp_dft_result}")
    print(f"Numpy FFT: {numpy_fft_result}")
    print(f"Poly DFT: {poly_dft_result}")


if __name__ == "__main__":
    main()
