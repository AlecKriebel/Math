#!/usr/bin/env python3
"""Independent exact finite diagnostics; no PDE certification or dependencies."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]
def tr(a):
    return [list(row) for row in zip(*a)]
def mul(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sub(a,b):
    return [[x-y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]
def diag(xs):
    return [[F(xs[i]) if i==j else F(0) for j in range(len(xs))] for i in range(len(xs))]
def zero(a):
    return all(x==0 for row in a for x in row)
def trace(a):
    return sum(a[i][i] for i in range(len(a)))
def conj(u,d):
    return mul(mul(u,d),tr(u))
def rotation(t,pairs):
    u=eye(4)
    c=(1-t*t)/(1+t*t)
    s=2*t/(1+t*t)
    for i,j in pairs:
        u[i][i]=u[j][j]=c
        u[i][j]=-s
        u[j][i]=s
    return u,c,s

p0=diag([1,1,0,0])
q0=diag([1,1,0,1])
r0=diag([F(1,2),F(1,2),F(1,5),F(4,5)])
rows=[]
for denominator in (8,16,32,64):
    t=F(1,denominator)
    u,c,s=rotation(t,[(0,2),(1,3)])
    values=[F(1,2)-t*t,F(1,2)+t*t,F(1,5),F(4,5)]
    r=conj(u,diag(values)); p=conj(u,p0); q=conj(u,q0)
    assert mul(tr(u),u)==eye(4)
    assert mul(p,p)==p and mul(q,q)==q and tr(p)==p and tr(q)==q
    assert mul(q,p)==p and mul(p,q)==p
    assert zero(sub(mul(r,p),mul(p,r))) and zero(sub(mul(r,q),mul(q,r)))
    assert trace(p)==2 and trace(q)==3
    dp=sub(p,p0); dq=sub(q,q0)
    assert mul(dp,dp)==diag([s*s]*4)
    assert mul(dq,dq)==diag([s*s,0,s*s,0])
    dr=sub(r,r0)
    frob_sq=sum(x*x for row in dr for x in row)
    rows.append({"t":str(t),"split_cluster_eigenvalues":[str(x) for x in values[:2]],"ranks":[2,3],"commutation_nesting_idempotence":True,"projection_distance_exact":str(s),"resolvent_difference_frobenius_sq":str(frob_sq)})

# Arbitrary single vector in a multiple eigenspace is not transportable as
# one branch: exact 3/5,4/5 rotation within the degenerate two-space.
u=eye(4); c=F(3,5); s=F(4,5)
u[0][0]=u[1][1]=c; u[0][1]=-s; u[1][0]=s
branch=conj(u,diag([1,0,0,0])); old_branch=diag([1,0,0,0])
db=sub(branch,old_branch)
assert mul(db,db)==diag([s*s,s*s,0,0])
assert conj(u,p0)==p0
branch_control={"rank_one_branch_distance_exact":str(s),"whole_cluster_distance_exact":"0","split_size_can_tend_to_zero_independently":True}

# Exact two-dimensional finite instance of the forbidden-width argument.
qs=[2,5,8,13]
forbidden_squared=set()
max_m=isqrt(9*max(qs))
for q in qs:
    for m in range(1,max_m+1):
        for ell in range(1,max_m+1):
            a2=F(m*m+ell*ell,q)
            if 4<a2<9:
                forbidden_squared.add(a2)
a=F(8,3)
assert 2<a<3 and a*a not in forbidden_squared
assert all((q*a*a).denominator!=1 for q in qs)
nonresonance={"dimension":2,"protected_lambda_units_pi2_over4":qs,"width_interval":[2,3],"forbidden_squared_width_count":len(forbidden_squared),"chosen_width":str(a),"checked_exactly_nonresonant":True,"max_multi_index_coordinate":max_m}

# Finite sections verify the exact identities underlying analytic infinite
# counterexamples; they do not prove an infinite-dimensional conclusion.
projection_escape=[]
for n in (2,4,8,16):
    pn=diag([int(j==n-1) for j in range(n)])
    assert mul(pn,pn)==pn and trace(pn)==1
    projection_escape.append({"n":n,"rank":1,"norm":1,"first_coordinate_image_norm":0})

out={"finite_diagnostics_only":True,"all_exact_assertions_passed":True,"split_cluster_and_nested_families":rows,"single_branch_negative_control":branch_control,"nonresonance_control":nonresonance,"escape_projection_finite_sections":projection_escape}
print(json.dumps(out,indent=2))
Path(__file__).with_name("CONTROLS_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
