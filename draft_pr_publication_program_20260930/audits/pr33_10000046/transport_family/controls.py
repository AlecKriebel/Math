#!/usr/bin/env python3
"""Independent labeled Edmonds-Karp exact transport controls; no old imports.

Standard library only. Every numeric optimum is certified by a permutation or
rational coupling and a literal Hall set, verified separately by check_certificates.py.
"""
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import product, permutations
from math import factorial, lcm, prod
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
checks = 0


def require(condition, description):
    global checks
    if not condition:
        raise AssertionError(description)
    checks += 1


def labeled_paths(d, n, start):
    moves = [tuple(s if k == axis else 0 for k in range(d))
             for axis in range(d) for s in (-1, 1)]
    answer = []
    for word in product(range(2*d), repeat=n):
        p = [tuple(start)]
        for letter in word:
            p.append(tuple(a+b for a, b in zip(p[-1], moves[letter])))
        answer.append((word, tuple(p)))
    return answer


def rational_transport(p, q, allowed):
    """Integer-scaled Edmonds-Karp on original labels, not range groups."""
    na, nb = len(p), len(q)
    scale = lcm(*(a.denominator for a in p+q))
    left_caps = [int(a*scale) for a in p]
    right_caps = [int(a*scale) for a in q]
    sink = na+nb+1
    source = 0
    residual = [dict() for _ in range(sink+1)]
    initial = {}

    def add(a, b, capacity):
        residual[a][b] = capacity
        residual[b][a] = 0
        initial[a, b] = capacity

    for i, a in enumerate(left_caps):
        add(source, i+1, a)
    for i, j in allowed:
        add(i+1, na+j+1, scale+1)
    for j, b in enumerate(right_caps):
        add(na+j+1, sink, b)
    value = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            a = queue.popleft()
            for b, capacity in residual[a].items():
                if capacity > 0 and b not in parent:
                    parent[b] = a
                    queue.append(b)
        if sink not in parent:
            reached = set(parent)
            break
        b = sink
        delta = scale
        while parent[b] is not None:
            a = parent[b]
            delta = min(delta, residual[a][b])
            b = a
        b = sink
        while parent[b] is not None:
            a = parent[b]
            residual[a][b] -= delta
            residual[b][a] += delta
            b = a
        value += delta
    safe = [[Q(0) for _ in q] for _ in p]
    for i, j in allowed:
        safe[i][j] = Q(initial[i+1, na+j+1]-residual[i+1][na+j+1], scale)
    A = [i for i in range(na) if i+1 in reached]
    B = sorted({j for i, j in allowed if i in A})
    require(value == scale-sum(left_caps[i] for i in A)+sum(right_caps[j] for j in B),
            'integer flow equals literal Hall cut')
    return Q(value, scale), safe, A


def finite_case(d, n, displacement, mode='full'):
    X = labeled_paths(d, n, (0,)*d)
    Y = labeled_paths(d, n, displacement)
    L = len(X)

    def safe(a, b):
        if mode == 'synchronous':
            return all(x != y for x, y in zip(a, b))
        if mode == 'drop_zero':
            return set(a[1:]).isdisjoint(b[1:])
        return set(a).isdisjoint(b)

    allowed = [(i, j) for i, (_, a) in enumerate(X)
               for j, (_, b) in enumerate(Y) if safe(a, b)]
    optimum, flow, A = rational_transport([Q(1, L)]*L, [Q(1, L)]*L, allowed)
    pairing = [-1]*L
    for i, j in allowed:
        if flow[i][j]:
            require(flow[i][j] == Q(1, L), 'integral scaled flow on each used edge')
            require(pairing[i] == -1, 'left label once')
            pairing[i] = j
    unused_right = sorted(set(range(L))-set(pairing))
    for i in range(L):
        if pairing[i] < 0:
            pairing[i] = unused_right.pop(0)
    require(sorted(pairing) == list(range(L)), 'completed literal permutation')
    safe_count = sum(safe(X[i][1], Y[j][1]) for i, j in enumerate(pairing))
    require(Q(safe_count, L) == optimum, 'permutation gives exact optimum')
    for k in range(n+1):
        target = (2*d)**(n-k)
        for side in (Counter(X[i][0][:k] for i in range(L)),
                     Counter(Y[j][0][:k] for j in pairing)):
            require(len(side) == (2*d)**k and set(side.values()) == {target},
                    'every complete prefix-cylinder marginal exact')
    if L <= 8:
        edges = set(allowed)
        exhaustive = max(sum((i, j) in edges for i, j in enumerate(perm))
                         for perm in permutations(range(L)))
        require(exhaustive == safe_count, 'literal exhaustive permutations')
        deficiency = max(mask.bit_count()-len({j for i, j in allowed if mask & (1 << i)})
                         for mask in range(1 << L))
        require(L-deficiency == safe_count, 'all Hall subsets independently exhausted')
    return {'d': d, 'N': n, 'displacement': list(displacement), 'event': mode,
            'L': L, 'safe_count': safe_count, 'optimum': str(optimum),
            'permutation': pairing, 'Hall_A': A}


