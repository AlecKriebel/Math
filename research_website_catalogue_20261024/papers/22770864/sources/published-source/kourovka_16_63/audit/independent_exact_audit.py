#!/usr/bin/env python3
"""Third reconstruction from paper formulas, using arbitrary-precision integers.
Does not import any supplied mathematical implementation. The proposed pivot
plan is checked against a freshly built matrix at precision five.
"""
from pathlib import Path
from itertools import combinations
from math import factorial, comb
import json, time, hashlib
ROOT=Path(__file__).resolve().parents[1]
LOGDIR=Path(__file__).resolve().parent/"reproduction"
LOGDIR.mkdir(exist_ok=True)
P=1009; D=31

def diff(a,r):
    return factorial(a)//factorial(a-r) if 0<=r<=a else 0

def tx(m,n,r,i,j):
    return sum((-1)**q*comb(r,q)*diff(m-i,r-q)*diff(i,q)*diff(n-j,q)*diff(j,r-q) for q in range(r+1))

C={}
def setc(i,j,k,v):
    if v:
        assert i!=j
        assert (i,j,k) not in C or C[i,j,k]==v
        C[i,j,k]=v;C[j,i,k]=-v
setc(0,1,1,2);setc(0,2,2,-2);setc(1,2,0,1)
mods=[(6,3),(4,10),(6,15),(2,22),(4,25),(0,30)]
for m,s in mods:
    for i in range(m+1):
        setc(0,s+i,s+i,m-2*i)
        if i:setc(1,s+i,s+i-1,i)
        if i<m:setc(2,s+i,s+i+1,m-i)
for a,b,c,r in [(0,0,2,3),(0,1,3,4),(0,2,3,5),(0,4,3,4),(1,1,3,3),(1,4,5,4),(4,4,3,3)]:
    m,s=mods[a];n,t=mods[b];out,u=mods[c]
    assert out==m+n-2*r
    for i in range(m+1):
        for j in range(n+1):
            if a==b and i>=j:continue
            if 0<=i+j-r<=out:setc(s+i,t+j,u+i+j-r,tx(m,n,r,i,j))

def br(x,y,tab=C):
    z={}
    for (a,b,k),v in tab.items():
        z[k]=z.get(k,0)+x.get(a,0)*y.get(b,0)*v
    return {k:v for k,v in z.items() if v}
E=[{i:1} for i in range(D)]
def jac(tab):
    count=0
    for i,j,k in combinations(range(D),3):
        z={}
        for a,b,c in [(i,j,k),(j,k,i),(k,i,j)]:
            for q,v in br(E[a],br(E[b],E[c],tab),tab).items():z[q]=z.get(q,0)+v
        assert all(v==0 for v in z.values()),(i,j,k,z)
        count+=1
    return count
start=time.monotonic();checks=jac(C)
others=[i for i in range(D) if i not in (0,1,3)]
basis=[E[0],{j:1 for j in (1,2,4,10,27)},E[3]]+[E[i] for i in others]
def adapted(z):
    return [z.get(0,0),z.get(1,0),z.get(3,0)]+[z.get(i,0)-(z.get(1,0) if i in (2,4,10,27) else 0) for i in others]
assert all(adapted(basis[i])==[int(i==j) for j in range(D)] for i in range(D))
Ca={}
for i,j in combinations(range(D),2):
    for k,v in enumerate(adapted(br(basis[i],basis[j]))):
        if v:Ca[i,j,k]=v;Ca[j,i,k]=-v
assert jac(Ca)==checks
w=[0,0,1]+[2]*28
scaled={(i,j,k):v*P**(2+w[i]+w[j]-w[k]) for (i,j,k),v in Ca.items()}
terms=[[i,j,k,v] for (i,j,k),v in sorted(C.items()) if i<j]
assert json.loads((ROOT/'data/lie31_brackets.json').read_text())['terms']==terms
presentation=json.loads((ROOT/'data/group_lie_presentation.json').read_text())
assert presentation['bracket_terms_i_lt_j']==[[i,j,k,v] for (i,j,k),v in sorted(scaled.items()) if i<j]
assert presentation['weights_w']==w and presentation['rank']==D and presentation['prime']==P
assert presentation['coefficient_ring']['exponent']==1689
assert presentation['group_order']==presentation['full_automorphism_order']=={'base':P,'exponent':52359}

def delta(tab):
    for i,j in combinations(range(D),2):
        for k in range(D):
            row={}
            for a in range(D):
                for col,v in [(k*D+a,tab.get((i,j,a),0)),(a*D+i,-tab.get((a,j,k),0)),(a*D+j,-tab.get((i,a,k),0))]:
                    row[col]=row.get(col,0)+v
            yield {c:v for c,v in row.items() if v}

