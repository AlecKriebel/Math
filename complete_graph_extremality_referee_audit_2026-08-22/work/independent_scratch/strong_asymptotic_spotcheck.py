"""Literal subset-chain checks of the strong-selection coefficient."""

from itertools import combinations
import sympy as sp


e = sp.symbols("e")


def fixation_in_e(weights):
    n = len(weights)
    states = [frozenset(S) for k in range(1, n) for S in combinations(range(n), k)]
    index = {S: z for z, S in enumerate(states)}
    Q = sp.zeros(len(states))
    b = sp.zeros(len(states), 1)
    for S in states:
        row = index[S]
        for target in range(n):
            mutant = sum(weights[u][target] for u in S if u != target)
            resident = sum(weights[u][target] for u in range(n) if u not in S and u != target)
            if mutant == 0:
                pm = sp.Rational(0)
            elif resident == 0:
                pm = sp.Rational(1)
            else:
                pm = mutant / (mutant + e * resident)
            for is_mutant, probability in ((True, pm), (False, 1-pm)):
                new = set(S)
                if is_mutant:
                    new.add(target)
                else:
                    new.discard(target)
                new = frozenset(new)
                probability /= n
                if len(new) == n:
                    b[row] += probability
                elif len(new) != 0:
                    Q[row, index[new]] += probability
    h = (sp.eye(len(states))-Q).inv(method="DM") * b
    return sp.cancel(sum(h[index[frozenset((i,))]] for i in range(n))/n)


def defect(weights):
    n = len(weights)
    total = sp.Rational(0)
    for target in range(n):
        sources = [u for u in range(n) if u != target]
        for u, z in combinations(sources, 2):
            total += (weights[u][target]-weights[z][target])**2 / (
                weights[u][target]*weights[z][target]
            )
    return sp.cancel(total)


examples = [
    [
        [sp.Rational(0), 2, 7],
        [5, sp.Rational(0), 3],
        [1, 11, sp.Rational(0)],
    ],
    [
        [sp.Rational(0), 2, 7, 5],
        [5, sp.Rational(0), 3, 2],
        [1, 11, sp.Rational(0), 13],
        [4, 3, 2, sp.Rational(0)],
    ],
]

for W in examples:
    n = len(W)
    rho = fixation_in_e(W)
    if n == 2:
        baseline = sp.Rational(1, 2)
    else:
        baseline = sp.Rational(n-1, n) * (1-e)/(1-e**(n-1))
    coefficient = sp.limit((baseline-rho)/e, e, 0)
    expected = defect(W)/(n**2*(n-2))
    assert sp.cancel(coefficient-expected) == 0
    print(f"n={n}_strong_coefficient=PASS value={coefficient}")

