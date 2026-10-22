from pathlib import Path
import hashlib,json,sympy as S
checks=0
def ck(b):
 global checks
 assert b;checks+=1
A=S.Matrix([[2,-1],[1,0]]);N=A-S.eye(2);ck(N*N==S.zeros(2)); counts={}
for r in range(-50,51):
 Ar=(A**r).applyfunc(lambda x:int(x)%7);ck(Ar==(S.eye(2)+r*N).applyfunc(lambda x:int(x)%7))
 count=0
 for a in range(7):
  for b in range(7):
   v=Ar*S.Matrix([a,b]);ok=(int(v[0])-a)%7==0 and (int(v[1])-b)%7==0
   ck(ok==((r*(a-b))%7==0));count+=ok
 counts[r]=count;ck(count==(49 if r%7==0 else 7))
 # Cap/cup forces equal colors; every external twist preserves them.
 for a in range(7):ck(all((v-a)%7==0 for v in Ar*S.Matrix([a,a])))
M=S.Matrix([[counts[k-j] for k in range(4)]+[7] for j in range(5)])
ck(M.det()==7**5*6**4);ck(M.rank()==5)
z,t=S.symbols('z t');phi=sum(z**i for i in range(7));red=lambda p:S.rem(S.expand(p),phi,z)
s=z+z**2+z**4;bar=z**3+z**5+z**6
ck(red(s+bar+1)==0);ck(red(s*bar-2)==0);ck(red((s-bar)**2+7)==0)
P=t**3-s*t**2+bar*t-1
ck(red(S.expand((t-z)*(t-z**2)*(t-z**4)-P))==0)
for x in range(7):ck(red(P.subs(t,z**(x*x%7))+(s-bar)*int(x==0))==0)
# Unique four-eigenvalue minimal polynomial: no pair of eigenvalues coincides.
for i in (0,1,2,4):
 for j in (0,1,2,4):
  if i<j:ck(red(z**i-z**j)!=0)
here=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':checks,'artifact_sha256':hashlib.sha256((here/'PARTIAL_RESULT.md').read_bytes()).hexdigest(),'closure_matrix':str(M),'normalized_determinant':1296,'scope':'Finite F7 crossing equations and exact cyclotomic operator identities only; no all-link Gaussian invariant or original-target resolution.'}
(here/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
