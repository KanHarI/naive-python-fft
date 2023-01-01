from math import ceil, log2

from naive_fft.iii_fft.fft import fft, ifft


def fft_three_sum(array: [int], upper_bound: int, target_sum: int):
    """values in array < upper bound"""
    trice_upper_bound_rounded = 2 ** (ceil(log2(upper_bound)) + 2)
    indices: [int] = [0] * trice_upper_bound_rounded
    double_indices: set[int] = set()
    if target_sum > 3 * (upper_bound - 1):
        raise ValueError("Target sun is too large")
    for n in array:
        if n < 0 or n >= upper_bound:
            raise ValueError("Array contains an element that is too large")
        if n * 3 == target_sum and n in double_indices:
            # Triple element sum
            return True
        if indices[n] > 0:
            double_indices.add(n)
        indices[n] = 1
    for double_index in double_indices:
        target_index = target_sum - 2 * double_index
        if target_index == double_index:
            continue
        if target_index < 0 or target_index > upper_bound:
            continue
        if indices[target_index] > 0:
            # Double and single
            return True
    indices_fft = fft(indices)
    indices_fft_cubed = [x**3 for x in indices_fft]
    indices_3_conv = ifft(indices_fft_cubed)  # indices * indices * indices
    indices_3_conv_int = [round(x.real) for x in indices_3_conv]
    if indices_3_conv_int[target_sum] >= 6:
        return True


def n_squared_three_sum(array: [int], upper_bound: int, target_sum: int):
    sorted_array = sorted(array)
    for i, n in enumerate(sorted_array):
        remains = target_sum - n
        if remains > 2 * (upper_bound - 1):
            continue
        start_idx = 0
        end_idx = len(sorted_array) - 1
        while start_idx < end_idx:
            if start_idx == i:
                start_idx += 1
                continue
            if end_idx == i:
                end_idx -= 1
                continue
            found_sum = sorted_array[start_idx] + sorted_array[end_idx]
            if found_sum == remains:
                return True
            if sorted_array[start_idx] + sorted_array[end_idx] < remains:
                start_idx += 1
            else:
                end_idx -= 1
    return False
