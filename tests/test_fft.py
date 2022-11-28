import random

from numpy.fft import fft as np_fft
from numpy.fft import ifft as np_ifft

from naive_fft.iii_fft.fft import fft as our_fft
from naive_fft.iii_fft.fft import ifft as our_ifft
from naive_fft.utils import l2

NUM_TESTS = 20
MAX_SIZE = 4

MAX_TOLERANCE = 1e-5


def test_outs_and_numpy_fft() -> None:
    for _ in range(NUM_TESTS):
        samples: list[complex] = []
        for _ in range(MAX_SIZE):
            samples.append(random.random() * 2 - 1 + 1j * (random.random() * 2 - 1))
        our_samples_fft = our_fft(samples)
        np_samples_fft = list(np_fft(samples))
        our_samples_ifft = our_ifft(samples)
        np_samples_ifft = list(np_ifft(samples))
        assert l2(our_samples_fft, np_samples_fft) < MAX_TOLERANCE
        assert l2(our_samples_ifft, np_samples_ifft) < MAX_TOLERANCE
