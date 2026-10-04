"""Exact finite pattern complexes for the sheared TM/Sturmian example."""
from thue_morse_language import language as tm
from quadratic_rotation import language as sturmian
from functools import lru_cache
@lru_cache(None)
def rectangles(n,m):
 return tuple(sorted({tuple(tuple((x[i+j],x[i+j+1],y[j]) for i in range(n)) for j in range(m)) for x in tm(n+m) for y in sturmian(m)}))
def crop(P,x0,x1,y0,y1):return tuple(tuple(row[x0:x1]) for row in P[y0:y1])
def complex(n):
 V=rectangles(n,n);H=rectangles(n+1,n);W=rectangles(n,n+1);C=rectangles(n+1,n+1);vi={w:i for i,w in enumerate(V)};hi={w:i for i,w in enumerate(H)};wi={w:i+len(H) for i,w in enumerate(W)}
 D1=[[0]*(len(H)+len(W)) for _ in V]
 for j,w in enumerate(H):D1[vi[crop(w,0,n,0,n)]][j]-=1;D1[vi[crop(w,1,n+1,0,n)]][j]+=1
 for j,w in enumerate(W,start=len(H)):D1[vi[crop(w,0,n,0,n)]][j]-=1;D1[vi[crop(w,0,n,1,n+1)]][j]+=1
 D2=[[0]*len(C) for _ in range(len(H)+len(W))]
 for j,w in enumerate(C):
  D2[hi[crop(w,0,n+1,0,n)]][j]+=1;D2[hi[crop(w,0,n+1,1,n+1)]][j]-=1;D2[wi[crop(w,1,n+1,0,n+1)]][j]+=1;D2[wi[crop(w,0,n,0,n+1)]][j]-=1
 return [V,H+W,C],[D1,D2],len(H)
def forgetting(n,m,small,large,hsmall,hlarge):
 assert m>=n and (m-n)%2==0;k=(m-n)//2;maps=[]
 for degree in range(3):
  index={w:i for i,w in enumerate(small[degree])};A=[[0]*len(large[degree]) for _ in small[degree]]
  for j,w in enumerate(large[degree]):
   width=n+int(degree==2 or (degree==1 and j<hlarge));height=n+int(degree==2 or (degree==1 and j>=hlarge));target=crop(w,k,k+width,k,k+height);A[index[target]][j]=1
  maps.append(A)
 return maps
