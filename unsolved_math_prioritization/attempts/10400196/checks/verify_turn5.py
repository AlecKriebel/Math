#!/usr/bin/env python3
"""Finite exact controls only; topology and Floer inputs require the cited proofs."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(value, name):
    assert value, name
    C[name]+=1
# Primary-input calibrations; arithmetic is checked, not the Floer calculation itself.
rows=[('minus_Sigma235',F(-2),0,F(1)),('Sigma237',F(0),-1,F(-1))]
for name,d,chi,lam in rows:
    ck(F(chi)-d/2==lam,'credited_Casson_normalization_control')
    ck((8*lam)%16==8,'same_Rochlin_value_control')
    ck((8*(F(chi)-d/2))%16==8,'Euler_correction_repairs_pair')
ck((-4*rows[0][1])%16==8 and (-4*rows[1][1])%16==0,'Floer_lift_separates_pair')
# Congruence d=(c^2-signature)/4 mod2 implies -4d has the positive Brown reduction.
for sig in [-3,-1,0,1,4]:
    for square in [F(-7,4),F(-1,3),F(0),F(1,4),F(9,4),F(8)]:
        for k in [-2,-1,0,1,2]:
            d=(square-sig)/4+2*k
            ck((-4*d-(sig-square))%8==0,'absolute_grading_implies_Brown_lift')
            for chi in [-2,-1,0,1,2]:
                fe=8*(F(chi)-d/2)
                ck((fe+4*d)%8==0,'Euler_lift_preserves_Brown_reduction')
# All four d values in one congruence class modulo2, with independent integer chis.
# This finite grid confirms the exact criterion, not that all tuples are realized.
for rho in [F(0),F(1,4),F(2,3)]:
    for k in product([-1,0,1],repeat=4):
        ds=[rho+2*x for x in k]
        dd=ds[0]-ds[1]-ds[2]+ds[3]
        ck((dd/2).denominator==1,'Brown_invariance_supplies_integer_half_difference')
        for chi in [(0,0,0,0),(0,0,0,1),(1,-1,2,-2),(-1,2,0,1)]:
            hs=[F(c)-d/2 for c,d in zip(chi,ds)]
            dh=hs[0]-hs[1]-hs[2]+hs[3]
            ck(dh.denominator==1,'Euler_second_difference_integral')
            ck(((8*dh)%16==0)==(dh%2==0),'degree_one_equivalent_to_even_second_difference')
# I^2 need not force even coefficients in integral finite cyclic group rings.
def mul(a,b):
    n=len(a);out=[0]*n
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[(i+j)%n]+=x*y
    return out
x=[-1,1,0,0];square=mul(x,x)
ck(square==[1,-2,1,0],'augmentation_square_exact')
ck(sum(square)==0,'augmentation_square_has_augmentation_zero')
ck(any(c%2 for c in square),'augmentation_square_not_two_divisible')
# kappa(Z[G]) at r=2 even contains coefficients with denominators.
kap=[F(3,4),F(-1,4),F(-1,4),F(-1,4)]
ck(sum(kap)==0 and kap[0]==F(3,4),'finite_cyclic_kappa_has_no_even_coefficient_conclusion')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'scope':'Arithmetic and parity controls only. Cited Floer calculations, topology, Y2 classification and all-manifold degree claims are not certified by this finite checker. Original target remains unsolved5/5.'},indent=2))
