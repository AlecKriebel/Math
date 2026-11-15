"""Finite F_2 checks of graphs.tex Lemma gr:programs; standard library only.
Does not verify the arithmetic theta bridge or the full 2-converse theorem.
"""
from itertools import combinations
import json

def tr(a):
    return [list(row) for row in zip(*a)] if a else []

def mul(a,b):
    return [[sum(x*y for x,y in zip(r,c))%2 for c in tr(b)] for r in a]

def det(a):
    a=[r[:] for r in a]; n=len(a)
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None: return 0
        a[j],a[pivot]=a[pivot],a[j]
        for i in range(j+1,n):
            if a[i][j]: a[i]=[x^y for x,y in zip(a[i],a[j])]
    return 1

def inv(a):
    n=len(a); z=[a[i][:]+[int(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if z[i][j]); z[j],z[pivot]=z[pivot],z[j]
        for i in range(n):
            if i!=j and z[i][j]: z[i]=[x^y for x,y in zip(z[i],z[j])]
    return [r[n:] for r in z]

def adj(a):
    n=len(a)
    return [[det([[a[r][c] for c in range(n) if c!=i]
                  for r in range(n) if r!=j]) for j in range(n)] for i in range(n)]

def pairing(c,a,d):
    return sum(c[i]*a[i][j]*d[j] for i in range(len(c)) for j in range(len(d)))%2

def program(b,singular,epsilon=0):
    n=3*b; basis=[[0]*n for _ in range(n)]
    block=[[1,1,0],[1,0,1],[1,0,0]] # Columns e=(111),u=(100),v=(010).
    for i in range(b):
        for r in range(3):
            for c in range(3): basis[3*i+r][3*i+c]=block[r][c]
    qa=[[0]*n for _ in range(n)]
    for i in range(b):
        qa[3*i][3*i]=1
        for j in range(b):
            t=int(i==j)^int(i==(j+1)%b) if singular else int(i==j)^int(i==j+1)
            qa[3*i+1][3*j+2]=t; qa[3*j+2][3*i+1]=t
    qa[3*(b-1)+2][3*(b-1)+2]=1 if singular else epsilon
    bi=inv(basis); q=mul(mul(tr(bi),qa),bi); c=bi[1][:]
    hs=[]
    for i in range(b):
        e=[int(r//3==i) for r in range(n)]
        hs.append([sum(q[r][j]*e[j] for j in range(n))%2 for r in range(n)])
    return q,c,hs

checked=0
for b in range(1,6):
    variants=[program(b,True),program(b,False,0),program(b,False,1)]
    assert variants[0][1:]==variants[1][1:]==variants[2][1:]
    for mask in range(1<<b):
        groups=[i for i in range(b) if mask>>i&1]; rows=[3*i+j for i in groups for j in range(3)]
        active_map={f'a{i}':bool(mask>>i&1) for i in range(b)}
        second='a1' if b>1 else 'second'; active_map[second]=bool(mask&(2 if b>1 else 1))
        if b>1: active_map['balance']=bool(mask&1)^bool(mask&2)
        active=[a for a,present in active_map.items() if present]; values=[]
        for q,c,hs in variants:
            qj=[[q[r][s] for s in rows] for r in rows]
            cols={a:[0]*len(rows) for a in active}
            for i in groups: cols[f'a{i}']=[hs[i][r] for r in rows]
            for a in ['a0',second]+(['balance'] if b>1 else []):
                if active_map[a]: cols[a]=[x^c[r] for x,r in zip(cols[a],rows)]
            assert [sum(cols[a][i] for a in active)%2 for i in range(len(rows))]==[sum(r)%2 for r in qj]
            ad=adj(qj)
            pairs={tuple(sorted((a,d))):pairing(cols[a],ad,cols[d]) for a,d in combinations(active,2)}
            values.append((det(qj),pairs))
        full=mask==(1<<b)-1; desired=tuple(sorted(('a0',second)))
        assert values[0][0]==int(not full)
        assert values[1][0]==values[2][0]==1
        if full: assert all(v==int(p==desired) for p,v in values[0][1].items())
        assert all((values[1][1][p]^values[2][1][p])==int(full and p==desired) for p in values[1][1])
        checked+=1
print(json.dumps({'group_dimensions':[1,2,3,4,5],'restrictions_checked':checked,
                  'programs_per_restriction':3,'result':'All grounding, constant and degree-one pair identities passed.'},indent=2))
