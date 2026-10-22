from fractions import Fraction

def zeros(a,b):return [[0]*b for _ in range(a)]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(A,B):
 if not A:return []
 if not B:return [[] for _ in A]
 return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def rank(A,p=0):
 if not A or not A[0]:return 0
 a=[[x%p if p else Fraction(x) for x in row] for row in A];r=0
 for j in range(len(a[0])):
  z=next((i for i in range(r,len(a)) if a[i][j]),None)
  if z is None:continue
  a[r],a[z]=a[z],a[r];v=pow(a[r][j],-1,p) if p else 1/a[r][j];a[r]=[(x*v)%p if p else x*v for x in a[r]]
  for i in range(r+1,len(a)):
   v=a[i][j]
   if v:a[i]=[(x-v*y)%p if p else x-v*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
