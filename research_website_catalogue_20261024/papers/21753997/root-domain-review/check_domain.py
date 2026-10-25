"""Independent exact check of the literal rate-domain issue; no source changes."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
import csv, datetime, hashlib, json, re

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
RELEASE = PAPER / 'sources/published-source/AlecKriebel-Math-26f7e00/weakly_reversible_continuum_no_common_factor/releases/v2.0'
MANUSCRIPT = RELEASE / 'source/MANUSCRIPT_V2.md'
PDF = RELEASE / 'output/pdf/manuscript-v2.0.0.pdf'
RATEFILE = RELEASE / 'data/rates.csv'
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(PDF) == 'fe429cf073b30cacfe1ba75624236cda2545c44076f711d4319dcb22ff79512b'
text = MANUSCRIPT.read_text()
complexes = {int(i): tuple(map(int, (x,y,z))) for i,x,y,z in re.findall(r'^\| (\d+) \| \$\((\d+),(\d+),(\d+)\)\$', text, re.M)}
assert len(complexes) == 10
rows = list(csv.DictReader(RATEFILE.open()))
assert len(rows) == 20
rates = {(int(r['source_index']),int(r['target_index'])): Q(r['clean_rate']) for r in rows}
assert all(k > 0 for k in rates.values())
assert max(rates.values()) == 10296 and sum(rates.values()) == 52464
assert [rates[2,j] for j in (4,7,9)] == [1629,1,653]

# Each coefficient is represented as a pair u + v*sqrt(2), with u,v rational.
changes = {(2,4): Q(1,10), (2,7): Q(-3,10), (2,9): Q(1,10)}
base, changed = [defaultdict(Q) for _ in range(3)], [defaultdict(lambda: [Q(0),Q(0)]) for _ in range(3)]
for (i,j), rate in rates.items():
    monomial = complexes[i]
    vector = tuple(b-a for a,b in zip(complexes[i],complexes[j]))
    for t, component in enumerate(vector):
        base[t][monomial] += rate*component
        changed[t][monomial][0] += rate*component
        changed[t][monomial][1] += changes.get((i,j),Q(0))*component
assert all(changed[t][m] == [c,Q(0)] for t,p in enumerate(base) for m,c in p.items())

# Check the clean rational field's ideal membership by exact polynomial division.
# Exponents are (x,y,z); the ordering is lexicographic z > y > x.
g1 = {(0,0,1):Q(1),(1,0,0):Q(-1),(0,1,0):Q(-1),(0,0,0):Q(1)}
g2 = {(0,2,0):Q(1),(1,1,0):Q(-2,7),(2,0,0):Q(1),(1,0,0):Q(-16,7),(0,1,0):Q(-16,7),(0,0,0):Q(16,7)}
lead = lambda p: max(p, key=lambda m: m[::-1])
def remainder(poly):
    p = {m:c for m,c in poly.items() if c}; out = {}
    while p:
        m = lead(p); coefficient = p[m]
        for g in (g1,g2):
            n = lead(g)
            if all(a >= b for a,b in zip(m,n)):
                shift = tuple(a-b for a,b in zip(m,n)); scale = coefficient/g[n]
                for v,c in g.items():
                    w = tuple(a+b for a,b in zip(v,shift)); p[w] = p.get(w,Q(0))-scale*c
                    if not p[w]: del p[w]
                break
        else:
            out[m] = p.pop(m)
    return out
assert all(not remainder(p) for p in base)

# 7/5 < sqrt(2) < 3/2, proved without numerical roots.
assert Q(7,5)**2 < 2 < Q(3,2)**2
lower, upper = Q(7,50), Q(3,20)
positivity_lower_bounds = {str(key): str(rate + (10*changes.get(key,Q(0)))*(lower if changes.get(key,Q(0)) >= 0 else upper)) for key,rate in rates.items()}
assert all(Q(v) > 0 for v in positivity_lower_bounds.values())
out = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'EXACT_COUNTEREXAMPLE_TO_UNRESTRICTED_REAL_RATE_READING',
    'location': 'Current PDF pages 2-5, introductory rate domain and Theorem 3.1',
    'eta': 'sqrt(2)/10',
    'changes': {'k24': '+eta', 'k27': '-3eta', 'k29': '+eta'},
    'all_twenty_modified_rates_strictly_positive': True,
    'rational_positivity_lower_bounds': positivity_lower_bounds,
    'all_field_coefficients_exactly_unchanged': True,
    'clean_field_remainders_modulo_printed_basis': [{},{},{}],
    'rational_free_parameter_conclusion_fails': 'Equation (10) forces a=k29=653+sqrt(2)/10, which is irrational.',
    'rational_rate_theorem_refuted': False,
    'integer_constructions_refuted': False,
    'source_modified': False,
    'bindings': {str(p.relative_to(PAPER)):digest(p) for p in (PDF,MANUSCRIPT,RATEFILE)},
    'script_sha256': digest(Path(__file__)),
}
(HERE/'result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','all_twenty_modified_rates_strictly_positive','all_field_coefficients_exactly_unchanged','rational_rate_theorem_refuted','integer_constructions_refuted')}))
