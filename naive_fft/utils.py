import math
from typing import List


def l2(p1: List[complex], p2: List[complex]) -> float:
    """Returns the sum of squares of differences's absolute value"""
    return math.sqrt(sum(map(lambda tpl: abs(tpl[0] - tpl[1]) ** 2, zip(p1, p2))))
