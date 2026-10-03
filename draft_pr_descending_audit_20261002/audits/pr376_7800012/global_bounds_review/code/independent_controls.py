#!/usr/bin/env python3
"""Exact controls not importing candidate code; rational complex phases."""
from fractions import Fraction as F
from collections import defaultdict,Counter
from itertools import product
from pathlib import Path
import json,random,math

Z=(F(0),F(0));O=(F(1),F(0))
def plus(a,b): return (a[0]+b[0],a[1]+b[1])
def times(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conjugate(a): return (a[0],-a[1])
def scaled(a,n): return (n*a[0],n*a[1])
def norm2(rows): return sum(z[0]**2+z[1]**2 for row in rows for z in row.values())
def matrix(l,hor,ver):
    rows=[{} for _ in range(l*l)]
    index=lambda x,y:(x%l)+l*(y%l)
    for y in range(l):
        for x in range(l):
            a=index(x,y)
            for b,z in [(index(x+1,y),hor[x,y]),(index(x,y+1),ver[x,y])]:
                rows[a][b]=z;rows[b][a]=conjugate(z)
    return rows
def multiply_right(rows,adj):
    out=[]
    for row in rows:
        nxt=defaultdict(lambda:Z)
        for a,z in row.items():
            for b,w in adj[a].items(): nxt[b]=plus(nxt[b],times(z,w))
        out.append({a:z for a,z in nxt.items() if z!=Z})
    return out
def fluxes(l,hor,ver):
    return {(x,y):times(times(hor[x,y],ver[(x+1)%l,y]),times(conjugate(hor[x,(y+1)%l]),conjugate(ver[x,y]))) for y in range(l) for x in range(l)}
checks=0
def check(x):
    global checks
    assert x;checks+=1

def check_matrix(l,hor,ver):
    n=l*l;rows=matrix(l,hor,ver);t2=multiply_right(rows,rows);t3=multiply_right(t2,rows)
    f=fluxes(l,hor,ver);s=sum(z[0] for z in f.values())
    es=[((x,y),((x+1)%l,y)) for y in range(l) for x in range(l)]+[((x,y),(x,(y+1)%l)) for y in range(l) for x in range(l)]
    rr=sum(times(f[p],f[q])[0] for p,q in es)
    moments=[norm2(rows),norm2(t2),norm2(t3)]
    check(moments==[4*n,28*n+8*s,232*n+144*s+12*rr])
    d=norm2([{a:plus(t3[i].get(a,Z),scaled(rows[i].get(a,Z),-8)) for a in set(t3[i])|set(rows[i])} for i in range(n)])
    check(d==40*n+16*s+12*rr)
    sos=F(48,n)*(s+F(n,6))**2+6*sum((f[p][0]+f[q][0]-2*s/n)**2+(f[p][1]-f[q][1])**2 for p,q in es)
    check(d-F(44*n,3)==sos);check(d>=F(44*n,3))
    check(all(times(z,conjugate(z))==O for row in rows for z in row.values()))
    return {'L':l,'tr2':str(moments[0]),'tr4':str(moments[1]),'tr6':str(moments[2]),'defect':str(d),'sos_residual':str(sos)}

# Independently count reduced words: stack cancellation proves 232 tree-like
# walks rather than classifying by the candidate's winding enumerator.
steps=((1,0),(-1,0),(0,1),(0,-1))
classification=Counter()
for word in product(steps,repeat=6):
    if tuple(map(sum,zip(*word)))!=(0,0): continue
    stack=[]
    for step in word:
        if stack and stack[-1]==(-step[0],-step[1]): stack.pop()
        else: stack.append(step)
    # Cyclic free reduction eliminates excursions spanning the chosen root.
    while len(stack)>=2 and stack[0]==(-stack[-1][0],-stack[-1][1]): stack=stack[1:-1]
    if not stack: classification['empty']+=1
    elif len(stack)==4: classification['square']+=1
    elif len(stack)==6: classification['rectangle']+=1
    else: raise AssertionError(stack)
check(dict(classification)=={'empty':232,'square':144,'rectangle':24})

rng=random.Random(202610030548)
roots=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1)),(F(3,5),F(4,5)),(F(3,5),F(-4,5))]
cases=[]
for l in [8,8,10]:
    hor={(x,y):rng.choice(roots) for y in range(l) for x in range(l)}
    ver={(x,y):rng.choice(roots) for y in range(l) for x in range(l)}
    cases.append(check_matrix(l,hor,ver))

# Deliberately invalid-size mutants: local walk formulas need no winding.
mutants=[]
for l,k in [(4,2),(6,3)]:
    hor={(x,y):O for y in range(l) for x in range(l)}
    ver=dict(hor);rows=matrix(l,hor,ver);power=rows
    for _ in range(1,k): power=multiply_right(power,rows)
    got=norm2(power);local=(36 if k==2 else 400)*l*l
    check(got-local==4*l*l)
    mutants.append({'mutant':'drop size threshold','L':l,'power':2*k,'actual':str(got),'false_local_prediction':local,'excess':4*l*l,'status':'FALSIFIED'})

# Strictly better mixed-rank allocation control. Each fixed
# spectrum has a convex E_r sequence, but a minimum over choices need not.
def energy(vals,r): return sum(sorted(vals)[:r],F(0))
spectra=[[F(-4),F(-1)]+[F(5,6)]*6,[F(-2)]*4+[F(2)]*4]
values=[min(energy(v,r) for v in spectra) for r in range(9)]
q=2
envelope=min(F(b-q,b-a)*values[a]+F(q-a,b-a)*values[b] for a in range(q+1) for b in range(q,9) if a!=b)
check(envelope<values[q]);check(envelope==F(-16,3))
# This abstract same-block-list control is not a lattice realization.
allocation_control={'values':[str(v) for v in values],'quarter':str(values[q]),'convexified_quarter':str(envelope),'realizability':'abstract only'}

# Exact symbolic countercontrol recorded as integer comparisons.
check(35>32)
mutants.append({'mutant':'second/fourth moments determine quarter energy','positive_squared_magnitudes_A':'(7,5,2+sqrt(3),2-sqrt(3))','positive_squared_magnitudes_B':'(8,4,2,2)','tr2':32,'tr4':176,'energy_A':'-sqrt(7)-sqrt(5)','energy_B':'-sqrt(8)-2','exact_comparison':'35>32 implies sqrt(35)>4*sqrt(2), so energy_A<energy_B','realizability':'abstract bipartite spectra, not asserted lattice realizable','status':'FALSIFIED'})

receipt={'status':'PASS','assertions':checks,'arithmetic':'exact fractions and Gaussian rationals','reduction_classification':dict(classification),'rational_phase_matrix_cases':cases,'invalid_generalization_mutants':mutants,'convexification_control':allocation_control,'universal_proof_boundary':'Finite exact controls supplement written proofs; no finite sampling is claimed universal.'}
out=Path(__file__).absolute().parent.parent/'receipts/independent_controls.json'
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
