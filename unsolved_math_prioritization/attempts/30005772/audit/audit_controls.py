#!/usr/bin/env python3
"""Independent exact-arithmetic audit. Standard library only; no author imports.

Run: python3 audit_controls.py
No source documents, private records, network, floating point, or dependencies.
Output is deterministic JSON. Finite checks supplement the report's proofs.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction as F
from itertools import permutations, product
from math import comb, factorial
import json

checks = Counter()
mutations = []


def require(condition, category):
    if not condition:
        raise AssertionError(category)
    checks[category] += 1


def reject(name, incorrect, correct):
    require(incorrect != correct, 'negative_controls')
    mutations.append({'name': name, 'incorrect': incorrect, 'correct': correct})


def moment(n, k):
    # Expand the shifted exponential integral directly; no recurrence.
    return sum(comb(n, j) * (k - 1) ** (n - j) * factorial(j)
               for j in range(n + 1))


def sparse_row(start, n, k, cap=None):
    # At time t the support is within [max(0,start-t),start+t].
    row = {start: 1}
    for _ in range(n):
        nxt = defaultdict(int)
        for i, weight in row.items():
            for j, edge in ((i - 1, i), (i, 2 * i + k), (i + 1, i + 1)):
                if j >= 0 and (cap is None or j <= cap):
                    nxt[j] += weight * edge
        row = dict(nxt)
    return row


def prefix_integral(n, h, k):
    if h > n:
        return 0
    return comb(n, h) * sum(
        comb(n - h, a) * (k - 1) ** (n - h - a) * factorial(a + h)
        for a in range(n - h + 1))


def step_options(h, m):
    # Code: next height, type, label. Types: 0=vertical,1=U,2=L,3=fixed.
    ans = []
    for target in (h - 1, h + 1):
        if target >= 0:
            ans += [(target, 0, lab) for lab in range(1, max(h, target) + 1)]
    ans += [(h, typ, lab) for typ in (1, 2) for lab in range(1, h + 1)]
    ans += [(h, 3, lab) for lab in range(1, m + 1)]
    return ans


def prefix_sets(n, m):
    paths = [()]
    for _ in range(n):
        paths = [p + (s,) for p in paths
                 for s in step_options(p[-1][0] if p else 0, m)]
    bins = defaultdict(list)
    for p in sorted(paths):
        bins[p[-1][0] if p else 0].append(p)
    return dict(bins)


def parity(path):
    return (-1) ** sum(t == 3 for _, t, _ in path)


def reverse_path(p, start):
    old = [start] + [s[0] for s in p]
    return tuple((old[j], p[j][1], p[j][2]) for j in reversed(range(len(p))))


def cancel(paths):
    stack, partner = [], {}
    for p in paths:
        if not stack or parity(p) == parity(stack[-1]):
            stack.append(p)
        else:
            q = stack.pop()
            partner[p], partner[q] = q, p
    return partner, set(stack)


def decode(path):
    # Restore downstep label pairs, then install permutation edges.
    partners, stack, last = {}, [], 0
    for t, (h, kind, label) in enumerate(path):
        if h > last:
            stack.append(t)
        elif h < last:
            partners[t] = stack.pop()
        last = h
    assert last == 0 and not stack
    upper, lower, fixed, edges = [], [], [], {}
    height = 0
    for v, (h, kind, lab) in enumerate(path):
        if kind == 3:
            edges[v] = v
            fixed.append(lab)
        elif h > height:
            upper += [v]
            lower += [v]
        elif h < height:
            source = upper.pop(path[partners[v]][2] - 1)
            target = lower.pop(lab - 1)
            edges[source], edges[v] = v, target
        elif kind == 1:
            source = upper.pop(lab - 1)
            edges[source] = v
            upper += [v]
        elif kind == 2:
            target = lower.pop(lab - 1)
            edges[v] = target
            lower += [v]
        height = h
    assert not upper and not lower
    perm = tuple(edges[v] for v in range(len(path)))
    assert sorted(perm) == list(range(len(path)))
    return perm, tuple(fixed)


def encode(perm, colors):
    # Independently recover raw ranks from boundary-crossing edges themselves.
    inv = [perm.index(v) for v in range(len(perm))]
    ci, raw = 0, []
    for v in range(len(perm)):
        upper = [u for u in range(v) if perm[u] >= v]
        lower = [u for u in range(v) if inv[u] >= v]
        assert len(upper) == len(lower)
        h, a, b = len(upper), inv[v], perm[v]
        if a == v:
            raw.append((h, 3, colors[ci])); ci += 1
        elif a > v and b > v:
            raw.append((h + 1, 0, None))
        elif a < v and b < v:
            raw.append((h - 1, 0, (upper.index(a) + 1, lower.index(b) + 1)))
        elif a < v:
            raw.append((h, 1, upper.index(a) + 1))
        else:
            raw.append((h, 2, lower.index(b) + 1))
    result, opens, old = list(raw), [], 0
    for j, (h, typ, label) in enumerate(raw):
        if h > old:
            opens.append(j)
        elif h < old:
            i = opens.pop()
            result[i] = (raw[i][0], 0, label[0])
            result[j] = (h, 0, label[1])
        old = h
    return tuple(result)


@lru_cache(None)
def linear_word(i, j, h):
    # Recurrence for the five-letter word generating function, not a multinomial.
    if min(i, j, h) < 0:
        return 0
    if i == j == h == 0:
        return 1
    if max(i, j, h) > i + j + h - max(i, j, h):
        return 0
    return (linear_word(i-1, j-1, h) + linear_word(i-1, j, h-1)
            + linear_word(i, j-1, h-1) + 2*linear_word(i-1, j-1, h-1))


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def integral(poly):
    return sum(c * factorial(j) for j, c in enumerate(poly))


def q_basis(n):
    # Build Q from its three-term recurrence, rather than explicit coefficients.
    basis = [[F(1)]]
    for h in range(n):
        p = [F(0)] * (h + 2)
        for j, c in enumerate(basis[h]):
            p[j + 1] += c
            p[j] -= (2*h + 1)*c
        if h:
            for j, c in enumerate(basis[h - 1]):
                p[j] -= h*c
        basis.append([c / (h + 1) for c in p])
    return basis


def square_weight(i, j, k):
    a, b = sorted((i, j))
    if a == b:
        return a*a + (2*a+k)**2 + (a+1)**2
    if b == a + 1:
        return 2*(a+1)*(2*a+k+1)
    if b == a + 2:
        return (a+1)*(a+2)
    return 0


def block_row(n, k, block_size, start=0, cap=None):
    row = {start: 1}
    for _ in range(n):
        out = defaultdict(int)
        for i, v in row.items():
            for j, weight in sparse_row(i, block_size, k).items():
                if cap is None or j <= cap:
                    out[j] += v*weight
        row = dict(out)
    return row


def main():
    # Direct permutation polynomials, independent of derangement recurrences.
    for n in range(9):
        fixed_counts = Counter(sum(i == v for i, v in enumerate(p))
                               for p in permutations(range(n)))
        for k in range(-8, 9):
            direct = sum(num*k**f for f, num in fixed_counts.items())
            require(direct == moment(n, k), 'direct_permutation_moments')
    for k in range(-16, 8):
        for n in range(33):
            row = sparse_row(0, n, k)
            require(row.get(0, 0) == moment(n, k), 'sparse_moments')
            require(sum(v*v for v in row.values()) == moment(2*n, k), 'even_squares')
            for h in range(n+3):
                require(row.get(h, 0) == prefix_integral(n, h, k),
                        'rodrigues_prefix_integral')
            require(sparse_row(0, n, k, cap=n) == row, 'reachable_truncation')

    # Independently decode ALL symmetric histories and compare whole classes.
    for n in range(7):
        for m in range(3):
            hist = prefix_sets(n, m).get(0, [])
            decoded = set()
            for p in hist:
                obj = decode(p)
                require(encode(*obj) == p, 'independent_history_roundtrip')
                require(obj not in decoded, 'independent_history_injection')
                require(parity(p) == (-1)**len(obj[1]), 'fixed_point_sign')
                decoded.add(obj)
            expected = {(p, colors) for p in permutations(range(n))
                        for colors in product(range(1,m+1),
                            repeat=sum(i == v for i,v in enumerate(p)))}
            require(decoded == expected, 'independent_history_surjection')

    # Pair-space construction includes a new exhaustive n=4, k=-1 case.
    for n, m in [(n,m) for n in range(4) for m in range(1,4)] + [(4,1)]:
        fixed, negatives = 0, 0
        for h, paths in prefix_sets(n,m).items():
            paired, residual = cancel(paths)
            require(len({parity(p) for p in residual}) <= 1, 'residual_same_sign')
            require(len(residual) == abs(prefix_integral(n,h,-m)), 'residual_size')
            for a,b in product(paths, repeat=2):
                def act(x,y):
                    return (paired[x],y) if x in paired else ((x,paired[y]) if y in paired else (x,y))
                x,y = act(a,b)
                require(act(x,y) == (a,b), 'independent_pair_involution')
                source = a + reverse_path(b,0)
                target = x + reverse_path(y,0)
                obj = decode(target)
                require(encode(*obj) == target, 'transported_target_valid')
                require(reverse_path(reverse_path(b,0),h) == b, 'reversal_labels')
                if (a,b) == (x,y):
                    require(parity(source) == 1, 'all_survivors_positive')
                    fixed += 1
                else:
                    require(parity(source) == -parity(target), 'pair_sign_reversal')
                negatives += parity(source) < 0
        require(fixed == moment(2*n,-m), 'independent_even_residual_count')
        require(fixed + 2*negatives == moment(2*n,m), 'every_negative_is_paired')

    # Non-symmetric raw-history weights must not be used in a square sum.
    reject('omit_label_symmetrization', 1**2+2**2+1**2, moment(4,0))
    reject('truncate_local_graph_to_vertices_0_1',
           block_row(2,-1,2,cap=1).get(0,0), moment(4,-1))
    reject('omit_upper_excursion_from_square_diagonal', 1, moment(2,-1))
    sample = next((p,q) for ps in prefix_sets(2,1).values()
                  for p,q in cancel(ps)[0].items())
    a,b = sample
    reject('flip_both_matched_halves', parity(a)*parity(a), -parity(b)*parity(b))

    # Local graph, terminal vector, negative-cycle obstruction.
    require([prefix_integral(5,h,-1) for h in range(6)] ==
            [8,120,320,480,360,120], 'local_terminal_vector')
    for n in range(31):
        row = block_row(n,-1,2)
        require(all(v >= 0 for v in row.values()), 'local_nonnegative')
        require(row.get(0,0) == moment(2*n,-1), 'local_even_walks')
        require(sum(v*prefix_integral(5,h,-1) for h,v in row.items()) ==
                moment(2*n+5,-1), 'local_odd_walks')
    for k in range(-80,9):
        for i in range(13):
            actual = sparse_row(i,2,k)
            for j in range(16):
                require(actual.get(j,0) == square_weight(i,j,k), 'square_formula')
        if k <= -2:
            s=(-k)//2
            cycle = [s-1,s,s+1,s-1] if k%2==0 else [s-1,s,s+2,s+1,s-1]
            val=1
            for i,j in zip(cycle,cycle[1:]):
                val *= square_weight(i,j,k)
            require(val < 0, 'negative_cycle')
    absolute_row = {0:1}
    for _ in range(3):
        nxt = defaultdict(int)
        for i,v in absolute_row.items():
            for j in range(max(0,i-2),i+3):
                nxt[j] += v*abs(square_weight(i,j,-2))
        absolute_row = nxt
    reject('take_absolute_values_of_all_square_weights', absolute_row[0], moment(6,-2))

    # Triple-product integrals vs independent five-letter word recurrence.
    basis=q_basis(18)
    for i in range(9):
        for j in range(9):
            pair=poly_mul(basis[i],basis[j])
            require(integral(pair) == int(i==j), 'orthonormality')
            for h in range(i+j+2):
                coeff=integral(poly_mul(pair,basis[h]))
                require(coeff == linear_word(i,j,h), 'linearization_word_recurrence')
                require(coeff >= 0 and coeff.denominator == 1, 'linearization_integrality')
    reject('remove_second_uvw_letter', 1, linear_word(1,1,1))

    # Entrywise eventual positivity, including high starting vertices.
    for r in range(2,21):
        k=1-r
        for n in range(4*r-1,4*r+4):
            row=sparse_row(0,n,k)
            require(all(row[h] > 0 for h in range(n+1)), 'uniform_prefix_bound')
            for i in [0,1,2,7,19,100,1000]:
                require(all(v >= 0 for v in sparse_row(i,n,k).values()),
                        'eventual_rows_high_vertices')
        for M in range(4*r,4*r+20):
            require(factorial(M) > 3**r*r**M, 'stronger_rational_bound_controls')
    for r in range(2,7):
        k,s=1-r,4*r
        for i in range(8):
            row=sparse_row(i,s,k)
            for j in range(8):
                via_words=sum(linear_word(i,j,h)*prefix_integral(s,h,k)
                              for h in range(min(s,i+j)+1))
                require(via_words == row.get(j,0), 'eventual_transfer_word_formula')
        for q in range(1,5):
            walked=block_row(q-1,k,s)
            require(max(walked) <= (q-1)*s, 'block_reachability_bound')
            for t in range(s):
                terminal={h:prefix_integral(s+t,h,k) for h in range(s+t+1)}
                require(all(v>0 for v in terminal.values()), 'terminal_colors_positive')
                count=sum(v*terminal.get(h,0) for h,v in walked.items())
                require(count == moment(q*s+t,k), 'eventual_block_graph')
    require(moment(1,-1)<0 and moment(3,-1)<0 and moment(5,-1)>0,
            'negative_odd_scope')
    require([prefix_integral(2,h,-1)*prefix_integral(3,h,-1) for h in range(3)]
            == [-4,0,12], 'unequal_half_mixed_signs')
    reject('all_size_unsigned_interpretation', abs(moment(3,-2)), moment(3,-2))
    print(json.dumps({'status':'PASS_PARTIAL_CONTROLS',
        'checks':dict(sorted(checks.items())), 'total_assertions':sum(checks.values()),
        'negative_mutations_rejected':mutations,
        'limits':'Finite controls support the universal proof; no all-size, naturalness, novelty, or peer-review claim.'},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
