#!/usr/bin/env python3
"""Independent exact controls; no numerical experiment certifies a PDE theorem."""
from fractions import Fraction as Q
from itertools import product
import json

counts = {}
def check(tag, truth):
    counts[tag] = counts.get(tag, 0) + 1
    if not truth:
        raise AssertionError(tag)

# A tiny exact polynomial ring in p,q,r,s; coefficient equality is not sampling.
zero = (0,0,0,0)
def const(a):
    return {zero:Q(a)} if a else {}
def var(i):
    e=list(zero);e[i]=1;return {tuple(e):Q(1)}
def add(*polys):
    out={}
    for f in polys:
        for e,a in f.items():out[e]=out.get(e,Q(0))+a
    return {e:a for e,a in out.items() if a}
def scale(a,f):
    return {e:a*b for e,b in f.items() if a*b}
def mul(f,g):
    out={}
    for e,a in f.items():
        for d,b in g.items():
            k=tuple(x+y for x,y in zip(e,d));out[k]=out.get(k,Q(0))+a*b
    return {e:a for e,a in out.items() if a}
def power(f,n):
    out=const(1)
    for _ in range(n):out=mul(out,f)
    return out
p,q,r,s=map(var,range(4));dp=add(p,scale(-1,r));dq=add(q,scale(-1,s))
dg0=add(dp,dq);dg1=add(power(q,3),scale(-1,p),scale(-1,power(s,3)),r)
actual=add(mul(dg0,dp),mul(dg1,dq))
expected=add(power(dp,2),mul(power(dq,2),add(power(q,2),mul(q,s),power(s,2))))
check('symbolic_monotonicity_polynomial',actual==expected)
check('symbolic_positive_quadratic_decomposition',add(power(q,2),mul(q,s),power(s,2))==scale(Q(1,2),add(power(add(q,s),2),power(q,2),power(s,2))))
t=q
plus_norm=add(power(t,2),power(add(t,power(t,3)),2))
minus_norm=add(power(t,2),power(add(t,scale(-1,power(t,3))),2))
check('symbolic_minty_denominator',plus_norm==mul(power(t,2),add(const(2),scale(2,power(t,2)),power(t,4))))
check('symbolic_minty_numerator',minus_norm==mul(power(t,2),add(const(2),scale(-2,power(t,2)),power(t,4))))
check('symbolic_minty_deficit',add(plus_norm,scale(-1,minus_norm))==scale(4,power(t,4)))

def field(x,k):
    a,b=x;return a+k*b,b**3-k*a
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
pts=list(product([Q(k,3) for k in range(-3,4)],repeat=2))
for k in [Q(-3),Q(-1),Q(0),Q(1),Q(2)]:
    for a in pts:
        for b in pts:
            if a==b:continue
            da=minus(a,b);df=minus(field(a,k),field(b,k))
            val=dot(da,df)
            form=da[0]**2+da[1]**2*(a[1]**2+a[1]*b[1]+b[1]**2)
            check('independent_skew_pairing',val==form)
            check('independent_strictness_and_jump_obstruction',val>0)
            check('independent_minty_difference',dot(tuple(x+y for x,y in zip(da,df)),tuple(x+y for x,y in zip(da,df)))-dot(minus(da,df),minus(da,df))==4*val)
for k in [Q(-3),Q(-1),Q(1),Q(2)]:
    for qv in [Q(j,5) for j in range(-12,13)]:
        det=k*k+3*qv*qv
        A=((Q(1),k),(-k,3*qv*qv));Ai=((3*qv*qv/det,-k/det),(k/det,Q(1)/det))
        for i,j in product(range(2),repeat=2):
            check('independent_inverse_product',sum(A[i][l]*Ai[l][j] for l in range(2))==int(i==j))
        check('independent_inverse_symmetric_part',Ai[0][1]+Ai[1][0]==0)
        check('independent_inverse_degeneracy', (Ai[0][0]==0)==(qv==0))
        check('independent_inverse_other_eigenvalue',Ai[1][1]>0)
for j in range(1,97):
    tv=Q(1,3**j);inc=field((Q(0),tv),Q(1))
    check('direct_qminus_on_bad_line',dot(inc,(0,tv))/(tv*tv)==tv*tv)
    check('direct_qplus_on_bad_line',dot(inc,(0,tv))/dot(inc,inc)==tv*tv/(1+tv**4))
    ratio=(2-2*tv*tv+tv**4)/(2+2*tv*tv+tv**4)
    check('independent_minty_ratio_strict',0<ratio<1)
    check('independent_minty_ratio_limit_bound',0<1-ratio<=2*tv*tv)
for n in range(1,81):
    c=Q(1,2**n);R=Q(1,2**(3*n+4));tail=R*R/(1-Q(1,64))
    check('independent_spike_tail',tail==c**6/252)
    check('independent_spike_relative_radius',R<=c/64)
    check('independent_spike_interior',c+R<1)
    for m in range(n+1,81):
        cm=Q(1,2**m);Rm=Q(1,2**(3*m+4))
        check('independent_spike_pairwise_disjoint',c-cm>R+Rm)
    for alpha in [Q(1,2),Q(2,3),Q(3,4),Q(7,8),Q(1)]:
        rv=c*alpha
        check('independent_nondyadic_density_bound',tail/rv**2<=Q(16,63)*rv**4)
    check('independent_energy_geometric_sum',sum((Q(1,2**m) for m in range(1,n+1)),Q(0))==1-Q(1,2**n))
print(json.dumps({'problem_id':30005995,'result':'PASS','assertions':sum(counts.values()),'groups':counts,'scope':'Exact polynomial identities and finite rational controls only; no PDE counterexample and no proof of unrestricted continuity.','mathematical_verdict':'NO RESOLUTION','approaches_completed':5},indent=2,sort_keys=True))
