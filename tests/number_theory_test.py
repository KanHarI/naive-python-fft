from naive_fft.number_theory import factorize, is_prime

MAX_TEST_FACTORIZE = 1_000

# fmt: off
PRIMES_UP_TO_100 = {
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
  73, 79, 83, 89, 97,
}
# fmt: on


def test_primes() -> None:
    for i in range(100):
        if i in PRIMES_UP_TO_100:
            assert is_prime(i)
        else:
            assert not is_prime(i)


def test_factorize() -> None:
    for i in range(1, MAX_TEST_FACTORIZE):
        factorization = factorize(i)
        for prime, power in factorization.items():
            assert is_prime(prime)
            for _ in range(power):
                assert i % prime == 0
                i //= prime
        assert i == 1
