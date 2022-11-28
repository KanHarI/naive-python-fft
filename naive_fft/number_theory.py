import collections
import math

GLOBAL_PRIMES_SET = {2, 3}
GLOBAL_PRIMES_LIST = [2, 3]
GLOBAL_PRIMES_CHECKED_UP_TO = 4


def reset_primes() -> None:
    global GLOBAL_PRIMES_SET
    global GLOBAL_PRIMES_LIST
    global GLOBAL_PRIMES_CHECKED_UP_TO
    GLOBAL_PRIMES_SET = {2, 3}
    GLOBAL_PRIMES_LIST = [2, 3]
    GLOBAL_PRIMES_CHECKED_UP_TO = 4


def populate_primes_up_to(n: int) -> None:
    global GLOBAL_PRIMES
    global GLOBAL_PRIMES_CHECKED_UP_TO

    if GLOBAL_PRIMES_CHECKED_UP_TO >= n:
        return

    while GLOBAL_PRIMES_CHECKED_UP_TO < n:
        GLOBAL_PRIMES_CHECKED_UP_TO += 1
        candidate_prime = GLOBAL_PRIMES_CHECKED_UP_TO
        max_relevant = math.ceil(math.sqrt(candidate_prime))
        for prime in GLOBAL_PRIMES_LIST:
            if candidate_prime % prime == 0:
                break
            if prime >= max_relevant:
                GLOBAL_PRIMES_SET.add(candidate_prime)
                GLOBAL_PRIMES_LIST.append(candidate_prime)
                break


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n <= GLOBAL_PRIMES_CHECKED_UP_TO:
        return n in GLOBAL_PRIMES_SET
    max_relevant = math.ceil(math.sqrt(n))
    populate_primes_up_to(max_relevant)
    for prime in GLOBAL_PRIMES_LIST:
        print(prime)
        if n % prime == 0:
            return False
        if prime > max_relevant:
            break
    return True


def factorize(n: int) -> collections.defaultdict[int, int]:
    assert n != 0, "Cannot factorize 0"
    max_relevant = math.ceil(math.sqrt(n))
    populate_primes_up_to(max_relevant)
    result: collections.defaultdict[int, int] = collections.defaultdict(int)
    update_max_relevant_flag = False
    for prime in GLOBAL_PRIMES_LIST:
        if prime > max_relevant:
            break
        while n % prime == 0:
            n //= prime
            update_max_relevant_flag = True
            result[prime] += 1
        if update_max_relevant_flag:
            max_relevant = math.ceil(math.sqrt(n))
    if n > 1:
        result[n] += 1
    return result
