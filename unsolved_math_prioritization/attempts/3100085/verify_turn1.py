from math import comb,gcd
from fractions import Fraction as F
from collections import Counter
import json

checks=Counter(); pair_count=0; collisions=[]
def check(k,b):
    assert b,k
    checks[k]+=1
def primes_to(n):return [p for p in range(2,n+1) if all(p%d for d in range(2,int(p**.5)+1))]
def vf(n,p):
    s=0
    while n:n//=p;s+=n
    return s
def key(v,r):
    g=r
    for x in v:g=gcd(g,abs(x))
    return r//g,tuple(x//g for x in v)

for n in range(3,81):
    ps=primes_to(n)
    V=[[vf(n,p)-vf(k,p)-vf(n-k,p) for p in ps] for k in range(n+1)]
    for k,v in enumerate(V):
        z=1
        for p,e in zip(ps,v):z*=p**e
        check('Legendre_binomial_reconstruction',z==comb(n,k))
        check('prime_valuation_bound',all(0<=e<=len([j for j in range(1,n+1) if p**j<=n]) for p,e in zip(ps,v)))
    D={}
    for a in range(n):
        for b in range(a+1,n+1):
            pair_count+=1;r=b-a;v=[x-y for x,y in zip(V[a],V[b])]
            if not any(v):
                check('zero_vector_exact_symmetry',a+b==n)
                continue
            d,e=key(v,r)
            check('primitive_rational_power_denominator',r%d==0 and gcd(d,*map(abs,e))==1)
            if n<=25:
                z=F(1)
                for p,u in zip(ps,e):z*=F(p)**u
                check('positive_radical_integer_power_identity',z**(r//d)==F(comb(n,a),comb(n,b)))
            for p,u in zip(ps,e):
                if u:
                    bound=0;power=p
                    while power<=n:bound+=1;power*=p
                    check('reduced_width_prime_bound',(r//d)*abs(u)<=bound)
            K=(d,e)
            for c,t in D.get(K,[]):
                if len({a,b,c,t})==4:collisions.append([n,a,b,c,t])
            D.setdefault(K,[]).append((a,b))
    if n<=30:
        for r in range(1,n):
            for a in range(n-r):
                check('fixed_width_strictly_increasing',F(comb(n,a),comb(n,a+r))<F(comb(n,a+1),comb(n,a+r+1)))
        for a in range(n):
            for b in range(a+3,n+1):
                c=a+1;t=b-1
                lhs=F(comb(n,a),comb(n,b))**(t-c)
                rhs=F(comb(n,c),comb(n,t))**(b-a)
                check('centered_width_comparison',(lhs<rhs if a+b<n else lhs>rhs if a+b>n else lhs==rhs))

check('no_allowed_collision_through80',not collisions)
check('exact_number_of_pairs',pair_count==88556)
out={'status':'PASS','n_range':[3,80],'candidate_pairs':pair_count,'collisions':collisions,
     'exact_assertions':sum(checks.values()),'counts':dict(sorted(checks.items())),
     'scope':'Exact all-real-parameter exclusion only through n=80 plus finite algebra controls. No conclusion for all n or historical novelty is inferred.'}
print(json.dumps(out,indent=2,sort_keys=True))
