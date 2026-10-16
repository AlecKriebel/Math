#!/usr/bin/env python3
"""Independent exact controls for the analytic representative; SymPy 1.14.0.

This tests concrete algebra behind the proof's uniform geometric estimates.
It does not use the original checker or certify flatness/normalization by samples.
Run with python -B boundary_controls.py; stdout is deterministic JSON.
"""
from itertools import combinations
import json
import sympy as s

if not __debug__:
    raise RuntimeError("Run without Python optimization: this exact control suite uses assertions.")

w, x, y, t = s.symbols('w x y t')
modulus = w*w + w + 1

def field(z):
    num, den = s.fraction(s.cancel(z))
    num = s.Poly(num, w, domain=s.QQ)
    den = s.Poly(den, w, domain=s.QQ)
    return (num * s.invert(den, s.Poly(modulus, w, domain=s.QQ))).rem(s.Poly(modulus, w, domain=s.QQ)).as_expr()

def conj(z):
    return field(z.subs(w, -1-w))

def norm2(z):
    value = field(z*conj(z))
    assert not value.has(w), value
    return value

def reduce_polynomial(z):
    return s.rem(s.expand(z), modulus, w).expand()

roots = [s.Integer(1), w, -1-w]
lines = []
for i, q in enumerate(roots):
    lines.append((f'A{i}', s.Integer(1), -q, s.Integer(0)))
for i, q in enumerate(roots):
    lines.append((f'B{i}', q, 4+2*q, -q))
for i, q in enumerate(roots):
    lines.append((f'C{i}', -(1+4*q), s.Integer(-2), s.Integer(1)))

F = (x**3-y**3)*(64*y**3-(t-x-2*y)**3)*((t-x-2*y)**3-64*x**3)
product = s.prod(a*x+b*y+c*t for _,a,b,c in lines)
assert reduce_polynomial(product-F) == 0
assert s.Poly(F,x).LC() == -65

points = {}
determinants = []
for li, lj in combinations(lines, 2):
    ni,a,b,c = li
    nj,A,B,C = lj
    determinant = field(a*B-A*b)
    assert determinant != 0, (ni,nj)
    determinants.append(str(determinant))
    u = field((b*C-B*c)/determinant)
    v = field((c*A-C*a)/determinant)
    key = (u,v)
    points.setdefault(key, []).append([ni,nj])

assert len(points) == 12
point_records = []
for (u,v), pairs in points.items():
    incidence = [name for name,a,b,c in lines if field(a*u+b*v+c)==0]
    assert len(incidence)==3
    assert len(pairs)==3
    n2 = norm2(u)+norm2(v)
    assert n2 <= 1
    point_records.append({'u':str(u),'v':str(v),'incidence':incidence,'norm_squared':str(n2)})
point_records.sort(key=lambda p: (p['u'],p['v']))

line_records=[]
for name,a,b,c in lines:
    N=norm2(a)+norm2(b)
    pc=(-c*conj(a)/N, -c*conj(b)/N)
    pc=tuple(field(z) for z in pc)
    direction=(-b,a)
    assert field(a*pc[0]+b*pc[1]+c)==0
    assert field(a*direction[0]+b*direction[1])==0
    assert field(pc[0]*conj(direction[0])+pc[1]*conj(direction[1]))==0
    distance_coefficient=field(norm2(pc[0])+norm2(pc[1]))
    assert distance_coefficient == norm2(c)/N
    # At |t| <= 1/4 the boundary circle radius squared is 1-d(t)^2.
    radius_squared_lower_bound = 1-distance_coefficient/16
    assert radius_squared_lower_bound >= s.Rational(207,208)
    line_records.append({'line':name,'spatial_normal_norm_squared':str(N),'distance_squared_over_abs_t_squared':str(distance_coefficient),'boundary_radius_squared_lower_bound':str(radius_squared_lower_bound)})

# Real risk control: each line can be individually transverse while their union
# has a singular boundary. At t=1, all three B lines pass through (1,0) on S^3.
B_lines=[ell for ell in lines if ell[0].startswith('B')]
assert all(field(a+c)==0 for _,a,b,c in B_lines)
assert all(norm2(c)/(norm2(a)+norm2(b))<1 for _,a,b,c in B_lines)
assert norm2(s.Integer(1))+norm2(s.Integer(0)) == 1

# A second boundary edge: B1 has d(t)^2=|t|^2/13; |t|^2=13
# collapses its boundary circle to a tangency point, so the parameter restriction
# cannot be silently removed.
_,a,b,c=B_lines[1]
assert norm2(c)/(norm2(a)+norm2(b)) == s.Rational(1,13)
assert 1-13*norm2(c)/(norm2(a)+norm2(b)) == 0

report = {
    'status':'PASS',
    'arithmetic':'exact Q[w]/(w^2+w+1); conjugation w -> -1-w',
    'factorization_identity':True,
    'x_leading_coefficient':-65,
    'nonzero_pairwise_spatial_direction_determinants':len(determinants),
    'singular_points_at_t_one':point_records,
    'max_singular_point_norm_squared_at_t_one':str(max(s.Rational(p['norm_squared']) for p in point_records)),
    'uniform_singularity_norm_bound':'||p(t)|| <= |t| <= 1/4 on the closed parameter disk',
    'line_geometry':line_records,
    'uniform_boundary_radius_squared_lower_bound':'207/208 on |t|<=1/4',
    'normalization_fiber_components':9,
    'ordinary_triple_points_nonzero_parameter':12,
    'negative_controls':{
        't_one_three_B_lines_collide_on_boundary_despite_individual_transversality':'detected exactly',
        'B1_tangency_at_abs_t_squared_thirteen':'detected exactly'
    },
    'scope':'Algebraic geometric controls only; universal analytic conclusions require AUDIT.md derivations.'
}
print(json.dumps(report,indent=2,sort_keys=True))
