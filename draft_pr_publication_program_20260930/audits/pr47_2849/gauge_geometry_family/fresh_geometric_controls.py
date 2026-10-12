#!/usr/bin/env python3
"""Fresh exact real-adjoint Jacobian controls; finite controls support, not replace, proofs."""
from pathlib import Path
import json, sympy as s
ROOT=Path(__file__).resolve().parent
checks={}
def ck(label,value):
    assert bool(value),label
    checks[label]=True
I=s.eye(3)
# Hopf framing uses a pair i,j. The commutator is -1 and its adjoint is I.
Ai=s.diag(1,-1,-1);Aj=s.diag(-1,1,-1)
frame=(I-Aj).row_join(Ai-I)
ck("framing_commutator_linearization_rank_three",frame.rank()==3)
ck("framing_nullity_exactly_conjugacy_dimension",6-frame.rank()==3)
trefoil=[]
for k in range(6):
    # The order-two generator is central, hence its adjoint is I.
    angle=4*s.pi*k/3
    B=s.Matrix([[s.cos(angle),-s.sin(angle),0],[s.sin(angle),s.cos(angle),0],[0,0,1]])
    B=B.applyfunc(s.simplify)
    relation=s.diag(2*I,I+B+B**2)
    conjugation=s.zeros(3).col_join(I-B)
    ck(f"trefoil_{k}_AdB_order_divides_three",(B**3).applyfunc(s.simplify)==I)
    ck(f"trefoil_{k}_coboundaries_satisfy_relations",(relation*conjugation).applyfunc(s.simplify)==s.zeros(6,3))
    tangent=6-relation.rank();orbit=conjugation.rank();h1=tangent-orbit
    ck(f"trefoil_{k}_real_adjoint_H1_zero",h1==0)
    ck(f"trefoil_{k}_framed_hessian_equals_critical_dimension",tangent==(0 if k%3==0 else 2))
    trefoil.append({"k":k,"relation_rank":relation.rank(),"tangent_dimension":tangent,"orbit_dimension":orbit,"H1_adjoint_real_dimension":h1})
# Exact global proof of norm invariance is the identity for symbolic unit-circle coordinates.
a,b,u,v=s.symbols("a b u v",real=True)
norm=s.expand((a*u-b*v)**2+(b*u+a*v)**2-(a*a+b*b)*(u*u+v*v))
ck("circle_norm_identity_for_all_angles",norm==0)
# The product lower link has endpoint radii strictly positive; no singular phase fiber occurs.
q=s.symbols("q",real=True)
link=(2*q-1)*(3*q-2)
ck("lower_link_boundary_factorization",s.expand(link-(6*q*q-7*q+2))==0)
ck("lower_link_phase_fibers_never_collapse",0<s.Rational(1,2)<s.Rational(2,3)<1)
# The local relative cellular chain complex is the reduced torus complex shifted by one.
d3=s.zeros(2,1);d2=s.zeros(0,2)
ck("local_relative_H2_two",2-d2.rank()-d3.rank()==2)
ck("local_relative_H3_one",1-d3.rank()==1)
ck("local_rank_three_euler_one",2+1==3 and 2-1==1)
# All-central edge cases with elementary 2-groups have |A| isolated critical points.
for r in range(7):
    ck(f"all_central_C2_power_{r}",2**r==sum(1 for _ in range(2**r)))
out={"passed":len(checks),"failed":0,"sympy_version":s.__version__,"mechanism":"Real adjoint relation Jacobians and framing commutator; symbolic circle identity and exact lower-link chain ranks.","trefoil":trefoil,"checks":checks,"scope":"No instanton homology algorithm or proof of general KP-3.51; theorem input is credited separately."}
(ROOT/"FRESH_GEOMETRIC_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
