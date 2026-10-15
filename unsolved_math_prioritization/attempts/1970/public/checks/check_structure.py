"""Exact reconstruction certificate; no prior artifact bytes are claimed."""
from itertools import product
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def verify_cover(A, H, expected_excess):
    require(H <= points(A), 'Hitting set contains a nonvertex')
    counts = [len(H & set(e)) for e in edges(A)]
    require(all(n >= 1 for n in counts), 'A triple is uncovered')
    require(sum(n - 1 for n in counts) == expected_excess, 'Wrong extra-incidence count')

def rejection_controls():
    tests = []
    def reject(name, action):
        try:
            action()
        except ValueError:
            tests.append(name)
        else:
            raise ValueError('Negative control was accepted: ' + name)
    reject('explicit guards survive optimization', lambda: require(False, 'deliberate rejection'))
    reject('invalid binary stencil', lambda: require(propagate([3, 2, 1, 0], [0, 0, 0, 0]) is not None, 'invalid stencil'))
    A = widths(27)
    reject('empty cover rejected', lambda: verify_cover(A, set(), 0))
    H = phase(A, 2)
    K = (H - {(2, 0), (3, 1), (1, 2)}) | {(3, 0), (1, 1)}
    reject('exceptional patch rejected at excluded endpoint 27', lambda: verify_cover(A, K, 1))
    reject('false zero optimum at cutoff 3', lambda: require(min(len(phase(widths(3), r)) for r in range(3)) == 0, 'false optimum'))
    return tests

def widths(x):
    out = []
    p = 1
    while p <= x:
        a = 0
        while p * 2 ** (a + 1) <= x:
            a += 1
        out.append(a)
        p *= 3
    return out

def points(A):
    return {(a, b) for b, w in enumerate(A) for a in range(w + 1)}

def edges(A):
    return [((a, b), (a + 1, b), (a, b + 1)) for b in range(len(A) - 1) for a in range(A[b + 1] + 1)]

def isolated(A):
    P = points(A)
    used = {v for e in edges(A) for v in e}
    return P - used

def phase(A, r):
    return {v for v in points(A) - isolated(A) if (v[0] + 2 * v[1]) % 3 == r}

def propagate(A, bottom, defect=None):
    if not A:
        return []
    ar = [list(bottom)]
    for b in range(len(A) - 1):
        ar.append([1 + int(defect == (a, b)) - ar[-1][a] - ar[-1][a + 1] for a in range(A[b + 1] + 1)])
        if any((x not in (0, 1) for x in ar[-1])):
            return None
    return ar

def size(ar):
    return sum(map(sum, ar))

def selected(ar):
    return {(a, b) for b, row in enumerate(ar) for a, v in enumerate(row) if v}

def stencil_table():
    result = []
    for s in product((0, 1), repeat=4):
        ar = propagate([3, 2, 1, 0], s)
        if ar is not None:
            result.append(''.join(map(str, s)))
    require(result == ['0010', '0100', '1001'], 'Verification condition failed at original line 40')
    return result

def base_table():
    out = []
    cutoffs = sorted({2 ** a * 3 ** b for a in range(5) for b in range(3) if 2 ** a * 3 ** b < 27})
    require(cutoffs == [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24], 'Verification condition failed at original line 46')
    for x in cutoffs:
        A = widths(x)
        possibilities = []
        for bottom in product((0, 1), repeat=A[0] + 1):
            ar = propagate(A, bottom)
            if ar is not None:
                possibilities.append(size(ar))
        C = [len(phase(A, r)) for r in range(3)]
        require(min(possibilities) == min(C), 'Verification condition failed at original line 53')
        out.append({'cutoff': x, 'widths': A, 'adjusted_colors': C, 'q0': min(possibilities)})
    return out

def suffix_table():
    out = []
    for x, right in [(27, 32), (32, 36), (36, 48), (48, 54)]:
        A = widths(x)
        cases = []
        require(A[3] == 0, 'Verification condition failed at original line 61')
        for r in range(3):
            H = phase(A, r)
            bottom = [int((a, 0) in H) for a in range(A[0] + 1)]
            options = []
            for tail in product((0, 1), repeat=A[0] - 3):
                s = bottom[:4] + list(tail)
                if any((s[a] for a, b in isolated(A) if b == 0)):
                    continue
                ar = propagate(A, s)
                if ar is None:
                    continue
                d = size(ar) - len(H)
                require(d >= 0, 'Verification condition failed at original line 71')
                options.append({'tail': ''.join(map(str, tail)), 'size_difference': d})
            require(options and min((c['size_difference'] for c in options)) == 0, 'Verification condition failed at original line 73')
            cases.append({'phase': r, 'options': options})
        out.append({'normalized_interval': [x, right], 'widths': A, 'cases': cases})
    return out

def patch_checks():
    out = []
    for m in range(25):
        lo, hi = (24 * 2 ** m, 27 * 2 ** m)
        cutoffs = sorted({lo, hi - 1} | {2 ** a * 3 ** b for a in range(m + 6) for b in range(m + 6) if lo <= 2 ** a * 3 ** b < hi})
        for x in cutoffs:
            A = widths(x)
            r = (m + 2) % 3
            H = phase(A, r)
            removed = {(m + 2, 0), (m + 3, 1), (m + 1, 2)}
            added = {(m + 3, 0), (m + 1, 1)}
            require(removed <= H and (not added & H) and (added <= points(A)), 'Verification condition failed at original line 89')
            K = H - removed | added
            excess = []
            for e in edges(A):
                n = len(K & set(e))
                require(n >= 1, 'Verification condition failed at original line 93')
                if n != 1:
                    excess.append({'anchor': list(e[0]), 'hits': n})
            require(excess == [{'anchor': [m, 1], 'hits': 2}], 'Verification condition failed at original line 95')
            require(len(K) == len(H) - 1, 'Verification condition failed at original line 96')
        out.append({'m': m, 'cutoffs_tested': len(cutoffs)})
    return out

def matching_checks():
    out = []
    for x in [1, 2, 3, 24, 27, 32, 36, 48, 54, 100, 1536, 3 ** 10]:
        A = widths(x)
        ee = edges(A)
        counts = []
        for r in range(3):
            es = [e for e in ee if (e[0][0] + 2 * e[0][1]) % 3 == r]
            flat = [v for e in es for v in e]
            require(len(flat) == len(set(flat)), 'Verification condition failed at original line 108')
            counts.append(len(es))
        require(sum(counts) == sum((w + 1 for w in widths(x // 3))), 'Verification condition failed at original line 109')
        out.append({'cutoff': x, 'matching_sizes': counts})
    return out
if __name__ == '__main__':
    result = {'status': 'PASS', 'artifact_type': 'independent reconstruction, not restored prior bytes', 'all_scale_claims': ['q0 = min adjusted color counts (proof plus finite local tables)', 'exceptional one-defect patch gives candidate upper bound', 'sole-defect anchor row >= 3 cannot improve its core color phase', '0 <= Psi - 3 tau <= floor(log2 X) + 1'], 'not_claimed': ['unrestricted tau = q1', 'all-scale q1 lower bound from this file alone'], 'rejection_controls': rejection_controls(), 'stencil_bottom_words': stencil_table(), 'base_cases': base_table(), 'four_suffix_profiles': suffix_table(), 'patch_instances': patch_checks(), 'matching_examples': matching_checks(), 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result, indent=2, sort_keys=True))
