#!/usr/bin/env python3
"""Fresh exact supplemental claims; no original audit scripts imported."""
import sys
sys.path.insert(0,"/Users/alec/Library/Python/3.11/lib/python/site-packages")
import sympy as s,json,datetime,hashlib
from pathlib import Path
checks=[]
def zero(label,x):
 x=s.simplify(x);assert x==0,(label,x);checks.append({"label":label,"residual":"0"})
def det(u,v):return u[0]*v[1]-u[1]*v[0]
def dot(u,v):return sum(x*y for x,y in zip(u,v))
def area(V):return s.simplify(sum(det(V[j],V[(j+1)%len(V)]) for j in range(len(V)))/2)
A,B,l,c,x,y=s.symbols("A B l c x y",positive=True)
a2=A+l;b2=B+l
T=s.Matrix([[a2,0,a2*c],[0,a2,0],[c,0,a2]])
dual=T*s.diag(A,B,-1)*T.T
line=s.Matrix([x,y,-a2])
dualpoly=s.expand((line.T*dual*line)[0]/a2**2).subs(c*c,A-B)
db=-c*l/B;Rb2=A*b2**2/B**2
expected=B*((x-db)**2+y*y-Rb2)
zero("polar-dual-actual-circle",s.expand(dualpoly-expected).subs(c*c,A-B))
# Projectivity pulls back auxiliary radius-a circle to original ellipse.
X=a2*(x+c)/(a2+c*x);Y=a2*y/(a2+c*x)
circle=s.factor(s.together(X*X+Y*Y-a2).as_numer_denom()[0])
circle=circle.subs(c*c,A-B)
boundary=b2*x*x+a2*y*y-a2*b2
zero("projectivity-boundary-circle",s.rem(s.expand(circle),boundary,y))
# Exact pointwise inverse/foot vectors and both distinct finite configurations.
rt=s.sqrt;a=rt(21);b=s.Integer(4);c=rt(5)
H=[s.Matrix(p) for p in [(a,0),(-3*a/5,s.Rational(16,5)),(-3*a/5,-s.Rational(16,5))]]
V=[s.Matrix(p) for p in [(0,4),(-s.Rational(21,5),-s.Rational(8,5)),(s.Rational(21,5),-s.Rational(8,5))]]
results=[]
for label,W in [("H",H),("V",V)]:
 Bareas=[];Dareas=[];Careas=[]
 for sign in [1,-1]:
  F=s.Matrix([sign*c,0]);outerfeet=[];inverses=[];chordfeet=[]
  for j,P in enumerate(W):
   normal=s.Matrix([P[0]/a**2,P[1]/b**2])
   outerfeet.append(F+(1-dot(normal,F))/dot(normal,normal)*normal)
   u=P-F;inverses.append(u/dot(u,u))
   next=W[(j+1)%len(W)];edge=next-P
   chordfeet.append(P+dot(F-P,edge)/dot(edge,edge)*edge)
  Bareas.append(area(outerfeet));Dareas.append(area(inverses));Careas.append(area(chordfeet))
 zero(label+"-outer-product",Bareas[0]*Bareas[1]-s.Rational(12544,25))
 zero(label+"-inverse-product",Dareas[0]*Dareas[1]-s.Rational(1,324))
 zero(label+"-original-chord-product",Careas[0]*Careas[1]-s.Rational(7225344,390625))
 zero(label+"-opposite-inverse-transfer-plus",Bareas[0]-s.Rational(2016,5)*Dareas[1])
 zero(label+"-opposite-inverse-transfer-minus",Bareas[1]-s.Rational(2016,5)*Dareas[0])
 results.append({"phase":label,"outer_areas":[str(t) for t in Bareas],"inverse_areas":[str(t) for t in Dareas],"chord_areas":[str(t) for t in Careas]})
out={"schema":"pr210-independent-supplemental-exact-v1","utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS","exact_assertions":len(checks),"checks":checks,"fixture_results":results,
"limits":"The symbolic projective identities and exact finite controls support the separately written general derivation. No novelty or primary-source attribution conclusion is drawn."}
p=Path(__file__).resolve().parent/"SUPPLEMENTAL_EXACT_RESULTS.json";p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":"PASS","exact":len(checks),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}))
