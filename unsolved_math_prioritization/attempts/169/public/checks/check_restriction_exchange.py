#!/usr/bin/env python3
"""Finite exact diagnostics, not an asymptotic test. Guards survive -O/-OO."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb, isqrt
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def choose(n, r):
    return comb(n, r) if n >= 0 and 0 <= r <= n else 0


def falling(n, r):
    if r < 0 or r > n:
        return 0
    v = 1
    for i in range(r):
        v *= n-i
    return v


def residual(p, A, T):
    return p-len({(a+t) % p for a in A for t in T})


def check_restriction(counts):
    for p in (3, 5, 7):
        G = set(range(p))
        k = isqrt(p)
        for K in range(k, p+1):
            for S_tuple in combinations(range(p), K):
                S = set(S_tuple)
                subsets = [set(z) for z in combinations(S_tuple, k)]
                for m in range(p+1):
                    for T_tuple in combinations(range(p), m):
                        T = set(T_tuple)
                        degrees = [len({(x-t) % p for t in T} & S) for x in range(p)]
                        predicted = sum((Fraction(choose(K-d, k), choose(K,k)) for d in degrees), Fraction())
                        observed = Fraction(sum(residual(p, A, T) for A in subsets), len(subsets))
                        require(predicted == observed, ('restriction identity',p,S_tuple,T_tuple))
                        counts['restriction_mean_identities'] += 1
                        total = Fraction(K*m, p)
                        lo = total.numerator//total.denominator
                        frac = total-lo
                        lower = p*((1-frac)*Fraction(choose(K-lo,k),choose(K,k))
                                   +frac*Fraction(choose(K-lo-1,k),choose(K,k)))
                        require(predicted >= lower, ('restriction convexity',p,S_tuple,T_tuple))
                        counts['restriction_jensen_bounds'] += 1
                for d in range(K-1):
                    lhs = Fraction(choose(K-d,k)-2*choose(K-d-1,k)+choose(K-d-2,k),choose(K,k))
                    rhs = Fraction(choose(K-d-2,k-2),choose(K,k)) if k >= 2 else Fraction()
                    require(lhs == rhs, ('discrete second difference',p,K,d))
                    counts['restriction_second_differences'] += 1


def exchange_case(p, A, T, q, counts):
    G = set(range(p)); k = len(A); m = len(T); old = residual(p,A,T)
    values=[]
    zero_counts=Counter()
    for D in combinations(sorted(T),q):
        for B in combinations(sorted(G-T),q):
            new=(T-set(D))|set(B)
            holes=G-{(a+t)%p for a in A for t in new}
            values.append(len(holes))
            for x in holes:
                for y in holes:
                    zero_counts[x,y]+=1
    denom=len(values)
    M=Fraction(sum(values),denom)
    second=Fraction(sum(h*h for h in values),denom)
    V=second-M*M
    N=[{(x-a)%p for a in A} for x in range(p)]
    C=[n&T for n in N]
    predicted_second=Fraction()
    for x in range(p):
        for y in range(p):
            dx=len(C[x]);dy=len(C[y]);s=len(C[x]&C[y]);r=len(N[x]&N[y])
            a=dx+dy-s;b=2*k-dx-dy-r+s
            if a>q:
                predicted=Fraction()
            else:
                predicted=Fraction(falling(q,a),falling(m,a))*Fraction(choose(p-m-b,q),choose(p-m,q))
            require(predicted == Fraction(zero_counts[x,y],denom), ('pair formula',p,A,T,q,x,y))
            predicted_second+=predicted
            counts['exchange_pair_probabilities'] += 1
    require(predicted_second == second, ('second moment',p,A,T,q))
    counts['exchange_second_moments'] += 1
    maximum=min(p,old+q*k)
    if M<maximum:
        bound=M-V/(maximum-M)
        require(min(values)<=bound, ('variance descent bound',p,A,T,q))
    else:
        require(min(values)==M==maximum, ('degenerate variance',p,A,T,q))
    counts['variance_descent_bounds'] += 1
    if min(values)>=old:
        delta=M-old
        require(0<=delta<=q*k and V<=delta*(q*k-delta), ('stationary variance bound',p,A,T,q))
        counts['no_improvement_variance_bounds'] += 1
    return {'p':p,'A':sorted(A),'T':sorted(T),'q':q,'old_holes':old,'outcomes':denom,
            'min_holes':min(values),'max_holes':max(values),'mean':str(M),'variance':str(V)}


def main():
    counts=Counter()
    check_restriction(counts)
    for p in (3,5,7):
        k=isqrt(p)
        for A in combinations(range(p),k):
            for m in range(1,min(3,p-1)+1):
                for T in combinations(range(p),m):
                    for q in range(1,min(m,p-m,2)+1):
                        exchange_case(p,set(A),set(T),q,counts)
    plateau=[exchange_case(11,{0,1,2},{0,1,4,8},q,counts) for q in (1,2)]
    require(plateau[0]['min_holes']==1 and plateau[1]['min_holes']==0, 'plateau diagnostic')
    result={'status':'PASS','checks':dict(sorted(counts.items())), 'plateau':plateau,
            'scope':'Exact finite random-restriction and collective-exchange formulas only; no original asymptotic conclusion.',
            'asymptotic_resolution_claimed':False,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
