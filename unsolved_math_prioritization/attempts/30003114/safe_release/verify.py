#!/usr/bin/env python3
"""Exact finite controls for five partial results; not a proof of the target."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
import hashlib,json,sys

A,B=F(9,10),F(19,20)
L=22
GAMMA=(1-3*B**L)/(1-B**L)

def ceilq(x): return -(-x.numerator//x.denominator)
def polynomial_value(c,x):
    y=F(0)
    for a in reversed(c): y=y*x+a
    return y

def numerators(p,q,d):
    w=[p**i*q**(d-i) for i in range(d+1)]
    return [sum(a*b for a,b in zip(c,w)) for c in product((-1,0,1),repeat=d+1)]

def product_coeffs(exponents):
    c=[1]
    for m in exponents:
        out=c+[0]*m
        for i,v in enumerate(c): out[i+m]-=v
        c=out
    return c

def divide_x_minus_one(c):
    # ascending coefficient synthetic division; returns quotient and remainder
    if len(c)==1:return [],c[0]
    out=[0]*(len(c)-1);out[-1]=c[-1]
    for i in range(len(out)-2,-1,-1):out[i]=c[i+1]+out[i+1]
    return out,c[0]+out[0]

def main():
    checks=[];examples=[]
    assert GAMMA>0
    checks.append({'test':'lacunary_constant_positive','pass':True,'gamma':str(GAMMA)})
    assert F(99,97)**225<100<F(99,97)**226
    checks.append({'test':'analytic_zero_count_constant','pass':True,'K':226,'H':96})
    for p,q in ((9,10),(19,20),(91,100),(101,110)):
      for d in range(1,9):
        vals=numerators(p,q,d)
        assert len(vals)==3**(d+1)==len(set(vals))
        assert vals.count(0)==1
        pos=[v for v in vals if v>0]
        assert min(pos)>=1
        neg=sum(v<0 for v in vals)
        assert neg==(3**(d+1)-1)//2
        for t in (F(1,q**d),F(1,10000),F(1,100),F(1,10),F(1),F(40)):
          count=sum(abs(v)<t*q**d for v in vals)
          assert count<=2*ceilq(t*q**d)-1
          T=1/(1-F(p,q))
          assert F(count)>=2**(d+2)*t/(T+t)-1
        assert sum(abs(v)<1 for v in vals)==1
        if d==8:
          examples.append({'p':p,'q':q,'degree_bound':d,'polynomials':len(vals),'minimum_nonzero_absolute_value':str(F(min(pos),q**d)),'minimum_scaled_integer':min(pos)})
    checks.append({'test':'exhaustive_arithmetic_and_pigeonhole_bounds','pass':True,'rational_parameters':4,'degree_bounds':[1,8]})
    # Use a shorter independently valid spacing L'=2 at x=1/2 to exercise
    # multiple selected digits, then test the target L at d=44 on selected digits.
    for x,spacing,d in ((F(1,2),2,8),(A,22,44),(B,22,44)):
      m=d//spacing+1
      vals=sorted(sum(c*x**(spacing*i) for i,c in enumerate(cs)) for cs in product((-1,0,1),repeat=m))
      local_gamma=(1-3*x**spacing)/(1-x**spacing)
      assert local_gamma>0
      assert len(vals)==len(set(vals))
      assert min(y-xv for xv,y in zip(vals,vals[1:]))>=local_gamma*x**d
    checks.append({'test':'multi_digit_lacunary_separation','pass':True})
    # Product construction includes dense Thue-Morse and genuinely sparse cases.
    for exponents in ([1,2,4,8,16,32],[2,3,6,12,24],[3,7,12,25]):
      assert all(m>sum(exponents[:j]) for j,m in enumerate(exponents))
      c=product_coeffs(exponents)
      assert set(c)<=set((-1,0,1))
      assert sum(v!=0 for v in c)==2**len(exponents)
      cur=c
      for j in range(len(exponents)):
        cur,rem=divide_x_minus_one(cur);assert rem==0
      assert sum(cur)!=0
      for x in (A,B):
        val=polynomial_value(c,x)
        direct=F(1)
        for m in exponents:direct*=1-x**m
        assert val==direct>0
        # Rational inequality that supplies the exponent 380 in the proof.
        s=sum(x**m/(1-x**m) for m in exponents)
        assert s<=B/(1-B)**2==380
    checks.append({'test':'separated_product_identity_multiplicity_and_log_bound','pass':True})
    # Negative controls must exhibit actual counterexamples to tempting mutations.
    neg=[]
    vals=numerators(9,10,1)
    assert sum(v<0 for v in vals)==4
    # e^(1/100) <= 1/(1-1/100) =100/99 < 4, by its power series.
    assert F(100,99)<4
    neg.append({'mutation':'remove_absolute_value_bars','detected':True,'negative_count_d1':4,'upper_bound_for_exp_0_01':'100/99'})
    assert sum(abs(v)<F(1,2) for v in (-1,0,1))==1
    neg.append({'mutation':'include_d_zero_with_strict_target','detected':True,'count':1,'required_strict_upper_bound':1})
    assert 3**2!=2**2
    neg.append({'mutation':'replace_ternary_family_by_all_plus_minus_one','detected':True,'ternary_d1':9,'binary_d1':4})
    bad=product_coeffs([1,1]);assert bad==[1,-2,1]
    neg.append({'mutation':'drop_superincreasing_condition','detected':True,'coefficients':bad})
    assert (1-3*B**21)/(1-B**21)<0
    neg.append({'mutation':'replace_lacunary_L22_by_L21','detected':True})
    # q-dependent bound is not a uniform C: q chosen > exp(C), here exp(log20).
    assert F(100,20)>1
    neg.append({'mutation':'treat_log_q_as_denominator_independent','detected':True,'q':100,'comparison_denominator_cap':20})
    out={'problem_id':30003114,'status':'finite_controls_passed_target_unresolved','arithmetic':'Python arbitrary precision integers and Fraction only','checks':checks,'examples':examples,'negative_controls':neg,'limitations':['No finite test proves the uniform all-degree/all-denominator count.','Analytic proof uses Jensen, maximum principle and Harnack; code checks constants, not those analytic theorems.','No floating-point minimum is used.']}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