def rank(rows,p=P):
    piv={}
    for source in rows:
        row={c:v%p for c,v in source.items() if v%p}
        while row:
            c=min(row);v=row[c]
            if c not in piv:
                iv=pow(v,-1,p);piv[c]={j:a*iv%p for j,a in row.items()};break
            for j,a in piv[c].items():
                q=(row.get(j,0)-v*a)%p
                if q:row[j]=q
                else:row.pop(j,None)
    return len(piv)
inner=rank([{a:C.get((a,j,k),0) for a in range(D)} for j in range(D) for k in range(D)])
dr=rank(delta(C));assert inner==30 and dr==931
unscaled=list(delta(C))
cert=json.loads((ROOT/'data/delta_rank_certificate.json').read_text())
minor=[[unscaled[i].get(j,0)%P for j in cert['pivot_columns']] for i in cert['source_rows']]
rawminor=(ROOT/'data/delta_rank_minor.txt').read_text().splitlines()
assert list(map(int,rawminor[0].split()))==[931,P]
assert minor==[list(map(int,line.split())) for line in rawminor[1:]]
assert rank([{j:v for j,v in enumerate(row) if v} for row in minor])==931

# Reconstruct exact matrix and perform elementary elimination modulo p^5.
# All arithmetic uses Python integers; no machine-width wraparound is possible.
precision=5;mod=P**precision
matrix={r:{c:v%mod for c,v in row.items() if v%mod} for r,row in enumerate(delta(scaled))}
matrix={r:row for r,row in matrix.items() if row}
plan=json.loads((ROOT/'data/smith_pivot_plan.json').read_text())
textplan=(ROOT/'data/smith_pivot_plan.txt').read_text().splitlines()
assert int(textplan[0])==len(plan)==931
assert [list(map(int,line.split())) for line in textplan[1:]]==[[q['row'],q['col'],q['valuation']] for q in plan]
usedcols=set();hist={};previous=-1
for step,item in enumerate(plan):
    r,c,v=(item[k] for k in ('row','col','valuation'))
    assert r in matrix and c not in usedcols
    power=P**v;value=matrix[r][c]
    assert v<precision and value%power==0 and value%(power*P)!=0
    assert v>=previous
    if v!=previous:
        assert all(a%power==0 for row in matrix.values() for a in row.values())
        previous=v
    inv=pow(value//power,-1,mod)
    pivot={j:a*inv%mod for j,a in matrix.pop(r).items()}
    assert pivot[c]==power
    assert all(a%power==0 for a in pivot.values())
    for q,row in list(matrix.items()):
        x=row.get(c,0)
        if not x:continue
        assert x%power==0
        f=x//power
        for j,a in pivot.items():
            z=(row.get(j,0)-f*a)%mod
            if z:row[j]=z
            else:row.pop(j,None)
        assert c not in row
        if not row:matrix.pop(q)
    usedcols.add(c);hist[v]=hist.get(v,0)+1
assert not matrix
assert hist=={0:87,1:55,2:758,3:6,4:25}
# Compare every numeric array in the original NumPy archive, if numpy is present.
archive_checked=False
try:
    import numpy as np
    archive=np.load(ROOT/'data/lie31_tables.npz',allow_pickle=False)
    for name,tab in [('C',C),('Ca',Ca)]:
        assert archive[name].shape==(D,D,D)
        assert all(int(archive[name][i,j,k])==tab.get((i,j,k),0) for i in range(D) for j in range(D) for k in range(D))
    assert archive['weights'].tolist()==w
    assert archive['P'].tolist()==[[basis[j].get(i,0) for j in range(D)] for i in range(D)]
    assert archive['Pinv'].tolist()==[[adapted(E[j])[i] for j in range(D)] for i in range(D)]
    archive_checked=True
except ImportError:pass
result={'status':'INDEPENDENT_EXACT_AUDIT_PASSED','jacobi_triples_per_basis':checks,
    'integer_coefficients':len(terms),'adapted_coefficients':len(Ca)//2,'max_abs_coefficient':max(map(abs,C.values())),
    'max_abs_scaled_coefficient':max(map(abs,scaled.values())),'inner_rank':inner,'derivation_rank':dr,
    'rank_minor_reconstructed_and_checked':True,'smith_precision':precision,'smith_multiplicities':hist,
    'smith_sum':sum(v*n for v,n in hist.items()),'residual_block_zero':not matrix,
    'portable_presentation_all_coefficients_match':True,'numpy_archive_all_arrays_match':archive_checked,
    'elapsed_seconds':time.monotonic()-start}
(LOGDIR/'independent_exact_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
