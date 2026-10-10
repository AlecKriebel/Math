"""Exact author-written controls. Samples do not prove the general odd-period claim."""
import sympy as s
import json
from collections import Counter
F=s.Rational
counts=Counter()
def check(ok,group):
 assert ok,group
 counts[group]+=1
def zero(x):return s.simplify(x)==0
def area(p):return s.simplify(sum(x*b-y*a for (x,y),(a,b) in zip(p,p[1:]+p[:1]))/2)
def invert(P,f,rho=1):
 return [tuple(s.simplify(t) for t in (f+rho**2*(x-f)/((x-f)**2+y*y),rho**2*y/((x-f)**2+y*y))) for x,y in P]
H=[(2*s.sqrt(2),0),(-4*s.sqrt(2)/3,F(5,3)),(-4*s.sqrt(2)/3,-F(5,3))]
V=[(0,s.sqrt(5)),(-F(8,3),-s.sqrt(5)/3),(F(8,3),-s.sqrt(5)/3)]
B=s.diag(F(1,8),F(1,5));Cdual=s.diag(F(32,9),F(5,9));output={}
for name,P in [('H',H),('V',V)]:
 P=[tuple(map(s.sympify,p)) for p in P]
 for i,(x,y) in enumerate(P):
  p=s.Matrix(P[i]);q=s.Matrix(P[(i+1)%3]);r=s.Matrix(P[(i-1)%3]);n=B*p
  check(zero(p.dot(n)-1),'outer_incidence')
  ell=s.Matrix.vstack(p.T,q.T).inv()*s.Matrix([1,1])
  check(zero(ell.dot(Cdual*ell)-1),'caustic_tangency')
  din=p-r;din=din/s.sqrt(din.dot(din));dout=q-p;dout=dout/s.sqrt(dout.dot(dout))
  reflected=din-2*din.dot(n)/n.dot(n)*n
  for j in range(2):check(zero(reflected[j]-dout[j]),'reflection_law')
 vals=[]
 for focus in [s.sqrt(3),-s.sqrt(3)]:
  Q=invert(P,focus);val=area(Q);vals.append(val)
  for (x,y),(u,v) in zip(P,Q):
   check(zero((u-focus)*(x-focus)+v*y-1),'unit_inversion')
   check(zero((u-focus)*y-v*(x-focus)),'inversion_collinearity')
  check(zero(area(invert(list(reversed(P)),focus))+val),'signed_reversal')
  check(zero(area(invert(P,focus,2))-16*val),'radius_scaling')
 product=s.simplify(vals[0]*vals[1]);check(product==F(5,256),'three_period_product')
 output[name]={'areas':list(map(str,vals)),'product':str(product)}

# Negative control: the asserted product need not be invariant for even period.
D=[(4,0),(0,3),(-4,0),(0,-3)]
R=[(F(16,5),F(9,5)),(-F(16,5),F(9,5)),(-F(16,5),-F(9,5)),(F(16,5),-F(9,5))]
negative=[]
for P in [D,R]:
 P=[tuple(map(s.sympify,p)) for p in P]
 for x,y in P:check(zero(x*x/16+y*y/9-1),'even_control_incidence')
 vals=[area(invert(P,f)) for f in [s.sqrt(7),-s.sqrt(7)]]
 check(zero(vals[0]-vals[1]),'even_focal_equality')
 negative.append(s.simplify(vals[0]*vals[1]))
check(negative[0]==F(1,36),'even_control_value')
check(negative[1]==F(625,20736),'even_control_value')
check(negative[0]!=negative[1],'even_product_negative_control')

# Exact complex tangency/contact identities, valid symbolically for all a>b>0.
a,b,lam=s.symbols('a b lam',positive=True);c=s.sqrt(a*a-b*b)
for eps in [1,-1]:
 for eta in [1,-1]:
  x,y=eps*a*a/c,eta*s.I*b*b/c
  check(zero(x*x/a**2+y*y/b**2-1),'complex_contact')
  check(zero(x*x/a**4+y*y/b**4),'isotropic_normal')
  check(zero((a*a-lam)*x*x/a**4+(b*b-lam)*y*y/b**4-1),'common_tangent')
  check(zero(x*x/(a*a-lam)+y*y/(b*b-lam)-1+lam**2/((a*a-lam)*(b*b-lam))),'unramified_residual')
  # One isotropic line through the matching focus passes through this point.
  z,w=x+s.I*y,x-s.I*y;f=eps*c
  check(zero((z-f)*(w-f)),'inversion_pole_contact')
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'counts':dict(counts),'three_period_controls':output,'even_products':list(map(str,negative)),'limits':'Exact symbolic identities and finite geometry controls only; the general theorem rests on the flag-curve pole/zero proof.'},indent=2))
