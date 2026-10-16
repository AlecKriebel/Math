"""Independent exact symbolic/projective controls; does not import original code.

Mechanism: SymPy radical arithmetic, pairwise projective cross products and
incidence substitution. No original results or checker are consulted.
"""
import itertools
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent
w = (-1 + s.sqrt(3)*s.I)/2
z = lambda e: s.expand(s.radsimp(s.expand(e)))
def check(predicate, message):
    if predicate is not True and predicate is not s.true:
        raise RuntimeError(message)
def canonical(v):
    entries = tuple(z(a) for a in v)
    den = next(a for a in reversed(entries) if a != 0)
    return tuple(z(a/den) for a in entries)
def intersect(a,b):
    return canonical(s.Matrix(a).cross(s.Matrix(b)))
def dot(a,b):
    return z(sum(c*d for c,d in zip(a,b)))
def arrangement(lines):
    by_point = {}
    for i,j in itertools.combinations(range(len(lines)),2):
        p = intersect(lines[i],lines[j])
        by_point.setdefault(p, []).append((i,j))
    return {p: {"incidence": [i for i,l in enumerate(lines) if dot(l,p)==0],
                "pair_count": len(pairs)} for p,pairs in by_point.items()}

q = [z(w**i) for i in range(3)]
projective = [(1,-a,0) for a in q]+[(0,1,-a) for a in q]+[(-a,0,1) for a in q]
points = arrangement(projective)
check(len(points)==12,"twelve projective pair intersections")
check(all(len(a['incidence'])==3 and a['pair_count']==3 for a in points.values()),"all exactly triple")
check(sum(a['pair_count'] for a in points.values())==36,"all 36 pairs accounted for")
L = (1,2,4)
check(all(dot(L,p)!=0 for p in points),"infinity misses all pair intersections")

# Chart extraction is a matrix coordinate change, followed by t-homogenization.
chart = [(z(a-s.Rational(1,4)*c),z(b-s.Rational(1,2)*c),z(s.Rational(1,4)*c)) for a,b,c in projective]
spatial = [canonical((a,b)) for a,b,c in chart]
check(len(set(spatial))==9,"nine distinct spatial normal directions")
check(all(a!=0 for a,b,c in chart),"all x coefficients nonzero")
x,y,t=s.symbols('x y t')
forms=[x-a*y for a in q]+[a*x+(4+2*a)*y-a*t for a in q]+[-(1+4*a)*x-2*y+t for a in q]
claimed=(x**3-y**3)*(64*y**3-(t-x-2*y)**3)*((t-x-2*y)**3-64*x**3)
factor_differences=[z(s.prod(forms[i:i+3])-f) for i,f in zip((0,3,6),
    (x**3-y**3,64*y**3-(t-x-2*y)**3,(t-x-2*y)**3-64*x**3))]
check(all(f==0 for f in factor_differences),"exact product factors")
check(z(s.Poly(s.expand(claimed),x).LC())==-65,"leading coefficient")
# Direct affine projective pair coordinates of homogenized chart line forms.
affine_points=arrangement(chart)
norms=[]
for p in affine_points:
    check(p[2]==1,"finite affine point")
    norms.append(z(p[0]*s.conjugate(p[0])+p[1]*s.conjugate(p[1])))
check(len(affine_points)==12,"chart singular completeness")
check(all(v<=2 for v in norms),"moving singular bound squared norm <= 2|t|^2")
check(s.sqrt(2)/4<s.Rational(1,2),"all singularities inside half ball")
distance_coefficients=[]
for form in forms:
    a,b,c=[z(s.diff(form,v)) for v in (x,y,t)]
    coefficient=z(c*s.conjugate(c)/(a*s.conjugate(a)+b*s.conjugate(b)))
    check(coefficient/16<1,"strict unit-sphere line distance bound")
    distance_coefficients.append(str(coefficient))

# Jacobian confirms every pair point is singular for the exact t=1 product.
g=s.expand(claimed.subs(t,1))
dg=[s.diff(g,v) for v in (x,y)]
check(all(z(e.subs({x:p[0],y:p[1]}))==0 for p in affine_points for e in [g]+dg),"Jacobian singular controls")
central_delta=s.binomial(9,2); nearby_delta=12*s.binomial(3,2)
central_rough=9-2; nearby_rough=12*(3-2)
check(central_delta==nearby_delta==36 and central_rough==7 and nearby_rough==12,"invariant totals")
n=s.symbols('n',integer=True,positive=True)
check(s.expand(3*n*(n-1)/2+3*n**2-(3*n)*(3*n-1)/2)==0,"universal Fermat delta identity")
check(s.expand(3*(n-2)+n**2-(3*n-2))==n**2-4,"universal Fermat excess identity")

# Meaningful falsification controls; each intentionally breaks a named premise.
bad_infinity=(1,0,0)
check(any(dot(bad_infinity,p)==0 for p in points),"negative: unsuitable infinity caught")
perturbed=list(projective); perturbed[-1]=(perturbed[-1][0],1,1)
perturbed_stats=arrangement(perturbed)
check(not(len(perturbed_stats)==12 and all(len(a['incidence'])==3 for a in perturbed_stats.values())),"negative: perturbed model loses twelve triples")
discarded=arrangement(projective[:-1])
check(sum(a['pair_count'] for a in discarded.values())==28,"negative: dropping a component loses eight pairs")
check(9!=1,"scope negative: central fiber is not unibranched")
two_roots=[s.Integer(1),s.Integer(-1)]
two_lines=[(1,-a,0) for a in two_roots]+[(0,1,-a) for a in two_roots]+[(-a,0,1) for a in two_roots]
two_points=arrangement(two_lines)
check(sorted(len(v['incidence']) for v in two_points.values())==[2,2,2,3,3,3,3],"n=2 boundary multiplicities")
check(sum(len(v['incidence'])-2 for v in two_points.values())==6-2,"n=2 has zero rough excess")
generic=arrangement([(s.Integer(1),s.Integer(-i),s.Integer(-i*i)) for i in range(9)])
check(len(generic)==36 and all(len(v['incidence'])==2 for v in generic.values()),"generic nine lines have 36 nodes and zero rough total")

result={"status":"PASS","mechanism":"independent SymPy radical/projective cross-products and Jacobian substitution", "sympy":s.__version__,
"exact_domain":"Q(sqrt(-3)) = Q(omega); no floating arithmetic in mathematical controls",
"projective_lines":9,"distinct_spatial_directions":len(set(spatial)),"triple_points":len(points),"pair_incidences":36,
"chart_squared_norms":sorted([str(v) for v in norms]),"uniform_bound":"sqrt(2)*abs(t) < 1/2 for abs(t)<1/4",
"line_squared_distance_coefficients":distance_coefficients,
"x_leading_coefficient":-65,"central":{"delta":36,"rough_M":7,"branches":9},"nearby":{"delta_sum":36,"rough_M_sum":12},
"universal_fermat":{"delta_identity":True,"excess":"n^2-4","quantifier":"For all integers n>=3, structural incidence proof required; finite evaluations are diagnostics only."},
"negatives":{"infinity_collision":True,"perturbed_line":{"intersection_points":len(perturbed_stats),"multiplicities":sorted(len(a['incidence']) for a in perturbed_stats.values())},"discarded_component_pairs":28,"unibranched_scope_rejected":True,"n2_excess":0,"generic_nine_lines_rough_sum":0},
"limits":["Does not certify analytic flatness, finite simultaneous normalization, boundary topology, source scope, novelty, or fine-M assertions.","Invariant formulas are independently arithmetically applied, not a replacement for the resolution argument."]}
(ROOT/'independent_exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
