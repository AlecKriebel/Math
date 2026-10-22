import itertools, json, sys
from pathlib import Path
from functools import lru_cache
import sympy as s
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import search
D = Path(__file__).parent

def rank(t):
    return tuple((1 + sum((y < x for y in t)) for x in t))

def contained(p, k):
    return {rank(tuple((p[i] for i in inds))) for inds in itertools.combinations(range(len(p)), k)}

def tree(p):
    if len(p) == 1:
        return ('leaf',)
    for k in range(1, len(p)):
        if max(p[:k]) < min(p[k:]):
            return (1, tree(rank(p[:k])), tree(rank(p[k:])))
        if min(p[:k]) > max(p[k:]):
            return (-1, tree(rank(p[:k])), tree(rank(p[k:])))
    raise ValueError(p)

def valid(t):
    return t[0] == 'leaf' or (t[1][0] != t[0] and valid(t[1]) and valid(t[2]))
T = sorted((p for p in itertools.permutations(range(1, 5)) if p not in [(2, 4, 1, 3), (3, 1, 4, 2)] and (2, 3, 1) in contained(p, 3)))
if not T == search.T:
    raise RuntimeError('check.py:24: T==search.T')
results = json.loads((ROOT / 'all_length4_results.json').read_text())
if not len(results) == 255:
    raise RuntimeError('check.py:26: len(results)==255')
counts = {tuple(r['basis']): [1] for r in results}
totals = [1]
canonical = 0
for n in range(1, 8):
    masks = []
    trees = set()
    for p in itertools.permutations(range(1, n + 1)):
        p4 = contained(p, 4)
        if (2, 4, 1, 3) in p4 or (3, 1, 4, 2) in p4:
            continue
        t = tree(p)
        if not valid(t):
            raise RuntimeError('check.py:33: valid(t)')
        if not t not in trees:
            raise RuntimeError('check.py:33: t not in trees')
        trees.add(t)
        canonical += 1
        masks.append(set((''.join(map(str, q)) for q in p4)))
    totals.append(len(masks))
    for r in results:
        key = tuple(r['basis'])
        v = sum((not set(key) & m for m in masks))
        counts[key].append(v)
        if not v == r['coefficients'][n]:
            raise RuntimeError("check.py:38: v==r['coefficients'][n]")
x, A, F = s.symbols('x A F')
b = x / (1 - x)
expr = s.factor((A - x - x * x / (1 - x) - (1 / (1 - A) - 1 - A) * ((1 - x) ** (-2) - 1)) * (1 - A) * (1 - x) ** 2)
polyF = s.factor(expr.subs(A, 1 - 1 / F) * F ** 2)
disc = s.factor(s.discriminant(polyF, F))
print('POLY', polyF, s.solve(polyF, F))
sol = (-x - 1 + s.sqrt((1 - x) * (1 - 5 * x))) / (2 * x * (x - 2))
if not s.simplify(polyF.subs(F, sol)) == 0:
    raise RuntimeError('check.py:50: s.simplify(polyF.subs(F,sol))==0')
cs = [int(s.expand(s.series(sol, x, 0, 8).removeO()).coeff(x, n)) for n in range(8)]
if not cs == counts['3412',]:
    raise RuntimeError("check.py:52: cs==counts[('3412',)]")
report = {'permutation_bruteforce_through': 7, 'all_nonempty_length4_bases_checked': len(results), 'candidate_patterns': [''.join(map(str, t)) for t in T], 'ambient_counts': totals, 'canonical_trees_checked': canonical, 'all_count_matches': True, '3412_polynomial': str(polyF), '3412_discriminant': str(disc), '3412_branch': str(sol), '3412_counts': cs}
(D / 'exact_checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
transition_checks = 0
state_checks = 0
for r in results:
    B = [tuple(map(int, b)) for b in r['basis']]
    S, trans, leaf = search.automaton(B)
    if not len(S) == r['states']:
        raise RuntimeError("check.py:60: len(S)==r['states']")
    if not len(trans) == r['transitions']:
        raise RuntimeError("check.py:61: len(trans)==r['transitions']")
    P = sorted(set.union(*(search.pats(p) for p in B)), key=lambda p: (len(p), p))
    reps = {leaf: (1,)}
    while len(reps) < len(S):
        old = len(reps)
        for u, v, w in trans:
            if u in reps and v in reps and (w not in reps):
                reps[w] = search.op(reps[u], reps[v], S[w][1])
        if not len(reps) > old:
            raise RuntimeError('check.py:68: len(reps)>old')
    for u, v, w in trans:
        p = search.op(reps[u], reps[v], S[w][1])
        bylen = {k: contained(p, k) for k in range(1, 5)}
        mask = sum((1 << i for i, q in enumerate(P) if q in bylen[len(q)]))
        if not mask == S[w][0]:
            raise RuntimeError('check.py:72: mask==S[w][0]')
        if not all((b not in bylen[len(b)] for b in B)):
            raise RuntimeError('check.py:73: all(b not in bylen[len(b)] for b in B)')
        if not valid(tree(p)):
            raise RuntimeError('check.py:74: valid(tree(p))')
        transition_checks += 1
    state_checks += len(S)
report.update({'witness_transition_checks': transition_checks, 'reachable_state_checks': state_checks, 'all_transition_matches': True})
(D / 'exact_checks.json').write_text(json.dumps(report, indent=2) + '\n')
print('Transitions', transition_checks, 'states', state_checks)
sep = s.series((1 - x - s.sqrt(1 - 6 * x + x * x)) / 2, x, 0, 12).removeO().expand()
extras = {n: s.Rational(sep.coeff(x, n), 2) - s.catalan(n - 1) for n in range(3, 12)}
val = sum((c / s.Integer(4) ** n for n, c in extras.items()))
if not val - s.Rational(1, 2) == s.Rational(779, 4194304):
    raise RuntimeError('check.py:84: val-s.Rational(1,2)==s.Rational(779,4194304)')
print('C_11: P(1/4) =', val)
if not transition_checks == 124258:
    raise RuntimeError('check.py:87: transition_checks==124258')
if not state_checks == 9218:
    raise RuntimeError('check.py:88: state_checks==9218')
if not canonical == 2321:
    raise RuntimeError('check.py:89: canonical==2321')
if not {str(n): int(c) for n, c in extras.items()} == json.loads((D / 'pole_checks.json').read_text())['P_coefficients']:
    raise RuntimeError("check.py:90: {str(n):int(c) for n,c in extras.items()}==json.loads((D/'pole_checks.json').read_text())['P_coefficients']")
if not str(val) == json.loads((D / 'pole_checks.json').read_text())['P_at_quarter']:
    raise RuntimeError("check.py:91: str(val)==json.loads((D/'pole_checks.json').read_text())['P_at_quarter']")
