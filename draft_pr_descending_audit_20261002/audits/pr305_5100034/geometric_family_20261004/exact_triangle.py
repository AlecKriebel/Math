"""Independent exact Euclidean control in Q(sqrt(2),sqrt(3),sqrt(5)). No third-party packages."""
from fractions import Fraction as F
import json
from pathlib import Path
class K:
 def __init__(self,x=0):
  if isinstance(x,K):self.c=x.c.copy()
  elif isinstance(x,dict):self.c={i:F(v) for i,v in x.items() if v}
  else:self.c={0:F(x)} if x else {}
 def __add__(self,x):
  x=K(x);d=self.c.copy()
  for i,v in x.c.items():d[i]=d.get(i,F(0))+v
  return K(d)
 __radd__=__add__
 def __neg__(self):return K({i:-v for i,v in self.c.items()})
 def __sub__(self,x):return self+-K(x)
 def __rsub__(self,x):return K(x)+-self
 def __mul__(self,x):
  x=K(x);d={}
  for i,u in self.c.items():
   for j,v in x.c.items():
    z=u*v
    for bit,n in enumerate([2,3,5]):
     if (i&j)&(1<<bit):z*=n
    m=i^j;d[m]=d.get(m,F(0))+z
  return K(d)
 __rmul__=__mul__
 def inv(self):
  if not self.c:raise ZeroDivisionError()
  mat=[[F(0) for j in range(9)] for i in range(8)]
  for j in range(8):
   col=self*K({j:1})
   for i,v in col.c.items():mat[i][j]=v
  mat[0][8]=1
  for j in range(8):
   k=next(i for i in range(j,8) if mat[i][j]);mat[j],mat[k]=mat[k],mat[j]
   piv=mat[j][j];mat[j]=[v/piv for v in mat[j]]
   for i in range(8):
    if i!=j:
     piv=mat[i][j];mat[i]=[v-piv*w for v,w in zip(mat[i],mat[j])]
  return K({i:mat[i][8] for i in range(8)})
 def __truediv__(self,x):return self*K(x).inv()
 def __rtruediv__(self,x):return K(x)*self.inv()
 def __eq__(self,x):return self.c==K(x).c
 def __float__(self):return sum(float(v)*(2**.5 if i&1 else 1)*(3**.5 if i&2 else 1)*(5**.5 if i&4 else 1) for i,v in self.c.items())+0.0
 def __repr__(self):return ' + '.join(str(v)+(('*sqrt('+str((2 if i&1 else 1)*(3 if i&2 else 1)*(5 if i&4 else 1))+')') if i else '') for i,v in sorted(self.c.items())) or '0'
 def data(self):return {'exact':str(self),'float':float(self)}
s2,s3,s5=K({1:1}),K({2:1}),K({4:1})
def add(p,q):return tuple(x+y for x,y in zip(p,q))
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def scale(k,p):return tuple(k*x for x in p)
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def area(poly):return sum(cross(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))/2
def projection(f,p,q):
 d=sub(q,p);return add(p,scale(dot(sub(f,p),d)/dot(d,d),d))
def foot_line(f,n,h):return add(f,scale((h-dot(n,f))/dot(n,n),n))
def intersect(n,h,m,k):
 den=cross(n,m)
 return ((h*m[1]-n[1]*k)/den,(n[0]*k-h*m[0])/den)
def serpoly(poly):return [[x.data() for x in p] for p in poly]
A,B=K(8),K(3);c=s5
P=[(2*s2,K(0)),(-F(8,5)*s2,F(3,5)*s3),(-F(8,5)*s2,-F(3,5)*s3)]
lam=K(F(72,25));ac2=A-lam;bc2=B-lam
Ns=[(p[0]/A,p[1]/B) for p in P]
T=[intersect(Ns[i],K(1),Ns[(i+1)%3],K(1)) for i in range(3)]
# Exact validation, including original sides and outer side indexing.
assert ac2-bc2==5 and float(lam)>0 and float(bc2)>0
for i in range(3):
 p,q=P[i],P[(i+1)%3]
 assert p[0]*p[0]/A+p[1]*p[1]/B==1
 d=sub(q,p);n=(-d[1],d[0]);h=dot(n,p)
 assert h*h==ac2*n[0]*n[0]+bc2*n[1]*n[1]
 # Every original side length is exactly 3sqrt(3) or 6sqrt(3)/5.
 length=3*s3 if i in [0,2] else F(6,5)*s3
 vin=scale(1/length,d)
 j=(i+1)%3; dout=sub(P[(j+1)%3],P[j]);outlen=3*s3 if j in [0,2] else F(6,5)*s3
 vout=scale(1/outlen,dout)
 reflected=sub(vin,scale(2*dot(vin,Ns[j])/dot(Ns[j],Ns[j]),Ns[j]))
 assert reflected==vout and dot(vin,vin)==1 and dot(vout,vout)==1
 assert dot(Ns[i],T[(i-1)%3])==1 and dot(Ns[i],T[i])==1
areas={};feet={};anti={}
for label,f in [('+',(s5,K(0))),('-',(-s5,K(0)))]:
 q=[projection(f,P[i],P[(i+1)%3]) for i in range(3)]
 qp=[foot_line(f,n,K(1)) for n in Ns]
 for i in range(3):
  assert dot(sub(q[i],f),sub(P[(i+1)%3],P[i]))==0
  assert dot(sub(qp[i],f),(-Ns[i][1],Ns[i][0]))==0
  assert dot(Ns[i],qp[i])==1
  assert dot(q[i],q[i])==ac2 and dot(qp[i],qp[i])==A
 # Direct outer-polygon projection reproduces qp with its cyclic shift.
 assert [projection(f,T[(i-1)%3],T[i]) for i in range(3)]==qp
 normals=[sub(p,f) for p in P];supports=[dot(normals[i],P[i]) for i in range(3)]
 antip=[intersect(normals[i],supports[i],normals[(i+1)%3],supports[(i+1)%3]) for i in range(3)]
 for i in range(3):
  assert dot(normals[i],antip[i])==supports[i]
  assert dot(normals[i],antip[(i-1)%3])==supports[i]
 feet[label]={'chord':serpoly(q),'outer':serpoly(qp)};anti[label]={'polygon':serpoly(antip),'area':area(antip).data()}
 areas['A'+label]=area(q);areas['Aprime'+label]=area(qp)
assert all(v!=0 for v in areas.values())
D=areas['A+']*areas['Aprime-']-areas['A-']*areas['Aprime+']
R=areas['A+']*areas['Aprime+']-areas['A-']*areas['Aprime-']
result={'status':'Exact rational multiquadratic arithmetic; all assertions passed','ellipse_squared_axes':[8,3],'caustic_squared_axes':[str(ac2),str(bc2)],'vertices':serpoly(P),'outer_vertices':serpoly(T),'signed_areas':{k:v.data() for k,v in areas.items()},'printed_target_cross_difference':D.data(),'reciprocal_correction_cross_difference':R.data(),'printed_target_ratios':{'original':(areas['A+']/areas['A-']).data(),'outer':(areas['Aprime+']/areas['Aprime-']).data()},'focal_feet':feet,'antipedal_controls':anti}
assert all(v!=0 for v in areas.values())
print(json.dumps(result,indent=2))
Path(__file__).with_name('exact_triangle_results.json').write_text(json.dumps(result,indent=2)+'\n')
