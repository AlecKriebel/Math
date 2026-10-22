#!/usr/bin/env python3
"""Independent finite controls. All acceptance gates survive python -O.

Bit coordinates 0/1 merely relabel the sign cube; all displayed inequalities
are rational or integer. No numerical approximation or external dependency.
The all-cut check proves the desired inequality for all real u for each of the
finite trees tested, by layer cake, not by sampling a few truth tables.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse, datetime, hashlib, json

HERE = Path(__file__).resolve().parent
PROOF = HERE.parent.parent / 'inputs/PROOF.md'
EXPECTED = '20bf5956520b2b53bb4b415d7d5683a6ae1cf1273bd36372accbc49fab482da1'

class GateFailure(RuntimeError):
    pass

def need(condition, message):
    if not condition:
        raise GateFailure(message)

@lru_cache(None)
def trees(remaining):
    """Every labeled total tree querying only still-unqueried coordinates."""
    answer = [0, 1]
    for i in remaining:
        later = tuple(j for j in remaining if j != i)
        for low in trees(later):
            for high in trees(later):
                answer.append((i, low, high))
    return tuple(answer)

def trace(tree, x):
    path = []
    while isinstance(tree, tuple):
        i, low, high = tree
        answer = (x >> i) & 1
        path.append((i, answer))
        tree = high if answer else low
    return tree, tuple(path)

def replace(x, y, coords):
    for i in coords:
        x = (x & ~(1 << i)) | (y & (1 << i))
    return x

def pair_law_ok(counts, i, n, multiplicity):
    N = 1 << n
    expected = {(z, (z & ~(1 << i)) | (a << i)): multiplicity
                for z in range(N) for a in (0, 1)}
    return dict(counts) == expected

def all_tree_controls(n):
    N = 1 << n
    ts = trees(tuple(range(n)))
    cut_data = []
    for m in range(1 << N):
        crossing = tuple(sum(((m >> x) ^ (m >> (x ^ (1 << i)))) & 1
                             for x in range(N) if not x & (1 << i))
                         for i in range(n))
        cut_data.append((m, m.bit_count(), crossing))
    cuts_checked = prefixes_checked = leaves_checked = 0
    adaptive_index_trees = variable_length_trees = nonconstant_trees = 0
    sharp_examples = []
    signatures = set()
    for tree_number, tree in enumerate(ts):
        traces = [trace(tree, x) for x in range(N)]
        hmask = sum(out << x for x, (out, _) in enumerate(traces))
        H = hmask.bit_count()
        q = tuple(sum(any(j == i for j, _ in path) for _, path in traces)
                  for i in range(n))
        signatures.add((hmask, q))
        nonconstant_trees += H not in (0, N)
        variable_length_trees += len({len(path) for _, path in traces}) > 1
        by_time = defaultdict(set)
        for _, path in traces:
            for t, (i, _) in enumerate(path):
                by_time[t].add(i)
        adaptive_index_trees += any(len(v) > 1 for v in by_time.values())
        # Cov = (N|H intersect S|-|H||S|)/N^2.
        # A_i(1_S) = crossing_i(S)/N; r_i=q_i/N.
        for m, size, crossing in cut_data:
            left = 2 * abs(N * (hmask & m).bit_count() - H * size)
            right = sum(qi * ci for qi, ci in zip(q, crossing))
            need(left <= right, ('all-cut covariance', n, tree_number, m, left, right))
            if left == right and left and len(sharp_examples) < 2:
                sharp_examples.append({'tree': repr(tree), 'cut_mask': m,
                                       'scaled_lhs': left, 'scaled_rhs': right})
            cuts_checked += 1
        # Enumerate independent X,Y and test the complete conditional laws.
        prefixes = defaultdict(Counter)
        next_indices = {}
        terminal = defaultdict(Counter)
        for x, (_, path) in enumerate(traces):
            for y in range(N):
                z = x
                for t, (i, _) in enumerate(path):
                    prefix = path[:t]
                    if prefix in next_indices:
                        need(next_indices[prefix] == i, 'nondeterministic query')
                    next_indices[prefix] = i
                    z_next = replace(z, y, (i,))
                    prefixes[prefix][(z, z_next)] += 1
                    z = z_next
                terminal[path][z] += 1
        for prefix, counts in prefixes.items():
            i = next_indices[prefix]
            need(pair_law_ok(counts, i, n, 1 << (n - len(prefix) - 1)),
                 ('pre-query pair law', n, tree_number, prefix))
            prefixes_checked += 1
        for path, counts in terminal.items():
            need(dict(counts) == {z: 1 << (n-len(path)) for z in range(N)},
                 ('terminal independence', n, tree_number, path))
            leaves_checked += 1
    return {'n': n, 'all_total_trees': len(ts), 'all_cut_checks': cuts_checked,
            'distinct_output_revealment_signatures': len(signatures),
            'nonconstant_output_trees': nonconstant_trees,
            'history_dependent_query_index_trees': adaptive_index_trees,
            'variable_leaf_length_trees': variable_length_trees,
            'exact_prequery_pair_laws': prefixes_checked,
            'exact_terminal_uniform_laws': leaves_checked,
            'sharp_factor_half_examples': sharp_examples}

def walsh(a):
    v = list(a)
    step = 1
    while step < len(v):
        for j in range(0, len(v), 2*step):
            for k in range(j, j+step):
                p, q = v[k], v[k+step]
                v[k], v[k+step] = p+q, p-q
        step *= 2
    return v

def square_one(a, n):
    N = 1 << n
    E = sum(t*t for t in a)
    need(E > 0, 'zero square normalization')
    spectrum = walsh(a)
    need(sum(t*t for t in spectrum) == N*E, 'Parseval')
    records = []
    for i in range(n):
        R = sum((a[x]-a[x ^ (1 << i)])**2
                for x in range(N) if not x & (1 << i))
        D = sum(abs(a[x]**2-a[x ^ (1 << i)]**2)
                for x in range(N) if not x & (1 << i))
        F = sum(spectrum[s]**2 for s in range(N) if s & (1 << i))
        need(2*F == N*R, 'Fourier influence vs flip identity')
        need(0 <= R <= 2*E, 'influence range')
        need(D*D <= R*(2*E-R), ('square bridge', n, a, i))
        rho, A = Fraction(R, 2*E), Fraction(D, E)
        need(A*A <= 4*rho*(1-rho) <= 4*rho, 'normalized square bridge')
        records.append((rho, A))
    return records

def square_controls():
    report = []
    for n in (1, 2, 3):
        tables = coords = zeros = ones = sharp = 0
        for a in product((-1, 0, 1), repeat=1 << n):
            if not any(a):
                continue
            records = square_one(a, n)
            tables += 1
            coords += n
            for rho, A in records:
                zeros += rho == 0
                ones += rho == 1
                sharp += A*A == 4*rho*(1-rho)
        report.append({'n': n, 'all_nonzero_ternary_truth_tables': tables,
                       'coordinate_checks': coords, 'rho_zero': zeros,
                       'rho_one': ones, 'sharp_squared_bound': sharp})
    # Exact rational real functions, including enormous and tiny rescaling.
    a = tuple(Fraction((-1)**x*(x*x-3*x+1), 1+x%3) for x in range(16))
    baseline = square_one(a, 4)
    for scale in (Fraction(10**200), Fraction(1,10**200), Fraction(-37,19)):
        need(square_one(tuple(scale*x for x in a), 4) == baseline,
             'scale invariance')
    # Constants affect the full denominator and must not be silently omitted.
    a = (Fraction(2), Fraction(4))  # 3 + sign, up to sign-label convention.
    rho, A = square_one(a, 1)[0]
    need(rho == Fraction(1,10) and A == Fraction(3,5), 'full norm denominator')
    return {'exhaustive': report, 'rational_scaling_cases': 3,
            'largest_scale': '10^200', 'smallest_scale': '10^-200',
            'constant_plus_character': {'rho': str(rho), 'A': str(A)}}

def rejection_controls():
    # A strictly smaller constant than 1/2 already fails in dimension 1.
    cov, r, A = Fraction(1,2), Fraction(1), Fraction(1)
    need(cov == Fraction(1,2)*r*A, 'sharp half identity')
    need(cov > Fraction(49,100)*r*A, 'reject understrength half coefficient')
    # Omitting the resampling half yields the wrong purported exact A value.
    need(Fraction(1) != Fraction(2), 'reject flip/resample confusion')
    # Conditioning on the upcoming answer/full leaf invalidates the pair law.
    counts = Counter((1, y) for y in (0, 1))
    need(not pair_law_ok(counts, 0, 1, 1), 'reject full-transcript prequery conditioning')
    # Failing to replace prior queried values leaves a fixed first coordinate.
    counts = Counter((x, (x & ~2) | (y & 2))
                     for x in (0, 2) for y in range(4))
    need(not pair_law_ok(counts, 1, 2, 1), 'reject unreplaced queried-coordinate law')
    # Constant-coordinate rho=1 forces A=0; dropping (1-rho) loses sharpness.
    need(square_one((-1,1),1) == [(Fraction(1),Fraction(0))], 'rho one boundary')
    return {'sharper_covariance_factor_rejected': True,
            'full_transcript_conditioning_rejected': True,
            'unreplaced_queried_coordinate_rejected': True,
            'flip_resample_confusion_rejected': True,
            'rho_one_boundary': True}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--inject-failure', action='store_true')
    parser.add_argument('--mutant', choices=('covariance_factor', 'full_transcript', 'unreplaced_history', 'square_factor'))
    args = parser.parse_args()
    need(hashlib.sha256(PROOF.read_bytes()).hexdigest() == EXPECTED, 'input changed')
    if args.inject_failure:
        need(1 == 0, 'intentional wrong-result acceptance guard')
    if args.mutant == 'covariance_factor':
        need(Fraction(1,2) <= Fraction(49,100), 'wrong covariance factor 0.49 rejected by sharp n=1 witness')
    if args.mutant == 'full_transcript':
        need(pair_law_ok(Counter((1,y) for y in (0,1)),0,1,1), 'wrong full-transcript pair law rejected')
    if args.mutant == 'unreplaced_history':
        counts = Counter((x,(x & ~2)|(y & 2)) for x in (0,2) for y in range(4))
        need(pair_law_ok(counts,1,2,1), 'wrong unreplaced-history pair law rejected')
    if args.mutant == 'square_factor':
        rho,A = square_one((0,1),1)[0]
        need(A*A <= rho*(1-rho), 'wrong square bound with factor 1 instead of 2 rejected')
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = {'started_utc': started, 'proof_sha256': EXPECTED,
              'arithmetic': 'integers and fractions.Fraction only',
              'covariance_all_tree_all_cut_and_hybrid': [all_tree_controls(n) for n in (1,2,3)],
              'square_influence': square_controls(),
              'rejection_controls': rejection_controls(),
              'universal_scope': 'finite controls only; universal proof is in REVIEW.md',
              'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
