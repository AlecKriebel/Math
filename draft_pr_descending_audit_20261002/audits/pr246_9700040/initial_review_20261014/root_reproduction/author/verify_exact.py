#!/usr/bin/env python3
"""Author exact controls; finite controls supplement the proof, not replace it."""
from stationary_law import F,partitions,contains,transpose,D,raw_by_size,enclosure
from functools import lru_cache
from itertools import permutations
from collections import Counter
from math import factorial,prod
import bisect,json
checks=Counter()
def check(ok,kind):
    assert ok,kind
    checks[kind]+=1

@lru_cache(None)
def tableaux(lam,mu=()):
    if not contains(lam,mu):return 0
    if lam==mu:return 1
    total=0
    for i,a in enumerate(lam):
        if a>(lam[i+1] if i+1<len(lam) else 0) and a>(mu[i] if i<len(mu) else 0):
            q=list(lam);q[i]-=1
            total+=tableaux(tuple(x for x in q if x),mu)
    return total

def rsk_prefix_shapes(perm):
    rows=[];shapes=[()]
    for x in perm:
        for row in rows:
            j=bisect.bisect_right(row,x)
            if j==len(row):row.append(x);break
            row[j],x=x,row[j]
        else:rows.append([x])
        shapes.append(tuple(map(len,rows)))
    return tuple(shapes)

allshapes=[p for n in range(8) for p in partitions(n)]
for lam in allshapes:
    for mu in allshapes:
        if not contains(lam,mu):continue
        d=sum(lam)-sum(mu);f=tableaux(lam,mu)
        for t in (F(0),F(1),F(2,3)):
            expected=F(f)*t**d/factorial(d)
            check(D(lam,mu,t)==expected,'skew_determinant_vs_corner_recursion')
            check(D(transpose(lam),transpose(mu),t)==expected,'transpose_identity')
        check(D(lam,mu,F(1),max(len(lam),len(mu))+2)==D(lam,mu),'padding')
for n in range(8):
    check(sum(tableaux(p)**2 for p in partitions(n))==factorial(n),'rs_normalization')
    hist=Counter();cuts=(0,n//3,2*n//3,n)
    for perm in permutations(range(1,n+1)):
        shapes=rsk_prefix_shapes(perm)
        hist[tuple(shapes[i] for i in cuts)]+=1
        # Separate actual time-sweep of rectangle points (u=i+1,v=perm[i]).
        tops=[]
        for u in sorted(range(1,n+1),key=lambda u:perm[u-1]):
            j=bisect.bisect_right(tops,u)
            if j==len(tops):tops.append(u)
            else:tops[j]=u
        for x in range(n+1):
            lis=shapes[x][0] if shapes[x] else 0
            check(bisect.bisect_right(tops,x)==lis,'time_sweep_vs_spatial_prefix')
    for chain,count in hist.items():
        expected=tableaux(chain[-1])*prod(tableaux(lam,mu) for mu,lam in zip(chain,chain[1:]))
        check(count==expected,'joint_prefix_shape_count')
for N in range(8):
    xs=(F(1,3),F(3,2),F(2));raw=raw_by_size(xs,(N+1,)*3,N)
    for n,v in enumerate(raw):check(v==xs[-1]**n/factorial(n),'poisson_coefficient_normalization')
for x in (F(1,3),F(1),F(3,2)):
    for N in (2,5,10):
        raw=raw_by_size((x,),(1,),N)
        check(raw==[F(1)]+[F(0)]*N,'first_exponential_law')
for x,y in ((F(1,2),F(1)),(F(1),F(2)),(F(2,3),F(5,3))):
    for N in (3,7,12):
        raw=raw_by_size((x,y),(1,2),N)
        check(raw==[(y-x)**n/factorial(n)**2 for n in range(N+1)],'known_two_particle_survival')
for n in range(30):
    # Coefficient of g'-g'' equals the old Poisson-mixture density.
    a=F(n+1,factorial(n+1)**2)-F((n+2)*(n+1),factorial(n+2)**2)
    b=F(n+1,factorial(n)*factorial(n+2))
    c=F(1,factorial(n))*(F(1,factorial(n+1))-F(1,factorial(n+2)))
    check(a==b==c,'known_two_particle_density')
examples=[]
for xs,rs in [((F(1),F(2)),(2,3)),((F(1,2),F(1),F(2)),(2,3,4)),((F(1),F(2)),(3,2))]:
    coarse=enclosure(xs,rs,8);fine=enclosure(xs,rs,18)
    check(coarse['lower']<=fine['lower']<=fine['upper']<=coarse['upper'],'nested_certificates')
    check(fine['width']==fine['upper']-fine['lower'],'certificate_width')
    check(0<=fine['lower']<=fine['upper']<=1,'probability_bounds')
    examples.append({'x':[str(x) for x in xs],'indices':rs,'cutoff':18,
                     'lower':str(fine['lower']),'upper':str(fine['upper']),
                     'width':str(fine['width']),
                     'display_only':[float(fine['lower']),float(fine['upper'])]})
print(json.dumps({'status':'PASS','assertions':sum(checks.values()),'categories':dict(checks),
                  'max_enumerated_permutation_size':7,'examples':examples,
                  'limits':'Finite exact algebra and enumeration controls; dynamics, uniqueness, all-index formula, convergence and source scope require the written proof and independent review.'},indent=2))
