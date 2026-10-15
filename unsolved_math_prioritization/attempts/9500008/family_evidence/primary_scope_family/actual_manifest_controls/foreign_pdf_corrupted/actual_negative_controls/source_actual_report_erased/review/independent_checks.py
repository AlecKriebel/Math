#!/usr/bin/env python3
"""Exact independent controls, not simulations or a Brownian-law certificate."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
import sympy as s
checks={}; path_cases=0; point_checks=0; prefix_count=0

def ck(name,value):
    assert bool(value),name
    checks[name]='PASS'
# Treat W's values as symbolic, independently of the source's stopped-walk code.
a,b,d,e=s.symbols('Wa Wau WaT WaTu')
rot=a+d-e
ck('rotation_difference',s.expand(rot-b-((d-e)-(b-a)))==0)
ck('left_endpoint',s.simplify(rot.subs({e:d})-a)==0)
ck('right_endpoint',s.simplify(rot.subs({e:a})-d)==0)
# Vary piece durations, including genuine zero pieces. Use independent direct
# piecewise-linear reversal and test horizons cutting through pieces.
patterns=[(0,1,3,0,2),(2,0,4),(0,0,2,1,1)]
def interp(vals,t):
    i=t.numerator//t.denominator
    if i==len(vals)-1:return vals[i]
    return vals[i]+(t-i)*(vals[i+1]-vals[i])
for lens in patterns:
    n=sum(lens)
    for signs in product((-1,1),repeat=n):
        chunks=[];i=0
        for m in lens:chunks.append(signs[i:i+m]);i+=m
        w=[F(0)];r=[F(0)]
        for chunk in chunks:
            for v in chunk:w.append(w[-1]+v)
            for v in reversed(chunk):r.append(r[-1]+v)
        j=0
        for chunk in chunks:
            m=len(chunk)
            for k in range(2*m+1):
                u=F(k,2);t=j+u
                assert interp(r,t)==w[j]+w[j+m]-interp(w,j+m-u)
                point_checks+=1
            j+=m
        for hh in range(2*n+1):
            H=F(hh,2);L=min(F(n),H+4)
            rg=[F(k,2) for k in range(hh+1)]
            wg=[F(k,2) for k in range(int(2*L)+1)]
            err=max(abs(interp(r,t)-interp(w,t)) for t in rg)
            omega=max(abs(interp(w,t)-interp(w,u)) for t in wg for u in wg if abs(t-u)<=4)
            assert err<=2*omega
        path_cases+=1
ck('rational_path_rotation_and_cut_horizons',path_cases==144)
ck('zero_duration_junctions_included',any(0 in z for z in patterns))
# Two stopped symmetric-walk pieces, each with an independent time-zero coin
# deciding whether its duration is zero; append a fresh four-step tail.
# The concatenated four-step prefix must remain a sequence of fair coins.
counts=Counter()
def stopped(bits,active,level):
    if not active:return ()
    total=0
    for j,v in enumerate(bits,1):
        total+=v
        if total==level:return bits[:j]
    return bits
for raw in product((-1,1),repeat=10):
    q1=stopped(raw[1:3],raw[0]==1,1)
    q2=stopped(raw[4:6],raw[3]==1,-1)
    seq=tuple(-v for v in q1+q2+raw[6:10])
    counts[seq[:4]]+=1
for word in product((-1,1),repeat=4):
    assert counts[word]==64
    prefix_count+=1
ck('randomized_zero_time_regeneration_prefixes',prefix_count==16)
# Constants in the reflection/union bound.
c,m=s.symbols('c m',positive=True)
ck('reflection_exponent',s.simplify((8*s.sqrt(c*m))**2/(16*c)-4*m)==0)
ck('dyadic_cover_count',(2**7+1)-0+1==2**7+2)
e4_lower=sum(F(4)**j/__import__('math').factorial(j) for j in range(4))
ck('exponential_tail_majorant',e4_lower>16)
ck('geometric_ratio',F(2,16)==F(1,8)<1)
ck('summable_majorant_sum',8*F(1,8)/(1-F(1,8))==F(8,7))
# Diffusive rescaling absorbs the error for each fixed finite L.
x=s.symbols('x',positive=True)
ck('scaled_log_error_vanishes',s.limit(s.sqrt(s.log(2+x))/s.sqrt(x),x,s.oo)==0)
out={'named_checks_passed':len(checks),'failed':0,'path_configurations':path_cases,'rotation_grid_equalities':point_checks,'randomized_zero_duration_prefix_laws':prefix_count,'checks':checks,'sympy_version':s.__version__,'scope':'Finite path algebra, zero-duration regeneration analogues, and exact tail constants. Brownian law, independence, and almost-sure statements are proved in the written review, not inferred from these tests.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
