#!/usr/bin/env python3
"""Original, dependency-free exact checks for the explicitly scoped partial results.
No external source text/data is needed. All checks remain active under python -O.
"""
import argparse
from fractions import Fraction
from itertools import product, combinations
from math import gcd, isqrt
import json
from pathlib import Path

CHECKS = 0

def require(value, message):
    global CHECKS
    CHECKS += 1
    if not value:
        raise ValueError(message)

def primes(n):
    return [p for p in range(2, n+1) if all(p % q for q in range(2, isqrt(p)+1))]

def genus(d):
    return (d-1)*(d-2)//2

def plane_h0(d, k):
    def binom(n): return n*(n-1)//2 if n >= 2 else 0
    return binom(k+2)-binom(k-d+2)

def hyper_h0(g, n):
    # Direct pole-order basis 1,x,x^2,... and y,xy,... with orders 2,2g+1.
    return n//2+1+max(0, (n-(2*g+1))//2+1)

def partitions(p):
    return [(b,m,e) for b in range(1,p-3)
            for m in range(2,p) for e in range(2,p) if b+m*e==p]

def characteristic_sequences(d):
    """Exhaust necessary characteristic data with conductor (d-1)(d-2).
    Branch multiplicity <= d-1. Characteristic gcd strictly drops; each
    positive increment consumes (old_gcd-1)*increment of the conductor.
    These conditions over-enumerate global curves, never assert existence.
    """
    target=(d-1)*(d-2)
    def extend(m, current_gcd, used, betas, generators):
        if current_gcd==1:
            if used==target:
                yield (m,tuple(betas),tuple(generators))
            return
        for inc in range(1,(target-used)//(current_gcd-1)+1):
            new_gcd=gcd(current_gcd,inc)
            if new_gcd==current_gcd:
                continue
            previous_gcd=gcd(m,*betas[:-1]) if len(betas)>1 else m
            generator=previous_gcd//current_gcd*generators[-1]+inc
            yield from extend(m,new_gcd,used+(current_gcd-1)*inc,
                              betas+[betas[-1]+inc],generators+[generator])
    for m in range(2,d):
        for beta in range(m+1,target//(m-1)+2):
            if beta % m:
                yield from extend(m,gcd(m,beta),(m-1)*(beta-1),[beta],[m,beta])

def semigroup_dp(gens, limit):
    present=[True]+[False]*(limit-1)
    for n in range(1,limit):
        present[n]=any(n>=a and present[n-a] for a in gens)
    return [n for n,ok in enumerate(present) if ok]

def semigroup_products(gens, limit):
    return sorted({sum(a*b for a,b in zip(gens,coeffs))
                   for coeffs in product(*(range((limit-1)//a+1) for a in gens))
                   if sum(a*b for a,b in zip(gens,coeffs))<limit})

# Hand-derived list and witnesses, separate from the general enumerator.
EXPECTED = [
    (2,(91,),(2,91),1,6), (3,(46,),(3,46),1,4),
    (4,(6,81),(4,6,87),1,5), (4,(10,73),(4,10,83),1,4),
    (4,(14,65),(4,14,79),2,9), (4,(18,57),(4,18,75),2,8),
    (4,(22,49),(4,22,71),2,7), (4,(26,41),(4,26,67),3,11),
    (4,(30,33),(4,30,63),4,16), (4,(31,),(4,31),4,16),
    (6,(8,63),(6,8,79),2,9), (6,(9,34),(6,9,43),2,7),
]

def validate_rows(rows, exhausted):
    keys={(r[0],r[1],r[2]) for r in rows}
    require(len(keys)==len(rows)==12,'exactly twelve distinct candidate rows required')
    require(keys==set(exhausted),'candidate inventory is not exhaustive')
    result=[]
    for m,betas,gens,j,count in rows:
        limit=11*j+1
        vals=semigroup_dp(gens,limit)
        require(vals==semigroup_products(gens,limit),'semigroup algorithms disagree')
        require(len(vals)==count,'incorrect semigroup witness count')
        required=(j+1)*(j+2)//2
        require(count!=required,'witness does not violate distribution identity')
        require(Fraction(1,m)+Fraction(1,betas[0])>=Fraction(3,11),'threshold mismatch')
        result.append(dict(multiplicity=m,characteristic_exponents=betas,
                           generators=gens,lct=str(Fraction(1,m)+Fraction(1,betas[0])),
                           j=j,half_open_upper_bound=limit,elements=vals,
                           count=count,required=required))
    return result

def must_reject(fn):
    try:
        fn()
    except ValueError:
        return True
    raise ValueError('negative control was incorrectly accepted')

def run():
    ps=[p for p in primes(199) if p>=5]
    hyper_cases=0
    for p in ps:
        g=genus(p)
        require(2*g-2==p*(p-3),'root degree identity')
        require(hyper_h0(g,p)==(p+1)//2,'odd-p fixed part dimension')
        for k in range(2*p+1):
            h=hyper_h0(g,k*p)
            require(h>=plane_h0(p,k),'semicontinuity necessary inequality')
            if k<=p-3:
                require(h-plane_h0(p,k)==k*(p-k-3)//2,'low power difference')
            else:
                require(h==k*p-g+1==plane_h0(p,k),'nonspecial formula')
            hyper_cases+=1
    require(partitions(5)==[(1,2,2)],'quintic net possibilities')
    require(partitions(11)==[(1,2,5),(1,5,2),(2,3,3),(3,2,4),(3,4,2),
                             (5,2,3),(5,3,2),(7,2,2)],'degree eleven net possibilities')
    for p in ps:
        require(all(m==1 and e==p for m in range(1,p+1) for e in range(2,p+1)
                    if m*e==p),'prime degree basepoint-free factorization')
        for alpha in range(1,p+1):
            require(((p*alpha)%(alpha*alpha)==0)==(p%alpha==0),'Cartier divisibility')
            for q in range(1,p+2):
                require((q*(q-3)==p*(p-3))==(q==p),'positive adjunction root')
    triples=[]
    for a in range(1,12):
        for b in range(a,12):
            for c in range(b,12):
                if a*a+b*b+c*c==3*a*b*c:triples.append((a,b,c))
    require(triples==[(1,1,1),(1,1,2),(1,2,5)],'bounded Markov list')
    require(not any(11 in t for t in triples),'eleven must be absent')
    for alpha in range(1,21):
        for m,n in product(range(1,21),repeat=2):
            require((m*n*alpha*alpha==1)==(alpha==m==n==1),'nodal two-component obstruction')
    all_sequences=list(characteristic_sequences(11))
    require(len(all_sequences)==len(set(all_sequences))==22,'all degree eleven signatures')
    threshold=[row for row in all_sequences if Fraction(1,row[0])+Fraction(1,row[1][0])>=Fraction(3,11)]
    result=validate_rows(EXPECTED,threshold)
    # Entire low range checked with both algorithms, not just witness cutoffs.
    for m,betas,gens in all_sequences:
        require(semigroup_dp(gens,121)==semigroup_products(gens,121),'full semigroup comparison')
        vals=semigroup_dp(gens,121)
        require(len([n for n in range(90) if n not in vals])==45,'delta gap count')
        require(89 not in vals and all(n in vals for n in range(90,121)),'conductor certificate')
    negatives=[]
    negatives.append(must_reject(lambda:validate_rows(EXPECTED[:-1],threshold)))
    bad=list(EXPECTED);bad[0]=bad[0][:-1]+(7,)
    negatives.append(must_reject(lambda:validate_rows(bad,threshold)))
    negatives.append(must_reject(lambda:require(len(semigroup_dp((2,91),13))==6,
                                                'closed-interval off-by-one negative control')))
    return dict(status='PASS',scope='partial results only; full conjecture unresolved',
                assertion_count=CHECKS,hyperelliptic_checks=hyper_cases,
                prime_range='5 through 199',markov_bounded_triples=triples,
                degree11_all_characteristic_signatures=len(all_sequences),
                degree11_threshold_signatures=len(threshold),
                degree11_survivors=0,negative_controls_passed=len(negatives),witnesses=result)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    report=run(); data=json.dumps(report,indent=2)+'\n'
    if args.output:Path(args.output).write_text(data)
    print(data)
