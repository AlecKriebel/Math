"""Finite exact controls for the two-stage Schur complement and bias formula."""
import sympy as s,json
from collections import Counter
C=Counter()
def ck(x,k):
 assert x,k
 C[k]+=1
for n in range(2,7):
 m=n-1
 B=s.zeros(m,n)
 for i in range(m):B[i,i]=i+1;B[i,n-1]=1
 R=s.eye(n)
 for i in range(n):
  for j in range(i+1,n):R[i,j]=s.Rational(i+j+1,n+2)
 M=R.T*R+s.eye(n)
 S=B*M.inv()*B.T
 for d in [s.Rational(1,5),s.Integer(1),s.Integer(3)]:
  f=s.Matrix([i+1 for i in range(m)]);p=s.Matrix([s.Rational((-1)**i,i+1) for i in range(m)])
  sigma=(B.T*B+d*M).inv()*B.T*(f+d*p)
  q=p+(f-B*sigma)/d
  ck(M*sigma-B.T*q==s.zeros(n,1),'first_mixed_equation')
  ck(B*sigma+d*q-f-d*p==s.zeros(m,1),'second_mixed_equation')
  ck(q==(S+d*s.eye(m)).inv()*(f+d*p),'reaction_Schur_formula')
  ck(B*sigma-f==d*(p-q),'exact_conservation_defect')
  mixed=M.inv()*B.T*S.inv()*f
  bias=M.inv()*B.T*d*(S+d*s.eye(m)).inv()*(p-S.inv()*f)
  ck((sigma-mixed-bias).applyfunc(s.simplify)==s.zeros(n,1),'mixed_flux_bias_formula')
lam,d=s.symbols('lambda delta',positive=True)
ck(s.simplify(lam/(lam+d)-1+d/(lam+d))==0,'fixed_coarse_eigenmode_bias')
x,y=s.symbols('x y');a1,a2,b=s.symbols('a1 a2 b')
ck(s.diff(a2+b*y,x)-s.diff(a1+b*x,y)==0,'RT0_element_curl_zero')
u=s.sin(s.pi*x)*s.sin(s.pi*y)
ck(s.simplify(-s.diff(u,x,2)-s.diff(u,y,2)-2*s.pi**2*u)==0,'square_eigenfunction')
for boundary in [u.subs(x,0),u.subs(x,1),u.subs(y,0),u.subs(y,1)]:ck(boundary==0,'homogeneous_boundary_trace')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Finite algebra checks only; no adaptive convergence theorem follows from them.'},indent=2,sort_keys=True))
