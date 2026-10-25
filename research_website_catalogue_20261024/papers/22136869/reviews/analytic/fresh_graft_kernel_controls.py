#!/usr/bin/env python3
"""Fresh exact controls for the injection/equivariance argument of Theorem 19.
No published code/certificate is imported. Kernels have 1, 2, and 3 output leaves.
"""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product,permutations
import hashlib,json
import sympy as s
R=s.Rational
M=lambda t:s.eye(4)*t+s.ones(4)*(1-t)/4
# Arbitrary distinct strict CT JC eigenvalues on each component edge.
P,Q,A,B,C,D=[M(R(a,b)) for a,b in [(1,2),(2,3),(3,5),(4,7),(5,8),(2,5)]]
patterns=[list(product(range(4),repeat=n)) for n in (1,2,3)]
L1=s.eye(4)
L2=s.Matrix([[P[x,a]*Q[x,b] for x in range(4)] for a,b in patterns[1]])
L3=s.Matrix([[sum(A[x,z]*B[z,a]*C[z,b]*D[x,c] for z in range(4)) for x in range(4)] for a,b,c in patterns[2]])
logs=[]
def check(x,label):
 if not x:raise AssertionError(label)
 logs.append(label)
for i,(L,pat,n,expected) in enumerate(zip([L1,L2,L3],patterns,[1,2,3],[s.eye(4),P,A*B])):
 check(L.shape==(4**n,4),'kernel dimensions '+str(i))
 check(all(sum(L[r,c] for r in range(L.rows))==1 for c in range(4)),'conditional normalization '+str(i))
 check(all(v>=0 for v in L),'kernel nonnegativity '+str(i))
 marginal=s.Matrix([[int(row[0]==a) for row in pat] for a in range(4)])
 reduced=marginal*L
 check(reduced==expected,'marginal equals path matrix '+str(i))
 check(reduced.det()>0,'path invertibility '+str(i))
 left=reduced.inv()*marginal
 check(left*L==s.eye(4),'explicit exact left inverse '+str(i))
 # GL(2,2) consists of all six permutations of the nonzero states.
 for pp in permutations((1,2,3)):
  tau=(0,)+pp
  check(all(L[pat.index(tuple(tau[a] for a in row)),tau[x]]==L[j,x] for j,row in enumerate(pat) for x in range(4)),f'equivariance component {i} permutation {pp}')
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':len(logs),'labels':logs,'scope':'Exact kernels on a six-leaf graft (1+2+3 components): normalized/nonnegative, explicit left inverses via path marginals, equivariance under all six state-group automorphisms. Analytic tensor-product argument, not finite enumeration, proves the arbitrary-n assertion.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('fresh_graft_kernel_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='labels'},indent=2))
