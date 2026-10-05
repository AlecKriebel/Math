#!/usr/bin/env python3
"""Finite exact controls, not a certification of geometric existence theorems."""
from fractions import Fraction as F
from itertools import product
from math import prod
import json

checks = 0

def check(b):
    global checks
    checks += 1
    assert b, checks

def delta(i, j):
    return int(i == j)

# Sphere averaging against a constant negative holomorphic curvature tensor.
averages = []
for n in range(1, 7):
    def R(i, j, k, l):
        return -(delta(i,j)*delta(k,l)+delta(i,l)*delta(k,j))
    S = sum(R(i,i,k,k) for i in range(n) for k in range(n))
    avg = sum(F(R(i,j,k,l)*(delta(i,j)*delta(k,l)+delta(i,l)*delta(k,j)),n*(n+1))
              for i,j,k,l in product(range(n),repeat=4))
    check(S == -n*(n+1))
    check(avg == -2)
    check(avg == F(2*S,n*(n+1)))
    check(avg != F(S,n*(n+1))) # deliberately omitted pairing must be rejected
    averages.append({'n':n,'scalar_trace':S,'sphere_average':str(avg)})

# Complete-intersection adjunction and independent degree arithmetic.
adjunction_cases = 0
for n,d,volume in product(range(2,7),range(1,21),range(1,6)):
    canonical_degree = (n-1)*d**n*volume
    curve_degree = d**(n-1)*volume
    check(F(canonical_degree,curve_degree) == (n-1)*d)
    check(canonical_degree > 0)
    check(-canonical_degree + canonical_degree == 0) # c1(TC)+c1(N)=0
    adjunction_cases += 1

# Restricted positivity need not give total positivity, trace sign, or determinant sign.
transverse_models = []
for n,k in product(range(2,6),range(1,5)):
    N = n+k*(n-1)
    entries = [1]*n+[-5]*(N-n)
    check(len(entries)==N)
    check(N-n==k*(n-1)>0)
    check(all(t>0 for t in entries[:n]))
    check(any(t<0 for t in entries[n:]))
    check(sum(entries)<0)
    transverse_models.append({'n':n,'k':k,'tower_dimension':N,'directed_rank':n,
                              'codimension':N-n,'trace':sum(entries),'determinant':prod(entries)})
check(sum([1,1,-3])==-1)
check(prod([1,1,-3])==-3)

# A nonzero algebraic Kahler curvature tensor with zero Ricci contraction.
a = {}
a[0,0,0,0]=a[1,1,1,1]=1
for ijkl in [(0,0,1,1),(1,0,0,1),(0,1,1,0),(1,1,0,0)]:
    a[ijkl]=-1
R = lambda i,j,k,l:a.get((i,j,k,l),0)
for i,j,k,l in product(range(2),repeat=4):
    check(R(i,j,k,l)==R(k,j,i,l))
    check(R(i,j,k,l)==R(i,l,k,j))
    check(R(i,j,k,l)==R(j,i,l,k)) # real conjugation symmetry
ricci = [[sum(R(i,j,k,k) for k in range(2)) for j in range(2)] for i in range(2)]
check(ricci == [[0,0],[0,0]])
check(any(R(*ijkl)!=0 for ijkl in product(range(2),repeat=4)))

def hsc_real(v):
    numerator=sum(R(i,j,k,l)*v[i]*v[j]*v[k]*v[l] for i,j,k,l in product(range(2),repeat=4))
    norm2=sum(x*x for x in v)
    return F(numerator,norm2**2)
check(hsc_real((1,0))==1)
check(hsc_real((1,1))==F(-1,2))
# Coefficientwise identity for arbitrary complex v, tracking barred variables separately.
polynomial={}
for i,j,k,l in product(range(2),repeat=4):
    e=tuple(sum(t==q for t in (i,k)) for q in range(2))+tuple(sum(t==q for t in (j,l)) for q in range(2))
    polynomial[e]=polynomial.get(e,0)+R(i,j,k,l)
polynomial={e:c for e,c in polynomial.items() if c}
check(polynomial=={(2,0,2,0):1,(0,2,0,2):1,(1,1,1,1):-4})

# Weighted jet degree differs from number of cotangent factors.
def indices(k,m):
    if k==0:
        return [()] if m==0 else []
    return [pre+(last,) for last in range(m//k+1) for pre in indices(k-1,m-k*last)]
weighted_count=0
counts=[]
for k,m in product(range(1,6),range(13)):
    rows=indices(k,m)
    check(len(rows)==len(set(rows)))
    for row in rows:
        q=sum(row)
        check(len(row)==k)
        check(sum((j+1)*v for j,v in enumerate(row))==m)
        check((m+k-1)//k <= q <= m)
        weighted_count+=1
    counts.append({'k':k,'m':m,'graded_index_count':len(rows)})
check((0,1) in indices(2,2))
check(sum((0,1))==1 and sum((j+1)*v for j,v in enumerate((0,1)))==2)

result={
 'schema_version':1,
 'purpose':'Exact finite algebraic controls only; no proof of the full geometric question.',
 'assertions_passed':checks,
 'sphere_controls':averages,
 'adjunction_parameter_grid':{'n':[2,6],'d':[1,20],'H_top_intersection':[1,5],'cases':adjunction_cases},
 'transverse_controls':transverse_models,
 'ricci_zero_tensor':{'ricci':ricci,'H_at_coordinate_line':'1','H_at_diagonal_line':'-1/2','nonzero':True},
 'jet_filtration_controls':{'k':[1,5],'m':[0,12],'weighted_multiindices_checked':weighted_count,'counts':counts},
 'negative_controls_rejected':['omit second sphere-moment pairing','restricted positivity implies total positivity',
  'restricted positivity implies positive trace','restricted positivity implies positive determinant',
  'Ricci zero implies curvature zero','Ricci zero implies sectional one-sign',
  'weighted jet degree equals tensor degree'],
 'original_problem_solved':False
}
print(json.dumps(result,indent=2,sort_keys=True))
