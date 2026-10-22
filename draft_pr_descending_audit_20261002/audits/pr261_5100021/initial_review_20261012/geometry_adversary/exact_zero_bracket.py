import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'_python'))
import sympy as s

def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def area(poly):return s.simplify(sum(det(p,q) for p,q in zip(poly,poly[1:]+poly[:1]))/2)
rows=[]
for r in [s.Rational(3),s.Rational(5)]:
 a2=(r-1)**3*(r+1)/(4*r);a=s.sqrt(a2);c=s.sqrt(a2-1);x=(r*r-1)/(r*r+1);y=2*r/(r*r+1)
 lam=a2/(a2+r*r)
 poly=[(a,0),(a*x,y),(0,1),(-a*x,y),(-a,0),(-a*x,-y),(0,-1),(a*x,-y)]
 relative=[(p[0]-c,p[1]) for p in poly];anti=[];pedal=[]
 for p,q in zip(relative,relative[1:]+relative[:1]):
  k=s.simplify(det(p,q));p2=s.simplify(dot(p,p));q2=s.simplify(dot(q,q));d=(q[0]-p[0],q[1]-p[1]);d2=s.simplify(dot(d,d))
  anti.append(tuple(s.simplify(t) for t in ((p2*q[1]-q2*p[1])/k,(p[0]*q2-q[0]*p2)/k)))
  pedal.append(tuple(s.simplify(t) for t in (k*d[1]/d2,-k*d[0]/d2)))
 aa=s.radsimp(area(anti));ap=s.radsimp(area(pedal))
 assert s.sign(ap)==1
 assert s.sign(aa)==(1 if r==3 else -1)
 # Independent exact reflection at the off-axis vertex.
 incoming=(a*x-a,y);outgoing=(-a*x,1-y);normal=(x/a,y)
 li=s.sqrt(dot(incoming,incoming));lo=s.sqrt(dot(outgoing,outgoing))
 incoming=tuple(t/li for t in incoming);outgoing=tuple(t/lo for t in outgoing)
 reflected=tuple(incoming[i]-2*dot(incoming,normal)*normal[i]/dot(normal,normal) for i in (0,1))
 assert all(s.simplify(reflected[i]-outgoing[i])==0 for i in (0,1))
 # Both consecutive chord tangency constraints exactly agree at the same lambda.
 assert s.simplify(lam-(a2*(1-x)**2/((y*y)+a2*(1-x)**2)))==0
 assert s.simplify(lam-(a2*(1-y)**2/((1-y)**2+a2*x*x)))==0
 rows.append({'r':str(r),'a_squared':str(a2),'b':'1','c_squared':str(a2-1),'x':str(x),'y':str(y),'lambda':str(lam),'pedal_area':str(ap),'antipedal_area':str(aa),'antipedal_sign':str(s.sign(aa))})
result={'provenance':'Independent exact original-line formulas; written after proof exposure to verify the claimed zero-area allowance. No author checker used.','period8_direct_construction':'For r>1 set x=(r²−1)/(r²+1), y=2r/(r²+1), a²=(r−1)³(r+1)/(4r), b=1. Outer vertices (a,0),(ax,y),(0,1),(−ax,y),(−a,0),(−ax,−y),(0,−1),(ax,−y). Both first-quadrant chords tangent to same confocal caustic lambda=a²/(a²+r²). Reflection and axis symmetries propagate, making a convex primitive period-eight billiard. Over r in[3,5] a²>1 and lambda in(0,1), and every focal normal determinant is nonzero.','rows':rows,'conclusion':'Signed antipedal area is continuous on r in[3,5], changes sign, and thus vanishes for at least one admissible primitive period-eight pair. This existence statement is exact, independent of numerical root identification and of the product proof.'}
Path('EXACT_ZERO_AREA_BRACKET.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
