from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import sympy as s
B=Path(__file__).parent;V=lambda x,y:s.Matrix([x,y]);cross=lambda p,q:s.det(s.Matrix.hstack(p,q))
def area(Q):return s.simplify(sum(cross(Q[i],Q[(i+1)%len(Q)]) for i in range(len(Q)))/2)
def areas(P,F):
 Q=[];R=[]
 for i,p in enumerate(P):
  q=P[(i+1)%len(P)];d=q-p;n1,n2=p-F,q-F
  Q.append(s.simplify(p+(F-p).dot(d)/d.dot(d)*d))
  R.append(s.simplify(s.Matrix.vstack(n1.T,n2.T).inv()*V(n1.dot(p),n2.dot(q))))
 return area(Q),area(R)
a,b=s.Rational(3,2),s.Integer(1);lam=s.Rational(9,25);F=V(s.sqrt(5)/2,0)
X=s.Rational(3,10)*s.sqrt(21)
P0=[V(a,0),V(s.Rational(9,10),s.Rational(4,5)),V(-s.Rational(9,10),s.Rational(4,5)),V(-a,0),V(-s.Rational(9,10),-s.Rational(4,5)),V(s.Rational(9,10),-s.Rational(4,5))]
P1=[V(0,1),V(-X,s.Rational(2,5)),V(-X,-s.Rational(2,5)),V(0,-1),V(X,-s.Rational(2,5)),V(X,s.Rational(2,5))]
rows=[]
for phase,P in [('major-axis',P0),('minor-axis',P1)]:
 assert len({tuple(p) for p in P})==6
 residuals=[]
 for i,p in enumerate(P):
  q,r=P[(i+1)%6],P[(i+2)%6];d=q-p;out=r-q
  bound=s.simplify(p[0]**2/a**2+p[1]**2/b**2-1)
  ac2,bc2=a*a-lam,b*b-lam;qa=d[0]**2/ac2+d[1]**2/bc2;qb=p[0]*d[0]/ac2+p[1]*d[1]/bc2;qc=p[0]**2/ac2+p[1]**2/bc2-1;disc=s.simplify(qb*qb-qa*qc)
  n=V(q[0]/a**2,q[1]/b**2);ref=s.simplify(d-2*d.dot(n)/n.dot(n)*n);refl=s.simplify(cross(ref,out))
  assert bound==disc==refl==0 and bool(s.N(ref.dot(out),50)>0)
  residuals.append({'boundary':str(bound),'caustic_discriminant':str(disc),'reflected_ray_cross':str(refl),'reflected_outgoing_dot_positive':True})
 AP,AS=areas(P,F);AP12,AS12=areas(P+P,F)
 assert s.simplify(AP12-2*AP)==0 and s.simplify(AS12-2*AS)==0
 rows.append({'phase':phase,'N6_vertices':[list(map(str,p)) for p in P],'physical_checks':residuals,'N6_pedal':str(AP),'N6_antipedal':str(AS),'N6_product':str(s.simplify(AP*AS)),'N12_repeated_product':str(s.simplify(AP12*AS12))})
assert s.simplify(s.sympify(rows[0]['N12_repeated_product'])-s.sympify(rows[1]['N12_repeated_product']))!=0
out={'status':'PASS','claim':'The unrestricted listed-N interpretation is false: two primitive N6 phases in the same strict elliptical caustic, each repeated twice to listed N12, have distinct focal area products. This is outside the pinned primitive target.','a':str(a),'b':str(b),'lambda':str(lam),'caustic_axes_squared':[str(a*a-lam),str(b*b-lam)],'focus':str(F[0]),'rows':rows,'exact_product_difference':str(s.simplify(s.sympify(rows[0]['N12_repeated_product'])-s.sympify(rows[1]['N12_repeated_product'])))}
(B/'EXACT_REPEATED_PERIOD.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
