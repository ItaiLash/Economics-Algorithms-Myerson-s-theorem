import heapq
import doctest

CONST_1 = [10, 20, 25, 50, 30]


def payments(values: list, choice_rules) -> list:
    """
    A method that calculates the appropriate payment rule according to Myerson's theorem
    for the choice rule received as input
    :param values: vector of values that represent each player value
    :param choice_rules: pointer to function that represent  a monotonic choice rule
    :return: the payments vector (in NIS) with an accuracy of 0.01 NIS

    Examples
    --------
    >>> val = [2., 4.1, 12.2, 12.3, 3.7]
    >>> print(payments(val, bigger_then_ten))
    ['-', '-', 10.000000000000046, 10.00000000000005, '-']
    >>> print(payments(val, highest_n_value_win))
    ['-', 3.700000000000008, 3.7000000000001805, 3.700000000000184, '-']
    >>> print(payments(val, greedy_a))
    ['-', 2.0000000000000444, 2.0000000000002167, 3.700000000000184, '-']
    """
    winners = choice_rules(values)
    payment = list()
    for i in range(len(winners)):
        if winners[i] is True:
            payment.append(threshold(values, i, choice_rules))
        else:
            payment.append('-')
    return payment


def threshold(values: list, value_index: int, choice_rules):
    vals = values.copy()
    while True:
        vals[value_index] -= 0.01
        cur_list = choice_rules(vals)
        if not cur_list[value_index]:
            return vals[value_index] + 0.01


# |———————————————————————————————————————————————————————————————————|
# |                      Monotonic choice rules                       |
# |———————————————————————————————————————————————————————————————————|

def highest_n_value_win(values: list, n: int = 3) -> list:
    indexes = heapq.nlargest(n, range(len(values)), key=values.__getitem__)
    return [x in indexes for x in range(len(values))]


def greedy_a(values: list, max_weight: int = 100):
    indexes = heapq.nlargest(len(values), range(len(values)), key=values.__getitem__)
    winners = [False] * len(values)
    weight = 0
    for i in indexes:
        if weight + CONST_1[i] < max_weight:
            winners[i] = True
            weight += CONST_1[i]
    return winners


def bigger_then_ten(values: list):
    return [x >= 10 for x in values]


if __name__ == '__main__':
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