def weighted_case(p, q, allowed, name):
    p, q = list(map(Q, p)), list(map(Q, q))
    value, safe, A = rational_transport(p, q, allowed)
    r = [a-sum(row) for a, row in zip(p, safe)]
    s = [q[j]-sum(row[j] for row in safe) for j in range(len(q))]
    missing = 1-value
    C = [[safe[i][j]+(r[i]*s[j]/missing if missing else 0)
          for j in range(len(q))] for i in range(len(p))]
    require([sum(row) for row in C] == p, 'weighted full row marginals')
    require([sum(row[j] for row in C) for j in range(len(q))] == q,
            'weighted full column marginals')
    require(sum(C[i][j] for i, j in allowed) == value, 'weighted objective attained')
    return {'name': name, 'p': list(map(str, p)), 'q': list(map(str, q)),
            'E': allowed, 'optimum': str(value), 'Hall_A': A,
            'full_coupling': [[str(v) for v in row] for row in C]}


def first_hit_count(d, displacement):
    """Absorbing DP confined to the endpoint box; shortest hit must be monotone."""
    endpoint = tuple(abs(a) for a in displacement)
    active = {(0,)*d: 1}
    absorbed = 0
    for t in range(1, 11):
        new = Counter()
        for z, number in active.items():
            for axis in range(d):
                for sign in (-1, 1):
                    nxt = list(z)
                    nxt[axis] += sign
                    nxt = tuple(nxt)
                    if nxt == endpoint:
                        require(t == 10, 'first hit cannot precede graph distance')
                        absorbed += number
                    elif all(0 <= a <= bound for a, bound in zip(nxt, endpoint)):
                        new[nxt] += number
        active = new
    predicted = factorial(10)//prod(factorial(a) for a in endpoint)
    require(absorbed == predicted, 'absorbing shortest-path DP equals multinomial')
    return predicted


