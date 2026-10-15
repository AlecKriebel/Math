#!/usr/bin/env python3
"""Independent exact audit controls; geometric existence is checked in AUDIT.md.

No source PDFs, source excerpts, network requests, or remote writes. Requires SymPy.
The Chow-ring calculations use an incidence hypersurface presentation rather than
copying the author's blowup-vector calculation.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import sympy as sp

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'author'
EXPECTED_MANIFEST = '572b23e2c5f2ddcaec74c05172542d9bfef69d317d6a0151f052bf4e0fc5c62c'
EXPECTED_PROOF = 'efa3b1a7c809bc244799048bd0cf25e9ac56e09d4f90c133ef5095b0458fbcc3'
counts = {}
def check(category, condition):
    if not bool(condition):
        raise AssertionError(category)
    counts[category] = counts.get(category, 0) + 1

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

check('frozen_bytes', sha(AUTHOR / 'SHA256SUMS') == EXPECTED_MANIFEST)
check('frozen_bytes', sha(AUTHOR / 'PROOF.md') == EXPECTED_PROOF)
for line in (AUTHOR / 'SHA256SUMS').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    check('frozen_bytes', sha(AUTHOR / name.strip()) == digest)

replays = []
for program, data in [('verify_intersections.py', 'intersection_results.json'),
                      ('verify_formulas.py', 'formula_results.json')]:
    proc = subprocess.run([sys.executable, str(AUTHOR / program)],
                          capture_output=True, text=True, check=True)
    actual = json.loads(proc.stdout)
    expected = json.loads((AUTHOR / data).read_text())
    check('author_output_replay', actual == expected)
    replays.append({'program': program, 'recorded_json_equal': True,
                    'number_of_rows': len(actual['results']),
                    'stdout_sha256': hashlib.sha256(proc.stdout.encode()).hexdigest()})

# S is the smooth incidence hypersurface in P^2 x B, B elliptic.
# In its ambient intersection ring h^3=b^2=0, integral(h^2 b)=1.
d, h, b = sp.symbols('d h b', integer=True)
D = d*h + 2*b
K = (d-3)*h + 2*b
c2 = 3*h*h - 3*h*D + D*D

def integral(poly):
    return sp.expand(poly).coeff(h, 2).coeff(b, 1)

symbolic = {
    'canonical_square': integral(K*K*D),
    'euler_number': integral(c2*D),
    'hyperplane_square_on_surface': integral(h*h*D),
    'hyperplane_dot_fibre': integral(h*b*D),
    'fibre_square': integral(b*b*D),
    'canonical_dot_fibre': integral(K*b*D),
}
expected_symbolic = {
    'canonical_square': 6*(d-1)*(d-3),
    'euler_number': 6*(d-1)**2,
    'hyperplane_square_on_surface': 2,
    'hyperplane_dot_fibre': d,
    'fibre_square': 0,
    'canonical_dot_fibre': d*(d-3),
}
for name in symbolic:
    check('symbolic_incidence_intersections', sp.expand(symbolic[name]-expected_symbolic[name]) == 0)
chi = sp.expand((symbolic['canonical_square']+symbolic['euler_number'])/12)
check('symbolic_incidence_intersections', sp.expand(chi-(d-1)*(d-2)) == 0)
check('symbolic_incidence_intersections', sp.expand(symbolic['canonical_dot_fibre']/2+1-(d-1)*(d-2)/2) == 0)
check('symbolic_incidence_intersections', sp.expand((d-3)**3-6*(d-1)-(d**3-9*d**2+21*d-21)) == 0)

# Degree-seven singular curve: exact singular-scheme and normalization controls.
x, y, z, s, t = sp.symbols('x y z s t')
f = z*(x**6-y**6)+x**7
partials = [sp.diff(f, v) for v in (x,y,z)]
z_chart = sp.groebner([q.subs(z, 1) for q in partials], x, y)
check('degree_seven_singular_scheme', [q.as_expr() for q in z_chart.polys] == [x**5, y**5])
# On Z=0, f=0 forces X=0, Y !=0. The Y=1 chart excludes a singularity.
y_infinity = sp.groebner([q.subs({y:1,z:0}) for q in partials], x)
check('degree_seven_singular_scheme', [q.as_expr() for q in y_infinity.polys] == [sp.Integer(1)])
a = s**6-t**6
param = {x:s*a, y:t*a, z:-s**7}
check('degree_seven_normalization', sp.expand(f.subs(param, simultaneous=True)) == 0)
check('degree_seven_normalization', sp.gcd(a, s**7) == 1)
check('degree_seven_normalization', sp.expand(param[x]*t-param[y]*s) == 0)
check('degree_seven_normalization', sp.gcd(t**6-1, sp.diff(t**6-1, t)) == 1)

# Reducible-locus dimension control, including every possible factor degree.
factor_cases = 0
for degree in range(2, 257):
    N = degree*(degree+3)//2
    dims = []
    for split in range(1, degree):
        image_dim = split*(split+3)//2 + (degree-split)*(degree-split+3)//2
        check('all_factor_splits', N-image_dim == split*(degree-split))
        dims.append(image_dim)
        factor_cases += 1
    check('pencil_dimension', N-max(dims) == degree-1)
    check('pencil_dimension', (max(dims)+1 < N) == (degree >= 3))

# Independent numerical interpretation after base change: T is the lifted
# section, Q a single fibre. T^2=-2, T.Q=1, Q^2=0, L=4Q+T numerically.
# Distinguishes pi^*F (two fibres) from Q (one fibre).
check('cover_degree_controls', 2*4*1-2 == 6)
check('cover_degree_controls', 4*0+1 == 1)
check('cover_degree_controls', 2*(4*0+1) == 2)
check('cover_degree_controls', -2+2 == 0)  # adjunction: T has genus one
check('cover_degree_controls', 2*(-2)+4 == 0)  # Riemann-Hurwitz for B -> P1

threshold_rows = []
for degree in range(4, 1001):
    k2 = int(symbolic['canonical_square'].subs(d, degree))
    c2value = int(symbolic['euler_number'].subs(d, degree))
    chivalue = int(chi.subs(d, degree))
    margin = (degree-3)**4-k2
    check('integer_threshold_and_geography', (margin>0) == (degree >= 7))
    check('integer_threshold_and_geography', 12*chivalue == k2+c2value)
    check('integer_threshold_and_geography', 0 < k2 <= 3*c2value)
    check('integer_threshold_and_geography', degree*(degree-3)+2 == (degree-1)*(degree-2))
    if degree <= 9 or degree == 1000:
        threshold_rows.append({'d':degree, 'K2':k2, 'c2':c2value, 'chi':chivalue,
                               'multiplicity':degree-1, 'strict_margin':margin})

# For every tested degree and e, check both extremal Bezout sums and an
# interior sum. The universal argument is algebraic: N.D=(d-3)e+(de-r).
bezout_cases = 0
for degree in range(4, 65):
    for e in range(1, 65):
        for r in (0, degree*e//2, degree*e):
            lhs = (2*degree-3)*e-r
            check('bezout_extrema', lhs == (degree-3)*e+(degree*e-r))
            check('bezout_extrema', lhs >= (degree-3)*e > 0)
            bezout_cases += 1

# Exact logarithmic-route control and the formal Hodge-obstruction model.
m, u = sp.symbols('m u', integer=True)
q = m*(m-1)-2
G = sp.Matrix([[2,1,q+2],[1,0,q],[q+2,q,0]])
check('earlier_routes', sp.expand(G.det()-4*q) == 0)
check('earlier_routes', G[:2,:2].det() == -1)
check('earlier_routes', sp.expand(((3+2*u)**2-13)/4-(u*u+3*u-1)) == 0)
for degree in range(1, 65):
    check('earlier_routes', (2*degree+1)*(2*degree) > degree*degree+2)
    check('earlier_routes', (2*degree+1)*(2*degree) > degree*degree+degree+2)

# The sharp small case is compared without floating-point roots.
check('degree_seven_exact_bound', 144 < 4**4)
check('degree_seven_exact_bound', 146 < 6**4)
check('degree_seven_exact_bound', 144 == 6*(7-1)*(7-3))
check('frozen_bytes', sha(AUTHOR / 'SHA256SUMS') == EXPECTED_MANIFEST)
check('frozen_bytes', sha(AUTHOR / 'PROOF.md') == EXPECTED_PROOF)

result = {
    'status':'PASS', 'controls_are_not_geometric_existence_proofs':True,
    'sympy_version':sp.__version__, 'assertion_counts':counts,
    'total_assertions':sum(counts.values()), 'author_replays':replays,
    'all_factor_splits_examined':factor_cases,
    'bezout_test_cases':bezout_cases,
    'symbolic_incidence_results':{k:str(sp.factor(v)) for k,v in symbolic.items()},
    'chi_O':str(sp.factor(chi)),
    'degree_seven_affine_singular_ideal':['x^5','y^5'],
    'threshold_selected_rows':threshold_rows,
    'author_manifest_sha256':EXPECTED_MANIFEST,
    'author_proof_sha256':EXPECTED_PROOF,
}
print(json.dumps(result,indent=2,sort_keys=True))
