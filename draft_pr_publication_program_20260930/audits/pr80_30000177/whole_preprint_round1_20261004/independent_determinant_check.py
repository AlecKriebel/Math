"""Fresh review reconstruction: density projection and exact determinant spectra.
Does not import or execute author/ROOT reconstruction. Standard library only.
"""
from fractions import Fraction as Q
from itertools import product,permutations
from pathlib import Path
import json

ops=((1,0,0,1),(0,1,1,0),(1,0,0,-1),(0,-1,1,0))
# Rows of real matrices I,X,Z,XZ on one qubit; Bell coefficients omit sqrt(2).
bells=((1,0,0,1),(1,0,0,-1),(0,1,1,0),(0,1,-1,0))
w=[Q(1,2) if sum(b)==1 else Q(0) for b in product(range(2),repeat=4)]

def density_after(x,y):
 out=[Q(0)]*16
 for a,b,c,d in product(range(2),repeat=4):
  out[8*a+4*b+2*c+d]=sum(Q(ops[x][2*a+u]*ops[y][2*b+v])*w[8*u+4*v+2*c+d] for u,v in product(range(2),repeat=2))
 return [[out[i]*out[k] for k in range(16)] for i in range(16)]

def projection(density,j):
 # Contract L=(a,c); retain R=(b,d), separately from ket branch method.
 mat=[]
 for b,d in product(range(2),repeat=2):
  row=[]
  for bb,dd in product(range(2),repeat=2):
   row.append(sum(Q(bells[j][2*a+c]*bells[j][2*aa+cc],2)*density[8*a+4*b+2*c+d][8*aa+4*bb+2*cc+dd] for a,c,aa,cc in product(range(2),repeat=4)))
  mat.append(row)
 return mat

def poly_mul(a,b):
 c=[Q(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def characteristic(m):
 out=[Q(0)]*5
 for perm in permutations(range(4)):
  sign=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
  term=[Q(sign)]
  for i in range(4):term=poly_mul(term,[-m[i][perm[i]],Q(i==perm[i])])
  for i,v in enumerate(term):out[i]+=v
 return out

def full_char(blocks):
 out=[Q(1)]
 for m in blocks:out=poly_mul(out,characteristic(m))
 return out

def char_eigs(eigs):
 out=[Q(1)]
 for v in eigs:out=poly_mul(out,[-v,Q(1)])
 return out

def avg(states):
 return [[[sum(t[j][r][s] for t in states)/len(states) for s in range(4)] for r in range(4)] for j in range(4)]

states={(x,y):[projection(density_after(x,y),j) for j in range(4)] for x,y in product(range(4),repeat=2)}
# Full characteristic-polynomial equality determines every multiplicity including zeros.
expected=[char_eigs(e) for e in ([Q(1,2),Q(1,4),Q(1,4)]+[Q(0)]*13,[Q(1,4)]*2+[Q(1,16)]*8+[Q(0)]*6,[Q(1,8)]*8+[Q(0)]*8,[Q(3,32)]*8+[Q(1,32)]*8)]
actual=[list(states.values()),[avg([states[x,y] for y in range(4)]) for x in range(4)],[avg([states[x,y] for x in range(4)]) for y in range(4)],[avg(list(states.values()))]]
counts=[]
for family,e in zip(actual,expected):
 for state in family:
  if full_char(state)!=e:raise RuntimeError('Characteristic polynomial mismatch')
 counts.append(len(family))
# Complete per-input branch table in receiver Bell order, no dropped branch.
traces={str(k):[str(sum(m[i][i] for i in range(4))) for m in v] for k,v in states.items()}
res={'status':'PASS_INDEPENDENT_DENSITY_AND_DETERMINANT_RECONSTRUCTION','families_characteristic_polynomials_verified':counts,'polynomial_degree':16,'branch_traces':traces,'new_imports_from_package':False}
print(json.dumps(res,indent=2))
