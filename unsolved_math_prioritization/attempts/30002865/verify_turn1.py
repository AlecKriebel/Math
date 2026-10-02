#!/usr/bin/env python3
"""Exact finite controls; does not prove the external smoothability theorem."""
from fractions import Fraction as F
import json

counts={}
def ck(v,kind):
    assert v,kind
    counts[kind]=counts.get(kind,0)+1

def trim(p):
    p=list(map(F,p))
    while len(p)>1 and not p[-1]:p.pop()
    return p

def add(p,q):
    return trim([(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))])

def scale(p,a):return trim([a*x for x in p])
def sub(p,q):return add(p,scale(q,-1))
def mul(p,q):
    r=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):r[i+j]+=a*b
    return trim(r)
def ev(p,x):
    r=F(0)
    for a in reversed(p):r=r*x+a
    return r

def rem(p,q):
    p=trim(p)
    while len(p)>=len(q) and p!=[0]:
        k=len(p)-len(q); a=p[-1]/q[-1]
        p=sub(p,[F(0)]*k+scale(q,a))
    return p

def mono(k):return [F(0)]*k+[F(1)]
def prod_roots(rr):
    q=[F(1)]
    for r in rr:q=mul(q,[-r,1])
    return q

q=prod_roots([0,0,1,1,2]);g=[mono(i) for i in range(4)]+[add(mono(4),q)]
ck(q==[0,0,-2,5,-4,1],'base_polynomial')
ck(F(1)*2-F(4)*1==-2,'noncollinearity')
for z in [F(0),F(1),F(2)]:ck(ev(q,z)==0,'support')

def projection(p,qt,t):
    r=rem(p,qt);r=r+[F(0)]*(5-len(r));v=rem(g[4],qt);v=v+[F(0)]*(5-len(v))
    assert 1+2*t
    c4=r[4]/(1+2*t);c=[r[j]-c4*v[j] for j in range(4)]+[c4]
    out=[F(0)]
    for a,b in zip(c,g):out=add(out,scale(b,a))
    return out

parameters=[F(0)]+[F(1,k) for k in range(3,31)]+[-F(1,k) for k in range(3,16)]
monomials=0
for t in parameters:
    rr=[F(0),t,F(1),1+t,F(2)];qt=prod_roots(rr)
    ck(len(qt)==6 and qt[-1]==1,'constant_monic_degree')
    v=rem(g[4],qt);v=v+[F(0)]*(5-len(v))
    ck(v[4]==1+2*t,'frame_determinant')
    ck(q[4]-qt[4]==2*t,'coefficient_difference')
    if t:ck(len(set(rr))==5,'distinct_nodes')
    for b in g:ck(projection(b,qt,t)==b,'fixed_range')
    for a in range(13):
        for b in range(17):
            monomials+=1
            # Substitute x=y^2 in x^a y^b; this defines the original bivariate map.
            p=mono(2*a+b);out=projection(p,qt,t)
            ck(rem(sub(out,p),qt)==[0],'quotient_identity')
            ck(projection(out,qt,t)==out,'idempotence')
            for r in rr:ck(ev(out,r)==r**(2*a+b),'interpolation')
            ck(projection(mul(p,qt),qt,t)==[0],'kernel_generator_q')
            # (x-y^2)x^a y^b specializes identically to zero.
            ck(sub(mono(2*(a+1)+b),mono(2*a+b+2))==[0],'kernel_generator_curve')
    for k in range(1,31):
        p=trim([F(((k+2)*i*i+3*i+7)%19-9,k) for i in range(31)])
        out=projection(p,qt,t)
        ck(rem(sub(out,p),qt)==[0],'combination_quotient')
        ck(projection(out,qt,t)==out,'combination_idempotence')
        for r in rr:ck(ev(out,r)==ev(p,r),'combination_interpolation')

# At a distant reduced fiber, the same fixed range can fail to interpolate.
t=-F(1,2);rr=[F(0),t,F(1),1+t,F(2)];qt=prod_roots(rr)
ck(len(set(rr))==5,'negative_control_distinct_nodes')
v=rem(g[4],qt);v=v+[F(0)]*(5-len(v))
ck(v[4]==0,'negative_control_singular_frame')
h=g[4]
for i in range(4):h=sub(h,scale(g[i],v[i]))
ck(h!=[0],'negative_control_nonzero_range_vector')
ck(rem(h,qt)==[0],'negative_control_kernel_intersection')
for r in rr:ck(ev(h,r)==0,'negative_control_all_evaluations_zero')
print(json.dumps({'problem_id':30002865,'status':'PASS','assertions':sum(counts.values()),'counts':counts,'rational_parameters':len(parameters),'bivariate_monomials_per_parameter':13*17,'monomial_cases':monomials,'parameter_domain':'0; 1/k for 3<=k<=30; -1/k for 3<=k<=15; singular negative control -1/2','monomial_box':'0<=a<=12, 0<=b<=16 for x^a y^b','linear_combinations_per_parameter':30,'arithmetic':'exact fractions; standard library only','scope':'Bounded checks of the explicit length-five fixed-range example. The general theorem uses the written lemma and credited external smoothability theorem.'},indent=2,sort_keys=True))
