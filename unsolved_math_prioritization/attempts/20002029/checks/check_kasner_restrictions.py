import sympy as s
from itertools import combinations

def f(p):
 p=[s.Rational(x) for x in p]
 n=len(p)+1
 K=s.zeros(n,n)
 for i in range(1,n):
  K[0,i]=K[i,0]=p[i-1]*(1-p[i-1])
 for i,j in combinations(range(1,n),2): K[i,j]=K[j,i]=-p[i-1]*p[j-1]
 norm2=4*sum(K[i,j]**2 for i,j in combinations(range(n),2))
 der2=4*norm2+8*sum(p[i-1]**2*sum((K[0,j]-K[i,j])**2 for j in range(1,n) if i!=j) for i in range(1,n))
 A=8*sum(K[i,j]**3 for i,j in combinations(range(n),2))
 B=6*sum(K[i,j]*K[i,k]*K[j,k] for i,j,k in combinations(range(n),3))
 return norm2,der2,A,B
P=[[-s.Rational(1,3),s.Rational(2,3),s.Rational(2,3),0,0],[-s.Rational(1,2),s.Rational(1,2),s.Rational(1,2),s.Rational(1,2),0],[-s.Rational(3,5),s.Rational(2,5),s.Rational(2,5),s.Rational(2,5),s.Rational(2,5)]]
M=[]
for p in P:
 a=f(p); M.append(a[1:]); print(p,a)
assert all(sum(p)==sum(x*x for x in p)==1 for p in P)
assert s.Matrix(M).det()==-s.Rational(65536,3125)
print('M',s.Matrix(M),'det',s.Matrix(M).det())

# Independent array evaluation of the covariant-derivative norm and contractions.
from itertools import product
for p in P:
 n=6
 K=s.zeros(n,n)
 for i in range(1,n): K[0,i]=K[i,0]=p[i-1]*(1-p[i-1])
 for i,j in combinations(range(1,n),2): K[i,j]=K[j,i]=-p[i-1]*p[j-1]
 def R(a,b,c,d):
  return K[a,b]*((a==c and b==d)-(a==d and b==c))
 # Orthonormal-frame connection coefficients Gamma(m,slot,u).
 def Gamma(m,slot,u):
  if m==0:return 0
  return p[m-1]*((slot==0 and u==m)-(slot==m and u==0))
 D=0
 for m in range(n):
  for inds in product(range(n), repeat=4):
   deriv=-2*R(*inds) if m==0 else 0
   for t in range(4):
    for u in range(n):
     q=list(inds); q[t]=u
     deriv-=Gamma(m,inds[t],u)*R(*q)
   D+=deriv**2
 A=B=0
 for a,b,c,d,e,ff in product(range(n),repeat=6):
  A+=R(a,b,c,d)*R(c,d,e,ff)*R(e,ff,a,b)
  B+=R(a,b,c,d)*R(a,e,c,ff)*R(b,e,d,ff)
 vals=f(p)
 assert (D,A,B)==vals[1:], ((D,A,B),vals)
 print('independent verification passed',p,(D,A,B))
