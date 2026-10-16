"""Independent finite exact outer-focal-PEDAL controls, no elliptic functions.

The N=3 pair is the same credited concrete example used in the completed
PR211 inverse-area audit (and Ferudun2026 DOI23096994 Sect6 for a different
ORIGINAL-vertex inversion target). Everything computed here is new pedal
geometry; none of that inversion conclusion is used. Finite diagnostics,
not the universal proof or evidence of novelty.
"""
from pathlib import Path
import json
import sympy as s

def clean(x):return s.factor(s.radsimp(s.simplify(x)))
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return clean(sum(det(p[j],p[(j+1)%len(p)]) for j in range(len(p)))/2)
exact=0

def zero(q):
 global exact
 assert clean(q)==0,clean(q);exact+=1

def footline(f,p,q):
 e=sub(q,p);tt=clean(dot(sub(f,p),e)/dot(e,e));return tuple(clean(p[j]+tt*e[j]) for j in (0,1))

aa,bb=s.Integer(21),s.Integer(16);lam=s.Rational(336,25);c=s.sqrt(5);a=s.sqrt(aa);b=s.sqrt(bb)
phases=[('H',[(a,0),(-3*a/5,s.Rational(16,5)),(-3*a/5,-s.Rational(16,5))]),('V',[(0,b),(-s.Rational(21,5),-s.Rational(8,5)),(s.Rational(21,5),-s.Rational(8,5))])]
rows=[]
for label,points in phases:
 outer=[]
 for j,p in enumerate(points):
  q=points[(j+1)%3];zero(p[0]**2/aa+p[1]**2/bb-1)
  incoming=sub(p,points[j-1]);outgoing=sub(q,p)
  incoming=tuple(clean(x/s.sqrt(dot(incoming,incoming))) for x in incoming)
  outgoing=tuple(clean(x/s.sqrt(dot(outgoing,outgoing))) for x in outgoing)
  normal=(p[0]/aa,p[1]/bb)
  reflected=tuple(clean(incoming[l]-2*dot(incoming,normal)*normal[l]/dot(normal,normal)) for l in [0,1])
  for l in [0,1]:zero(reflected[l]-outgoing[l])
  nx,ny=q[1]-p[1],p[0]-q[0];ell=nx*p[0]+ny*p[1]
  zero(ell**2-(aa-lam)*nx**2-(bb-lam)*ny**2)
  ap,bp=p[0]/aa,p[1]/bb;aq,bq=q[0]/aa,q[1]/bb;dd=clean(ap*bq-aq*bp);assert dd!=0
  Q=(clean((bq-bp)/dd),clean((ap-aq)/dd));outer.append(Q)
  zero(ap*Q[0]+bp*Q[1]-1);zero(aq*Q[0]+bq*Q[1]-1)
 pedals=[];original=[]
 for sign in [1,-1]:
  f=(sign*c,s.Integer(0));feet=[];chordfeet=[]
  for j,p in enumerate(points):
   q=footline(f,outer[j-1],outer[j]);feet.append(q)
   n=(p[0]/aa,p[1]/bb);zero(dot(n,q)-1);zero(det(sub(q,f),n));zero(dot(q,q)-aa)
   # The foot map is a projective map of original ellipse onto auxiliary circle.
   projective=(aa*(p[0]+sign*c)/(aa+sign*c*p[0]),aa*p[1]/(aa+sign*c*p[0]))
   for l in [0,1]:zero(q[l]-projective[l])
   chordfeet.append(footline(f,p,points[(j+1)%3]))
  pedals.append(feet);original.append(chordfeet)
 B=[area(q) for q in pedals];A=[area(q) for q in original];prod=clean(B[0]*B[1]);orig=clean(A[0]*A[1])
 for r in [3,5]:
  zero(area(pedals[0]*r)*area(pedals[1]*r)-r*r*prod)
 for scale in [s.Rational(2,7),s.Integer(3)]:
  changed=[[(scale*x,scale*y) for x,y in q] for q in pedals]
  zero(area(changed[0])*area(changed[1])-scale**4*prod)
 zero(area(list(reversed(pedals[0])))*area(list(reversed(pedals[1])))-prod)
 # A rigid rotation plus translation changes no shoelace area.
 for q,Bf in zip(pedals,B):
  moved=[(s.Rational(3,5)*x-s.Rational(4,5)*y+7,s.Rational(4,5)*x+s.Rational(3,5)*y-11) for x,y in q]
  zero(area(moved)-Bf)
 rows.append(dict(phase=label,outer_vertices=[[str(x) for x in q] for q in outer],outer_focal_pedal_areas=[str(x) for x in B],outer_product=str(prod),original_chord_pedal_areas=[str(x) for x in A],original_product=str(orig)))
zero(s.sympify(rows[0]['outer_product'])-s.sympify(rows[1]['outer_product']))
assert rows[0]['outer_product']!=rows[0]['original_product']
# Exact generic algebraic projection-to-circle conjugacy, distinct from finite orbit checks.
X,Y,e,t=s.symbols('X Y e t')
# Set e=2t/(1+t^2), sqrt(1-e^2)=(1-t^2)/(1+t^2), |t|<1.
ee=2*t/(1+t*t);gg=(1-t*t)/(1+t*t)
qx=(X+ee)/(1+ee*X);qy=gg*Y/(1+ee*X)
z=X+s.I*Y;mob=(z+t)/(1+t*z)
for expr in [qx*qx+qy*qy-1,(qx+s.I*qy)*(1+t*z)-(z+t)]:
 num,den=s.fraction(s.factor(expr));zero(s.rem(num,Y*Y+X*X-1,Y)/den)
out=dict(status='PASS finite exact geometric controls',sympy=s.__version__,exact_zero_assertions=exact,ellipse_squared_axes=[str(aa),str(bb)],caustic_parameter=str(lam),caustic_squared_axes=[str(aa-lam),str(bb-lam)],phases=rows,repetition_factors=[3,5],length_scaling_degree=4,orientation_and_rigid_motion_checked=True,projective_and_Mobius_auxiliary_circle_maps_derived=True,limits='Finite exact algebra and two genuine N=3 phases. No universal conclusion, interval certification or novelty claim; repeated traversal follows exact shoelace linearity.')
print(json.dumps(out,indent=2))
