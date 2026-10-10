#!/usr/bin/env python3
"""Independent exact finite controls. No geometric or PDE theorem is certified."""
from fractions import Fraction
from itertools import product
from math import factorial, comb, prod
import json

count=0
families={}
def verify(name, predicate):
    global count
    assert predicate, (name,count)
    count+=1
    families[name]=families.get(name,0)+1

def sphere_moment(i,j,k,l,n):
    unbar=[0]*n; bar=[0]*n
    unbar[i]+=1;unbar[k]+=1;bar[j]+=1;bar[l]+=1
    if unbar!=bar:return Fraction(0)
    return Fraction(factorial(n-1)*prod(factorial(a) for a in unbar),factorial(n+1))

for n in range(1,8):
    for i,j,k,l in product(range(n),repeat=4):
        expected=Fraction(int(i==j and k==l)+int(i==l and k==j),n*(n+1))
        verify('sphere_moment_coefficient',sphere_moment(i,j,k,l,n)==expected)
    # R = B_ik conjugate(B_jl) for symmetric real B is an algebraic Kahler tensor.
    for mode in range(4):
        B=[[((i+j+mode)%5-2) if mode else int(i==j) for j in range(n)] for i in range(n)]
        R=lambda i,j,k,l:B[i][k]*B[j][l]
        scalar=sum(R(i,i,k,k) for i,k in product(range(n),repeat=2))
        avg=sum(R(i,j,k,l)*sphere_moment(i,j,k,l,n) for i,j,k,l in product(range(n),repeat=4))
        verify('general_kahler_sphere_trace',avg==Fraction(2*scalar,n*(n+1)))

adjunction=0
for n,d,Hn in product(range(2,8),range(1,17),range(2,10,2)):
    # Formal intersection algebra; does not claim every parameter tuple is realized.
    Cdegree=Hn*prod([d]*(n-1))
    KCdegree=(n-1)*d*Cdegree
    verify('complete_intersection_ratio',Fraction(KCdegree,Cdegree)==(n-1)*d)
    verify('ambient_zero_degree_consistency',-KCdegree+(n-1)*d*Cdegree==0)
    adjunction+=1

for n,k in product(range(2,8),range(1,7)):
    N=n+k*(n-1); M=n+1; diagonal=[1]*n+[-M]*(N-n)
    verify('tower_dimension_rank',N-n==k*(n-1)>0)
    verify('directed_not_total',min(diagonal[:n])>0 and min(diagonal)<0)
    verify('directed_not_positive_trace',sum(diagonal)<0)
verify('directed_not_positive_determinant',prod([1,1,-3])==-3)

# The tensor of the quartic x^2*xb^2+y^2*yb^2-4*x*y*xb*yb.
def R(i,j,k,l):
    if i==j==k==l:return 1
    return -1 if sorted([i,k])==[0,1] and sorted([j,l])==[0,1] else 0
for i,j,k,l in product(range(2),repeat=4):
    verify('ricci_model_symmetries',R(i,j,k,l)==R(k,j,i,l)==R(i,l,k,j)==R(j,i,l,k))
ricci=[[sum(R(i,j,k,k) for k in range(2)) for j in range(2)] for i in range(2)]
verify('ricci_model_trace_zero',ricci==[[0,0],[0,0]])
def H(a,b):
    return Fraction(a**4+b**4-4*a*a*b*b,(a*a+b*b)**2)
verify('ricci_zero_not_flat',R(0,0,0,0)==1)
verify('ricci_zero_not_sectional_one_sign',H(1,0)==1 and H(1,1)==Fraction(-1,2))

# Independent generating-series ranks for polynomial jets.
def convolution(a,b,M):
    return [sum(a[j]*b[t-j] for j in range(t+1)) for t in range(M+1)]
rank_cases=0
for n,k in product(range(1,5),range(1,6)):
    M=12; coefficients=[1]+[0]*M
    for j in range(1,k+1):
        factor=[comb(n+t//j-1,t//j) if t%j==0 else 0 for t in range(M+1)]
        coefficients=convolution(coefficients,factor,M)
    actual=[0]*(M+1)
    for row in product(*(range(M//j+1) for j in range(1,k+1))):
        degree=sum(j*a for j,a in enumerate(row,1))
        if degree<=M:
            actual[degree]+=prod(comb(n+a-1,a) for a in row)
            verify('weighted_versus_tensor_bounds',(degree+k-1)//k<=sum(row)<=degree)
    for m in range(M+1):
        verify('GG_graded_rank_generating_series',actual[m]==coefficients[m]);rank_cases+=1
verify('weighted_degree_not_tensor_degree',2*1!=1)

# Periodic Fourier differentiation never produces a zero-frequency constant.
for dimension in range(1,5):
    velocity=tuple(range(1,dimension+1))
    for frequency in product(range(-2,3),repeat=dimension):
        multiplier=-sum(v*f for v,f in zip(velocity,frequency))**2
        constant_coefficient=multiplier if all(f==0 for f in frequency) else 0
        verify('periodic_directional_second_derivative_mean',constant_coefficient==0)

result={
 'schema_version':1,
 'purpose':'Independent finite algebraic controls, not an analytic or geometric proof certificate.',
 'assertions_passed':count,
 'families':families,
 'complete_intersection_formal_cases':adjunction,
 'graded_rank_cases':rank_cases,
 'negative_controls_rejected':[
  'Sphere average with only one contraction',
  'Directed positivity implies total positivity',
  'Directed positivity implies positive full trace or determinant',
  'Ricci-flat implies flat',
  'Ricci-flat implies one-signed sectional curvature',
  'Weighted jet degree equals number of tensor factors',
  'A periodic directional second derivative can have strictly positive mean'
 ],
 'original_problem_solved':False,
 'analytic_proofs_verified_by_code':False
}
print(json.dumps(result,indent=2,sort_keys=True))
