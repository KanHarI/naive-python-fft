import math


def l2(p1: list[complex], p2: list[complex]) -> float:
    return math.sqrt(sum(map(lambda tpl: abs(tpl[0] - tpl[1]) ** 2, zip(p1, p2))))
