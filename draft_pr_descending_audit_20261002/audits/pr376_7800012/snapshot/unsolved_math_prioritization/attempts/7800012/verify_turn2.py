from itertools import product
from collections import Counter
from fractions import Fraction as F
import random,json
from gaussian_matrix import matrix,matmul,scale,add,conj,mul,Z
checks=0;matrixcases=0;rng=random.Random(780001202)
def check(x):
 global checks
 assert x;checks+=1
steps=[(1,0),(-1,0),(0,1),(0,-1)]
classification=Counter()
for word in product(steps,repeat=6):
 x=y=0;path=[(x,y)]
 for dx,dy in word:x+=dx;y+=dy;path.append((x,y))
 if (x,y)!=(0,0):continue
 winding={}
 for a in range(-3,3):
  for b in range(-3,3):
   w=0
   for (x,y),(xx,yy) in zip(path,path[1:]):
    if x==xx and x>a:
     if y==b and yy==b+1:w+=1
     if yy==b and y==b+1:w-=1
   if w:winding[a,b]=w
 if not winding:classification['empty']+=1
 elif len(winding)==1:check(set(winding.values()) in [{1},{-1}]);classification['square']+=1
 else:
  check(len(winding)==2);check(set(winding.values()) in [{1},{-1}]);a,b=list(winding);check(abs(a[0]-b[0])+abs(a[1]-b[1])==1);classification['rectangle']+=1
check(dict(classification)=={'empty':232,'square':144,'rectangle':24})
cs=[1,0,-1,0];ss=[0,1,0,-1]
def norm2(A):return sum(a*a+b*b for row in A for a,b in row)
for L in [8,10,12]:
 N=L*L
 for case in range(6):
  u={(x,y):rng.randrange(4) for x in range(L) for y in range(L)};v={(x,y):rng.randrange(4) for x in range(L) for y in range(L)}
  flux={(x,y):(u[x,y]+v[(x+1)%L,y]-u[x,(y+1)%L]-v[x,y])%4 for x in range(L) for y in range(L)};S=sum(cs[a] for a in flux.values())
  edges=[((x,y),((x+1)%L,y)) for x in range(L) for y in range(L)]+[((x,y),(x,(y+1)%L)) for x in range(L) for y in range(L)]
  R=sum(cs[(flux[p]+flux[q])%4] for p,q in edges)
  T=matrix(L,u,v);T2=matmul(T,T);T3=matmul(T2,T)
  check(norm2(T)==4*N);check(norm2(T2)==28*N+8*S);check(norm2(T3)==232*N+144*S+12*R)
  defect=norm2([[add(T3[i][j],scale(T[i][j],-8)) for j in range(N)] for i in range(N)])
  check(defect==40*N+16*S+12*R)
  residual=F(48,N)*(S+F(N,6))**2+6*sum((cs[flux[p]]+cs[flux[q]]-F(2*S,N))**2 for p,q in edges)+6*sum((ss[flux[p]]-ss[flux[q]])**2 for p,q in edges)
  check(defect-F(44*N,3)==residual);check(defect>=F(44*N,3));matrixcases+=1
# Quadratic-field exact scalar comparisons for rational s in[0,4].
def sign(a,b):
 if not b:return (a>0)-(a<0)
 if not a:return (b>0)-(b<0)
 if a>0 and b>0:return 1
 if a<0 and b<0:return -1
 z=a*a-2*b*b
 return ((z>0)-(z<0)) if a>0 else -((z>0)-(z<0))
for denominator in range(1,25):
 for numerator in range(4*denominator+1):
  s=F(numerator,denominator);f2=s*s*(s*s-8)**2
  # M²(s-r)²=(384+256sqrt2)(s²+8−4s sqrt2).
  a=384*(s*s+8)-2048*s-f2;b=256*(s*s+8)-1536*s
  check(sign(a,b)>=0);check(f2<=64*s*s)
print(json.dumps(dict(assertions=checks,closed_walk_classification=dict(classification),random_matrix_cases=matrixcases,scope='Exact controls for all-L>=8 moment identities, defect bound and coarse energy gap; energy optimizer unresolved.'),indent=2,sort_keys=True))
