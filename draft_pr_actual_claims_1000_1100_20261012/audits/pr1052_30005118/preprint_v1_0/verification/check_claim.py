#!/usr/bin/env python3
"""New finite corroboration; explicit guards remain active under Python -O."""
import json

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def subsets(values):
    values = tuple(values)
    for mask in range(1 << len(values)):
        yield frozenset(x for i, x in enumerate(values) if mask & (1 << i))

def sums(a, n=None):
    return frozenset(x+y if n is None else (x+y) % n for x in a for y in a)

def transfer(s, restricted=False):
    s = frozenset(s)
    if not s:
        return 3, frozenset({0}) if restricted else frozenset()
    t = min(s)
    if t % 2:
        return 5, frozenset({0, 1})
    b = frozenset(x-t for x in s)
    return max(3, 2*max(b)+1), b

def verify_sparse(n, b, a):
    if type(n) is not int or n < 1:
        return False
    if not isinstance(b, list) or not isinstance(a, list):
        return False
    if any(type(x) is not int or not 0 <= x < n for x in b+a):
        return False
    if b != sorted(set(b)) or a != sorted(set(a)) or len(a) > len(b):
        return False
    return sums(a, n) == frozenset(b)

def verify_dense(n, b, a):
    if type(n) is not int or n < 1 or not isinstance(b, str) or not isinstance(a, str):
        return False
    if len(b) != n or len(a) != n or set(b+a)-set('01'):
        return False
    return sums([i for i, bit in enumerate(a) if bit == '1'], n) == frozenset(i for i, bit in enumerate(b) if bit == '1')

def main():
    roots = targets = strong = 0
    for n in range(1, 12):
        m = (n-1)//2
        integer_targets = {sums(a) for a in subsets(range(m+1))}
        cyclic_targets = set()
        for a in subsets(range(n)):
            b = sums(a, n)
            roots += 1
            cyclic_targets.add(b)
            require(len(a) <= len(b), 'translation cardinality bound')
            if n % 2 and 0 in b and all(2*x < n for x in b):
                require(0 in a and a <= b and sums(a) == b, 'every canonical root lift')
                strong += 1
        if n % 2:
            for b in subsets(range(m+1)):
                if 0 in b:
                    require((b in cyclic_targets) == (b in integer_targets), 'existence transfer')
                    targets += 1
    sources = 0
    for s in subsets(range(-4, 5)):
        for restricted in (False, True):
            n, b = transfer(s, restricted)
            if restricted:
                require(n % 2 and 0 in b and all(2*x < n for x in b), 'all restricted outputs')
            if not s:
                require(b in (frozenset(), frozenset({0})), 'empty branch')
            elif min(s) % 2:
                require((n, b) == (5, frozenset({0, 1})), 'negative/positive odd minimum')
            else:
                require(b == frozenset(x-min(s) for x in s) and n > 2*max(b), 'normalization')
        sources += 1
    r = (-(1 << 16384), -(1 << 16384)+(1 << 8192))
    n, b = transfer(sums(r))
    a = sorted(x-min(r) for x in r)
    require(verify_sparse(n, sorted(b), a), 'large binary witness')
    valid = [verify_sparse(1, [0], [0]), verify_sparse(2, [0], [1]), verify_sparse(3, [], []), verify_dense(1, '1', '1'), verify_dense(2, '10', '01')]
    invalid = [verify_sparse(True, [0], [0]), verify_sparse(0, [], []), verify_sparse(3, [0, 0], [0]), verify_sparse(3, [3], [0]), verify_sparse(3, [1, 0], [0]), verify_sparse(3, [], [0]), verify_dense(3, '10', '100'), verify_dense(3, '200', '100'), verify_dense(0, '', '')]
    require(all(valid) and not any(invalid), 'encoding/verifier controls')
    require(sums({3}, 5) == {1} and sums({2}, 4) == {0}, 'boundary controls')
    require(sums({1, 4}, 5) == {0, 2, 3}, 'strict-bound control')
    # Explicit formula indices must be relabeled, not used as a numeric size.
    clauses = ((10**100, -(10**100), 7), (7, 7, 7))
    labels = {abs(x) for clause in clauses for x in clause}
    mapping = {x: i+1 for i, x in enumerate(sorted(labels))}
    relabeled = tuple(tuple((1 if x > 0 else -1)*mapping[abs(x)] for x in clause) for clause in clauses)
    require(max(abs(x) for clause in relabeled for x in clause) == 2, 'variable relabeling')
    q = len(labels)+len(clauses)
    require(q == 4 and 2**17*(2**8*q*q)**2*2**24 == 2**57*q**4, 'source numeric composition')
    require(8*(4*5**8)+2 == 12500002 < 2**24 and 512*16**2 == 2**17, 'reconstructed coarse constants')
    return {'all_checks_passed': True, 'universal_proof_role': 'finite corroboration only', 'cyclic_roots': roots, 'anchored_targets': targets, 'strong_root_checks': strong, 'signed_source_branch_checks': sources, 'huge_sparse_n_bits': n.bit_length(), 'valid_encoding_controls': len(valid), 'invalid_encoding_controls': len(invalid), 'formula_relabeling_and_source_constants_checked': True}

if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
