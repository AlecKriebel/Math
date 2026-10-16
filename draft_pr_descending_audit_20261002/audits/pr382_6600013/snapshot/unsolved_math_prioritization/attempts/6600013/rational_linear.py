from fractions import Fraction as F

def rank(A):
 if not A:return 0
 A=[[F(x) for x in row] for row in A];r=0
 for j in range(len(A[0])):
  k=next((k for k in range(r,len(A)) if A[k][j]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];a=A[r][j];A[r]=[x/a for x in A[r]]
  for k in range(r+1,len(A)):
   a=A[k][j]
   if a:A[k]=[x-a*y for x,y in zip(A[k],A[r])]
  r+=1
  if r==len(A):break
 return r

def matmul(A,B):return [[sum(x*B[k][j] for k,x in enumerate(row)) for j in range(len(B[0]))] for row in A]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def kron(A,B):return [[a*b for a in ar for b in br] for ar in A for br in B]
