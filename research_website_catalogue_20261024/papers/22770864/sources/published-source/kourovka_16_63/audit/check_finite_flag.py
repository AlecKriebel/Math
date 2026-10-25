#!/usr/bin/env python3
"""Independent exact finite-field audit. Standard library only; reads no bundle data."""
from fractions import Fraction
from itertools import combinations
from math import factorial
import json

p = 1009
blocks = [('U', 6), ('V', 4), ('W', 6), ('T', 2), ('R', 4), ('Z', 0)]
names = ['h','e','f'] + [f'{s}{i}' for s,m in blocks for i in range(m+1)]
index = {v:i for i,v in enumerate(names)}
n = len(names)
C = {}

def put(a,b,c,v):
    if not v: return
    i,j,k = (index[t] for t in (a,b,c))
    assert i != j
    assert (i,j) not in C
    C[i,j] = {k:v}
    C[j,i] = {k:-v}

put('h','e','e',2); put('h','f','f',-2); put('e','f','h',1)
for s,m in blocks:
    for i in range(m+1):
        put('h',f'{s}{i}',f'{s}{i}',m-2*i)
        if i: put('e',f'{s}{i}',f'{s}{i-1}',i)
        if i<m: put('f',f'{s}{i}',f'{s}{i+1}',m-i)

def derivative(a,b,dx,dy):
    if a<dx or b<dy: return 0
    return factorial(a)//factorial(a-dx)*factorial(b)//factorial(b-dy)

degrees = dict(blocks)
for s,t,o,r in [('U','U','W',3),('U','V','T',4),('U','W','T',5),
                ('U','R','T',4),('V','V','T',3),('V','R','Z',4),('R','R','T',3)]:
    m,l=degrees[s],degrees[t]
    for i in range(m+1):
        for j in range(l+1):
            if s==t and j<=i: continue
            v=sum((-1)**q*factorial(r)//(factorial(q)*factorial(r-q))*
                  derivative(m-i,i,r-q,q)*derivative(l-j,j,q,r-q)
                  for q in range(r+1))
            if v: put(f'{s}{i}',f'{t}{j}',f'{o}{i+j-r}',v)

def add(out,v,scale=1):
    for k,c in v.items():
        out[k]=out.get(k,0)+scale*c
        if not out[k]: del out[k]
    return out

def bracket(v,w):
    out={}
    for a,ca in v.items():
        for b,cb in w.items(): add(out,C.get((a,b),{}),ca*cb)
    return out

def basis(i): return {i:1}

for a,b,c in combinations(range(n),3):
    out={}
    for i,j,k in [(a,b,c),(b,c,a),(c,a,b)]:
        add(out,bracket(basis(i),C.get((j,k),{})))
    assert not out, (a,b,c,out)

class Span:
    def __init__(self): self.rows={}
    def insert(self, v):
        v={i:c%p for i,c in v.items() if c%p}
        for i,w in sorted(self.rows.items()):
            if i in v:
                a=v[i]
                for j,c in w.items():
                    v[j]=(v.get(j,0)-a*c)%p
                    if not v[j]: del v[j]
        if not v: return False
        i=min(v); inv=pow(v[i],-1,p)
        self.rows[i]={j:c*inv%p for j,c in v.items()}
        return True

def rank(rows):
    s=Span()
    for row in rows: s.insert(row)
    return len(s.rows)

x=basis(index['h'])
y={index[v]:1 for v in ['e','f','U1','V0','R2']}
t=basis(index['U0'])
span=Span(); words=[]
for v in [x,y]:
    assert span.insert(v); words.append(v)
i=0
while i<len(words):
    for g in [x,y]:
        v=bracket(g,words[i])
        if span.insert(v): words.append({k:c%p for k,c in v.items() if c%p})
    i+=1
assert len(words)==31

tau=[basis(i) for i in range(n)]
for j in range(5):
    tau[index[f'V{j}']]=basis(index[f'R{j}'])
    tau[index[f'R{j}']]=basis(index[f'V{j}'])
tau[index['Z0']]={index['Z0']:-1}
for i,j in combinations(range(n),2):
    lhs={}
    for k,v in C.get((i,j),{}).items(): add(lhs,tau[k],v)
    assert lhs==bracket(tau[i],tau[j])

# Independently form the 1-cocycle equations d(c)=0 for sl2 basis h,e,f.
cohomology={}
for m in [0,2,4,6]:
    d=m+1
    def act(s,j):
        if s==0: return {j:m-2*j}
        if s==1: return {j-1:j} if j else {}
        return {j+1:m-j} if j<m else {}
    eqs=[]
    for a,b in combinations(range(3),2):
        rows=[{} for _ in range(d)]
        for c,v in C.get((a,b),{}).items():
            for j in range(d): rows[j][c*d+j]=v
        for j in range(d):
            for k,v in act(a,j).items(): rows[k][b*d+j]=rows[k].get(b*d+j,0)-v
            for k,v in act(b,j).items(): rows[k][a*d+j]=rows[k].get(a*d+j,0)+v
        eqs.extend(rows)
    coboundaries=[]
    for j in range(d):
        coboundaries.append({s*d+k:v for s in range(3) for k,v in act(s,j).items() if v})
    zr=3*d-rank(eqs); br=rank(coboundaries)
    assert zr==br
    cohomology[m]=[zr,br]

# Every derivation is inner by the audited classification. Directly check
# that ad(u) preserving F2 and F3 has precisely the one central parameter.
flag_rows=[]
for v,allowed in [(x,[x,y]),(y,[x,y]),(t,[x,y,t])]:
    # Membership in the relevant span: subtract h,e,U0 coordinates,
    # since these are pivot coordinates of x,y,t respectively.
    cols=[]
    for a in range(n):
        z=bracket(basis(a),v)
        for pv,w in zip([index['h'],index['e'],index['U0']],allowed):
            add(z,w,-z.get(pv,0))
        cols.append(z)
    flag_rows.extend({a:col[k] for a,col in enumerate(cols) if k in col} for k in range(n))
flag_rank=rank(flag_rows)
assert flag_rank==30

# Exterior-cube character decomposition over Q.
weights=[6-2*i for i in range(7)]
char={}
for triple in combinations(weights,3):
    q=sum(triple); char[q]=char.get(q,0)+1
summands=[]
while char:
    m=max(char); summands.append(m)
    for q in range(m,-m-1,-2):
        char[q]-=1
        if not char[q]: del char[q]
assert summands==[12,8,6,4,0]

result={'prime':p,'basis_dimension':n,'integer_jacobi_triples':4495,
        'generated_dimension_mod_p':len(words),'tau_bracket_pairs':465,
        'cohomology_cocycle_coboundary_dimensions':cohomology,
        'inner_flag_constraint_rank_mod_p':flag_rank,
        'exterior_cube_V6_highest_weights':summands,'status':'PASS'}
print(json.dumps(result,indent=2))
