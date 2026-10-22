from fractions import Fraction as F
from itertools import combinations
import json
n=0
def ck(x):
 global n
 assert x;n+=1
P=[(F(0),F(4)),(F(-4),F(-2)),(F(4),F(-2)),(F(0),F(-1)),(F(1),F(1,2)),(F(-1),F(1,2))]
sq=lambda p:sum(x*x for x in p)
sub=lambda x,y:tuple(a-b for a,b in zip(x,y))
faces=[];margins=[];E=set()
for I in combinations(range(6),3):
 u,v,w=[P[i] for i in I];a,b=sub(v,u),sub(w,u);det=a[0]*b[1]-a[1]*b[0]
 if not det:continue
 r,s=(sq(v)-sq(u))/2,(sq(w)-sq(u))/2
 c=((r*b[1]-s*a[1])/det,(a[0]*s-b[0]*r)/det);rad=sq(sub(c,u))
 gaps=[sq(sub(P[j],c))-rad for j in range(6) if j not in I]
 if min(gaps)>0:
  faces.append(I);margins+=gaps;E.update(combinations(I,2));ck(abs(det)>=3);ck(max(map(abs,c))<=F(19,2))
ck(set(faces)=={(0,1,5),(0,2,4),(0,4,5),(1,2,3),(1,3,5),(2,3,4),(3,4,5)})
ck(min(margins)==F(85,14));ck(set(combinations(range(6),2))-E=={(0,3),(1,4),(2,5)})
tri=[I for I in combinations(range(6),3) if all(e in E for e in combinations(I,2))]
ck(len(tri)==8);ck(sum(any(i>=3 for i in I) for I in tri)==7)
h=F(1,10000);ck(F(16,3)/(1-F(16,3)*4*h)<6);ck(11065*h<F(85,14));ck(64*h+8*h*h<1)
# Independent exact all-dimension witness margins for bounded test dimensions.
for d in range(2,10):
 for k in range(2,d+1):
  z=tuple(F(0) for _ in range(d));es=[tuple(F(i==j) for j in range(d)) for i in range(d)];A=[z]+es[:k]
  B=tuple(F(1,k+1) if j<k else F(0) for j in range(d));guards=[tuple(s*2*x for x in es[j]) for j in range(k,d) for s in [-1,1]]
  sites=A+[B]+guards
  for i,j in combinations(range(k+1),2):
   if i==0:c=tuple(F(1,2) if l==j-1 else F(-1) if l<k else F(0) for l in range(d))
   else:c=tuple(F(2) if l in [i-1,j-1] else F(-2) if l<k else F(0) for l in range(d))
   r=sq(sub(c,A[i]));ck(sq(sub(c,A[j]))==r)
   for l,p in enumerate(sites):
    if l not in [i,j]:ck(sq(sub(c,p))-r>=F(5,9))
  h=F(1,1000*d*d);ck(160*d*h<F(5,9));ck(-F(k*k,(k+1)**2)+20*d*h<0)
print(json.dumps({'status':'PASS','independent_exact_assertions':n,'octahedral_faces':len(faces),'octahedral_triangles':len(tri),'tested_dimensions':[2,9]},indent=2))
