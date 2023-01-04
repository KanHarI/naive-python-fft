import random
from typing import List

import matplotlib.pyplot as plt  # type: ignore

from naive_fft.iii_fft.fft import fft, ifft

RANDOM_SIGNAL_LENGTH = 1000
OFFSET = 0


def main() -> None:
    random_signal: List[complex] = []
    for i in range(RANDOM_SIGNAL_LENGTH):
        random_signal.append(random.random() - 0.5)
    offset_random_signal = random_signal[OFFSET:] + random_signal[:OFFSET]
    for i in range(RANDOM_SIGNAL_LENGTH):
        offset_random_signal[i] += random.random() - 0.5
        pass
    random_signal_fft = fft(random_signal)
    offset_random_signal_fft = fft(offset_random_signal)
    convolution_fft = [
        x * y for (x, y) in zip(random_signal_fft, offset_random_signal_fft)
    ]
    convolution = ifft(convolution_fft)
    plt.plot([abs(x) for x in convolution])
    plt.show()


if __name__ == "__main__":
    main()