def main():
    cases = [(d, n, (2,)+(0,)*(d-1)) for d in (1, 2, 3) for n in (0, 1, 2, 3)]
    cases += [(4, 2, (2, 0, 0, 0)), (2, 2, (1, 1)), (3, 2, (1, 1, 0))]
    cases += [(3, 3, (10, 0, 0)), (4, 3, (10, 0, 0, 0)),
              (3, 3, (3, -4, 3)), (4, 2, (2, -3, 1, 4)),
              (1, 0, (0,)), (3, 1, (0, 0, 0)), (1, 10, (10,))]
    finite = [finite_case(*case) for case in cases]
    for d in (1, 2, 3):
        values = [Q(row['optimum']) for row in finite if row['d'] == d
                  and row['displacement'] == [2]+[0]*(d-1)]
        require(all(a >= b for a, b in zip(values, values[1:])), 'restriction monotonicity')
    # Full-range/time-zero controls solve both the actual and substituted graphs.
    sync = finite_case(1, 2, (2,), 'synchronous')
    dropped = finite_case(1, 0, (0,), 'drop_zero')
    require(sync['optimum'] == '1' and finite[2]['optimum'] == '3/4',
            'synchronous substitute falsely certifies full avoidance')
    require(dropped['optimum'] == '1' and finite[19]['optimum'] == '0',
            'omitting time zero falsely permits shared starts')
    finite += [sync, dropped]
    weighted = [weighted_case(['3/4', '1/4'], ['1/4', '3/4'], [(0, 0), (1, 1)],
                              'unequal_diagonal'),
                weighted_case(['3/4', '1/4'], ['1/4', '3/4'], [(0, 0)],
                              'unequal_single_edge'),
                weighted_case(['1', '0'], ['0', '1'], [(0, 0), (1, 1)],
                              'zero_weight_diagonal')]
    require(weighted[0]['optimum'] == '1/2', 'unweighted perfect matching is false for weights')
    require(weighted[1]['optimum'] == '1/4', 'unweighted half matching is false for weights')
    require(weighted[2]['optimum'] == '0', 'zero weight edges cannot convey mass')
    count_rows = []
    for d in (3, 4):
        for a in product(range(11), repeat=d):
            if sum(a) == 10:
                count_rows.append({'d': d, 'displacement': a,
                                   'words': first_hit_count(d, a)})
    for d, v in [(3, (3, -4, 3)), (4, (2, -3, 1, 4))]:
        count_rows.append({'d': d, 'displacement': v, 'words': first_hit_count(d, v)})
    # A finite-alphabet countermodel has fixed iid fair marginal laws throughout.
    vanishing = [weighted_case(['1/2']*2, ['1/2']*2, [(0, 0), (0, 1)], 'bit_N1')]
    for n in range(2, 7):
        L = 2**n
        vanishing.append(weighted_case([Q(1, L)]*L, [Q(1, L)]*L,
                                      [(0, j) for j in range(L)], 'bit_N'+str(n)))
    require([Q(row['optimum']) for row in vanishing] == [Q(1, 2**n) for n in range(1, 7)],
            'strictly positive consistent masses decay to zero')
    # All nearest-neighbor paths, correct every one-time law, wrong joint law.
    # At horizon three, alter only the four words passing through zero at t=2.
    bad = []
    for word in product((-1, 1), repeat=3):
        mass = Q(1, 8)
        if word in [(-1, 1, -1), (1, -1, 1)]:
            mass = Q(0)
        if word in [(-1, 1, 1), (1, -1, -1)]:
            mass = Q(1, 4)
        bad.append((mass, word))
    for t in range(4):
        fake, true = Counter(), Counter()
        for mass, word in bad:
            fake[sum(word[:t])] += mass
            true[sum(word[:t])] += Q(1, 8)
        require(fake == true, 'nearest-neighbor fake has each one-time marginal correct')
    require(any(mass != Q(1, 8) for mass, word in bad), 'fake violates complete three-step cylinder law')
    # Append an independent ordinary SRW after t=3: the correct law of X_3
    # and the Markov transition kernel preserve every later one-time law.
    moving = []
    for n in range(1, 7):
        pairs = []
        for word in product((0, 1), repeat=n):
            flipped = word[:-1]+(1-word[-1],)
            pairs.append((word, flipped))
        require(len({b for a, b in pairs}) == 2**n, 'moving-event coupling exact iid finite marginals')
        require(all(a[:-1] == b[:-1] and a != b for a, b in pairs),
                'moving equality event has zero mass while all earlier fixed events have one')
        moving.append({'N': n, 'R_N_mass': '0', 'all_R_k_for_k_lt_N_mass': '1'})
    mutants = [
        {'name': 'synchronous_for_full', 'rejected': True, 'actual': '3/4', 'mutant': '1'},
        {'name': 'delete_time_zero', 'rejected': True, 'actual': '0', 'mutant': '1'},
        {'name': 'unweighted_for_weighted', 'rejected': True, 'actual': '1/2', 'mutant': '1'},
        {'name': 'finite_positive_implies_positive_limit', 'rejected': True,
         'actual': 'lim 2^-N=0', 'mutant': 'positive'},
        {'name': 'one_time_laws_for_path_law', 'rejected': True,
         'actual': 'nearest-neighbor words have probabilities 0,1/8,1/4 rather than all 1/8',
         'mutant': 'valid complete SRW law'},
        {'name': 'moving_clopen_event_weak_passage', 'rejected': True,
         'actual': 'flip only bit N: pi_N(R_N)=0; weak diagonal limit has pi(R)=1',
         'mutant': 'vary N with measure'}]
    certificates = {'finite': finite, 'weighted': weighted, 'vanishing': vanishing,
                    'first_hits': count_rows, 'fake_path_law': [
                        {'mass': str(mass), 'word': word} for mass, word in bad],
                    'moving_clopen': moving}
    (HERE/'certificates.json').write_text(json.dumps(certificates, indent=2)+'\n')
    summary = {'pass': True, 'solver': 'original-label integer-scaled Edmonds-Karp',
               'checks': checks, 'finite_certificates': len(finite),
               'weighted_certificates': len(weighted), 'vanishing_certificates': len(vanishing),
               'distance_ten_counts': len(count_rows), 'mutants': mutants,
               'scope': 'Exact finite controls only; full universal result is PROOF.md; no uniform 3D bound.'}
    (HERE/'controls_results.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
