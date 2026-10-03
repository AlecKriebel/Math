from thue_morse_language import language as tm
from quadratic_rotation import language as sturmian
from rational_linear import matmul,rank
import json
checks=0
def check(x):
 global checks
 assert x;checks+=1
p={n:len(tm(n)) for n in range(1,130)};check([p[n] for n in range(1,7)]==[2,4,6,10,12,16])
for n in range(2,65):
 check(p[2*n]==p[n]+p[n+1]);check(p[2*n+1]==2*p[n+1])
for n in range(1,129):check(p[n+1]-p[n] in [2,4]);check(p[n]<=4*n)
for a in range(2,7):
 n=2**(a-1);chi=(n+2)*(p[2*n+2]-2*p[2*n+1]+p[2*n])+p[2*n+1]-p[2*n];check(chi==2*n+6)
 n=3*2**(a-2)
 if 2*n+2<=129:
  chi=(n+2)*(p[2*n+2]-2*p[2*n+1]+p[2*n])+p[2*n+1]-p[2*n];check(chi==-2*n)
def rectangles(n,m):
 return {tuple(tuple((x[i+j],x[i+j+1],y[j]) for i in range(n)) for j in range(m)) for x in tm(n+m) for y in sturmian(m)}
def crop(P,x0,x1,y0,y1):return tuple(tuple(row[x0:x1]) for row in P[y0:y1])
records=[]
for n,m in [(1,1),(2,2),(3,3),(2,3),(3,2)]:
 V=sorted(rectangles(n,m));H=sorted(rectangles(n+1,m));W=sorted(rectangles(n,m+1));C=sorted(rectangles(n+1,m+1));vi={w:i for i,w in enumerate(V)};hi={w:i for i,w in enumerate(H)};wi={w:i+len(H) for i,w in enumerate(W)}
 check(len(V)==p[n+m]*(m+1));D1=[[0]*(len(H)+len(W)) for _ in V]
 for j,w in enumerate(H):D1[vi[crop(w,0,n,0,m)]][j]-=1;D1[vi[crop(w,1,n+1,0,m)]][j]+=1
 for j,w in enumerate(W,start=len(H)):D1[vi[crop(w,0,n,0,m)]][j]-=1;D1[vi[crop(w,0,n,1,m+1)]][j]+=1
 D2=[[0]*len(C) for _ in range(len(H)+len(W))]
 for j,w in enumerate(C):
  D2[hi[crop(w,0,n+1,0,m)]][j]+=1;D2[hi[crop(w,0,n+1,1,m+1)]][j]-=1;D2[wi[crop(w,1,n+1,0,m+1)]][j]+=1;D2[wi[crop(w,0,n,0,m+1)]][j]-=1
 check(all(x==0 for row in matmul(D1,D2) for x in row));r1=rank(D1);r2=rank(D2);betti=[len(V)-r1,len(H)+len(W)-r1-r2,len(C)-r2];chi=len(V)-len(H)-len(W)+len(C)
 check(betti[0]==1);check(betti[0]-betti[1]+betti[2]==chi);check(chi==(m+2)*(p[n+m+2]-2*p[n+m+1]+p[n+m])+p[n+m+1]-p[n+m])
 records.append(dict(n=n,m=m,cells=[len(V),len(H)+len(W),len(C)],betti=betti,chi=chi))
print(json.dumps(dict(assertions=checks,complete_thue_morse_lengths=129,exact_pattern_complexes=records,scope='Exact finite controls for a proved source-admissible obstruction to raw approximant-rank bounds; limiting cohomology is finite, not a source counterexample.'),indent=2,sort_keys=True))
