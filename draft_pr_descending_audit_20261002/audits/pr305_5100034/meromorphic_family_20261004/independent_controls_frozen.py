from fractions import Fraction as F
import json

def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def area(q):return sum((cross(q[i],q[(i+1)%len(q)]) for i in range(len(q))),F(0))/2
def foot(u,v,f):
 d=(v[0]-u[0],v[1]-u[1]);den=d[0]*d[0]+d[1]*d[1]
 if not den:raise ValueError('zero-length side')
 t=((f[0]-u[0])*d[0]+(f[1]-u[1])*d[1])/den
 return(u[0]+t*d[0],u[1]+t*d[1])
def pedals(p,f):return [foot(p[i],p[(i+1)%len(p)],f) for i in range(len(p))]
P=[(F(5),F(0)),(F(0),F(3)),(F(-5),F(0)),(F(0),F(-3))]
# Outer polygon vertices are consecutive intersections of tangent lines at P.
O=[(F(5),F(3)),(F(-5),F(3)),(F(-5),F(-3)),(F(5),F(-3))]
res=[]
for scale in [F(1),F(2),F(1,3)]:
 for reverse in [False,True]:
  for repeats in [1,2,3]:
   pp=[(scale*x,scale*y) for x,y in P];oo=[(scale*x,scale*y) for x,y in O]
   if reverse:pp=list(reversed(pp));oo=list(reversed(oo))
   pp*=repeats;oo*=repeats
   aps=[area(pedals(poly,(sign*4*scale,F(0)))) for poly in [pp,oo] for sign in [1,-1]]
   determinant=aps[0]*aps[3]-aps[1]*aps[2]
   assert determinant==0
   res.append({'scale':str(scale),'reverse':reverse,'repeats':repeats,'areas':list(map(str,aps)),'determinant':str(determinant)})
print(json.dumps(res,indent=2))
