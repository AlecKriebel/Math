"""Independent exact diagnostics, not a geometric classification of links."""
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

counts = {}
def check(category, condition):
    assert condition, category
    counts[category] = counts.get(category, 0) + 1

def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3))
                       for j in range(3)) for i in range(3))

def h(a, b, c):
    return ((1, a, c), (0, 1, b), (0, 0, 1))

for m, n, u, v in product(range(-4, 5), range(-4, 5), range(-1, 2), range(-1, 2)):
    # A matrix calculation independent of the submitted free-series engine.
    x, y = h(m, 0, u), h(0, n, v)
    xi, yi = h(-m, 0, -u), h(0, -n, -v)
    check('unitriangular_commutator', mm(mm(mm(x, y), xi), yi) == h(0, 0, m*n))
    check('inverse_commutator', mm(mm(mm(y, x), yi), xi) == h(0, 0, -m*n))

def multiply(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] += a*b
    return out

for mu in range(2, 9):
    for a, b, c, k, ell in product(range(-2, 3), repeat=5):
        link = [0]*(mu-1) + [a, 0, b, 0, 3]
        component = [1, 0, c, 0, -2]
        factor = [1, 0, k, 0, ell]
        new_link, new_component = multiply(link, factor), multiply(component, factor)
        check('full_polynomial_delta1', new_link[mu-1] == a)
        check('full_polynomial_delta2', new_link[mu+1] - new_link[mu-1]*new_component[2] == b-a*c)

def partitions(labels):
    if not labels:
        yield ()
        return
    first, rest = labels[0], labels[1:]
    for tail in partitions(rest):
        yield ((first,),) + tail
    for j, second in enumerate(rest):
        remaining = rest[:j] + rest[j+1:]
        for tail in partitions(remaining):
            yield ((first, second),) + tail

telephone = [1, 1]
for n in range(2, 9):
    telephone.append(telephone[-1] + (n-1)*telephone[-2])
for n in range(1, 9):
    actual = list(partitions(tuple(range(n))))
    check('split_partition_counts', len(actual) == telephone[n])
    check('split_partition_uniqueness', len(set(actual)) == len(actual))
    for blocks in actual:
        check('split_partition_labels', sorted(x for b in blocks for x in b) == list(range(n)))
        check('split_partition_sizes', all(len(b) in (1, 2) for b in blocks))

for n in range(4, 16):
    core = frozenset((0, 1, 2))
    for pair in combinations(range(n), 2):
        check('pair_cannot_see_triple', not core.issubset(pair))
    check('triple_is_visible_to_all_sublinks', core in map(frozenset, combinations(range(n), 3)))
    check('extra_split_component', len(set(range(n)) - core) >= 1)
for signs in product((-1, 1), repeat=3):
    check('orientation_nonvanishing', abs(signs[0]*signs[1]*signs[2]) == 1)

root = Path(__file__).resolve().parent
report = {
    'artifact_sha256': hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),
    'exact_assertions': sum(counts.values()),
    'categories': counts,
    'scope': 'Integer matrix commutators, formal polynomial multiplication, split-label partitions and triple detection. These do not prove a geometric realization or a clasper classification.'
}
(root/'independent_checks.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
print(json.dumps(report, sort_keys=True))
