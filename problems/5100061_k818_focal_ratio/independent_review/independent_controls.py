#!/usr/bin/env python3
"""Independent exact geometry controls for k818's denominator exception.
No author code is imported. The all-period theorem is a credited dependency.
"""
import sympy as s
import json
from itertools import combinations
Q=s.Rational
P=[s.Matrix(x) for x in [(2,0),(Q(4,3),s.sqrt(5)/3),(-Q(4,3),s.sqrt(5)/3),(-2,0),(-Q(4,3),-s.sqrt(5)/3),(Q(4,3),-s.sqrt(5)/3)]]
count=0
def zero(v):
 global count
 assert s.simplify(v)==0,v
 count+=1
def positive(v):
 global count
 assert s.simplify(v).is_positive,v
 count+=1
def wedge(p,q):return p[0]*q[1]-p[1]*q[0]
def area(V):
 # Triangulate from the first vertex, allowing signed/crossing polygons.
 return s.simplify(sum(wedge(V[i]-V[0],V[i+1]-V[0]) for i in range(1,len(V)-1))/2)
C=s.diag(Q(32,9),Q(5,9));E=s.diag(4,1)
zero(C[0,0]-C[1,1]-3)
for i in range(2):positive(C[i,i]);positive(E[i,i]-C[i,i])
for p,q in combinations(P,2):positive((p-q).dot(p-q))
for i,p in enumerate(P):
 q=P[(i+1)%6]; prev=P[(i-1)%6];d=q-p
 zero((p.T*E.inv()*p)[0]-1)
 positive(wedge(p,q))
 n=s.Matrix([-d[1],d[0]]);a=n.dot(p)
 zero(a*a-(n.T*C*n)[0])
 contact=s.simplify(C*n/a)
 zero((contact.T*C.inv()*contact)[0]-1)
 zero(n.dot(contact)-a)
 lam=s.simplify((contact-p).dot(d)/d.dot(d))
 positive(lam);positive(1-lam)
 for x in contact-p-lam*d:zero(x)
 incoming=(p-prev)/s.sqrt((p-prev).dot(p-prev));outgoing=d/s.sqrt(d.dot(d))
 normal=E.inv()*p;tangent=s.Matrix([-normal[1],normal[0]])
 zero((incoming-outgoing).dot(tangent));zero((incoming+outgoing).dot(normal))
 positive(incoming.dot(normal));positive(-outgoing.dot(normal))
# Antipedals by homogeneous cross products, without solving author linear systems.
areas=[]
for focus_sign in (-1,1):
 F=s.Matrix([focus_sign*s.sqrt(3),0]);lines=[];inverted=[]
 for p in P:
  v=p-F;norm=v.dot(v);positive(norm)
  lines.append(s.Matrix([v[0],v[1],-v.dot(p)]))
  inverted.append(s.simplify(F+v/norm))
 U=[]
 for i,line in enumerate(lines):
  h=line.cross(lines[(i+1)%6]);positive(h[2]**2)
  u=s.simplify(h[:2,0]/h[2]);U.append(u)
  zero(line.dot(s.Matrix([u[0],u[1],1])))
  zero(lines[(i+1)%6].dot(s.Matrix([u[0],u[1],1])))
 zero(area(P)-20*s.sqrt(5)/9)
 zero(area(inverted)-15*s.sqrt(5)/8)
 zero(area(U))
 positive(area(P));positive(area(inverted))
 zero(area(P)/area(inverted)-Q(32,27))
 zero(area(list(reversed(inverted)))+area(inverted))
 zero(area(list(reversed(U)))+area(U))
 areas.append((area(inverted),area(U)))
for x,y in zip(*areas):zero(x-y)
zero(Q(4)*2**3/((2*2-1)*(2+1)**2)-Q(32,27))
print(json.dumps({'status':'PASS','independent_exact_assertions':count,'period':6,'pairwise_distinct_vertices':True,'caustic_semiaxes_squared':['32/9','5/9'],'caustic_contacts_inside_each_segment':True,'both_original_foci':True,'original_area':'20*sqrt(5)/9','inverse_area':'15*sqrt(5)/8','antipedal_area':'0','original_over_inverse':'32/27','scope':'Exact exceptional orbit, primitivity, tangency, reflection and signed areas; no finite control substitutes for the credited all-period dependencies.'},indent=2))
