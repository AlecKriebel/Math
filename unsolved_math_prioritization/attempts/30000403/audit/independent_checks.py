#!/usr/bin/env python3
"""Fresh audit controls; no author implementation imported. Requires SymPy.
Finite and generic certificates do not formally verify the descent theorem.
"""
from itertools import permutations, combinations
from pathlib import Path
import json, sys
import sympy as sp
from sympy.polys.domains import QQ_I
K=QQ_I
I=K.convert(sp.I)
checks=0
def ck(x):
    global checks
    checks+=1
    if not x: raise AssertionError(f'check {checks}')
def elt(x):return K.convert(x)
def norm(v):
    first=next((x for x in v if x),None)
    return tuple(x/first for x in v) if first else None
def mul(a,b):
    return norm((a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3]))
def inv(a):return norm((a[3],-a[1],-a[2],a[0]))
def det(a):return a[0]*a[3]-a[1]*a[2]
def nullbasis(rows):
    a=[list(r) for r in rows];piv=[];r=0
    for c in range(4):
        p=next((j for j in range(r,len(a)) if a[j][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r]; t=a[r][c]; a[r]=[u/t for u in a[r]]
        for j in range(len(a)):
            if j!=r:
                t=a[j][c];a[j]=[u-t*v for u,v in zip(a[j],a[r])]
        piv.append(c);r+=1
        if r==len(a):break
    out=[]
    for c in range(4):
        if c in piv:continue
        v=[elt(0)]*4;v[c]=elt(1)
        for j,p in enumerate(piv):v[p]=-a[j][c]
        out.append(tuple(v))
    return out
# All six point correspondences enforced at once, not three-point interpolation.
def stabilizer(a):
    b=-1/elt(K.to_sympy(a).conjugate());pts=[(elt(0),elt(1)),(elt(1),elt(0)),(elt(1),elt(1)),(elt(-1),elt(1)),(a,elt(1)),(b,elt(1))]
    out=[];ranks={}
    for perm in permutations(range(6)):
        rows=[]
        for j,t in enumerate(perm):
            x,z=pts[j];y,w=pts[t];rows.append((w*x,w*z,-y*x,-y*z))
        bases=nullbasis(rows);rank=4-len(bases);ranks[rank]=ranks.get(rank,0)+1
        if bases:
            ck(len(bases)==1)
            if det(bases[0]):out.append(list(perm))
    return pts,out,ranks
pts,good,rankgood=stabilizer(elt(2)+2*I)
_,negative,ranknegative=stabilizer(elt(2)+I)
ck(good==[list(range(6))]);ck(len(negative)==2)
# Binary quartic invariants, avoiding the author's cross-ratio formula implementation.
x,z=sp.symbols('x z');rows=[]
for subset in combinations(range(6),4):
    f=sp.Poly(sp.prod(K.to_sympy(pts[j][1])*x-K.to_sympy(pts[j][0])*z for j in subset),x,z)
    A,B,C,D,E=[f.coeff_monomial(x**(4-i)*z**i) for i in range(5)]
    iq=12*A*E-3*B*D+C*C
    jq=72*A*C*E+9*B*C*D-27*A*D*D-27*B*B*E-2*C**3
    j=sp.expand_complex(sp.cancel(6912*iq**3/(4*iq**3-jq**2)))
    rows.append({'subset':list(subset),'J':[str(sp.simplify(sp.re(j))),str(sp.simplify(sp.im(j)))]})
ck(len(set(tuple(r['J']) for r in rows))==15)
expected=json.loads(Path(__file__).with_name('REPLAY_CONTROL_RESULTS.json').read_text())['four_subset_J_values']
ck(rows==expected)
# Full exact normalizer closure over Q(i), its V4 action, and complex conjugation.
idm=tuple(map(elt,(1,0,0,1)));A=norm(tuple(map(elt,(-1,0,0,1))));B=tuple(map(elt,(0,1,1,0)))
E=[idm,A,B,mul(A,B)]
S=norm((I,elt(0),elt(0),elt(1)));T=norm(tuple(map(elt,(1,1,1,-1))))
N={idm};pending=[idm]
while pending:
    n=pending.pop()
    for g in [S,T]:
        t=mul(n,g)
        if t not in N:N.add(t);pending.append(t)
ck(len(N)==24)
actions=set();rational=0
for n in N:
    p=tuple(E.index(mul(mul(n,e),inv(n))) for e in E[1:]); actions.add(p)
    nc=norm(tuple(elt(K.to_sympy(t).conjugate()) for t in n))
    ck(nc in N)
    pc=tuple(E.index(mul(mul(nc,e),inv(nc))) for e in E[1:])
    ck(pc==p)
    if nc==n:rational+=1
ck(len(actions)==6);ck(rational==8)
# Generic V4 formulas independently derived from F'(e), all root permutations.
a,b,c=sp.symbols('a b c');roots=[a,b,c];m=[]
for t in roots:
    others=[u for u in roots if u!=t];delta=(t-others[0])*(t-others[1]);M=sp.Matrix([[t,delta-t*t],[1,-t]]);m.append(M)
    ck(sp.expand(M.det()+delta)==0);ck(all(sp.expand(u)==0 for u in M*M-delta*sp.eye(2)))
for i,j in permutations(range(3),2):
    lhs=list(m[i]*m[j]);rhs=list(m[3-i-j])
    ck(all(sp.expand(lhs[u]*rhs[v]-lhs[v]*rhs[u])==0 for u in range(4) for v in range(4)))
for p in permutations(range(3)):
    sub=dict(zip(roots,[roots[j] for j in p]))
    for i in range(3):ck(all(sp.expand(u)==0 for u in m[i].subs(sub,simultaneous=True)-m[p[i]]))
# All possible subgroup images of an S3 cubic-etale action have concrete Q-polynomials.
t=sp.symbols('t')
cubics=[('trivial',t*(t-1)*(t-3),'1'),('C2',t*(t*t-2),'C2'),('C3',t**3-3*t+1,'C3'),('S3',t**3-t-1,'S3')]
cubic_data=[]
for label,f,expected_group in cubics:
    poly=sp.Poly(f,t);disc=sp.discriminant(f,t);ck(disc!=0)
    if label in ['C3','S3']:
        group,_=sp.polys.numberfields.galois_group(poly);ck(group.order()==(3 if label=='C3' else 6))
    cubic_data.append({'action':label,'polynomial':str(f),'discriminant':str(disc),'factor_degrees':[p.degree() for p,k in sp.factor_list(poly)[1]]})
# Explicit quadratic conic: parametrization over Q(i), antipodal action under conjugation.
u,v=sp.symbols('u v',real=True)
q=sp.Matrix([u*u-v*v,sp.I*(u*u+v*v),2*u*v]);ck(sp.expand(sum(t*t for t in q))==0)
anti=q.subs({u:-v,v:u},simultaneous=True);conj=q.conjugate();ck(all(sp.expand(anti[i]+conj[i])==0 for i in range(3)))
output={'status':'pass','assertions':checks,'python':sys.version.split()[0],'sympy':sp.__version__,'independence':'No author module imported; full six-correspondence linear systems and binary quartic invariants are alternative algorithms.', 'all_permutations_per_configuration':720,'sharp_stabilizer':good,'negative_stabilizer':negative,'sharp_linear_system_rank_counts':rankgood,'negative_linear_system_rank_counts':ranknegative,'four_subset_J_values':rows,'normalizer_order':len(N),'normalizer_Q_rational_elements':rational,'normalizer_quotient_actions':sorted(list(map(list,actions))),'cubic_etale_actions':cubic_data,'conic':'X^2+Y^2+Z^2=0; Q(i) parametrization and antipodal conjugation checked','limits':'Finite/generic algebra certificates only; not formal proof of general descent or exhaustive literature research.'}
print(json.dumps(output,indent=2))
