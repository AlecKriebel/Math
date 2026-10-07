#!/usr/bin/env python3
"""Independent exact finite checks; no universal analytic claim is certified."""
from collections import Counter
from fractions import Fraction as Q
from math import comb, isqrt
import json
from pathlib import Path

counts=Counter()
def check(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group]+=1

def floor_reference(t,n):
    # Binary search using (candidate-t+n)^2 versus 2*n^2, not isqrt.
    lo,hi=-2000,20000
    def le_sqrt(a):
        return a <= 0 or a*a <= 2*n*n
    while lo+1<hi:
        mid=(lo+hi)//2
        if le_sqrt(Q(mid)-t+n): lo=mid
        else: hi=mid
    return lo

def floor_fast(t,n):
    a,b=t.numerator,t.denominator
    return (a+isqrt(2*n*n*b*b))//b-n

for t in [Q(-13,7),Q(0),Q(1,17),Q(1,2),Q(23,7)]:
    f=[floor_fast(t,n) for n in range(513)]
    for n,v in enumerate(f):
        check('independent_quadratic_floor',v==floor_reference(t,n))
    digits=[b-a for a,b in zip(f,f[1:])]
    for v in digits: check('binary_digits', v in (0,1))
    for start in [0,1,19,127]:
        for length in range(1,129):
            s=sum(digits[start:start+length])
            check('shifted_block_telescope',s==f[start+length]-f[start])
            c=s+length
            check('exact_irrational_discrepancy',(c-1)**2<2*length*length<(c+1)**2)
    for p in range(1,65):
        check('finite_period_candidates_rejected',any(digits[n]!=digits[n+p] for n in range(512-p)))

for D in range(2,31):
    for d in range(1,D+1):
        for m in range(1,13):
            check('iterate_degree_deficit',D**m-d**m == (D-d)*sum(D**i*d**(m-i-1) for i in range(m)))
            check('zero_deficit_iff_complete_degree',(D**m==d**m)==(D==d))

for i in range(1,100):
    rho=Q(i,100)
    delta=(1-rho)/2
    for n in range(1,51):
        check('good_time_uniform_constants',rho**n<1-delta and 0<delta<1)

for i in range(1,200):
    t=Q(i,200)
    E=(1+t)/(1-t)
    check('koebe_coefficient_identity',4*t/(1-t)**2 == E**2-1)

# Rational Pythagorean directions have exact unit modulus.
for z in [Q(-9,10),Q(-1,3),Q(0),Q(1,2),Q(9,10)]:
    for t in [Q(1,20),Q(1,4),Q(1,2),Q(9,10)]:
        for u,v in [(Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13))]:
            a,b=t*u,t*v
            den=(1+z*a)**2+(z*b)**2
            wr=((z+a)*(1+z*a)+z*b*b)/den
            wi=(b*(1+z*a)-(z+a)*z*b)/den
            coeff=((1+t)/(1-t))**2-1
            check('disk_ball_growth_control',(wr-z)**2+wi**2<=coeff**2*(1-abs(z))**2)

# Independent binomial construction and full Gauss-Jordan elimination.
def parts_power(x,y,n):
    re=sum(Q((-1)**(j//2)*comb(n,j))*x**(n-j)*y**j for j in range(0,n+1,2))
    im=sum(Q((-1)**((j-1)//2)*comb(n,j))*x**(n-j)*y**j for j in range(1,n+1,2))
    return re,im

def rref(rows):
    a=[row[:] for row in rows]
    pivots=[]
    row=0
    for col in range(len(a[0])):
        p=next((j for j in range(row,len(a)) if a[j][col]),None)
        if p is None: continue
        a[row],a[p]=a[p],a[row]
        d=a[row][col]
        a[row]=[v/d for v in a[row]]
        for j in range(len(a)):
            if j!=row and a[j][col]:
                d=a[j][col]
                a[j]=[v-d*w for v,w in zip(a[j],a[row])]
        pivots.append(col)
        row+=1
        if row==len(a): break
    return pivots,a[:row]

rank_results=[]
for degree in range(1,9):
    for part in ['real','imag']:
        rows=[]
        for n in range(2,degree+3):
            for j in range(1,degree+1):
                x,y=Q(1,n),Q(1,8)+Q(j,4*(degree+1))
                row=[Q(0)]*(2*(degree+1))
                for k in range(1,degree+1):
                    re,im=parts_power(x,y,k-1)
                    row[2*k:2*k+2]=[k*re,-k*im] if part=='real' else [k*im,k*re]
                rows.append(row)
        pivots,r=rref(rows)
        free=set(range(2*(degree+1)))-set(pivots)
        check('comb_polynomial_rank',len(pivots)==2*degree-1)
        check('comb_exact_free_coefficients',free==({0,1,3} if part=='real' else {0,1,2}))
        # RREF pivot equations contain no remaining free-variable contribution.
        check('comb_only_affine_nullspace',all(all(not line[c] for c in free) for line in r))
        rank_results.append({'degree':degree,'zero_derivative_part':part,'rank':len(pivots),'free_coefficients':sorted(free)})

result={'problem_id':5300048,'status':'pass','arithmetic':'exact integer and rational','counts':dict(sorted(counts.items())),'total_assertions':sum(counts.values()),'polynomial_controls':rank_results,'limitations':['Finite tests do not establish continuity, accessibility, identity principles, source theorems, or infinite aperiodicity.','Period-candidate tests reject only the listed finite candidates; the proof uses irrational frequency.','No source PDFs, source text, or dataset contents are included.']}
print(json.dumps(result,indent=2,sort_keys=True))
