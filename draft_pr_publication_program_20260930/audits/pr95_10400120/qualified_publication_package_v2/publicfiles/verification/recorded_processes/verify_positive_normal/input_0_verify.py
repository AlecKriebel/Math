def require(condition, message="explicit guard failed"):
 if not condition: raise AssertionError(message)
import numpy as np,itertools,json,hashlib
from pathlib import Path
# Phi_100 = x^40-x^30+x^20-x^10+1.
def red(a):
 a=list(map(int,a))+[0]*max(0,40-len(a))
 for j in range(len(a)-1,39,-1):
  c=a[j]
  if c:
   for d,s in [(10,1),(20,-1),(30,1),(40,-1)]:a[j-d]+=s*c
 return np.array(a[:40],dtype=object)
MON=[red([0]*i+[1]) for i in range(100)]
def mul(a,b):return red(np.convolve(a,b))
def shift(a,k):return mul(a,MON[k%100])
def conj(a):
 r=np.zeros(40,dtype=object)
 for j,c in enumerate(a):r+=c*MON[-j%100]
 return r
labels=[x for x in itertools.product(range(6),repeat=4) if sum(x)<=5]
X=[]
for lab in labels:
 y=[sum(lab[i:])+4-i for i in range(5)];X.append(tuple(5*a-sum(y) for a in y))
perms=list(itertools.permutations(range(5)))
signs=[(-1)**sum(p[i]>p[j] for i in range(5) for j in range(i+1,5)) for p in perms]
def snum(x,y):
 out=np.zeros(40,dtype=object)
 for p,sgn in zip(perms,signs):
  dot=sum(x[i]*y[p[i]] for i in range(5));require(dot%5==0)
  out+=sgn*MON[(-2*(dot//5))%100]
 return out
S=[[None]*126 for _ in X]
for i,x in enumerate(X):
 for j in range(i,126):S[i][j]=S[j][i]=snum(x,X[j])

T=[]
for x in X:
 z=sum(a*a for a in x)-sum(a*a for a in X[0]);require(z%5==0);T.append((z//5)%100)
A=np.zeros(40,dtype=object)
for j in range(126):A+=shift(mul(S[0][j],S[0][j]),5*T[j])
B=np.zeros(40,dtype=object)
for i in range(126):
 inner=np.zeros(40,dtype=object)
 for j in range(126):inner+=shift(mul(S[i][j],S[j][0]),2*T[j])
 B+=shift(mul(S[0][i],inner),3*T[i])
AA=mul(A,conj(A));BB=mul(B,conj(B));DD=mul(S[0][0],conj(S[0][0]));diff=50000*AA-BB

def expected(terms):
 a=np.zeros(40,dtype=object)
 for j,c in terms.items():a[j]=c
 return a
checks=[(S[0][0],{0:5,20:-10,30:10}),
 (A,{0:12500,10:-20000,20:10000,30:-20000}),
 (B,{0:-3750000,20:-2500000,30:2500000}),
 (DD,{0:125,20:-200,30:200}),
 (AA,{0:406250000,20:125000000,30:-125000000}),
 (BB,{0:20312500000000,20:12500000000000,30:-12500000000000}),
 (diff,{20:-6250000000000,30:6250000000000})]
for actual,target in checks:require(list(actual)==list(expected(target)))
require(len(labels)==126 and len(perms)==120)
require(any(diff) and any(AA) and any(BB) and any(DD))
r={k:list(map(int,v)) for k,v in dict(A=A,B=B,S00=S[0][0],AA=AA,BB=BB,DD=DD,difference=diff).items()}
r.update({'weight_count':126,'weyl_permutation_count':120,'symmetric_entries_computed':8001,'final_polynomial_identities':7,'all_pass':True,'arithmetic':'Python arbitrary-precision integers in NumPy object arrays; no floating point in certificate','artifact_sha256':hashlib.sha256((Path(__file__).resolve().parent.parent / 'pr95_note.tex').read_bytes()).hexdigest()})
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:r[k] for k in ['weight_count','final_polynomial_identities','all_pass','artifact_sha256']}))
