from fractions import Fraction as F
from math import gcd,isqrt
import json

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def dot(a,b,g):return g[0]*a[0]*b[0]+g[1]*a[1]*b[1]
def area(v):return sum((det(v[i],v[(i+1)%len(v)]) for i in range(len(v))),F(0))/2
def constructs(v,g):
 q=[];r=[];formula=F(0)
 for A,B in zip(v,v[1:]+v[:1]):
  d=sub(B,A);dd=dot(d,d,g);need(dd>0,'distinct consecutive endpoints')
  f=dot(A,d,g)/dd;q.append((A[0]-f*d[0],A[1]-f*d[1]))
  H,J,C=dot(A,A,g),dot(B,B,g),dot(A,B,g)
  matrix_det=g[0]*g[1]*det(A,B);need(matrix_det!=0,'finite antipedal intersection')
  X=((H*g[1]*B[1]-J*g[1]*A[1])/matrix_det,
     (g[0]*A[0]*J-g[0]*B[0]*H)/matrix_det)
  need(dot(A,X,g)==H and dot(B,X,g)==J,'direct antipedal equations')
  r.append(X)
  formula+=(H*J-(H+J)*C/2)/(g[0]*g[1]*det(A,B))
 need(area(r)==formula,'actual area and collected edge formula')
 return area(q),area(r),g[0]*g[1]*area(q)*area(r)
def square_root(q):
 n,d=isqrt(q.numerator),isqrt(q.denominator)
 need(n*n==q.numerator and d*d==q.denominator,'rational orbit edge length')
 return F(n,d)
def reflected(v,g,outer,caustic):
 for i,A in enumerate(v):
  P,B=v[i-1],v[(i+1)%len(v)]
  need(A[0]**2/outer[0]+A[1]**2/outer[1]==1,'outer ellipse')
  D=sub(B,A);alpha,beta=D[1],-D[0];w=alpha*A[0]+beta*A[1]
  need(w*w==caustic[0]*alpha*alpha+caustic[1]*beta*beta,'exact caustic tangency')
  u=sub(A,P);vout=D;lu=square_root(dot(u,u,g));lv=square_root(dot(D,D,g))
  u=(u[0]/lu,u[1]/lu);vout=(D[0]/lv,D[1]/lv)
  normal=(A[0]/(outer[0]*g[0]),A[1]/(outer[1]*g[1]))
  coeff=2*dot(u,normal,g)/dot(normal,normal,g)
  need(vout==(u[0]-coeff*normal[0],u[1]-coeff*normal[1]),'exact reflection')

first=[(F(1),F(0)),(F(-3,5),F(16,5)),(F(-3,5),F(-16,5))]
second=[(F(0),F(4)),(F(-21,5),F(-8,5)),(F(21,5),F(-8,5))]
reflected(first,(F(21),F(1)),(F(1),F(16)),(F(9,25),F(64,25)))
reflected(second,(F(1),F(1)),(F(21),F(16)),(F(189,25),F(64,25)))
A=constructs(first,(F(21),F(1)));B=constructs(second,(F(1),F(1)))
need(A[2]==B[2],'same-caustic primitive triangle phases')
for orbit,g in [(first,(F(21),F(1))),(second,(F(1),F(1)))]:
 base=constructs(orbit,g)
 reverse=constructs(list(reversed(orbit)),g)
 need(reverse[0]==-base[0] and reverse[1]==-base[1] and reverse[2]==base[2],'reversal')
 for repeat in (2,3):need(constructs(orbit*repeat,g)[2]==repeat**2*base[2],'repetition')
 scaled=[(2*x,2*y) for x,y in orbit]
 need(constructs(scaled,g)[2]==16*base[2],'physical quartic scaling')
diamond=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
rectangle=[(F(5),F(3)),(F(-5),F(3)),(F(-5),F(-3)),(F(5),F(-3))]
D=constructs(diamond,(F(5),F(3)));R=constructs(rectangle,(F(1,8),F(1,8)))
need(D[2]==F(225,4) and R[2]==F(289,4),'same-caustic even counterexample')
# Generic rational polygons test the actual-construction identity without any
# billiard or convexity assumption. They do not test phase invariance.
points=[]
for t in [F(-3),F(-2),F(-1),F(-1,2),F(0),F(1,3),F(1),F(2),F(4)]:
 points.append((5*(1-t*t)/(1+t*t),6*t/(1+t*t)))
generic=0
for n in (3,5,7,9):
 for start in range(9):
  for winding in range(1,n):
   if gcd(winding,n)!=1:continue
   v=[points[(start+(j*winding)%n)%9] for j in range(n)]
   if any(det(a,b)==0 for a,b in zip(v,v[1:]+v[:1])):continue
   constructs(v,(F(1),F(1)));generic+=1
arithmetic=0;even_failures=0
for n in range(3,202):
 for tau in range(1,(n+1)//2):
  if gcd(n,tau)!=1:continue
  residues={(2*tau*j)%n for j in range(n)}
  if n%2:
   need(len(residues)==n,'odd orbit subgroup')
   need(sum((tau*(2*j+1))%n==0 for j in range(n))==1,'unique opposite-edge class at vertex-pole phase')
   arithmetic+=1
  else:
   need(len(residues)==n//2 and (tau%2)==1,'even subgroup split')
   even_failures+=1
# Opposite endpoint numerator must not be treated as removable.
P=(F(1),F(0));Q=(F(-1),F(0));H=dot(P,P,(F(1),F(1)))
need(H*H-(2*H)*dot(P,Q,(F(1),F(1)))/2==2,'opposite finite numerator retained')
# Formal Laurent odd part removes order2 but retains order1.
laurent={-2:F(7),-1:F(11),0:F(3),1:F(5)}
odd={k:v-((-1)**k)*v for k,v in laurent.items()}
need(odd[-2]==0 and odd[-1]==22,'incident pole cancellation')
print(json.dumps({'status':'PASS_SOURCE_ONLY_ADVERSARIAL_CONTROLS',
 'primitive_triangle_products':[str(A[2]),str(B[2])],
 'triangle_coordinate_areas':[list(map(str,A[:2])),list(map(str,B[:2]))],
 'even_products':[str(D[2]),str(R[2])],'generic_direct_construction_polygons':generic,
 'odd_primitive_winding_arithmetic_cases':arithmetic,'even_subgroup_negative_cases':even_failures,
 'negative_controls':['even four-period phase dependence','opposite endpoints leave nonzero numerator',
 'even subgroup does not have odd trace period','repeated list changes product by r^2',
 'Laurent odd part retains simple pole'],
 'assertions_used':False,'native_imports_or_runs':[],
 'scope':'Exact line geometry, two reflected triangle phases, boundary counterexample and arithmetic; elliptic all-period divisor proof remains analytic in INITIAL.md.'},indent=2,sort_keys=True))
