#!/usr/bin/env python3
"""Fresh exact tuple-coordinate checks of the first-nonzero non-word model.

The independent model uses no author code or low-bit integer identity. A separate
final section reproduces the author checker. Finite tests supplement the
countable-product proof; they do not provide a group word counterexample.
"""
from pathlib import Path
from itertools import product
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import runpy


def f(point):
    out = [0] * len(point)
    for j, value in enumerate(point):
        if value:
            out[j] = 1
            break
    return tuple(out)


def plus(a, b):
    return tuple((x + y) % 2 for x, y in zip(a, b))


def multiple(k, a):
    return tuple((k*x) % 2 for x in a)


def unit(n, i):
    return tuple(int(j == i) for j in range(n))


def check_level(n):
    domain = list(product((0, 1), repeat=n))
    zero = (0,) * n
    image_counts = Counter(f(a) for a in domain)
    expected = {zero} | {unit(n, j) for j in range(n)}
    assert set(image_counts) == expected
    assert image_counts[zero] == 1
    for j in range(n):
        assert image_counts[unit(n, j)] == 2**(n-j-1)
    power_checks = 0
    for a in domain:
        for k in range(-17, 18):
            assert f(multiple(k, a)) == multiple(k, f(a))
            power_checks += 1
        # The first nonzero prefix cylinder must be constant on all its tails.
        if any(a):
            j = a.index(1)
            assert f(a) == unit(n, j)
            assert a[:j] == (0,) * j
    next_image = {(0,) * (n+1)} | {unit(n+1, j) for j in range(n+1)}
    output_fibers = {y: [z for z in next_image if z[:n] == y] for y in expected}
    assert len(output_fibers[zero]) == 2
    assert all(len(zs) == 1 for y, zs in output_fibers.items() if y != zero)
    for a in product((0, 1), repeat=n+1):
        assert f(a)[:n] == f(a[:n])
    return {'n': n, 'domain_size': len(domain), 'image_size': len(expected),
            'input_fiber_at_zero': image_counts[zero],
            'nonzero_input_fiber_sizes': [image_counts[unit(n, j)] for j in range(n)],
            'one_output_fiber_splits': True, 'integer_power_checks': power_checks,
            'prefix_compatibility': 'PASS'}


def tree_counts(max_level=25):
    # Encode a nonzero value by its one-based coordinate, and zero by0.
    # A coherent finite path is determined by its first switch or no switch.
    paths = {()}
    out = []
    for n in range(max_level+1):
        new = set()
        for path in paths:
            previous = path[-1] if path else 0
            for value in range(n+1):
                if not path or (value if value <= n-1 else 0) == previous:
                    new.add(path+(value,))
        paths = new
        assert len(paths) == n+1
        assert {path[-1] for path in paths} == set(range(n+1))
        for path in paths:
            nonzero = [value for value in path if value]
            assert not nonzero or len(set(nonzero)) == 1
        out.append({'depth': n, 'coherent_prefixes': len(paths)})
    return out


def negative_controls():
    e1, e2 = (1, 0), (0, 1)
    assert f(plus(e1, e2)) != plus(f(e1), f(e2))
    swap = lambda a: (a[1], a[0])
    assert f(swap((1, 1))) != swap(f((1, 1)))
    # One-variable words on F2^n are the zero map or the identity.
    assert f(e1) != (0, 0)
    assert f((1, 1)) != (1, 1)
    return {'nonadditive': True, 'not_one_variable_word': True,
            'coordinate_swap_naturality_fails': True,
            'scope': 'Extra confirmation of non-word status; no general fusion theorem follows.'}


def reproduce_author():
    source = Path(__file__).resolve().parent.parent/'topological/check_thin_branch.py'
    submitted = source.with_name('THIN_BRANCH_CHECK.json')
    ns = runpy.run_path(str(source), run_name='fresh_review_import')
    reproduced = ns['check']()
    original = json.loads(submitted.read_text())
    reproduced.pop('timestamp_utc')
    original.pop('timestamp_utc')
    assert reproduced == original
    return {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'submitted_sha256': hashlib.sha256(submitted.read_bytes()).hexdigest(),
            'all_non_timestamp_fields_identical': True, 'inputs_edited': False}


def main():
    levels = [check_level(n) for n in range(13)]
    out = {'utc': datetime.now(timezone.utc).isoformat(),
           'arithmetic': 'exact coordinate tuples over F2',
           'scope': 'Non-word compact-map obstruction and finite profile only; no solution of21.122',
           'independent_levels': levels, 'coherent_prefix_counts': tree_counts(),
           'negative_controls': negative_controls(), 'author_reproduction': reproduce_author()}
    Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'verdict': 'PASS', 'levels': len(levels),
                      'power_checks': sum(x['integer_power_checks'] for x in levels),
                      'author_reproduction': 'identical apart fromUTC', 'non_word_scope': True}))


if __name__ == '__main__':
    main()
