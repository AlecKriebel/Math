from itertools import permutations, combinations
from collections import Counter
from math import comb
from pathlib import Path
import json, sys

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def standardize(p):
    rank = {value: i + 1 for i, value in enumerate(sorted(p))}
    return tuple(rank[value] for value in p)

def avoids(p, pattern):
    return not any(standardize(tuple(p[i] for i in indices)) == pattern
                   for indices in combinations(range(len(p)), len(pattern)))

def sizes(p):
    current = p
    result = []
    while current:
        if len(result) % 2 == 0:
            m = len(current)
            for k in range(1, len(current) + 1):
                if not avoids(tuple(v for v in current if v > len(current) - k), (2, 1, 3)):
                    m = k - 1
                    break
            current = standardize(tuple(v for v in current if v <= len(current) - m))
        else:
            m = len(current)
            for k in range(1, len(current) + 1):
                if not avoids(current[:k], (1, 3, 2)):
                    m = k - 1
                    break
            current = standardize(current[m:])
        result.append(m)
    return result

N = 8
profiles = {}
a = [1]
b = {(0, K): 1 for K in range(1, 4)}
for n in range(1, N + 1):
    profiles[n] = [sizes(p) for p in permutations(range(1, n + 1))
                   if avoids(p, (1, 3, 2, 4))]
    a.append(len(profiles[n]))
    for K in range(1, 4):
        b[n, K] = sum(len(profile) <= K for profile in profiles[n])

checks = 0
marked_objects = 0
for n in range(1, N + 1):
    for K in range(1, 4):
        Z = Counter()
        for profile in profiles[n]:
            for start in range(len(profile)):
                for length in range(1, min(K, len(profile) - start) + 1):
                    end = start + length
                    m = sum(profile[start:end])
                    k = (profile[start - 1] if start else 0) + (profile[end] if end < len(profile) else 0)
                    Z[m, k] += 1
                    marked_objects += 1
        for m in range(1, n + 1):
            for boundary_cap in range(n - m + 1):
                actual = sum(value for (mass, k), value in Z.items() if mass == m and k <= boundary_cap)
                bound = (n - m + 1) * a[n - m] * b[m, K] * comb(2 * m + boundary_cap + 1, boundary_cap)
                require(actual <= bound, (n, K, m, boundary_cap, actual, bound))
                checks += 1

result = {'status': 'passed', 'scope': 'Finite regression only; asymptotic proof is separate',
          'max_n': N, 'block_lengths_checked': [1, 2, 3],
          'finite_inequalities_checked': checks, 'marked_objects_enumerated': marked_objects,
          'avoidance_counts': a,
          'at_most_K_cell_counts': [{'n': n, 'K': K, 'count': b[n, K]}
                                    for n in range(1, N + 1) for K in range(1, 4)]}
output = sys.argv[1] if len(sys.argv) > 1 else 'ISOLATED_BLOCK_FINITE_CHECKS.json'
Path(__file__).with_name(output).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
