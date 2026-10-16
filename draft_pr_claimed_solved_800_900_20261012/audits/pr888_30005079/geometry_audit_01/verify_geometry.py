"""Independent exact finite checks supporting the analytic geometry report.

This script does not establish K-stability, H-minimality or irrationality.
It reads no candidate code and changes only GEOMETRY_CHECK_RESULTS.json beside itself.
"""
import json
from pathlib import Path
import sympy as sp

m = sp.symbols('m', integer=True, nonnegative=True)
x = sp.symbols('x0:4')
lam = sp.symbols('lam')
coefficients = (1, 2, 3, 4)
f = sum(v**2 for v in x)
q = sum(c*v**2 for c, v in zip(coefficients, x))
chart_results = []
for j in range(4):
    chart = {x[j]: sp.Integer(1)}
    polynomials = [f.subs(chart), q.subs(chart)]
    polynomials += [((c-lam)*v).subs(chart) for c, v in zip(coefficients, x)]
    variables = [v for i, v in enumerate(x) if i != j] + [lam]
    basis = sp.groebner(polynomials, *variables)
    assert list(basis) == [1]
    chart_results.append({'projective_chart': j, 'singular_locus_unit_ideal': True})

normals = ((1, 0), (0, 1), (-1, 1), (0, -1))
dets = [int(sp.det(sp.Matrix([normals[i], normals[(i+1) % 4]]))) for i in range(4)]
assert dets == [1, 1, 1, 1]
assert sp.det(sp.hessian(f, x)) == 16

def quadric_hilbert(d):
    return (d+1)*(d+2)*(2*d+3)/6

# The complete-intersection ideal powers have generators u^(m-i)q^i of
# degree m+i and syzygies q*g_i-u*g_(i+1) of degree m+i+2.
# Telescoping their Hilbert functions at degree 3m gives this expression.
hv = sp.expand(quadric_hilbert(2*m) + quadric_hilbert(2*m-1)
               - quadric_hilbert(m-1))
expected_hv = 5*m**3 + sp.Rational(15, 2)*m**2 + sp.Rational(9, 2)*m + 1
assert sp.simplify(hv-expected_hv) == 0
hs = sp.expand(sp.summation(2*m+sp.Symbol('j')+1, (sp.Symbol('j'), -m, m)))
assert sp.simplify(hs-(4*m**2+4*m+1)) == 0
hx = sp.expand(hv*hs)
anticanonical_volume_x = sp.factorial(5)*hx.coeff(m, 5)
assert anticanonical_volume_x == 2400

results = {
    'kind': 'independent_exact_supporting_checks',
    'curve_gradient_dependence_projective_charts': chart_results,
    'toric_consecutive_determinants': dets,
    'node_hessian_determinant': 16,
    'first_factor_hilbert_polynomial': str(hv),
    'toric_ehrhart_polynomial': str(hs),
    'product_hilbert_polynomial': str(hx),
    'product_anticanonical_volume': int(anticanonical_volume_x),
    'first_anticanonical_section_dimensions': {
        'V': int(hv.subs(m, 1)), 'S': int(hs.subs(m, 1)), 'X': int(hx.subs(m, 1))},
    'limitations': 'Exact symbolic checks; not proofs of flatness, K-stability, H-minimality, or irrationality.'
}
Path(__file__).with_name('GEOMETRY_CHECK_RESULTS.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results, indent=2))
