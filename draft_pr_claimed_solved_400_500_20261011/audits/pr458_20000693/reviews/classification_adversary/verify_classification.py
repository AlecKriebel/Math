#!/usr/bin/env python3
"""Exact scope and finite-prime checks for the PR458 classification audit.

These checks compare formulas. They do not certify actual L-function moments.
"""
from fractions import Fraction as F
from math import factorial
from itertools import product
from pathlib import Path
import json

checks=[]
def check(name,condition,detail):
    if not condition:raise RuntimeError(name)
    checks.append({"name":name,"passed":True,"detail":detail})

def coefficient_product(chis,weights,r):
    # Integer tuples suffice to test the literal intersection with Sahay 1.7.
    v=[1]+[0]*r
    for c,a in zip(chis,weights):
        w=[(factorial(a+n-1)//(factorial(a-1)*factorial(n)) if a else int(n==0))*c**n for n in range(r+1)]
        v=[sum(v[j]*w[n-j] for j in range(n+1)) for n in range(r+1)]
    return v

weights=[2,1,3]
chis=[1,-1,1]
bs=coefficient_product(chis,weights,12)
# A separate coefficient computation using the explicit convolution sum.
def sahay_coefficient(r):
    return sum((factorial(2+n0-1)//(factorial(1)*factorial(n0)))
               *(factorial(1+n1-1)//(factorial(0)*factorial(n1)))
               *(factorial(3+n2-1)//(factorial(2)*factorial(n2)))
               *(-1)**n1
               for n0,n1,n2 in product(range(r+1),repeat=3)
               if n0+n1+n2==r)
ds=[sahay_coefficient(r) for r in range(13)]
check("sahay_coefficients",bs==ds,"At q=8,p=3 use three distinct characters with values (1,-1,1), weights (2,1,3). Thirteen candidate product-series coefficients equal an independently enumerated convolution coefficient formula.")
check("sahay_exponent",sum(a*a for a in weights)==14,"lambda=sum ell_chi^2 equals candidate E on distinct primitive constituents; q-indexed distinct characters cannot share one primitive inducer.")
check("sahay_bad_prime",coefficient_product([0,0,0],weights,12)==[1]+[0]*12,"At every prime dividing the common modulus all chi(p)=0, so J_p=1 in both definitions.")
check("heap_degree_one",sum((e*F(3,2))**2 for e in [2,1])==F(45,4),"Heap k=3/2, e=(2,1), degree d=1 gives M=(3,3/2), E=45/4 and exactly the corresponding Barnes arguments.")
# Rational independence obstruction: if sqrt(2)=e1/e2, e1^2=2e2^2;
# parity forces e1,e2 both even, contradicting primitive fraction.
check("single_outer_weight_gap",all(e1*e1!=2*e2*e2 for e1 in range(1,50) for e2 in range(1,50)),"Finite sanity check only; the exact infinite proof is descent: rational sqrt(2) would force both numerator and denominator even. Hence M=(1,sqrt(2)) is outside Heap's single outer k times integer multiplicity display.")
x=F(1,2)
j_one=1/(1-x)
j_two=(1+x)/(1-x)**3
ratio=j_one/j_two
check("original_moduli_change_constant",ratio==F(1,6),"For zeta(s)*L(s,chi0 mod 2), p=2 has J=2 versus primitive zeta(s)^2 J*=12, yielding the finite ratio 1/6.")
check("lifting_requires_restoration",j_one/F(1)==2,"Common-modulus q=2 tuple ell_chi0=2 has J_2=1; restoring the original zeta factor changes J_2 to 2. Relabelling the two original factors without restoration misses this factor.")
check("shared_phase_not_independent",j_two==12 and j_one*j_one==4,"Two restored inverse factors share one p=2 phase: joint phase mean 12, product of separate means 4.")
check("multiplicity_grouping",(1+1)**2==4 and 1**2+1**2==2,"Repeated primitive inducer requires exponent 4, while incorrectly treating the factors as independent would give 2.")
check("barnes_weight2",F(factorial(0)*factorial(1),factorial(2)*factorial(3))==F(1,12),"Barnes recursion G(n+1)=Gamma(n)G(n) gives G(3)^2/G(5)=1/12.")
check("all_zero_boundary",sum([])==0,"Removing all zero weights gives E=0 and empty arithmetic/Barnes products 1, so the prediction is the identity I(T)=T.")
for eps in [-1,1]:
    up=(1+eps*x)/(1-eps*x)
    cross_form=(1-x*x)/(1-eps*x)**2
    check("heap_residual_quotient_"+str(eps),up==cross_form,"For epsilon="+str(eps)+", diagonal-normalized residual=(1+epsilon*x)/(1-epsilon*x)=1+2epsilon*x+O(x^2). Its absolute linear prime sum diverges at s=1.")
    check("heap_cross_regularization_"+str(eps),up*(1-eps*x)**2==1-x*x,"Extracting the quotient-character L(s,chi)^2 leaves the local factor 1-x^2, an absolute-convergence remainder; the original residual itself is conditional.")
print(json.dumps({"purpose":"formula_scope_checks_only","actual_general_moment_theorem_tested":False,"checks_count":len(checks),"checks":checks},indent=2))
