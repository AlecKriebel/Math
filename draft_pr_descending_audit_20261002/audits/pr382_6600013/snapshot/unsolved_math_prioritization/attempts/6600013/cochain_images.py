from fractions import Fraction as F
from rational_linear import rank,matmul

def transpose(A):return [list(x) for x in zip(*A)]
def nullspace(A):
 A=[[F(x) for x in row] for row in A];cols=len(A[0]);pivots=[];r=0
 for j in range(cols):
  k=next((k for k in range(r,len(A)) if A[k][j]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];a=A[r][j];A[r]=[x/a for x in A[r]]
  for k in range(len(A)):
   a=A[k][j]
   if k!=r and a:A[k]=[x-a*y for x,y in zip(A[k],A[r])]
  pivots.append(j);r+=1
  if r==len(A):break
 basis=[]
 for j in range(cols):
  if j in pivots:continue
  v=[F(0)]*cols;v[j]=1
  for i,p in enumerate(pivots):v[p]=-A[i][j]
  basis.append(v)
 return transpose(basis)
def image_rank(boundary,images):return rank([a+b for a,b in zip(boundary,images)])-rank(boundary)
