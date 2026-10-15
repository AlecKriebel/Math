#!/usr/bin/env python3
"""Independent exact checks of a possible repair, attributed to Ferudun (2026), Thm 4.2.
No prior verifier is imported. Fraction elimination and exhaustive row choices suffice.
"""
from fractions import Fraction as F
from itertools import combinations, product
import hashlib,json
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions must be enabled')

def rank(matrix):
 m=[list(map(F,r)) for r in matrix];i=0
 for j in range(len(m[0])):
  pivot=next((k for k in range(i,len(m)) if m[k][j]),None)
  if pivot is None:continue
  m[i],m[pivot]=m[pivot],m[i];q=m[i][j];m[i]=[v/q for v in m[i]]
  for k in range(len(m)):
   if k!=i:
    q=m[k][j];m[k]=[a-q*b for a,b in zip(m[k],m[i])]
  i+=1
  if i==len(m):break
 return i

def image_rows(n):
 return [[int(i==r) for i in range(n) for j in range(n)] for r in range(n)]
def apply(matrix,v):return [sum(a*b for a,b in zip(r,v)) for r in matrix]
n=5
A=image_rows(n)+[[int(j==col) for i in range(n) for j in range(n)] for col in range(n)]+[[int(j-i==d) for i in range(n) for j in range(n)] for d in range(1-n,n)]
b=[0,0,0,1,0, 0,1,0,0,0, 1,0,0,0,1, 1,0,0,0,0, 0,0,1,0,0]
c=[1,0,0,-1,0, 0,-2,0,1,1, 0,0,1,0,-1, -1,1,0,0,0, 0,1,-1,0,0]
s=[2*x-1 for x in b]
target=apply(A,b)
assert apply(A,c)==[0]*len(A)
assert all(-1<=x+v<=1 for x,v in zip(s,c))
assert all(v*x<=0 for v,x in zip(c,s))
choices=[list(combinations(range(n),r)) for r in target[:n]]
solutions=[];tested=0
for rows in product(*choices):
 candidate=[int(j in rows[i]) for i in range(n) for j in range(n)];tested+=1
 if apply(A,candidate)==target:solutions.append(candidate)
assert solutions==[b]
# A row-space exposing certificate, independently recomputed from line potentials.
rho=[1,0,-1,1,0];gamma=[-1,0,1,0,1];delta=[2,0,-1,2,0,2,0,-1,0]
f=apply(list(zip(*A)),rho+gamma+delta)
support=[j for j,v in enumerate(c) if v]
assert len(support)==11
assert {j for j,v in enumerate(f) if not v}==set(support)
assert all(v*x<=0 for v,x in zip(f,s))
restricted=[[row[j] for j in support] for row in A]
assert rank(restricted)==10
# For feasible e=z-s: f_j e_j >=0 and f.e=0 forces e off support zero.
# Restricted nullspace is span(c). Cube bounds then give precisely 0<=lambda<=1.
lo=F(0);hi=F(1)
for x,v in zip(s,c):
 if v:
  a,bound=sorted([F(-1-x,v),F(1-x,v)])
  assert a<=lo<=hi<=bound
assert any(v==-2 and x==1 for x,v in zip(s,c))
assert any(abs(v)==1 for v in c)
# If sign(A^T mu)=s, c_j*(A^T mu)_j is strictly negative on support;
# their sum must also equal (A c)^T mu=0. Therefore no mu has that full sign.
assert all(c[j]*s[j]<0 for j in support)
# The draft's two-direction example admits the correct common pattern at every
# positive scale, despite the limiting exact optimizer being zero.
B=image_rows(3)+[[int(j==col) for i in range(3) for j in range(3)] for col in range(2)]
y=[3,1,1,3,1];direction=[1,0,0,1,0]
common=[1,1,1,1,0,0,1,0,0]
eps_checks=[]
for eps in (F(1,2),F(1,10),F(1,1000000)):
 mu=[eps*v for v in direction];q=apply(list(zip(*B)),mu)
 assert [int(v>0)-int(v<0) for v in q]==common
 gap=sum((v-w)**2 for v,w in zip(mu,y))/2+sum(abs(v) for v in q)-F(sum(w*w for w in y),2)
 assert gap==eps*eps
 eps_checks.append({'epsilon':str(eps),'objective_gap':str(gap),'correct_common_pattern':True})
report={'verdict':'verified_repair_is_prior','attribution':'Alper Ferudun, DOI 10.5281/zenodo.23110494, Theorem 4.2; issued 2026-10-02','matrix_shape':[len(A),n*n],'row_conditioned_binary_images_enumerated':tested,'binary_solutions':len(solutions),'kernel_support':support,'fixed_pixels':n*n-len(support),'restricted_rank':rank(restricted),'box_segment_lambda':[str(lo),str(hi)],'no_full_sign_backprojection':'Ac=0, while sign(A^T mu)=s would force c^T A^T mu<0','draft_example_correct_approximate_signs':eps_checks,'numerical_or_central_path_claims_used':False,'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(report,indent=2))
