#!/usr/bin/env python3
"""Exact F2 arithmetic for the authored S4 Bockstein calculation.
No network, downloaded source, or third-party package is required.
This checks the published mod-2 ring model, not an integral Fox-Neuwirth differential.
"""
import json, math
from pathlib import Path
MAX_DEGREE = 80

def check(condition, label):
    """Unlike assert, correctness checks must remain active under python -O."""
    if not condition:
        raise RuntimeError('Verification failed: ' + label)

def basis(d):
    return [(a,b,c) for a in range(d+1) for b in range(d//2+1)
            for c in range(d//3+1) if a+2*b+3*c==d and not(a and c)]

def toggle(s,x):
    if x in s:s.remove(x)
    else:s.add(x)

def differential(p):
    out=set()
    for a,b,c in p:
        if (a+b)%2 and c==0:toggle(out,(a+1,b,c))
        if b%2 and a==0:toggle(out,(0,b-1,c+1))
    return out

def multiply_x(p):return {(a+1,b,c) for a,b,c in p if c==0}
def multiply_y(p):return {(a,b+1,c) for a,b,c in p}
def symmetric_power(m):
    p0,p1=set(),{(1,0,0)}
    if m==0:return p0
    for _ in range(2,m+1):p0,p1=p1,multiply_x(p1)^multiply_y(p0)
    return p1

def skyline(d):
    out=[]
    for i in range(d+1):
        j=d-i
        if i<j:out.append((f'Q({i},{j})',{(a,b+i,c) for a,b,c in symmetric_power(j-i)}))
    for c in range(d//3+1):
        if (d-3*c)%2==0:
            b=(d-3*c)//2
            out.append((f'M({b},{c})',{(0,b,c)}))
    return out

def rank(cols):
    piv={}
    for v in cols:
        while v:
            k=v.bit_length()-1
            if k in piv:v^=piv[k]
            else:piv[k]=v;break
    return len(piv)

def bits(p,bas):
    ids={x:i for i,x in enumerate(bas)}
    return sum(1<<ids[x] for x in p)

rows=[]
for d in range(MAX_DEGREE+1):
    B,Bn=basis(d),basis(d+1)
    cols=[bits(differential({x}),Bn) for x in B]
    previous=[] if d==0 else [bits(differential({x}),B) for x in basis(d-1)]
    check(all(not differential(differential({x})) for x in B), 'Original verification condition at line 62')
    sky=skyline(d)
    check(len(sky)==len(B) and rank([bits(p,B) for _,p in sky])==len(B), 'Original verification condition at line 64')
    survivors=[]
    if d%4==0:survivors.append({(0,d//2,0)})
    if d>=3 and d%4==3:survivors.append({(0,(d-3)//2,1)})
    check(all(not differential(p) for p in survivors), 'Original verification condition at line 68')
    e2=len(B)-rank(cols)-rank(previous)
    check(e2==len(survivors), 'Original verification condition at line 70')
    check(rank(previous+[bits(p,B) for p in survivors])==rank(previous)+e2, 'Original verification condition at line 71')
    # Greedy independent d1 images in degree d select primary integral
    # Bocksteins of actual skyline classes of degree d-1.
    selected=[]; selected_cols=[]
    for name,p in ([] if d==0 else skyline(d-1)):
        col=bits(differential(p),B)
        if rank(selected_cols+[col])>len(selected_cols):
            selected.append(name);selected_cols.append(col)
    check(len(selected)==rank(previous), 'Original verification condition at line 79')
    four=int(d>0 and d%4==0)
    # E2 has exactly one source-target pair z*v^k -> v^(k+1).
    d2out=int(d>=3 and d%4==3)
    d2in=int(d>=4 and d%4==0)
    check(e2-d2out-d2in==int(d==0), 'Original verification condition at line 84')
    rows.append({'degree':d,'mod2_dimension':len(B),'first_bockstein_rank':rank(cols),
                 'E2_dimension':e2,'order2_factors':len(selected),'order4_factors':four,
                 'primary_skyline_sources':selected,
                 'secondary_skyline_source':f'M({d//2-2},1)' if four else None})
# Generic preferred-basis counterexample: exact chain and quotient checks.
D0=[[2,2],[4,0],[-4,0]];D1=[[0,2,2]]
check(all(sum(D1[0][k]*D0[k][j] for k in range(3))==0 for j in range(2)), 'Original verification condition at line 91')
# In cycle coordinates (a,k=x-y), relation lattice has columns (2,4),(2,0).
# Its quotient is Z/2 + Z/4; allowed elements generate a and 2k, not k.
H={(a,k) for a in range(2) for k in range(4)}
allowed={(a,(2*b)%4) for a in range(2) for b in range(2)}
check(len(H)==8 and len(allowed)==4 and (0,1) not in allowed, 'Original verification condition at line 96')
check((4*1)%4==0 and (2*1)%4!=0, 'Original verification condition at line 97')
# Cyclic resolution coefficients and normalized Bocksteins, through degree 80.
for exponent in (1,2,3,4):
    order=2**exponent
    ds=[0 if d%2==0 else order for d in range(MAX_DEGREE+2)]
    check(all(ds[d]*ds[d+1]==0 for d in range(MAX_DEGREE+1)), 'Original verification condition at line 102')
    check(all(ds[d]//order==1 for d in range(1,MAX_DEGREE+1,2)), 'Original verification condition at line 103')
# Exact Mackey orbit enumeration: C8 acts on the 70 four-element subsets.
# Stabilizer C4 occurs only for the even and odd subsets; C2 stabilizers
# act as two transpositions on the selected four letters.
from itertools import combinations
subsets={tuple(c) for c in combinations(range(8),4)}
def shift(t,k):return tuple(sorted((x+k)%8 for x in t))
remaining=set(subsets);orbits=[]
while remaining:
    seed=min(remaining);orbit={shift(seed,k) for k in range(8)}
    remaining-=orbit
    stabilizer=[k for k in range(8) if shift(seed,k)==seed]
    orbits.append({'representative':seed,'orbit_size':len(orbit),
                   'stabilizer_order':len(stabilizer)})
check(len(subsets)==70, 'Original verification condition at line 117')
check(sum(x['orbit_size'] for x in orbits)==70, 'Original verification condition at line 118')
check(sorted(x['stabilizer_order'] for x in orbits)==[1]*8+[2,4], 'Original verification condition at line 119')
check([x['representative'] for x in orbits if x['stabilizer_order']==4]==[(0,2,4,6)], 'Original verification condition at line 120')
# Transfer-square coefficient for the equal width-four gathered columns.
check(math.comb(4,2)%2==0, 'Original verification condition at line 122')
# C8 regular-representation p2 restriction coefficient (an optional cross-check).
check((1**2*2**2+1**2*3**2+2**2*3**2)%8==1, 'Original verification condition at line 124')
# The S4 block has odd-index inclusion for 4 <= n <= 7.
check([math.comb(n,4) for n in range(4,8)]==[1,5,15,35], 'Original verification condition at line 126')
check(all(math.comb(8,a)%2==0 for a in range(1,8)), 'Original verification condition at line 127')
result={'status':'PASS','scope':'Exact algebra checks; not a general skyline-conjecture test',
        'max_degree':MAX_DEGREE,'S4_rows':rows,
        'abstract_counterexample':{'cohomology_order':8,'allowed_subgroup_order':4,'index':2},
        'cyclic_resolutions_checked':[2,4,8,16],
        'C8_Mackey_orbits':orbits,
        'S4_odd_indices':[1,5,15,35],
        'S8_equal_column_transfer_coefficient':math.comb(4,2)}
Path(__file__).with_name('TEST_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','max_degree':MAX_DEGREE,
                  'S4_degrees_checked':len(rows),'abstract_counterexample_index':2}))
