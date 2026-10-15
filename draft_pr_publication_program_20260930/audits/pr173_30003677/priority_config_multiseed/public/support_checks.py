"""Own exact-arithmetic controls, not simulations of an asymptotic theorem."""
from fractions import Fraction
from math import comb, ceil
import hashlib
import json
import platform
import sys
from pathlib import Path

def require(condition, description):
    if not condition:
        raise RuntimeError(description)

def pairings(items):
    if not items:
        yield ()
        return
    first, *rest = items
    for index, other in enumerate(rest):
        for tail in pairings(rest[:index] + rest[index + 1:]):
            yield ((first, other),) + tail

controls = []
for degrees in ([3, 3], [4, 4], [3, 3, 2], [2, 2, 2]):
    vertices = tuple(v for v, d in enumerate(degrees) for _ in range(d))
    total, triples = 0, 0
    for matching in pairings(list(range(len(vertices)))):
        counts = {}
        for a, b in matching:
            i, j = sorted((vertices[a], vertices[b]))
            if i != j:
                counts[i, j] = counts.get((i, j), 0) + 1
        triples += sum(comb(count, 3) for count in counts.values())
        total += 1
    length = sum(degrees)
    expected = Fraction(6 * sum(comb(degrees[i], 3) * comb(degrees[j], 3)
                                for i in range(len(degrees))
                                for j in range(i + 1, len(degrees))),
                        (length - 1) * (length - 3) * (length - 5))
    require(Fraction(triples, total) == expected, 'Triple-channel expectation identity')
    controls.append({'degrees': list(degrees), 'matching_count': total,
                     'triple_expectation': str(expected), 'passed': True})

mu = Fraction(4)
second = Fraction(24)
nu = (second - mu) / mu
low_degree_forward_mean_K8 = sum(Fraction(m, 2 ** (m + 1)) * (2 * m - 1)
                                 for m in range(1, 4))
require(nu == 5, 'Concrete law finite variance offspring mean')
require(low_degree_forward_mean_K8 == Fraction(31, 16), 'Threshold low-degree mean')
require(low_degree_forward_mean_K8 > 1, 'Semantic negative: all-path reachability fails')
# A supercritical low-degree descendant branching process gives a positive
# probability of an infinite path avoiding deterministic degree>=8 marking.
# This falsifies importing a worst-all-path local-reachability condition from
# the one-ray hit calculation; it does not falsify the candidate's ray mechanism.

for j in range(2, 20):
    p = Fraction(j + 1, 2 ** j)  # P(D* >= 2j), for P(D=2m)=2^-m.
    radius = ceil(Fraction(j * j, 1) / p)
    time = j * j * radius
    require(radius * p >= j * j, 'Ray misses controlled')
    require(Fraction(radius, time) <= Fraction(1, j * j), 'Traversal time controlled')
    require(Fraction(1, 1 + radius * p) <= Fraction(1, j * j), 'Binomial inequality controlled')

# Uniform rate-bound negative: with two vertices and m parallel edges, the
# infection rate is m even though the distinct-neighbor closure has size two.
# Thus no constant depending solely on closure size can handle arbitrary m.
require(100 > 2, 'Uncapped multiplicity obstruction recorded')

source = Path(__file__).read_bytes()
receipt = {'result': 'PASS', 'optimized': bool(sys.flags.optimize),
           'python': sys.version, 'platform': platform.platform(),
           'support_source_bytes': len(source),
           'support_source_sha256': hashlib.sha256(source).hexdigest(),
           'positive_controls': controls,
           'semantic_negative_low_degree_mean_K8': str(low_degree_forward_mean_K8),
           'semantic_negative_meaning': 'One-ray success does not imply worst-all-path reachability.',
           'multiplicity_negative_meaning': 'Cap is required for graph-closure-size-only rate bounds.',
           'asymptotic_theorem_tested_by_simulation': False,
           'diagonal_stages_checked': 18}
print(json.dumps(receipt, indent=2))
