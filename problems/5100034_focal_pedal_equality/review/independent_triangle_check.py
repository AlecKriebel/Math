#!/usr/bin/env python3
"""Independent exact source-scope control, constructed directly from two triangles."""
import sympy as s,json
r=s.sqrt(13);a=s.Integer(2);b=s.Integer(1);c=s.sqrt(3)
ac=2*(r-1)/3;bc=(4-r)/3
assert s.simplify(ac*ac-bc*bc-c*c)==0
ux=ac/a;uy=bc/b
Px=[s.Matrix([a,0]),s.Matrix([-ac,b*s.sqrt(1-ux*ux)]),s.Matrix([-ac,-b*s.sqrt(1-ux*ux)])]
Py=[s.Matrix([0,b]),s.Matrix([-a*s.sqrt(1-uy*uy),-bc]),s.Matrix([a*s.sqrt(1-uy*uy),-bc])]
checks=1
F=[s.Matrix([c,0]),s.Matrix([-c,0])]
def det(u,v):return s.det(s.Matrix.hstack(u,v))
def area(Q):return s.simplify(sum(det(Q[i],Q[(i+1)%3]) for i in range(3))/2)
def pedal(P,f):
 Q=[]
 for i in range(3):
  v=P[(i+1)%3]-P[i];Q.append(s.simplify(P[i]+((f-P[i]).dot(v)/v.dot(v))*v))
 return Q
records=[]
for P in [Px,Py]:
 for p in P:
  assert s.simplify(p[0]**2/a**2+p[1]**2/b**2-1)==0;checks+=1
 for i in range(3):
  p,q=P[i],P[(i+1)%3];v=q-p;n=s.Matrix([v[1],-v[0]]);H=s.simplify(n.dot(p))
  assert s.simplify(ac**2*n[0]**2+bc**2*n[1]**2-H**2)==0;checks+=1
 A=[area(pedal(P,f)) for f in F]
 records.append(A)
R=s.simplify(records[0][0]/records[0][1]);Ry=s.simplify(records[1][0]/records[1][1])
expected=(2*(r-3)+c*(4-r))/(2*(r-3)-c*(4-r))
assert s.simplify(R-expected)==0;checks+=1
assert Ry==1;checks+=1
assert s.simplify(R-1)!=0;checks+=1
out={'status':'PASS','exact_assertions':checks,'ellipse_axes':[2,1],
'caustic_axes':['2*(sqrt(13)-1)/3','(4-sqrt(13))/3'],
'x_axis_triangle_ratio':str(R),'expected_ratio':str(expected),'y_axis_triangle_ratio':str(Ry),
'qualification':'Two exact 3-periodic triangles in the same confocal family refute the imported phase-constancy addition. This does not refute the actual source ratio-equality assertion.'}
print(json.dumps(out,indent=2))
