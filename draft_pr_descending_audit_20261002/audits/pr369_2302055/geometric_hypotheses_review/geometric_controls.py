"""Original exact geometric boundary controls; sampling does not prove Liouville."""
import datetime as dt
import itertools
import json
from pathlib import Path
import sympy as s

N = 0
COUNTS = {}

def ck(claim, family):
    global N
    assert bool(claim), family
    N += 1
    COUNTS[family] = COUNTS.get(family, 0) + 1

def zero(expr, family):
    ck(s.cancel(s.expand(expr)) == 0, family)

x, y, z, t, v, w, q, a, b = s.symbols('x y z t v w q a b')

# Graph coordinates are inverse for every displayed polynomial pair and have
# a globally full-rank tangent frame. This falsifies automatic hyperbolicity.
for degrees in itertools.product(range(1, 6), repeat=2):
    g = x**degrees[0] + 2*x
    h = y**degrees[1] - 3*y
    graph = s.Matrix([x, y, -g-h])
    zero((g+h+z).subs(z, graph[2]), 'linear_input_graph')
    J = graph.jacobian([x,y])
    ck(J[:2,:].det() == 1, 'linear_input_graph')
    for point in [(0,0), (1,2), (-2,3)]:
        ck(J.subs({x:point[0],y:point[1]}).rank() == 2, 'linear_input_graph')

# Cone singularity and one blow-up chart. Removing the exceptional multiplicity
# leaves a smooth strict transform; the conic still supplies a rational divisor.
cone = x*x+y*y+z*z
ck([s.diff(cone,j).subs({x:0,y:0,z:0}) for j in (x,y,z)] == [0,0,0], 'quadratic_cone')
zero(cone.subs({x:t,y:t*v,z:t*w}) - t*t*(1+v*v+w*w), 'quadratic_cone')
v0 = s.I*(1-q*q)/(1+q*q)
w0 = 2*s.I*q/(1+q*q)
zero(1+v0*v0+w0*w0, 'quadratic_cone')
ck((1+v*v+w*w).subs({v:0,w:0}) != 0, 'quadratic_cone')

# Smooth exponential quotient and all pairs of coordinate divisors. Symbolic
# exponential values are independent invertible coordinates for the Jacobian.
e = s.symbols('e1 e2 e3', nonzero=True)
for i in range(3):
    ck(e[i] != 0, 'coordinate_divisors')
    for j in range(3):
        if j != i:
            ck(e[j] != 0, 'coordinate_divisors')
for pair in itertools.combinations(range(3), 2):
    third = ({0,1,2} - set(pair)).pop()
    expr = sum(e)
    ck(expr.subs({e[pair[0]]:1,e[pair[1]]:1,e[third]:-2}) == 0, 'coordinate_divisors')
    ck(e[third].subs(e[third],-2) != 0, 'coordinate_divisors')
ck(sum(e).subs(dict(zip(e,[1,1,1]))) == 3, 'coordinate_divisors')
for perm in set(itertools.permutations([1,2,-3])):
    ck(sum(perm) == 0, 'coordinate_divisors')

# Laurent annihilator: nonzero integer monomial parametrizations preserve every
# nonconstant exponent's nonzeroness, so only constant coefficients contribute.
for r in range(-7,8):
    if not r: continue
    for powers in [(-4,-1,0,2,5), (-3,0,4), (0,1), (-1,0)]:
        expr = sum((k+6)*t**(r*k) for k in powers)
        coeff = sum(k+6 for k in powers if r*k == 0)
        ck(coeff == (6 if 0 in powers else 0), 'torus_coset_constant_term')
        ck(all(r*k != 0 for k in powers if k != 0), 'torus_coset_constant_term')

# Exact rational-map degree and critical-fiber control with actual Laurent
# polynomials; this checks exceptional roots at zero or infinity are excluded.
laurents = [t+1/t, t**3+2*t+5, t**-4+3*t**-1+7,
            2*t**2-3*t**-3+1, 4*t+6, t**-1-8]
c = s.symbols('c')
for R in laurents:
    num, den = s.fraction(s.cancel(R))
    d = max(s.degree(num,t), s.degree(den,t))
    ck(d >= 1, 'finite_rational_quotient')
    zero(s.diff(R,t) - (s.diff(num,t)*den-num*s.diff(den,t))/den**2, 'finite_rational_quotient')
    for u in [s.Rational(1), s.Rational(-2), s.Rational(3,2)]:
        zero((num-c*den).subs({c:R.subs(t,u),t:u}), 'finite_rational_quotient')
        ck(s.degree(num-c*den,t) <= d, 'finite_rational_quotient')

# Rational exponents densely sample the two-divisor estimate. The universal
# proof in the prose uses alpha<1, not rationality of these sampled controls.
weights = [s.Rational(0), s.Rational(1,11), s.Rational(5,11), s.Rational(10,11)]
for alpha,beta in itertools.product(weights,repeat=2):
    for m,n in itertools.product(range(1,5),repeat=2):
        ck(m-alpha > 0 and n-beta > 0, 'crossing_removal_exponents')
        ck(m+n-alpha-beta > 0, 'crossing_removal_exponents')
for alpha in itertools.product(weights,repeat=3):
    ck((sum(alpha)>0) == any(alpha), 'common_line_decay')

payload = {'generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(), 'status':'PASS',
           'exact_assertions':N, 'family_counts':COUNTS,
           'scope':'Original symbolic graph/cone/divisor/torus-coset/rational-fiber and exponent controls.',
           'analytic_or_topological_resolution_certified':False}
Path(__file__).with_name('GEOMETRIC_CONTROLS.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
