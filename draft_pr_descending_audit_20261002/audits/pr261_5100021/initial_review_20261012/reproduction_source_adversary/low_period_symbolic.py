from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import sympy as s
B=Path(__file__).parent
V=lambda x,y:s.Matrix([x,y])
def cross(p,q):return s.det(s.Matrix.hstack(p,q))
def area(pts):return s.simplify(sum(cross(pts[i],pts[(i+1)%len(pts)]) for i in range(len(pts)))/2)
def constructions(P,M):
 Q=[];R=[]
 for i,p in enumerate(P):
  q=P[(i+1)%len(P)];d=q-p
  Q.append(s.simplify(p+((M-p).dot(d)/d.dot(d))*d))
  n1,n2=p-M,q-M
  R.append(s.simplify(s.Matrix.vstack(n1.T,n2.T).inv()*V(n1.dot(p),n2.dot(q))))
 return Q,R

a,b=s.Integer(5),s.Integer(3);lam=a*a*b*b/(a*a+b*b)
# Two algebraic closed quadrilaterals. The second comes from perpendicular
# outer-ellipse normals; all physical constraints are verified below.
P0=[V(a,0),V(0,b),V(-a,0),V(0,-b)]
p=V(3,s.Rational(12,5));q=V(-500/s.sqrt(10729),81/s.sqrt(10729));P1=[p,q,-p,-q]
rows=[]
for phase,P in [('axis',P0),('nonaxis-algebraic',P1)]:
 boundary=[];tangency=[];reflection=[]
 for i,p in enumerate(P):
  q=P[(i+1)%4];r=P[(i+2)%4];d=q-p;out=r-q
  boundary.append(s.simplify(p[0]**2/a**2+p[1]**2/b**2-1))
  ac2,bc2=a*a-lam,b*b-lam
  aa=d[0]**2/ac2+d[1]**2/bc2;bb=p[0]*d[0]/ac2+p[1]*d[1]/bc2;cc=p[0]**2/ac2+p[1]**2/bc2-1
  tangency.append(s.simplify(bb*bb-aa*cc))
  n=V(q[0]/a**2,q[1]/b**2);ref=s.simplify(d-2*d.dot(n)/n.dot(n)*n)
  # Zero cross product and positive dot means exact outgoing ray is the reflected ray.
  reflection.append({'parallel_residual':str(s.simplify(cross(ref,out))),'positive_dot':bool(s.N(ref.dot(out),50)>0)})
 focus_results=[]
 for sign in (1,-1):
  Q,R=constructions(P,V(sign*4,0));AP,AS=area(Q),area(R);prod=s.simplify(AP*AS)
  focus_results.append({'focus':sign*4,'pedal_area':str(AP),'antipedal_area':str(AS),'product':str(prod),'equals_axis_formula':s.simplify(prod-16*a**4*b**4/(a*a+b*b)**2)==0})
 assert all(x==0 for x in boundary+tangency)
 assert all(r['parallel_residual']=='0' and r['positive_dot'] for r in reflection)
 assert all(r['equals_axis_formula'] for r in focus_results)
 rows.append({'phase':phase,'vertices':[list(map(str,x)) for x in P],'boundary_residuals':list(map(str,boundary)),'tangency_discriminants':list(map(str,tangency)),'reflection_checks':reflection,'foci':focus_results})
out={'scope':'Exact a=5,b=3, primitive N=4,w=1 at two physically validated phases; no general-N proof','lambda':str(lam),'axis_product_formula':'16*a^4*b^4/(a^2+b^2)^2','rows':rows,'sympy':s.__version__}
(B/'LOW_PERIOD_SYMBOLIC.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
