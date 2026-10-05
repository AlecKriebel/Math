#!/usr/bin/env python3
"""Generic matrix identities and an independent SymPy sharpness replay."""
import sympy as s
from itertools import permutations,combinations
import json
from pathlib import Path
count=0
def ck(v):
 global count
 count+=1
 assert v,f'assertion {count}'
def peq(A,B):
 aa=list(A);bb=list(B)
 return all(s.expand(aa[i]*bb[j]-aa[j]*bb[i])==0 for i in range(4) for j in range(i))
e=s.symbols('e0:3');M=[]
for j,x in enumerate(e):
 u,v=[e[t] for t in range(3) if t!=j]
 m=s.Matrix([[x,u*v-x*(u+v)],[1,-x]]);M.append(m)
 ck(s.expand(m.det()+(x-u)*(x-v))==0)
 ck(all(s.expand(t)==0 for t in m*m-(x-u)*(x-v)*s.eye(2)))
for j,l in permutations(range(3),2):ck(peq(M[j]*M[l],M[3-j-l]))
for p in permutations(range(3)):
 subs=dict(zip(e,[e[j] for j in p]))
 for j in range(3):ck(M[j].subs(subs,simultaneous=True)==M[p[j]])
I=s.I;ps=[s.Matrix(x) for x in [(0,1),(1,0),(1,1),(-1,1),(2+2*I,1),(-(1+I)/4,1)]]
def norm(p):return (s.Integer(1),s.Integer(0)) if s.simplify(p[1])==0 else (s.simplify(p[0]/p[1]),s.Integer(1))
def cross(a,b):return a.det() if b is None else s.det(s.Matrix.hstack(a,b))
base=list(map(norm,ps));automorphisms=[]
for p in permutations(range(6),3):
 a,b,c=[ps[j] for j in p]
 mat=s.Matrix.hstack(cross(a,c)*b,-cross(b,c)*a)
 images=[norm(mat*t) for t in ps]
 if set(images)==set(base):automorphisms.append([base.index(t) for t in images])
ck(automorphisms==[list(range(6))])
rows=[]
for p in combinations(range(6),4):
 a,b,c,d=[ps[j] for j in p]
 L=s.simplify(cross(a,c)*cross(b,d)/(cross(a,d)*cross(b,c)))
 J=s.expand_complex(s.simplify(256*(L*L-L+1)**3/(L*L*(L-1)**2)))
 rows.append({'subset':list(p),'J':[str(s.simplify(s.re(J))),str(s.simplify(s.im(J)))]})
expected=json.loads(Path(__file__).with_name('CONTROL_RESULTS.json').read_text())['four_subset_J_values']
ck(rows==expected)
print(json.dumps({'status':'pass','symbolic_and_independent_assertions':count,'mobius_candidates':120,'generic_root_variables':list(map(str,e)),'sympy_version':s.__version__,'limits':'Exact generic identities and independent finite replay, not a formal verification of the universal proof.'},indent=2))
