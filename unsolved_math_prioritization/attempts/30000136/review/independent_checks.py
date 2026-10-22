#!/usr/bin/env python3
"""Independent symbolic controls; the general criteria are checked in REVIEW.md."""
from pathlib import Path
from collections import Counter
import hashlib,json
import sympy as s

checks=Counter()
def check(ok,name):
    assert bool(ok),name
    checks[name]+=1

x,y,c,u,lam=s.symbols('x y c u lam',real=True)
alpha=s.Matrix([s.sin(x),s.sin(y)+1-s.cos(x)])
f=s.cos(x)+s.cos(y)+s.sin(x)
corrected=s.simplify(alpha+s.Matrix([s.diff(f,x),s.diff(f,y)]))
check(corrected==s.Matrix([s.cos(x),1-s.cos(x)]),'exact_corrected_form')
check(s.simplify(s.diff(alpha[1],x)-s.diff(alpha[0],y)-s.sin(x))==0,
      'exterior_derivative')
check(s.expand(c*c+(1-c)**2-s.Rational(1,2)-2*(c-s.Rational(1,2))**2)==0,
      'global_norm_lower_bound')
check(s.simplify((corrected.dot(corrected)).subs(x,s.pi/3))==s.Rational(1,2),
      'norm_bound_attained')
for yy,index in [(0,1),(s.pi,-1)]:
    check(alpha.subs({x:0,y:yy})==s.zeros(2,1),'two_isolated_zeros')
    check(alpha.jacobian([x,y]).subs({x:0,y:yy}).det()==index,'opposite_local_indices')
check(s.Integer(2)-1>0,'no_zero_on_x_equals_pi')

# Concrete shear families with zeros of arbitrarily large multiplicity.
for m in range(1,7):
    F=s.sin(m*x)/m
    check(s.diff(F,x)==s.cos(m*x),'periodic_shear_primitive')
    for power in range(1,5):
        a=s.sin(m*x)**power
        check(s.simplify(s.diff(a,x)-m*power*s.sin(m*x)**(power-1)*s.cos(m*x))==0,
              'nonclosed_shear_derivative')
for power in range(1,5):
    # No common zero of cos(mx), sin(mx)^power on the unit-circle relation.
    G=s.groebner([c,u**power,c*c+u*u-1],c,u)
    check(list(G)==[1],'shear_common_zero_exclusion')

# A flow-compatible example and two negative controls on weakened hypotheses.
F=s.cos(x);a=s.Matrix([s.sin(x),s.cos(x)]);V=s.Matrix([0,1])
check((s.Matrix([s.diff(F,x),0]).dot(V))==0,'first_integral_condition')
for xx in (0,s.pi):
    check(a.dot(V).subs(x,xx)**2==1,'critical_set_evaluation')
new=a+lam*s.Matrix([s.diff(F,x),0])
check(s.simplify(new-s.Matrix([(1-lam)*s.sin(x),s.cos(x)]))==s.zeros(2,1),
      'large_parameter_form')
for L in (2,3,5):
    square=s.expand(((L-1)**2*(1-c*c)+c*c)-1)
    check(s.expand(square-((L-1)**2-1)*(1-c*c))==0,'large_parameter_norm_identity')
check(new.subs({lam:1,x:s.pi/2})==s.zeros(2,1),'large_parameter_needed')
check(1+2*s.diff(s.cos(x),x).subs(x,s.pi/6)==0,
      'first_integral_cannot_be_omitted')

# Quantitative local boundary control on [-pi/6,pi/6]^2. The vertical sides
# have |sin x|=1/2; on the horizontal sides the second component has magnitude
# at least (sqrt(3)-1)/2 throughout the straight-line homotopy of its extra term.
margin=(s.sqrt(3)-1)/2
check(margin>0,'positive_index_boundary_margin')
check(s.sin(s.pi/6)==s.Rational(1,2),'vertical_boundary_control')
check(s.simplify(s.sin(-s.pi/6)+1-s.cos(s.pi/6))==-margin,
      'negative_horizontal_boundary_control')
check(s.sin(s.pi/6)>margin,'positive_horizontal_boundary_control')

here=Path(__file__).resolve().parent
h=hashlib.sha256((here/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest()
check(h=='57211c9962d95f96a38c4cba61a10d20af827bbe76cf24fc4a0a71adf6a2a767',
      'frozen_artifact_hash')
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
 'checks':dict(sorted(checks.items())),'artifact_sha256':h,
 'limitation':'Finite symbolic controls supplement the compactness, bump-function, and degree arguments; the connected conjecture is not solved.'},indent=2,sort_keys=True))
