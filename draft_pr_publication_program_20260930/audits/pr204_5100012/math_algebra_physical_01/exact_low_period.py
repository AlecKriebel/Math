#!/usr/bin/env python3
"""Direct exact N=3 and N=4 Euclidean controls, no elliptic functions or author code."""
import sys,json
import sympy as s
from collections import Counter
C=Counter()
def zero(x,label):
 r=s.simplify(s.expand(x))
 if r!=0:r=s.simplify(s.radsimp(r))
 if r!=0:raise RuntimeError(label+': '+str(r))
 C[label]+=1

def positive(x,label):
 q=s.simplify(x)
 if q.is_positive is not True:
  if s.sign(q)!=1:raise RuntimeError(label+': positivity not exact '+str(q))
 C[label]+=1

def dot(p,q):return (p.T*q)[0]
def cross(p,q):return s.det(s.Matrix.hstack(p,q))
def area(P):return s.simplify(sum(cross(p,q) for p,q in zip(P,P[1:]+P[:1]))/2)
def vals(P,a,b,lam):
 feet=[]
 for i,p in enumerate(P):
  before=P[(i-1)%len(P)];q=P[(i+1)%len(P)];d=q-p
  zero(p[0]**2/a**2+p[1]**2/b**2-1,'boundary')
  Aq=d[0]**2/(a*a-lam)+d[1]**2/(b*b-lam)
  Bq=2*(p[0]*d[0]/(a*a-lam)+p[1]*d[1]/(b*b-lam))
  Cq=p[0]**2/(a*a-lam)+p[1]**2/(b*b-lam)-1
  zero(Bq*Bq-4*Aq*Cq,'caustic_tangent_discriminant')
  inc=p-before;n=s.Matrix([p[0]/a**2,p[1]/b**2]);refl=inc-2*dot(inc,n)*n/dot(n,n)
  zero(cross(refl,d),'specular_parallel')
  positive(dot(refl,d),'specular_forward')
  foot=p-dot(p,d)*d/dot(d,d);zero(dot(foot,d),'origin_foot');feet.append(foot)
 positive(lam,'lambda_positive');positive(b*b-lam,'proper_caustic')
 A=area(P);B=area(feet);positive(A,'signed_area_positive');positive(B,'pedal_area_positive')
 return A,B,s.simplify(A*B)
a=s.Integer(2);b=s.Integer(1);S=a*a+b*b;lam4=a*a*b*b/S
D4=[s.Matrix(p) for p in [(a,0),(0,b),(-a,0),(0,-b)]]
x=a*a/s.sqrt(S);y=b*b/s.sqrt(S)
R4=[s.Matrix(p) for p in [(x,y),(-x,y),(-x,-y),(x,-y)]]
u=vals(D4,a,b,lam4);v=vals(R4,a,b,lam4)
zero(u[2]-v[2],'four_phase_product_equal')
zero(u[2]-8*a**4*b**4/S**2,'four_explicit_product')
# Exact N=3 caustic from two axis-symmetric orbits. Solve tangent discriminant,
# not Cayley/Jacobi closure: (a²-b²)c²-2b²c-a²=0.
D=s.sqrt(a**4-a*a*b*b+b**4)
c=(b*b-D)/(a*a-b*b);d=(a*a-D)/(b*b-a*a)
sx=s.sqrt(1-c*c);sy=s.sqrt(1-d*d);lam3=s.simplify(a*a*(1-c*c))
zero(lam3-b*b*(1-d*d),'three_same_caustic')
T3=[s.Matrix(p) for p in [(a,0),(a*c,b*sx),(a*c,-b*sx)]]
U3=[s.Matrix(p) for p in [(0,b),(-a*sy,b*d),(a*sy,b*d)]]
t=vals(T3,a,b,lam3);w=vals(U3,a,b,lam3)
zero(t[2]-w[2],'three_phase_product_equal')
# Excluded primitive6, same proper caustic lambda=4/9, two axis phases.
lam6=s.Rational(4,9);r=s.sqrt(5)/3;q=4*s.sqrt(2)/3
H6=[s.Matrix(p) for p in [(2,0),(s.Rational(4,3),r),(-s.Rational(4,3),r),(-2,0),(-s.Rational(4,3),-r),(s.Rational(4,3),-r)]]
J6=[s.Matrix(p) for p in [(0,1),(-q,s.Rational(1,3)),(-q,-s.Rational(1,3)),(0,-1),(q,-s.Rational(1,3)),(q,s.Rational(1,3))]]
g=vals(H6,a,b,lam6);h=vals(J6,a,b,lam6)
positive((g[2]-h[2])**2,'excluded_six_product_nonconstant')
# Repeating each list twice multiplies both signed shoelace sums by2, hence product by4.
zero(area(H6+H6)-2*area(H6),'repeated_list_area_doubles')
positive((4*g[2]-4*h[2])**2,'formal_twelve_repeated_six_counterexample')
for P,N in [(D4,4),(R4,4),(T3,3),(U3,3),(H6,6),(J6,6)]:
 for i in range(N):
  for j in range(i):positive(dot(P[i]-P[j],P[i]-P[j]),'distinct_vertices_least_period')
if '--false-identity' in sys.argv:zero(t[2]-(w[2]+1),'FALSE_three_phase_product_plus_one')
result={'status':'PASS','exact_checks':dict(C),'checks_total':sum(C.values()),'axes':[str(a),str(b)],'four_lambda':str(lam4),'four_diamond':[str(x) for x in u],'four_rectangle':[str(x) for x in v],'three_lambda':str(lam3),'three_axis_a':[str(x) for x in t],'three_axis_b':[str(x) for x in w],'six_lambda':str(lam6),'six_axis_a':[str(x) for x in g],'six_axis_b':[str(x) for x in h],'six_exact_product_difference':str(s.simplify(g[2]-h[2])),'formal_twelve_repeated_product_difference':str(s.simplify(4*(g[2]-h[2]))),'limits':'Exact physical geometry at two distinct N=3 phases and two N=4 phases for axes 2,1; excluded primitive N=6 and twice-repeated formal N=12 exact counterexamples; no universal target-phase theorem. Independent authored mechanism, no author code imported.'}
print(json.dumps(result,indent=2))
