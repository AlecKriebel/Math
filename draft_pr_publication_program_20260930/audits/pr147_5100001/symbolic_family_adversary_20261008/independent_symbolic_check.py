"""Independent exact identities; does not import or read the submitted verifier.

Formal polynomial identities are reduced modulo c*c+d*d=1 and
D*D=A*A*d*d+B*B*c*c. Positivity and geometric implications are proved
separately in REVIEW.md. SymPy supplies an independent algebra diagnostic.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
import sympy as s

A, B, c, d, D = s.symbols('A B c d D', real=True)
U = A*d*d + B*c*c
S = A+B
G = s.groebner([D*D-A*A*d*d-B*B*c*c, c*c+d*d-1], D, c, d, A, B)
checks = []

def zero(label, expression):
    numerator = s.fraction(s.cancel(expression))[0]
    residual = s.expand(G.reduce(s.expand(numerator))[1])
    if residual != 0:
        raise RuntimeError((label, str(residual)))
    checks.append({'label': label, 'residual': str(residual)})

u = s.Matrix([c, d])
v = s.Matrix([-A*d/D, B*c/D])
det = s.det(s.Matrix.hstack(u, v))
dot = u.dot(v)
zero('T maps the unit circle to the unit circle', v.dot(v)-1)
zero('positive determinant formula', det-U/D)
zero('Gram determinant', det*det+dot*dot-1)
zero('positive next normalization', A*A*v[1]**2+B*B*v[0]**2-(A*B/D)**2)
Tv = s.Matrix([-A*v[1], B*v[0]])/(A*B/D)
zero('T square x equals minus identity', Tv[0]+c)
zero('T square y equals minus identity', Tv[1]+d)
zero('support denominator identity', D*D+A*B-S*U)
zero('support-square expanded numerator', A*(D*d-B*c)**2+B*(D*c+A*d)**2-S*U*U)
zero('normal support line value', (d-B*c/D)*c-(c+A*d/D)*d+U/D)

w1 = (u+v)/(1+dot)
w2 = (v-u)/(1-dot)
zero('first outer tangent intersection on u tangent', u.dot(w1)-1)
zero('first outer tangent intersection on v tangent', v.dot(w1)-1)
zero('second outer tangent intersection on v tangent', v.dot(w2)-1)
zero('second outer tangent intersection on -u tangent', (-u).dot(w2)-1)
zero('normalized outer area determinant', s.det(s.Matrix.hstack(w1, w2))-2*D/U)
zero('outer/orbit area ratio', (2*s.det(s.Matrix.hstack(w1, w2)))/(2*det)-2*D*D/(U*U))

normal_norm_P = c*c/A+d*d/B
normal_norm_Q = v[0]**2/A+v[1]**2/B
zero('normal squared norm at P', normal_norm_P-U/(A*B))
zero('normal squared norm at Q', normal_norm_Q-U/(D*D))
half_P_sq = 1-1/(S*normal_norm_P)
half_Q_sq = 1-1/(S*normal_norm_Q)
zero('half-angle sine squared at P', half_P_sq-D*D/(S*U))
zero('half-angle sine squared at Q', half_Q_sq-A*B/(S*U))
H = A*B*D*D/(S*S*U*U)
ratio = 2*D*D/(U*U)
K = 2*A*B*D**4/(S*S*U**4)
zero('four half-angle product', half_P_sq*half_Q_sq-H)
zero('printed product complete formula', ratio*H-K)
zero('quotient constant for the complete period-four family', ratio/H-2*S*S/(A*B))
zero('orbit-cycle symmetry of the area ratio',
     2*(A*B/D)**2/(A*v[1]**2+B*v[0]**2)**2-ratio)

P_norm_sq = A*c*c+B*d*d
Q_norm_sq = A**3*d*d/D**2+B**3*c*c/D**2
P_dot_Q = (B*B-A*A)*c*d/D
side_product_sq = (P_norm_sq+Q_norm_sq)**2-4*P_dot_Q**2
zero('product of side lengths squared', side_product_sq-S*S*U**4/D**4)
zero('sum of side lengths leading to perimeter 4sqrt(S)',
     P_norm_sq+Q_norm_sq+S*U*U/D**2-2*S)
zero('lower bound square decomposition', D*D-U*U-(A-B)**2*c*c*d*d)
zero('upper bound square decomposition', S*S*U*U-4*A*B*D*D-(A-B)**2*(A*d*d-B*c*c)**2)

# A separate direct identity for a general unit direction, not just the map.
a, b, vx, vy = s.symbols('a b vx vy', real=True)
x, y = a*c, b*d
lam = a*a*b*b/(a*a+b*b)
cross = x*vy-y*vx
normal_dot = x*vx/(a*a)+y*vy/(b*b)
expression = cross**2-(a*a-lam)*vy**2-(b*b-lam)*vx**2-(lam-a*a*b*b*normal_dot**2)
G2 = s.groebner([c*c+d*d-1, vx*vx+vy*vy-1], c, vx, d, vy, a, b)
residual = G2.reduce(s.expand(s.fraction(s.cancel(expression))[0]))[1]
if residual != 0:
    raise RuntimeError(('general reflection identity', str(residual)))
checks.append({'label': 'general unit-direction confocal reflection identity', 'residual': str(residual)})

# Exact negative controls: the printed product must fail constancy; swapping
# the axis intercepts in a support line must fail tangency to this caustic.
KD_formula = s.cancel(K.subs({c: 1, d: 0, D: B}))
KR_formula = s.cancel(2*A*B*(A*B)**2/(S*S*(2*A*B/S)**4))
if s.cancel(KD_formula-2*A*B/S**2) != 0 or s.cancel(KR_formula-S**2/(8*A*B)) != 0:
    raise RuntimeError('representative formula specialization failed')
KD = KD_formula.subs({A: 16, B: 9})
KR = KR_formula.subs({A: 16, B: 9})
difference = KR-KD
if difference != s.Rational(58849, 720000) or not difference > 0:
    raise RuntimeError('two exact representatives did not separate')
wrong_support_residual = s.Rational(16**2,25)*s.Rational(1,3**2)+s.Rational(9**2,25)*s.Rational(1,4**2)-1
if wrong_support_residual == 0:
    raise RuntimeError('swapped-weight tangent negative control unexpectedly passed')
negative_controls = {
    'printed_product_rejected_as_constant_exact_difference': str(difference),
    'wrong_axis_support_line_x_over_b_plus_y_over_a_equals_1_rejected_residual': str(wrong_support_residual),
    'A_over_Aprime_in_place_of_Aprime_over_A_diamond': str(s.Rational(72,625)),
    'A_over_Aprime_in_place_of_Aprime_over_A_rectangle': str(s.Rational(72,625)),
    'note': 'The reciprocal area ratio accidentally repairs the printed product at period four; it is a convention-sensitive alternate quantity, not the target.'
}

result = {
    'utc': datetime.now(timezone.utc).isoformat(),
    'status': 'PASS_EXACT_ALGEBRA_DIAGNOSTIC_NOT_A_SUBSTITUTE_FOR_GEOMETRIC_PROOF',
    'sympy_version': s.__version__,
    'identity_count': len(checks),
    'identities': checks,
    'negative_controls': negative_controls,
    'uses_author_verifier': False,
    'scope': 'PR147 period-four family, no mathematical priority or publication verdict'
}
Path(__file__).with_name('SYMBOLIC_RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
