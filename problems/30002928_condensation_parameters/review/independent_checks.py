import sympy as S,json
from fractions import Fraction as F
n=0
def ck(v):
 global n
 assert v;n+=1
z,beta,h,u,m,r,aa=S.symbols('z beta h u m r aa',real=True)
A=lambda z:S.atanh(z)/beta
H=lambda z:A(z)-z
W=lambda z:z*z/2-h*z-S.log(S.cosh(beta*z))/beta
ck(S.simplify(S.diff(W(z),z)-(z-h-S.tanh(beta*z)))==0)
ck(S.simplify(S.diff(A(z),z,2)-2*z/(beta*(1-z*z)**2))==0)
ck(S.simplify(S.diff(2*z/(beta*(1-z*z)**2),z)-(2+6*z*z)/(beta*(1-z*z)**3))==0)
ck(S.simplify(W(z)-W(-z)+2*h*z)==0)
# Independently test the general nonlocal boundary integration identity,
# using mixtures of even exponentials and distinct resolvent-kernel rates.
for b in range(5,12):
 for c in range(1,6):
  rates=[1,2,3];weights=[F(1),F(c,7),F(2,5)];D=sum(weights)
  peak=sum(w*F(b,b+a) for a,w in zip(rates,weights))
  lhs=F(0)
  for a,wa in zip(rates,weights):
   for k,wk in zip(rates,weights):
    lhs+=wa*wk*a*(F(b*b,(b*b-k*k)*(a+k))-F(k*b,(b*b-k*k)*(a+b)))
  stress=sum(wa*wk*F(b*b,2*(b+a)*(b+k)) for a,wa in zip(rates,weights) for k,wk in zip(rates,weights))
  ck(lhs==D*peak-stress)
# Exact reflected-kernel positivity and decoupled strip/tail geometry.
J=lambda x:max(F(0),F(1)-abs(x))
for i in range(1,16):
 for j in range(1,16):
  x,y=F(i,10),F(j,10);K=J(x-y)-J(x+y)
  ck(K>=0)
  if abs(x-y)<1:ck(K>0)
# Endpoint coefficient follows from the second u derivative of D at0,r.
ck(S.simplify(aa**2*(1-1/aa)/(4*r)-aa*(aa-1)/(4*r))==0)
print(json.dumps({'status':'PASS','independent_assertions':n,'scope':'symbolic derivatives and exact identity/geometry controls; analytic proofs reviewed separately'},indent=2))
