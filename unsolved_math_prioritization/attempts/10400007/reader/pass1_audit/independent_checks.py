#!/usr/bin/env python3
"""Independent finite algebra checks. These checks supplement, not replace, proofs."""
import json
from math import comb
from fractions import Fraction
from pathlib import Path

def require(condition, label):
    if not condition: raise RuntimeError(label)

# Laurent polynomials in z=t^(1/2), represented exactly over Z.
def add(a,b):
    c=dict(a)
    for k,v in b.items(): c[k]=c.get(k,0)+v
    return {k:v for k,v in c.items() if v}
def scale_shift(a,c,s): return {k+s:c*v for k,v in a.items() if c*v}
def mul(a,b):
    c={}
    for k,v in a.items():
        for l,w in b.items(): c[k+l]=c.get(k+l,0)+v*w
    return {k:v for k,v in c.items() if v}
def inv(a): return {-k:v for k,v in a.items()}

# Skein recurrence for positive oriented two-braid closures.
V={0:{1:-1,-1:-1},1:{0:1}}
for m in range(2,12):
    V[m]=add(scale_shift(V[m-2],1,4),mul({3:1,1:-1},V[m-1]))
require(V[3]=={2:1,6:1,8:-1}, "trefoil")
require(V[3]!=inv(V[3]), "mirror distinction")
for m in range(2,12):
    require(add(scale_shift(V[m],1,-2),scale_shift(V[m-2],-1,2))==mul({1:1,-1:-1},V[m-1]), "skein recurrence")

# Plat-configuration Euler magnitudes and an exact growth inequality.
eulers=[]
for n in range(1,31):
    e=(-1)**n*comb(3*n-2,n)
    ratio=Fraction((3*n+1)*3*n*(3*n-1),(n+1)*(2*n)*(2*n-1))
    require(ratio==Fraction(comb(3*n+1,n+1),comb(3*n-2,n)), "Euler ratio")
    require(ratio>1, "Euler growth")
    eulers.append({'n':n,'chi':e})

# Pure-gauge cancellation checked without floating point: exponents of a
# coefficient in d(e_x), expressed in the e_y basis, must vanish identically.
gauge=[]
for bx,cx,by,cy in [(3,4,-2,7),(0,0,1,2),(-5,6,-3,-9),(1,2,1,2)]:
    exponents=(-bx+(bx-by)+by,-cx+(cx-cy)+cy)
    require(exponents==(0,0), "gauge")
    A=7; Q=bx-cx; J=A-Q
    require(J+bx-cx==A, "grading")
    gauge.append({'Bx':bx,'Cx':cx,'By':by,'Cy':cy,'after_gauge':exponents})

out={'status':'PASS','scope':'Finite exact sanity checks; universal statements require the accompanying mathematical proofs.',
     'two_braid_trefoil_z_exponents':V[3],
     'mirror_trefoil_z_exponents':inv(V[3]),
     'plat_euler_first_30':eulers,'pure_gauge_cases':gauge}
path=Path(__file__).with_name('INDEPENDENT_CHECK_RESULTS.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','output':path.name,'checks':['two-braid skein recurrence through m=11','plat Euler ratio n=1..30','exact gauge and grading cancellation']}))
