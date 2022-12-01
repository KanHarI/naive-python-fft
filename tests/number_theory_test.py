import time
import typing

from naive_fft.i_number_theory.number_theory import (
    factorize,
    is_prime,
    populate_primes_up_to,
    reset_primes,
    sigma_0,
    sigma_1,
)

MAX_TEST_FACTORIZE = 1_000

# fmt: off
PRIMES_UP_TO_100 = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97,
}
# fmt: on


def test_primes() -> None:
    for i in range(1, 101):
        if i in PRIMES_UP_TO_100:
            assert is_prime(i)
            assert sigma_0(i) == 2
            assert sigma_1(i) == i + 1
        else:
            assert not is_prime(i)
            if i == 1:
                assert sigma_0(i) == 1
                assert sigma_1(i) == 1
            else:
                assert sigma_0(i) > 2
                assert sigma_1(i) > i + 1


def test_factorize() -> None:
    for i in range(1, MAX_TEST_FACTORIZE):
        factorization = factorize(i)
        for prime, power in factorization.items():
            assert is_prime(prime)
            for _ in range(power):
                assert i % prime == 0
                i //= prime
        assert i == 1


def test_prime_population_performance() -> None:
    reset_primes()
    t_0 = time.time()
    populate_primes_up_to(100_000)
    t_1 = time.time()
    # Actually more than x15 faster on my machine
    # Python is way slower than js...
    assert t_1 - t_0 < 1


MERSENNE_EXPONENTS = [2, 3, 5, 7, 13, 17]


def mersenne_exponent_to_perfect_num(mersenne_exponent: int) -> int:
    return typing.cast(int, 2 ** (mersenne_exponent - 1) * (2**mersenne_exponent - 1))


PERFECT_NUMBERS: list[int] = list(
    map(mersenne_exponent_to_perfect_num, MERSENNE_EXPONENTS)
)


def test_perfect_numbers() -> None:
    assert 6 in PERFECT_NUMBERS
    assert 28 in PERFECT_NUMBERS
    assert 17 not in PERFECT_NUMBERS
    assert 12 not in PERFECT_NUMBERS
    for perfect_number in PERFECT_NUMBERS:
        assert sigma_1(perfect_number) == perfect_number * 2
