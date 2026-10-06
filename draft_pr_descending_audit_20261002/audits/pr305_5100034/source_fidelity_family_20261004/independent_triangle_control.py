from decimal import Decimal as D, getcontext
import json
getcontext().prec=85
zero=D(0); one=D(1); two=D(2)
a=two;b=one;c=D(3).sqrt();delta=D(13).sqrt()
ac=two*(delta-one)/D(3);bc=(D(4)-delta)/D(3)
y=(one-ac*ac/(a*a)).sqrt();x=a*(one-bc*bc).sqrt()
triangles={'major_phase':[(a,zero),(-ac,y),(-ac,-y)],'minor_phase':[(zero,b),(-x,-bc),(x,-bc)]}
def dot(p,q):return sum(pi*qi for pi,qi in zip(p,q))
def sub(p,q):return tuple(pi-qi for pi,qi in zip(p,q))
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def norm(p):return dot(p,p).sqrt()
def foot(f,p,q):
 v=sub(q,p);lam=dot(sub(f,p),v)/dot(v,v)
 return tuple(pi+lam*vi for pi,vi in zip(p,v))
def area(q):return sum(cross(q[i],q[(i+1)%len(q)]) for i in range(len(q)))/two
def tangentfoot(f,p):
 n=(p[0]/(a*a),p[1]/(b*b));lam=(one-dot(f,n))/dot(n,n)
 return tuple(fi+lam*ni for fi,ni in zip(f,n))
ans={'context_precision':getcontext().prec,'a':str(a),'b':str(b),'ac':str(ac),'bc':str(bc),'foci':[[str(c),'0'],[str(-c),'0']]}
for label,p in triangles.items():
 qplus=[foot((c,zero),p[i],p[(i+1)%3]) for i in range(3)]
 qminus=[foot((-c,zero),p[i],p[(i+1)%3]) for i in range(3)]
 outerplus=[tangentfoot((c,zero),u) for u in p]
 outerminus=[tangentfoot((-c,zero),u) for u in p]
 ap,am,op,om=map(area,[qplus,qminus,outerplus,outerminus])
 ellipse=[];reflections=[];tangencies=[]
 for i,u in enumerate(p):
  ellipse.append(u[0]*u[0]/(a*a)+u[1]*u[1]/(b*b)-one)
  outgoing=sub(p[(i+1)%3],u);previous=sub(p[(i-1)%3],u)
  bisector=tuple(v/norm(outgoing)+w/norm(previous) for v,w in zip(outgoing,previous))
  normal=(u[0]/(a*a),u[1]/(b*b))
  reflections.append(cross(bisector,normal))
  v=outgoing;n=(v[1],-v[0]);h=dot(n,u)
  tangencies.append(h*h-ac*ac*n[0]*n[0]-bc*bc*n[1]*n[1])
 ans[label]={'points':[[str(w) for w in z] for z in p],'signed_areas':dict(zip(['orbit_plus','orbit_minus','outer_plus','outer_minus'],map(str,[ap,am,op,om]))),'orbit_ratio':str(ap/am),'outer_ratio':str(op/om),'ratio_equality_residual':str(ap/am-op/om),'ellipse_residuals':list(map(str,ellipse)),'reflection_bisector_cross_residuals':list(map(str,reflections)),'common_caustic_tangency_residuals':list(map(str,tangencies))}
expected=(two-c)/(two+c)*(delta+two*c)/(delta-two*c)
ans['major_expected_exact_ratio']={'expression':'(2-sqrt(3))/(2+sqrt(3)) * (sqrt(13)+2sqrt(3))/(sqrt(13)-2sqrt(3))','value':str(expected),'residual':str(D(ans['major_phase']['orbit_ratio'])-expected)}
assert all(abs(D(t))<D('1e-75') for k in triangles for lab in ['ellipse_residuals','reflection_bisector_cross_residuals','common_caustic_tangency_residuals'] for t in ans[k][lab])
assert all(abs(D(ans[k]['ratio_equality_residual']))<D('1e-75') for k in triangles)
assert abs(D(ans['major_expected_exact_ratio']['residual']))<D('1e-75')
assert abs(D(ans['major_phase']['orbit_ratio'])-D(ans['minor_phase']['orbit_ratio']))>one
print(json.dumps(ans,indent=2))
