"""Exact finite diagnostics for the independently explained prior-containment bridge.
These controls do not prove Bi's analytic theorem or novelty by computation.
"""
import hashlib,json
from pathlib import Path
from fractions import Fraction
import sympy as s

checks=[]
def check(name,value):
    if value is not True:
        raise RuntimeError(name+': '+str(value))
    checks.append(name)
def equal(name,a,b):
    if isinstance(a,s.MatrixBase): value=all(s.simplify(x)==0 for x in a-b)
    else: value=s.simplify(a-b)==0
    check(name,bool(value))

A=s.Matrix([[2,1,0],[0,3,1],[1,0,2]])
G=A.T*A
check('nonsingular_ambient_derivative',A.det()!=0)
check('positive_metric_sylvester',all(G[:k,:k].det()>0 for k in range(1,4)))
# Source facet covectors, pulled target normals and metric normal inner products.
covs=[s.Matrix([1,0,0]),s.Matrix([0,1,0]),s.Matrix([1,2,0]),s.Matrix([0,0,-1])]
for j,u in enumerate(covs):
    w=A.T.inv()*u
    equal('metric_normal_length_'+str(j),(u.T*G.inv()*u)[0],w.dot(w))
    equal('normal_pushforward_'+str(j),A*G.inv()*u,w)
for j,u in enumerate(covs):
    for k,v in enumerate(covs):
        if j<k:
            equal('metric_target_gram_'+str(j)+'_'+str(k),(u.T*G.inv()*v)[0],(A.T.inv()*u).dot(A.T.inv()*v))
# Product with an interval: old normals and lengths unchanged; new end normals perpendicular.
GP=s.diag(G,1)
for j,u in enumerate(covs):
    up=s.Matrix([*u,0]); ep=s.Matrix([0,0,0,1])
    equal('product_old_normal_norm_'+str(j),(up.T*GP.inv()*up)[0],(u.T*G.inv()*u)[0])
    equal('product_old_end_orthogonality_'+str(j),(up.T*GP.inv()*ep)[0],0)
equal('product_end_unit',(ep.T*GP.inv()*ep)[0],1)
for j,u in enumerate(covs):
    for k,v in enumerate(covs):
        if j<k:
            up=s.Matrix([*u,0]);vp=s.Matrix([*v,0])
            equal('product_old_gram_'+str(j)+'_'+str(k),(up.T*GP.inv()*vp)[0],(u.T*G.inv()*v)[0])
# A weakly smooth bijection with interior inverse can lose the needed corner metric.
x=s.symbols('x',real=True)
weak=s.diag(9*x**4,1,1)
equal('degenerate_corner_determinant',weak.det().subs(x,0),0)
equal('positive_interior_determinant',weak.det().subs(x,s.Rational(1,2)),s.Rational(9,16))
# Deficits measure extra exterior turn in units of pi. An n-gon already has 2.
for m in (3,4,7,19):
    old_exterior=Fraction(2,m)
    deficits=[Fraction(0) for _ in range(m)]
    deficits[-1]=Fraction(1,100)
    check('planar_strict_deficit_contradicts_nonnegative_arc_turn_'+str(m),sum([old_exterior+d for d in deficits])>2)
    check('planar_no_deficit_allows_zero_arc_turn_'+str(m),sum([old_exterior for _ in range(m)])==2)
# Angle supplement reversal, including a strict point; exact values in units of pi.
for j,(old,new) in enumerate([(Fraction(2,3),Fraction(2,3)),(Fraction(2,3),Fraction(1,2)),(Fraction(3,4),Fraction(1,4))]):
    check('interior_exterior_weak_reversal_'+str(j),(new<=old)==((1-new)>=(1-old)))
    check('interior_exterior_strict_reversal_'+str(j),(new<old)==((1-new)>(1-old)))
print(json.dumps({'check_count':len(checks),'checks':checks,'result':'PASS','limits':'Finite exact diagnostics; authored derivation establishes the general implication. No PDE theorem or historical originality certified.'},indent=2))
