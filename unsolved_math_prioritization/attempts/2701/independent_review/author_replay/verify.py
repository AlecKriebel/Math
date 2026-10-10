from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
from math import gcd
import json,hashlib
n=0
def tr(A):return list(map(list,zip(*A)))
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
V1=[[3,2],[1,3]];V2=[[1,2],[1,9]];W=[[3,2,0,0],[1,3,0,0],[0,0,-1,-2],[0,0,-1,-9]]
C=[[1,2],[-2,-1],[3,0],[0,1]];C0=[[0,2],[-3,-1],[6,0],[-1,1]]
for D in [C,C0]:assert mm(mm(tr(D),W),D)==[[0,0],[0,0]];n+=1
assert gcd(*[abs(det([C0[i],C0[j]])) for i,j in combinations(range(4),2)])==2;n+=1
assert gcd(*[abs(det([C[i],C[j]])) for i,j in combinations(range(4),2)])==1;n+=1
Q=[[F(-1),F(-2)],[F(2,3),F(1,3)]]
assert mm(mm(tr(Q),V2),Q)==V1 and det(Q)==1;n+=1
for a,b in product(range(-20,21),repeat=2):
 x,y,z,t=[a*r[0]+b*r[1] for r in C]
 assert a==x-2*t and b==t;n+=1
 assert (2*x+y)%3==0 and z%3==0;n+=1
for x,y in product(range(-20,21),repeat=2):
 image=mm(Q,[[x],[y]])
 assert all(z[0].denominator==1 for z in image)==((2*x+y)%3==0);n+=1
count=0
for a,b,c,d in product(range(3),repeat=4):
 P=[[a,b],[c,d]]
 if det(P)%3:
  R=mm(mm(tr(P),[[2,0],[0,0]]),P)
  assert any(v%3 for row in R for v in row);n+=1;count+=1
assert count==48;n+=1
for V in [V1,V2]:
 for t in range(-20,21):
  D=[[V[i][j]-t*V[j][i] for j in range(2)] for i in range(2)]
  assert det(D)==7*t*t-13*t+7;n+=1
S1=[[6,3],[3,6]];S2=[[2,3],[3,18]]
assert det(S1)==det(S2)==27 and gcd(*sum(S1,[]))==3 and gcd(*sum(S2,[]))==1;n+=1
r={'assertions':n,'all_pass':True,'GL2_F3_checked':48,'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'Exact lattice and rational-isometry diagnostics; no geometric concordance claim.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
