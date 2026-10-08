"""Exact finite controls supporting, not replacing, the written proofs."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import gcd
import json

class CheckFailure(Exception):
    pass

counts = Counter()
def require(condition, label):
    if not condition:
        raise CheckFailure(label)
    counts[label.split(':', 1)[0]] += 1

def orbit_counts(a,b,r,s,L):
    return Counter((pow(a,n,s)*pow(b,k,s)*r)%s for n in range(L+1) for k in range(L+1))

def factors(n):
    d=2; out={}
    while d*d<=n:
        while n%d==0:
            out[d]=out.get(d,0)+1; n//=d
        d+=1
    if n>1: out[n]=out.get(n,0)+1
    return out

def independent(a,b):
    fa,fb=factors(a),factors(b); primes=set(fa)|set(fb)
    return any(fa.get(p,0)*fb.get(q,0)!=fa.get(q,0)*fb.get(p,0) for p in primes for q in primes)

def cut(base, bound):
    L=0; v=1
    while v*base<bound:
        L+=1; v*=base
    return L

def cover(points, delta):
    points=sorted(set(points)); k=0; end=None
    for x in points:
        if end is None or x>end:
            k+=1; end=x+delta
    return k

def brute_cover(points,delta):
    xs=sorted(set(points)); n=len(xs)
    if not n:return 0
    masks=[]
    for x in xs:
        masks.append(sum(1<<j for j,y in enumerate(xs) if x<=y<=x+delta))
    target=(1<<n)-1; reachable={0}
    for k in range(n+1):
        if target in reachable:return k
        reachable={r|m for r in reachable for m in masks}
    raise CheckFailure('brute cover did not terminate')

def energy(U,p,r,q):
    return sum(min(z,p-z)*q<=p for u in U for v in U for z in [(r*(u-v))%p])

def isprime(p):return p>=2 and all(p%d for d in range(2,int(p**0.5)+1))

def run():
    counts.clear()
    # Independent exhaustive set-cover oracle for all small grid subsets.
    for den in range(2,8):
        for mask in range(1,1<<den):
            pts=[F(j,den) for j in range(den) if mask>>j&1]
            for q in (2,3,5,9):
                require(cover(pts,F(1,q))==brute_cover(pts,F(1,q)), 'cover_oracle:greedy equals exhaustive')
    # The fixed-point classification requires no multiplicative independence.
    for a in range(2,10):
      for b in range(2,10):
       for s in range(2,36):
        if gcd(s,a*b)!=1:continue
        for r in range(1,s):
         if gcd(s,r)!=1:continue
         singleton=len(orbit_counts(a,b,r,s,1))==1
         require(singleton==((a-1)%s==0 and (b-1)%s==0),'fixed_point:iff')
    require(independent(4,7) and set(orbit_counts(4,7,1,3,20))=={1},'fixed_point:literal witness')
    pairs=((2,3),(4,7),(4,6),(6,10),(8,9))
    for a,b in pairs:
      require(independent(a,b),'independence:base pairs')
      for s in range(2,402):
       if gcd(s,a*b)!=1:continue
       L=cut(a*b,s)
       U=[a**n*b**k for n in range(L+1) for k in range(L+1)]
       require(len(set(U))==(L+1)**2 and max(U)<s,'injectivity:integer rectangle')
       for r in set((1,s//2,s-1)):
        if gcd(s,r)!=1:continue
        pts=[F(z,s) for z in orbit_counts(a,b,r,s,L)]
        require(len(pts)==len(U),'injectivity:unit dilation')
        require(cover(pts,F(1,2*s))==len(U),'injectivity:fine cover')
        for q in (3,7,11):
         require(cover(pts,F(1,q))*(s//q+1)>=len(U),'injectivity:grid occupancy')
    # Exact band construction; this does not certify Baker constants.
    for a,b in pairs:
     for s in (1009,10007,100003):
      for r in (1,2,3,7):
       if gcd(s,r*a*b)!=1:continue
       ys=[]; k=0
       while 2*r*b**(2*k)<=s:
        n=0
        while 2*r*b**k*a**(n+1)<=s:n+=1
        y=F(r*a**n*b**k,s); ys.append(y)
        require(F(1,2*a)<y<=F(1,2),'seed_band:exact endpoints')
        k+=1
       require(len(ys)==len(set(ys)),'seed_band:distinctness')
    # Difference construction at an exact rational logarithmic-scale proxy.
    for a,b in pairs:
     for s in (1009,10007,100003,1000003):
      if gcd(s,a*b)!=1:continue
      for r in (1,s//3,s-1):
       if gcd(s,r)!=1:continue
       L0=cut((a*b)**2,s)
       B=sorted(orbit_counts(a,b,r,s,L0))
       if len(B)<2:continue
       dx,x,y=min((y-x,x,y) for x,y in zip(B,B[1:]))
       d=F(dx,s); delta=F(1,s.bit_length()**4)
       require(d>=F(1,s),'difference:grid separation')
       require(d<=F(1,len(B)-1),'difference:pigeonhole')
       j0=0
       while a**j0*d<4*delta:j0+=1
       ts=[]; j=j0
       while a**j*d<=F(1,4):ts.append((j,a**j*d));j+=1
       if not ts:continue
       H=L0+cut(a,s)+1; A=orbit_counts(a,b,r,s,H)
       for j,t in ts:
        xx=(pow(a,j,s)*x)%s; yy=(pow(a,j,s)*y)%s
        require(xx in A and yy in A and F((yy-xx)%s,s)==t,'difference:membership')
       require(all(v-u>2*delta for (_,u),(_,v) in zip(ts,ts[1:])),'difference:packing')
       K=cover([F(z,s) for z in A],delta)
       require(K*K>=len(ts),'difference:cover transfer')
    # Exact average energy, packing consequence, and Markov exception counts.
    for p in range(5,200):
     if not isprime(p):continue
     for a,b in ((2,3),(4,7)):
      if p in factors(a*b):continue
      L=cut(a*b,p); U=sorted({a**n*b**k for n in range(L+1) for k in range(L+1)})
      T=len(U)
      for q in (3,5,7,11,31):
       es=[energy(U,p,r,q) for r in range(1,p)]
       total=T*(p-1)+2*(p//q)*T*(T-1)
       require(sum(es)==total,'energy:mean identity')
       bad=0
       for r,E in enumerate(es,1):
        K=cover([F((r*u)%p,p) for u in U],F(1,q))
        require(K*E>=T*T,'energy:cover lower bound')
        if E*(p-1)>3*total:bad+=1
       require(3*bad<=p-1,'energy:Markov count')
    # Exact cancellation and total variation of empirical measures.
    for a,b in pairs:
     for s in (11,17,25,35,61):
      if gcd(s,a*b)!=1:continue
      for r in (1,s-1):
       for L in range(7):
        c=orbit_counts(a,b,r,s,L)
        for g,other in ((a,b),(b,a)):
         pc=Counter()
         for x,w in c.items():pc[(g*x)%s]+=w
         diff={x:pc[x]-c[x] for x in set(pc)|set(c)}
         boundary=Counter()
         for k in range(L+1):
          boundary[(pow(g,L+1,s)*pow(other,k,s)*r)%s]+=1
          boundary[(pow(other,k,s)*r)%s]-=1
         require(all(diff.get(x,0)==boundary[x] for x in set(diff)|set(boundary)),'empirical:boundary cancellation')
         require(sum(abs(z) for z in diff.values())<=2*(L+1),'empirical:variation bound')
    # Sparse periodic orbit and its exact symbolic partition distribution.
    for a in range(2,6):
     for m in range(2,65):
      s=a**m-1; U=[a**j for j in range(m)]
      require({a*u%s for u in U}==set(U),'symbolic:cycle')
      for ell in range(1,m):
       c=Counter((a**ell*u)//s for u in U)
       expected=Counter({0:m-ell})
       expected.update({a**t:1 for t in range(ell)})
       require(c==expected,'symbolic:partition distribution')
       require(cover([F(u,s) for u in U],F(1,a**ell))<=ell+1,'symbolic:cover upper bound')
    return {'status':'PASS','checks':sum(counts.values()),'families':dict(sorted(counts.items())),
            'scope':'Exact finite controls only; the universal arguments are the written proofs and the credited Baker input.'}

def negative(name):
    if name=='nonunit_injectivity':
        require(len(orbit_counts(2,3,7,35,1))==4,'negative:nonunit falsely claimed injective')
    elif name=='dependent_injectivity':
        require(len(orbit_counts(2,4,1,101,2))==9,'negative:dependent bases falsely claimed injective')
    elif name=='energy_without_diagonal':
        p=11;U=[1,2,3,6];q=5;T=len(U)
        require(sum(energy(U,p,r,q) for r in range(1,p))==2*(p//q)*T*(T-1),'negative:omitted diagonal')
    elif name=='composite_permutation':
        p=15;U=[1,4];q=3;T=len(U)
        require(sum(energy(U,p,r,q) for r in range(1,p))==T*(p-1)+2*(p//q)*T*(T-1),'negative:composite extension')
    elif name=='false_sparse_period':
        a=2;m=5;s=a**m+1;U={a**j for j in range(m)}
        require({a*u%s for u in U}==U,'negative:wrong sparse denominator')
    elif name=='zero_boundary':
        c=orbit_counts(2,3,1,101,2);pc=Counter()
        for x,w in c.items():pc[2*x%101]+=w
        require(pc==c,'negative:finite rectangle exactly invariant')
    elif name=='false_cover':
        require(cover([F(0),F(1,2)],F(1,4))==1,'negative:one interval crosses separated points')
    else:raise CheckFailure('unknown negative control')
    raise RuntimeError('negative control unexpectedly survived')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--negative');args=parser.parse_args()
    try:
        if args.negative:negative(args.negative)
        print(json.dumps(run(),sort_keys=True,indent=2))
    except CheckFailure as exc:
        print('REJECTED: '+str(exc));raise SystemExit(2)
