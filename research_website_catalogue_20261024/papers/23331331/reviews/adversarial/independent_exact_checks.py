#!/usr/bin/env python3
"""Independent exact Laurent and Cartesian polynomial audit; standard library only."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt
import json

COUNT=0
def require(v,label):
 global COUNT
 COUNT+=1
 if not v:raise RuntimeError(label)
@dataclass(frozen=True)
class Q:
 p:F=F(0)
 q:F=F(0)
 def __post_init__(self):object.__setattr__(self,'p',F(self.p));object.__setattr__(self,'q',F(self.q))
 @staticmethod
 def get(a):return a if isinstance(a,Q) else Q(a)
 def __add__(self,b):b=Q.get(b);return Q(self.p+b.p,self.q+b.q)
 __radd__=__add__
 def __neg__(self):return Q(-self.p,-self.q)
 def __sub__(self,b):return self+-Q.get(b)
 def __rsub__(self,b):return Q.get(b)+-self
 def __mul__(self,b):
  if isinstance(b,P):return NotImplemented
  b=Q.get(b);return Q(self.p*b.p+30*self.q*b.q,self.p*b.q+self.q*b.p)
 __rmul__=__mul__
 def inverse(self):d=self.p*self.p-30*self.q*self.q;require(d!=0,'nonzero exact field denominator');return Q(self.p/d,-self.q/d)
 def __truediv__(self,b):return self*Q.get(b).inverse()
 def __rtruediv__(self,b):return Q.get(b)*self.inverse()
 def __pow__(self,k):
  if k<0:return self.inverse()**(-k)
  a=Q(1)
  for _ in range(k):a=a*self
  return a
 def __bool__(self):return bool(self.p or self.q)
 def sign(self):
  if not self:return 0
  if not self.q:return 1 if self.p>0 else -1
  if not self.p:return 1 if self.q>0 else -1
  if self.p>0 and self.q>0:return 1
  if self.p<0 and self.q<0:return -1
  d=self.p*self.p-30*self.q*self.q
  return (1 if d>0 else -1)*(1 if self.p>0 else -1)
 def encode(self):return [str(self.p),str(self.q)]
class P:
 def __init__(self,a=0,n=2):
  self.n=n
  self.d={k:Q.get(v) for k,v in a.items() if Q.get(v)} if isinstance(a,dict) else ({(0,)*n:Q.get(a)} if Q.get(a) else {})
 def get(self,b):
  if isinstance(b,P):require(b.n==self.n,'ring dimension');return b
  return P(b,self.n)
 @classmethod
 def var(cls,j,n=2):a=[0]*n;a[j]=1;return cls({tuple(a):Q(1)},n)
 def __add__(self,b):
  b=self.get(b);r=dict(self.d)
  for k,v in b.d.items():r[k]=r.get(k,Q())+v
  return P(r,self.n)
 __radd__=__add__
 def __neg__(self):return P({k:-v for k,v in self.d.items()},self.n)
 def __sub__(self,b):return self+-self.get(b)
 def __rsub__(self,b):return self.get(b)+-self
 def __mul__(self,b):
  b=self.get(b);r={}
  for k,v in self.d.items():
   for l,w in b.d.items():
    z=tuple(a+c for a,c in zip(k,l));r[z]=r.get(z,Q())+v*w
  return P(r,self.n)
 __rmul__=__mul__
 def __truediv__(self,b):
  if isinstance(b,P):return self*(b**-1)
  return self*Q.get(b).inverse()
 def __pow__(self,k):
  if k<0:
   require(len(self.d)==1,'only monomial inverse');(e,c),=self.d.items();return P({tuple(k*a for a in e):c**k},self.n)
  r=P(1,self.n)
  for _ in range(k):r=r*self
  return r
 def __eq__(self,b):return self.d==self.get(b).d
 def encode(self):return [{'exponents':list(k),'coefficient_Qsqrt30':v.encode()} for k,v in sorted(self.d.items())]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def moments(points):
 s=P(0,points[0][0].n);tx=P(0,s.n);ty=P(0,s.n)
 for p,q in zip(points,points[1:]+points[:1]):
  c=cross(p,q);s=s+c/2;tx=tx+c*(p[0]+q[0]);ty=ty+c*(p[1]+q[1])
 return s,tx,ty
def scale_physical(poly,degree,A):
 out={}
 for k,v in poly.d.items():
  power=degree-sum(k);require(power%2==0,'antipodal parity removes radical scale');out[k]=v*(A**(power//2))
 return P(out)
def exact_sqrt(q):
 q=Q.get(q);require(q.q==0 and q.p>0,'positive rational squared length');z=q.p
 for c in [1,30]:
  r=z/F(c);a=isqrt(r.numerator);b=isqrt(r.denominator)
  if a*a==r.numerator and b*b==r.denominator:return Q(F(a,b),0) if c==1 else Q(0,F(a,b))
 raise RuntimeError('squared length not in chosen exact field')

def main():
 results={}
 # Entire antipodal edge-moment expansion from the definition, before any support substitution.
 x,y,h,k,t,s=[P.var(j,6) for j in range(6)]
 def edge(sign):
  p=sign*h*x-t*x*x;q=sign*k*y-t*y*y
  pb=sign*h/x-s/(x*x);qb=sign*k/y-s/(y*y)
  return (pb*q-p*qb)*(p+q)
 average=(edge(1)+edge(-1))/2
 c=k*k*x*x-h*h*y*y+2*h*k*(x**3/y-y**3/x)
 b=h*h*x*x/(y*y)-k*k*y*y/(x*x)+h*k*(x/y-y/x)
 cubic=-(t*t*s)*(y*y/(x*x)-x*x/(y*y))*(x*x+y*y)
 require(average==c*t+b*s+cubic,'full independent antipodal cubic expansion')
 require(average!=c*s+b*t+cubic,'conjugation swap negative control')
 results['antipodal_edge_universal_polynomial_identity']=True
 # Independent Laurent reductions in the free ring Q[x±1,y±1,H,D,e].
 x,y,H,D,e=[P.var(j,5) for j in range(5)]
 hs=H+e*(x*x+x**-2)/2;ks=H+e*(y*y+y**-2)/2
 hk=D*(y/x+x/y)/2+e*(x*y+(x*y)**-1)/2
 c=ks*x*x-hs*y*y+2*hk*(x**3/y-y**3/x)
 b=hs*x*x/(y*y)-ks*y*y/(x*x)+hk*(x/y-y/x)
 Z=x*x;W=y*y;r=Z/W-W/Z;v=Z*Z/W-W*W/Z
 require(c==D*v+3*e*r/2+(D+H)*(Z-W)+e*(Z*Z-W*W),'universal first local Laurent identity')
 require(b==(D/2+H)*r+e*v/2+e*(Z-W)/2+e*(W**-1-Z**-1),'universal second local Laurent identity')
 require(v+(W/Z-Z/W)*(Z+W)==W-Z,'local doubled-normal telescope')
 require((y/x-x/y)*(x+y)==(2+y/x+x/y)*(y-x),'unit-complex local identity cleared of2i')
 cosd=(y/x+x/y)/2;coss=(x*y+(x*y)**-1)/2
 target=(D*D-e*e)*cosd*cosd-(H*H-e*e+e*(H-D)*(x*x+x**-2+y*y+y**-2)/2)
 require(target==hk*hk-hs*ks,'support-square reduction without assuming converse')
 results['local_Laurent_identities_exact']=5
 # Rectangle branch uses independent arbitrary Cartesian variables.
 X,Y,A,B=[P.var(j,4) for j in range(4)]
 area,tx,ty=moments([(A,Y),(X,B),(-A,Y),(X,-B)])
 require(area==2*A*B and tx==4*A*B*X and ty==4*A*B*Y,'arbitrary rectangle moment polynomials')
 results['rectangle_universal_polynomials']=True
 # Star: rebuild actual feet directly from tangent line equations in scaled Cartesian coordinates.
 ar=F(221,96);br=F(27625,20736);lam=F(125,96);ratio=Q(0,F(5,36))
 uvs=[(0,1),(F(-12,13),F(-5,13)),(1,0),(F(-12,13),F(5,13)),(0,-1),(F(12,13),F(5,13)),(-1,0),(F(12,13),F(-5,13))]
 require(ratio*ratio==Q(br/ar),'coordinate-field scale ratio')
 verts=[(Q(u),ratio*v) for u,v in uvs];normals=[(Q(u),Q(v)/ratio) for u,v in uvs]
 X=P.var(0);Y=P.var(1);feet=[]
 for u,v in uvs:
  nx=Q(u);ny=Q(v)/ratio;den=nx*nx+ny*ny
  factor=(1-nx*X-ny*Y)/den;feet.append((X+nx*factor,Y+ny*factor))
 sn,txn,tyn=moments(feet);S=scale_physical(sn,2,ar);TX=scale_physical(txn,3,ar);TY=scale_physical(tyn,3,ar)
 expectedS=-Q(0,F(1,134784))*(20736*(X*X+Y*Y)-123539)
 expectedTX=-Q(0,F(1,109512))*X*(41472*(X*X+Y*Y)-272935)
 expectedTY=-Q(0,F(1,97344))*Y*(52992*(X*X+Y*Y)-347633)
 require(S==expectedS and TX==expectedTX and TY==expectedTY,'complete unrestricted Cartesian star moment polynomials')
 # Tangency and unit-velocity specular reflection, every edge/vertex independently.
 ca=(ar-lam)/ar;cb=(br-lam)/ar
 winding=0
 for i,p in enumerate(verts):
  q=verts[(i+1)%8];prev=verts[(i-1)%8];n=normals[i]
  require(p!=q,'distinct adjacent vertices')
  dx=q[0]-p[0];dy=q[1]-p[1];line=(dy,-dx);offset=dot(line,p)
  require(line[0]**2*ca+line[1]**2*cb==offset**2,'exact confocal tangency')
  vin=(p[0]-prev[0],p[1]-prev[1]);vout=(q[0]-p[0],q[1]-p[1]);f=2*dot(vin,n)/dot(n,n)
  reflected=(vin[0]-f*n[0],vin[1]-f*n[1])
  require(cross(reflected,vout)==Q(0) and dot(reflected,vout).sign()>0 and dot(reflected,reflected)==dot(vin,vin),'exact unit-velocity reflection via positive parallel reflected vector')
  require(cross(n,normals[(i+1)%8]).sign()>0,'positive support-normal sine')
  if (p[1].sign()<=0<q[1].sign()) or (q[1].sign()<=0<p[1].sign()):
   xhit=(p[0]*q[1]-q[0]*p[1])/(q[1]-p[1])
   if xhit.sign()>0:winding+=1 if q[1].sign()>p[1].sign() else -1
 require(len(set(verts))==8 and winding==3,'primitive eight distinct vertices and exact winding3')
 H=(ar+br)/2;e=(ar-br)/2;d=1-lam*(1/ar+1/br);Fv=H*d+2*lam;v=-4*e*lam*d/(Fv*Fv-e*e*d*d);R2=-2*Fv/d
 require((d,Fv,v,R2)==(F(-120,221),F(2795,1728),F(7,13),F(123539,20736)),'exact star parameter values')
 G=2*Fv+d*(X*X+Y*Y);S0=S.d[(0,0)]
 require(S==S0*G/(2*Fv),'complete area ratio polynomial')
 aa=Fv+2*H*d+e*v*d;bb=2*Fv*v+3*e*d+v*d*(X*X+Y*Y)/2
 cxnum=3*G*X/2-X*(aa+bb);cynum=3*G*Y/2-Y*(aa-bb)
 require(3*G*TX==6*S*cxnum and 3*G*TY==6*S*cynum,'global formula versus unrestricted Cartesian polynomial certificate')
 require(3*G*TX!=6*S*cynum,'swapped-coordinate negative control')
 residual_x=-Q(0,F(1,109512))*(41472*R2-272935)
 require(residual_x==Q(0,F(17,72)),'exact nonzero first-moment coefficient on singular circle')
 require(F(17,72)*F(13,144)==F(221,10368),'diagnostic square-root coefficient at printed circle point')
 results['star']={'all_edge_tangencies':8,'all_vertex_unit_velocity_reflections':8,'distinct_vertices':8,'winding':winding,'signed_area_polynomial':S.encode(),'first_moment_x_polynomial':TX.encode(),'first_moment_y_polynomial':TY.encode(),'d':str(d),'F':str(Fv),'v':str(v),'undefined_radius_squared':str(R2),'nonzero_Tx_over_X_on_circle':residual_x.encode(),'global_formula_exact_as_polynomial_after_clearing_G':True}
 # Translation law for an arbitrary 4-vertex closed chain with formal coordinates.
 xx=[P.var(j,10) for j in range(10)];pts=[(xx[2*j],xx[2*j+1]) for j in range(4)];shift=(xx[8],xx[9]);sa,ta,tb=moments(pts);ss,ua,ub=moments([(p[0]+shift[0],p[1]+shift[1]) for p in pts])
 require(ss==sa and ua==ta+6*shift[0]*sa and ub==tb+6*shift[1]*sa,'arbitrary coordinate translation identity finite algebra control')
 results['translation_control_arbitrary_4vertex_coordinates']=True
 print(json.dumps({'verdict':'PASS_OWN_EXACT_CHECKS_ONLY','predicate_count_including_ring_and_denominator_guards':COUNT,'mechanisms':['Formal antipodal moment expansion','Free Laurent coefficient identities','Universal arbitrary rectangle branch','Direct Cartesian star projections and whole polynomials','Exact tangency/unit-reflection/winding','Singular-circle nonzero moment','Coordinate translation and deliberate conjugation/coordinate faults'],'results':results,'finite_checks_not_all_period_proof':True,'supplied_code_results_or_foreign_proofs_read':False},indent=2))
if __name__=='__main__':main()
