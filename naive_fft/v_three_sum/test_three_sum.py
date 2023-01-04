import random
import time

from tqdm import tqdm

from naive_fft.v_three_sum.three_sum import fft_three_sum, n_squared_three_sum

NUM_RUNS = 10
ARRAY_LENGTH = 40_000
ARRAY_MAX = 80_000


def test_three_manual() -> None:
    array = [17, 10, 20, 15]
    assert fft_three_sum(array, 21, 47)
    assert n_squared_three_sum(array, 21, 47)
    assert not fft_three_sum(array, 21, 46)
    assert not n_squared_three_sum(array, 21, 46)
    array_2 = [1, 1, 1]
    assert fft_three_sum(array_2, 2, 3)
    assert n_squared_three_sum(array_2, 2, 3)
    assert not fft_three_sum(array_2, 2, 2)
    assert not n_squared_three_sum(array_2, 2, 2)
    array_3 = [13, 13, 12]
    assert fft_three_sum(array_3, 14, 38)
    assert n_squared_three_sum(array_3, 14, 38)
    assert not fft_three_sum(array_3, 14, 37)
    assert not n_squared_three_sum(array_3, 14, 37)


def test_three_sum_automatic_and_timing() -> None:
    fft_time = 0.0
    n_quared_time = 0.0
    for i in tqdm(range(NUM_RUNS)):
        array = []
        for j in range(ARRAY_LENGTH):
            array.append(random.randint(0, ARRAY_MAX - 1))
        target_sum = random.randint(0, 3 * (ARRAY_MAX - 1))
        fft_start_time = time.time()
        is_three_sum_fft = fft_three_sum(array, ARRAY_MAX, target_sum)
        fft_end_time = time.time()
        n_squared_start_time = time.time()
        is_three_sum_n_squared = n_squared_three_sum(array, ARRAY_MAX, target_sum)
        n_squared_end_time = time.time()
        assert is_three_sum_fft == is_three_sum_n_squared
        fft_time += fft_end_time - fft_start_time
        n_quared_time += n_squared_end_time - n_squared_start_time
    print("fft_time:", fft_time)
    print("n_squared_time:", n_quared_time)


if __name__ == "__main__":
    test_three_manual()
    test_three_sum_automatic_and_timing()
