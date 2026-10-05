#!/usr/bin/env python3
"""Replay proof certificates using Fraction only; no optimization solver needed."""
from verify_math import data, F, product
from itertools import combinations
import json,pathlib,copy
INDEX=list(product(range(4),repeat=3))

def system(t,c,a,triangle):
 P,Q,p,q,v=data(t,c,a);xy,xz,yz=triangle;A=[];b=[]
 def add(row,rhs): A.append([F(x) for x in row]);b.append(F(rhs))
 for i,j in product(range(4),repeat=2):
  add([int(u==i and w==j) for u,w,z in INDEX],p[i][j][xy])
  add([int(u==i and z==j) for u,w,z in INDEX],p[i][j][xz])
  add([int(w==i and z==j) for u,w,z in INDEX],p[i][j][yz])
 for pos,(i,j,k) in enumerate(INDEX):
  if 0 in (i,j,k):
   value=int((i,j,k) in [(0,xy,xz),(xy,0,yz),(xz,yz,0)])
   add([int(h==pos) for h in range(64)],value)
 for i,j,k in product(range(1,4),repeat=3):
  if q[i][j][k]==0:add([Q[r][i]*Q[s][j]*Q[u][k] for r,s,u in INDEX],0)
 return A,b

def verify(cert):
 t,c,a=cert['t'],cert['c'],cert['a'];tri=cert['triangle'];P,Q,p,q,v=data(t,c,a)
 assert p[tri[1]][tri[2]][tri[0]]>0, 'required base triangle must occur'
 A,b=system(t,c,a,tri);assert len(A)==cert['equation_count']
 y=[F(0)]*len(A)
 for i,z in cert['multipliers']:y[i]=F(z)
 lhs=[sum(y[i]*A[i][j]for i in range(len(A)))for j in range(64)]
 rhs=sum(y[i]*b[i]for i in range(len(A)))
 expected=[F(0)]*64
 for ijk,z in cert['nonnegative_lhs']:expected[INDEX.index(tuple(ijk))]=F(z)
 assert lhs==expected and rhs==F(cert['negative_rhs'])
 assert min(lhs)>=0 and rhs<0
 return {'array':[t*(c+1)+a,t*c,a+1,1,c,t*(c+1)],'triangle':tri,'nonnegative_terms':len(cert['nonnegative_lhs']),'negative_rhs':str(rhs)}

def crown_positive_control(n):
 V=list(product(range(2),range(n)))
 def d(u,v):return 0 if u==v else 2 if u[0]==v[0] else 3 if u[1]==v[1] else 1
 cache={};count=0
 for x,y,z in combinations(V,3):
  tri=(d(x,y),d(x,z),d(y,z))
  if tri not in cache:cache[tri]=system(1,n-2,0,tri)
  A,b=cache[tri];X=[0]*64
  for w in V:X[INDEX.index((d(x,w),d(y,w),d(z,w)))]+=1
  assert all(sum(u*v for u,v in zip(row,X))==rhs for row,rhs in zip(A,b))
  count+=1
 return count

def main():
 root=pathlib.Path(__file__).parent;certs=json.loads((root/'TRIPLE_CERTIFICATES.json').read_text());results=[verify(z)for z in certs]
 bad=copy.deepcopy(certs[0]);bad['negative_rhs']=str(-F(bad['negative_rhs']))
 caught=False
 try:verify(bad)
 except AssertionError:caught=True
 assert caught
 bad=copy.deepcopy(certs[0]);bad['multipliers'][0][1]=str(F(bad['multipliers'][0][1])+1)
 caught2=False
 try:verify(bad)
 except AssertionError:caught2=True
 assert caught2
 out={'exact_rational_certificates':results,'positive_control_crown_base_triples':{str(n):crown_positive_control(n)for n in (3,4)},'negative_controls':{'changed_rhs_rejected':caught,'changed_multiplier_rejected':caught2},'limitation':'Certificates rule out only their listed arrays. Their absence or parameter feasibility does not prove existence.'}
 (root/'TRIPLE_CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
