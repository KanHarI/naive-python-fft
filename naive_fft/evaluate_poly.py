import math
from math import e

from naive_fft.number_theory import factorize

VERBOSE = False

# This algorithm is inefficient for degrees with large prime factors
# There are other algorithms, for numbers with large prime factors -
# we will not discuss it today, as it requires more group theory than
# appropriate for today (or that I have experience teaching).
# You can read about them in
# https://en.wikipedia.org/wiki/Fast_Fourier_transform#Other_FFT_algorithms
#
def polynomial_to_roots(poly: list[complex]) -> list[complex]:
    """Evaluate a polynomial of degree n at n roots of unity, defining it
    uniquely"""
    # This is a variation on the Cooley–Tukey FFT algorithm:
    # https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
    #
    # example input:
    # [f, e, d, c, b, a] =>
    # f(x) = ax^5 + bx^4 + cx^3 + dx^2 + ex + f
    # n = 6, the number of terms
    n = len(poly)
    if n == 0:
        return []
    if n == 1:
        return [poly[0]]

    # Find the complex n'th root
    phase_z = 2 * math.pi / n
    z = e ** (phase_z * (1j))
    # Same as:
    # z = math.cos(phase_z) + 1j * math.sin(phase_z)

    # purpose - we want to return the polynomial evaluated at 1, z, z^2, ..., z^5
    # expected return val:
    # [f(1), f(z), f(z^2), f(z^3), f(z^4), f(z^5)]

    factorization = factorize(n)

    # Let us call the largest prime factor p
    p = 1
    for prime_factor in factorization.keys():
        if prime_factor > p:
            p = prime_factor

    # We will split the number of terms in the polynomial into n = p * q, where p is the largest prime factor
    q = n // p

    unit_roots_of_nth_order: list[complex] = [1]
    unit_roots_of_prime_order: list[complex] = [1]
    for i in range(n - 1):
        unit_roots_of_nth_order.append(unit_roots_of_nth_order[-1] * z)
        if (i + 1) % q == 0:
            unit_roots_of_prime_order.append(unit_roots_of_nth_order[-1])
    # in our example, n = 6, and therefore z = e^(2pi*i/6),
    # unit_roots_of_nth_order = [1, z, z^2, z^3, z^4, z^5]
    # unit_roots_of_prime_order = [1, z^2, z^4]
    # NOTE: z^6 = 1

    split_polynomials: list[list[complex]] = [[] for _ in range(p)]
    for idx, coefficient in enumerate(poly):
        split_polynomials[idx % p].append(coefficient)
    # Decomposing the polynomial:
    # ax^5 + bx^4 + cx^3 + dx^2 + ex + f
    # = x^2(ax^3 + d) + x(bx^3 + e) + (cx^3 + f)
    #
    # We ca similarly split any poly of degree n = p * q into p polys of degree q
    #
    # split_polynomials = [[f, c], [e, b], [a, d]]
    # f_0(z^3) := cz^3 + f
    # f_1(z^3) := bz^3 + e
    # f_2(z^3) := az^3 + d
    # We will now look at them as functions of t := z^3:
    # f_0(t) := ct + f
    # f_1(t) := bt + e
    # f_2(t) := at + d
    # split_polynomials = [f_0, f_1, f_2]
    # NOTE: for all k, m: f_k(z^m) = f_k(z^(m+q))

    evaluated_split_poly: list[list[complex]] = list(
        map(polynomial_to_roots, split_polynomials)
    )
    # evaluated_split_poly = [[f_0(t=1), f_0(t=-1)], [f_1(t=1), f_1(t=-1)], [f_2(t=1), f_2(t=-1)]] =>
    # As functions of z:
    # [[f_0(z^0), f_0(z^3)], [f_1(z^0), f_1(z^3)], [f_2(z^0), f_2(z^3)]]

    # initialize zeroes for result
    result: list[complex] = [0 for _ in range(n)]

    if VERBOSE:
        print("unit_roots_of_nth_order", unit_roots_of_nth_order)
        print("unit_roots_of_prime_order", unit_roots_of_prime_order)
        print("evaluated_split_poly", evaluated_split_poly)
        print("largest_prime_factor", p)

    # Reminder: f(x) = ax^5 + bx^4 + cx^3 + dx^2 + ex + f
    # f(x) = x^2(ax^3 + d) + x(bx^3 + e) + (cx^3 + f)
    # f(z^m) = z^(2m)(a*z^(3m) + d) + z^m(b*z^(3m) + e) + z^0(c*z^(3m) + f)
    #
    # Reminder: z^6 = 1 = z^0
    # f(1) = f(z^0) = 1(a + d) + 1(b + e) + 1(c + f) = z^(0*2)f_2(z^0) + z^(0*1)f_1(z^0) + z^(0*0)f_0(z^0)
    # f(z) = f(z^1) = z^2(a*z^3 + d) + z(bz^3 + e) + 1(cz^3 + f) = z^(1*2)f_2(z^3) + z^(1*1)f_1(z^3) + z^(1*0)f_0(z^3)
    # f(z^2) = z^4(a*z^6 + d) + z^2(bz^6 + e) + 1(cz^6 + f) = z^(2*2)f_2(z^0) + z^(2*1)f_1(z^0) + z^(2*0)f_0(z^0)
    # f(z^3) = z^6(a*z^9 + d) + z^3(bz^9 + e) + 1(cz^9 + f) = z^(3*2)f_2(z^3) + z^(3*1)f_1(z^3) + z^(3*0)f_0(z^3)
    # f(z^4) = z^8(a*z^12 + d) + z^4(bz^12 + e) + 1(cz^12 + f) = z^(4*2)f_2(z^0) + z^(4*1)f_1(z^0) + z^(4*0)f_0(z^0)
    # f(z^5) = z^10(a*z^15 + d) + z^5(bz^15 + e) + 1(cz^15 + f) = z^(5*2)f_2(z^3) + z^(5*1)f_1(z^3) + z^(5*0)f_0(z^3)
    # f(z^6) = f(z^0) = f(1)
    #
    # f(z^m) = z^(m*0)f_0(z^(m*3)) + z^(m*1)f_1(z^(m*3)) + z^(m*2)f_2(z^(m*3))
    #
    # Reminder: evaluated subpolys are
    # [[f_0(z^0), f_0(z^3)], [f_1(z^0), f_1(z^3)], [f_2(z^0), f_2(z^3)]]
    #
    # For all k in 0,1,2, f_k(z^(m*3)) is in the position [k, m % 2] in the evaluated array
    for i in range(n):
        # n * p multiplications of every level.
        # if the prime factors are bounded by p_max, and assuming the smallest prime is p_min,
        # we get asymptotic runtime - assuming n is much larger than p_max:
        #
        # O(p_max * n * log(n)/log(p_min))
        #
        for j, single_evaluated_poly in enumerate(evaluated_split_poly):
            result[i] += (
                unit_roots_of_nth_order[(i * j) % n] * single_evaluated_poly[i % q]
            )
    if VERBOSE:
        print("result", result)
    return result
