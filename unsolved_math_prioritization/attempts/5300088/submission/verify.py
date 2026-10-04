#!/usr/bin/env python3
"""Exact finite algebra controls, not a proof of McMullen's conjecture."""
from fractions import Fraction as Q
import json

checks = 0

def check(v, description):
    global checks
    checks += 1
    if not v:
        raise RuntimeError(description)

def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def trans(a):
    return [list(x) for x in zip(*a)]

def mv(a,v):
    return tuple(sum(a[i][k]*v[k] for k in range(4)) for i in range(4))

J=[[Q(0) for _ in range(4)] for _ in range(4)]
I=[[Q(int(i==j)) for j in range(4)] for i in range(4)]
for i in range(4): J[i][i]=Q(1 if i==0 else -1)

word_counts={}
for q in range(3,31):
    t=Q(q*q-1,q*q+1); k=Q(2*q,q*q+1)
    c=Q(q**4+1,2*q*q); s=Q(q**4-1,2*q*q)
    check(c*c-s*s==1,'Lorentz identity')
    check(t*t+k*k==1,'cap slab identity')
    check(2*t*t>1,'four closed caps disjoint')
    check((s-c*t)/(c-s*t)==t,'side pairing boundary')
    check(c-s*t>0,'side pairing positive denominator')
    check(Q(1,1)/(c+s)==Q(1,q*q),'octahedron height')
    check(Q(1,q**4+2)<k*k,'depth lower bound below upper bound')
    check(q*q-2*q-1>0,'depth upper bound less than L')
    A=[[c,s,0,0],[s,c,0,0],[0,0,0,-1],[0,0,1,0]]
    B=[[c,0,s,0],[0,1,0,0],[s,0,c,0],[0,0,0,1]]
    Ai=mul(mul(J,trans(A)),J); Bi=mul(mul(J,trans(B)),J)
    for M,Mi in ((A,Ai),(B,Bi)):
        check(mul(mul(trans(M),J),M)==J,'preserve Lorentz form')
        check(mul(M,Mi)==I,'matrix inverse')
    check(mv(A,(1,0,1,0))==(c,s,0,1),'positive ideal endpoint')
    check(mv(A,(1,0,-1,0))==(c,s,0,-1),'negative ideal endpoint')
    check(mv(A,(1,0,0,0))[0]==c,'generator displacement')
    check(mv(B,(1,0,0,0))[0]==c,'second generator displacement')
    # Independent finite-word stress test. All-word proof is the ping-pong proof.
    if q in (3,4,5,7):
        mats=(A,Ai,B,Bi)
        frontier=[(-1,(Q(1),Q(0),Q(0),Q(0)))]
        count=0
        for depth in range(1,6):
            nxt=[]
            for old,v in frontier:
                for letter,M in enumerate(mats):
                    if old>=0 and letter==(old^1):
                        continue
                    w=mv(M,v)
                    check(w[0]>=c,'finite reduced-word displacement >= 2L')
                    check(sum(J[i][i]*w[i]*w[i] for i in range(4))==1,'word remains on H3')
                    axis=1 if letter<2 else 2
                    sign=1 if letter%2==0 else -1
                    check(sign*w[axis]>t*w[0],'finite ping-pong halfspace')
                    nxt.append((letter,w));count+=1
            frontier=nxt
        check(count==sum(4*3**(d-1) for d in range(1,6)),'reduced word count')
        word_counts[str(q)]=count

# Rank-versus-genus implication negative control, expressed through cosh r.
n,g,cosh_r=2,100,10
check(n<=g and cosh_r<=2*g and cosh_r>2*n,'rank/genus wrong direction control')

# Exact identity behind chi(partial M) and rank bound for sampled Betti data.
euler_cases=0
for n in range(1,21):
    for b1 in range(n+1):
        for b2 in range(b1):
            chi=1-b1+b2
            check(-2*chi<=2*(n-1),'boundary Euler bound')
            euler_cases+=1

print(json.dumps({'status':'passed','checks':checks,'parameter_q_range':[3,30],
 'finite_reduced_words_per_parameter':word_counts,'word_max_length':5,
 'euler_cases':euler_cases,
 'scope':'Exact finite identities and negative controls only. Infinite-word and geometric statements rely on the written proofs; target remains unsolved.'},indent=2,sort_keys=True))
