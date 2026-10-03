"""Small exact Gaussian-integer matrices for finite flux certificates."""
Z=(0,0);ONE=(1,0)
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return(a[0],-a[1])
def scale(a,k):return(a[0]*k,a[1]*k)
def matmul(A,B):
 n=len(A);C=[[Z for j in range(n)] for i in range(n)]
 for i in range(n):
  for k in range(n):
   if A[i][k]!=Z:
    for j in range(n):
     if B[k][j]!=Z:C[i][j]=add(C[i][j],mul(A[i][k],B[k][j]))
 return C
def matrix(L,u,v):
 roots=[(1,0),(0,1),(-1,0),(0,-1)];N=L*L;T=[[Z for j in range(N)] for i in range(N)]
 for x in range(L):
  for y in range(L):
   a=x+L*y
   for b,e in [(((x+1)%L)+L*y,u[x,y]),(x+L*((y+1)%L),v[x,y])]:T[a][b]=roots[e%4];T[b][a]=conj(T[a][b])
 return T
