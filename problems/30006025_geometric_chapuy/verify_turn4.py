#!/usr/bin/env python3
"""Exact supplementary checks for turn 4; standard library only."""
from fractions import Fraction as Q
import json

nchecks = 0
def ck(x):
    global nchecks
    assert x
    nchecks += 1

def atan_bounds(x, even_terms):
    assert even_terms % 2 == 0
    low = sum(((-1)**j * x**(2*j+1) / (2*j+1)
               for j in range(even_terms)), Q(0))
    return low, low + x**(2*even_terms+1)/(2*even_terms+1)

def tan_add(x, y): return (x+y)/(1-x*y)
t = Q(1,5)
t2 = tan_add(t,t)
t4 = tan_add(t2,t2)
ck(t2 == Q(5,12)); ck(t4 == Q(120,119))
ck(tan_add(t4, -Q(1,239)) == 1)
# 0 < 4 atan(1/5)-atan(1/239) < 4/5 < pi/2 fixes the branch.
ck(4*(Q(1,5)-Q(1,5)**3/3)-Q(1,239)>0)
ck(Q(4,5)<1)
a,b=atan_bounds(Q(1,5),8)
c,d=atan_bounds(Q(1,239),4)
lo,hi=16*a-4*d,16*b-4*c
ck(lo < hi); ck(lo>Q(157,50)); ck(hi<Q(22,7))
ck(Q(157,50)**2>9)
ck(Q(157,50)**2*11>108)
ck(Q(22,7)**2*10<99)
ck(Q(157,150)**2*Q(99,100)>Q(26,25)**2)
ck(Q(157,150)**2*Q(99,100)-Q(26,25)**2 == Q(739,250000))
# A=4*pi*(g-1): A^2+4*pi*A has coefficients 16*pi^2*(g^2-g).
ck((16,-32+16,16-16)==(16,-16,0))
for g in range(2,102):
    E,V=6*g-3,4*g-2
    ck(3*V==2*E); ck(V-E+1==2-2*g)
    ck(Q(6*g,E)>1)
    if g>=12: ck(lo*lo*(g-1)>9*g)
    else: ck(hi*hi*(g-1)<9*g)
    if g>=100: ck((lo/3)**2*Q(g-1,g)>Q(26,25)**2)
# Independent rational vectors: net increment, L1, weighted stretch and max error.
vec_cases=0
for E in range(1,21):
    x=[Q(i+1,E+1) for i in range(E)]
    for seed in range(9):
        y=[z*Q(1+((i+seed)%7),4) for i,z in enumerate(x)]
        S,S1=sum(x),sum(y)
        net=S1-S; L1=sum(abs(a-b) for a,b in zip(x,y))
        ck(L1>=net)
        ck(S1/S<=max(b/a for a,b in zip(x,y)))
        ck(max(abs(a-b) for a,b in zip(x,y))>=L1/E)
        ck(sum(a/S*(b/a) for a,b in zip(x,y))==S1/S)
        vec_cases+=1
print(json.dumps({"assertions":nchecks,"arithmetic":"exact fractions; no floating-point tests",
 "pi_lower":str(lo),"pi_upper":str(hi),
 "first_excluded_integer_genus":12,
 "finite_genus_controls":100,"rational_vector_controls":vec_cases,
 "scope":"Exact supplementary algebra; the intrinsic disk theorem is a credited primary dependency."},indent=2)+"\n",end="")
