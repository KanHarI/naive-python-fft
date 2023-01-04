import os
from typing import List

import numpy as np
from scipy.io import wavfile  # type: ignore

from naive_fft.iii_fft.fft import fft, ifft

CURRENT_DIR = os.path.dirname(__file__)
ASSETS_DIR = f"{CURRENT_DIR}/../assets"


SAMPLE_MAX = 32768


def bandpass_filter_sample(
    frequency_data: List[complex],
    sample_rate: int,
    min_frequency: float,
    max_frequency: float,
) -> float:
    length = len(frequency_data)
    frequency_data[0] = 0 + 0j
    frequency_data[length // 2] = 0 + 0j
    saved_up_samples = 2
    for i in range(1, length // 2):
        effective_wavelength_in_samples = length / i
        effective_wavelength_in_seconds = effective_wavelength_in_samples / sample_rate
        effective_frequency = 1 / effective_wavelength_in_seconds
        if effective_frequency < min_frequency or effective_frequency > max_frequency:
            frequency_data[i] = 0 + 0j
            frequency_data[-i] = 0 + 0j
            saved_up_samples += 2
    return saved_up_samples / length


def compress_audio_file(
    source_file_name: str,
    dest_file_name: str,
    min_frequency: float,
    max_frequency: float,
) -> None:
    # Read WAV file
    sample_rate, data = wavfile.read(f"{ASSETS_DIR}/{source_file_name}")
    assert data.dtype == np.int16

    # Split data into left and right channels
    left_channel = data[:, 0] / SAMPLE_MAX
    right_channel = data[:, 1] / SAMPLE_MAX
    left_channel_list = list(left_channel)
    right_channel_list = list(right_channel)

    # Get FFT of every channel
    left_channel_fft = fft(left_channel_list)
    right_channel_fft = fft(right_channel_list)

    # Lose information about all frequencies outside of a set range
    saved_percent = bandpass_filter_sample(
        left_channel_fft, sample_rate, min_frequency, max_frequency
    )
    bandpass_filter_sample(right_channel_fft, sample_rate, min_frequency, max_frequency)
    data_reconstructed = (
        (np.array([ifft(left_channel_fft), ifft(right_channel_fft)]) * SAMPLE_MAX)
        .astype(np.int16)
        .T
    )
    print(f"Compression ratio: {saved_percent*100}%. Output: {dest_file_name}")
    wavfile.write(f"{ASSETS_DIR}/{dest_file_name}", sample_rate, data_reconstructed)


if __name__ == "__main__":
    compress_audio_file("ensoniq-source-sample.wav", "ensoniq_80_to_5k.wav", 80, 5_000)
    compress_audio_file(
        "ensoniq-source-sample.wav", "ensoniq_40_to_10k.wav", 40, 10_000
    )
    compress_audio_file(
        "ensoniq-source-sample.wav", "ensoniq_30_to_15k.wav", 30, 15_000
    )
    compress_audio_file(
        "ensoniq-source-sample.wav", "ensoniq_20_to_20k.wav", 20, 20_000
    )
