import math
import random
from typing import List

import matplotlib.pyplot as plt  # type: ignore

from naive_fft.iii_fft.fft import fft

BASE_FREQUENCY = 100 * 2 * math.pi
NUM_SAMPLES = 1000
NOISE_MAGNITUDE = 10


def main() -> None:
    samples: List[complex] = []
    for i in range(NUM_SAMPLES):
        samples.append(
            math.sin(BASE_FREQUENCY * i / NUM_SAMPLES)
            + random.random() * NOISE_MAGNITUDE
            - NOISE_MAGNITUDE / 2
        )
    fig = plt.figure()
    plt.plot(samples)
    plt.show()  # Total noise. Can not see frequency as a human
    samples_fft = fft(samples)
    plt.plot([abs(x) for x in samples_fft])
    plt.show()


if __name__ == "__main__":
    main()
