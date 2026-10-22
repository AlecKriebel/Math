#!/usr/bin/env python3
"""Exact prime-field quotient/rank checks, using raw degree-two generators."""
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import argparse


def require(condition,message):
    if not condition: raise RuntimeError(message)


def rref(rows,p,ncols=None):
    a=[[v%p for v in row] for row in rows]
    ncols=len(a[0]) if a else ncols
    piv=[]; r=0
    for c in range(ncols):
        q=next((q for q in range(r,len(a)) if a[q][c]),None)
        if q is None: continue
        a[r],a[q]=a[q],a[r]
        u=pow(a[r][c],-1,p); a[r]=[(u*v)%p for v in a[r]]
        for k in range(len(a)):
            if k!=r and a[k][c]:
                u=a[k][c]; a[k]=[(v-u*w)%p for v,w in zip(a[k],a[r])]
        piv.append(c); r+=1
        if r==len(a): break
    return a[:r],piv


def setup(n,p):
    mons=list(combinations_with_replacement(range(2*n),2)); ix={m:i for i,m in enumerate(mons)}
    def row(terms):
        v=[0]*len(mons)
        for i,j,c in terms:v[ix[tuple(sorted((i,j)))]]+=c
        return v
    rel=[]
    for i in range(n):
        rel.append(row([(i,n+i,1)]))
        for j in range(i+1,n):rel.append(row([(i,j,1)]))
        for j in range(i,n):rel.append(row([(n+i,n+j,1)]))
        others=[j for j in range(n) if j!=i]
        for j in others[1:]:rel.append(row([(i,n+j,1),(i,n+others[0],-1)]))
    rr,piv=rref(rel,p,len(mons)); free=[j for j in range(len(mons)) if j not in piv]
    def reduce(v):
        v=[z%p for z in v]
        for r,c in zip(rr,piv):
            u=v[c]
            if u:v=[(a-u*b)%p for a,b in zip(v,r)]
        return [v[c] for c in free]
    def multiplication(a,b):
        coeff=a+b
        columns=[reduce(row([(i,j,coeff[i]) for i in range(2*n)])) for j in range(2*n)]
        matrix=list(map(list,zip(*columns)))
        rank=len(rref(matrix,p,2*n)[1])
        square=reduce(row([(i,j,coeff[i]*coeff[j]*(1 if i==j else 2)) for i,j in mons]))
        return rank,any(square)
    return len(free),multiplication


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Also create a new JSON result file; existing files are never overwritten.")
    args = parser.parse_args()
    tests=[]
    for p in [2,3,5,7]:
        for n in range(2,13):
            h2,mult=setup(n,p)
            rank,sq=mult([1]*n,[0]*n)
            expected=2*n-(1 if (n-1)%p==0 else 0)
            require(h2==2*n and rank==expected and sq, f'Witness or quotient failure p={p}, n={n}')
            tests.append(dict(p=p,n=n,h2=h2,rank_x_sum=rank,square_nonzero=sq,expected_lefschetz=(n-1)%p!=0))
    exhaustive=[]
    for p,n in [(2,2),(2,3),(2,4),(3,2),(3,3),(3,4)]:
        h2,mult=setup(n,p); total=0; good=0
        for coeff in product(range(p),repeat=2*n):
            a=list(coeff[:n]); b=list(coeff[n:]); rank,sq=mult(a,b)
            predicted=(n-1)%p!=0 and all(a)
            require((rank==2*n)==predicted, f'Arbitrary-form determinant failure p={p}, n={n}, coeff={coeff}')
            require(not predicted or sq, f'Strong Lefschetz square failure p={p}, n={n}, coeff={coeff}')
            total+=1; good+=rank==2*n
        exhaustive.append(dict(p=p,n=n,forms_checked=total,weak_and_strong_lefschetz_forms=good))
    result=dict(description='Exact modular ranks from the raw quadratic-generator quotient; no floating arithmetic.',grid=tests,exhaustive=exhaustive)
    encoded = json.dumps(result,indent=2)+'\n'
    historical = Path(__file__).with_name('results.json')
    require(encoded.encode('utf-8') == historical.read_bytes(), 'Computed results differ from historical results.json')
    if args.output is not None:
        with args.output.open('x', encoding='utf-8', newline='') as stream:
            stream.write(encoded)
    print(json.dumps(dict(grid_tests=len(tests),exhaustive=exhaustive,status='PASS'),indent=2))
if __name__=='__main__':main()
