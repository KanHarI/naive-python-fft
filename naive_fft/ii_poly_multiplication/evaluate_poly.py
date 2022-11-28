from math import e, pi

from naive_fft.i_number_theory.number_theory import factorize

VERBOSE = False


# This algorithm is inefficient for degrees with large prime factors
# There are other algorithms, for numbers with large prime factors -
# we will not discuss it today, as it requires more group theory than
# appropriate for today (or that I have experience teaching).
# You can read about them in
# https://en.wikipedia.org/wiki/Fast_Fourier_transform#Other_FFT_algorithms
#


def evaluate_poly(poly: list[complex]) -> list[complex]:
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

    # Find the n'th root of unity
    phase_w = 2 * pi / n
    w = e ** (phase_w * (1j))
    # Same as:
    # w = math.cos(phase_w) + 1j * math.sin(phase_w)

    # purpose - we want to return the polynomial evaluated at 1, w, w^2, ..., w^5
    # expected return val:
    # [f(1), f(w), f(w^2), f(w^3), f(w^4), f(w^5)]

    factorization = factorize(n)

    # Let us call the largest prime factor p
    p = 0
    for prime_factor in factorization.keys():
        if p is None or prime_factor > p:
            p = prime_factor

    # We will split the number of terms in the polynomial into n = p * q, where p is the largest prime factor
    q = n // p

    unit_roots_of_nth_order: list[complex] = [1]
    for i in range(n - 1):
        unit_roots_of_nth_order.append(unit_roots_of_nth_order[-1] * w)
    # in our example, n = 6, and therefore z = e^(2pi*i/6),
    # unit_roots_of_nth_order = [1, w, w^2, w^3, w^4, w^5]
    # NOTE: w^6 = w^0 = 1

    split_polynomials: list[list[complex]] = [list() for _ in range(p)]
    for idx, coefficient in enumerate(poly):
        split_polynomials[idx % p].append(coefficient)
    # Decomposing the polynomial:
    # ax^5 + bx^4 + cx^3 + dx^2 + ex + f
    # = x^2(ax^3 + d) + x(bx^3 + e) + (cx^3 + f)
    #
    # We ca similarly split any poly of degree n = p * q into p polys of degree q
    #
    # split_polynomials = [[f, c], [e, b], [a, d]]
    # f_0(w) := cw^3 + f
    # f_1(w) := bw^3 + e
    # f_2(w) := aw^3 + d
    # We will now look at them as functions of t := w^3:
    # f_0(t) := ct + f
    # f_1(t) := bt + e
    # f_2(t) := at + d
    # split_polynomials = [f_0, f_1, f_2]
    #
    # NOTE: for all k, m: f_k(w^m) = f_k(w^(m+6))

    evaluated_split_poly: list[list[complex]] = list(
        map(evaluate_poly, split_polynomials)
    )
    # evaluated_split_poly = [[f_0(t=1), f_0(t=-1)], [f_1(t=1), f_1(t=-1)], [f_2(t=1), f_2(t=-1)]] =>
    # As functions of z:
    # [[f_0(w^0), f_0(w^3)], [f_1(w^0), f_1(w^3)], [f_2(w^0), f_2(w^3)]]

    # initialize zeroes for result
    result: list[complex] = [0 for _ in range(n)]

    if VERBOSE:
        print("unit_roots_of_nth_order", unit_roots_of_nth_order)
        print("evaluated_split_poly", evaluated_split_poly)
        print("largest_prime_factor", p)

    # Reminder: f(x) = ax^5 + bx^4 + cx^3 + dx^2 + ex + f
    # f(x) = x^2(ax^3 + d) + x(bx^3 + e) + (cx^3 + f)
    # f(w^m) = w^(2m)(a*w^(3m) + d) + w^m(b*w^(3m) + e) + w^0(c*w^(3m) + f)
    #
    # Reminder: w^6 = 1 = w^0
    # f(1) = f(w^0) = 1(a + d) + 1(b + e) + 1(c + f) = w^(0*2)f_2(w^0) + w^(0*1)f_1(w^0) + w^(0*0)f_0(w^0)
    # f(w) = f(w^1) = w^2(a*w^3 + d) + z(bw^3 + e) + 1(cw^3 + f) = w^(1*2)f_2(w^3) + w^(1*1)f_1(w^3) + w^(1*0)f_0(w^3)
    # f(w^2) = w^4(a*w^6 + d) + w^2(bw^6 + e) + 1(cw^6 + f) = w^(2*2)f_2(w^0) + w^(2*1)f_1(w^0) + w^(2*0)f_0(w^0)
    # f(w^3) = w^6(a*w^9 + d) + w^3(bw^9 + e) + 1(cw^9 + f) = w^(3*2)f_2(w^3) + w^(3*1)f_1(w^3) + w^(3*0)f_0(w^3)
    # f(w^4) = w^8(a*w^12 + d) + w^4(bw^12 + e) + 1(cw^12 + f) = w^(4*2)f_2(w^0) + w^(4*1)f_1(w^0) + w^(4*0)f_0(w^0)
    # f(w^5) = w^10(a*w^15 + d) + w^5(bw^15 + e) + 1(cw^15 + f) = w^(5*2)f_2(w^3) + w^(5*1)f_1(w^3) + w^(5*0)f_0(w^3)
    # f(w^6) = f(w^0) = f(1)
    #
    # f(w^m) = w^(m*0)f_0(w^(m*3)) + w^(m*1)f_1(w^(m*3)) + w^(m*2)f_2(w^(m*3))
    #
    # Reminder: evaluated subpolys are
    # [[f_0(w^0), f_0(w^3)], [f_1(w^0), f_1(w^3)], [f_2(w^0), f_2(w^3)]]
    #
    # For all k in 0,1,2, f_k(w^(m*3)) is in the position [k, m % 2] in the evaluated array
    for i in range(n):
        # n * p multiplications of every level.
        #
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
