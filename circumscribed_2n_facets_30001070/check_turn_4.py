import sympy as S
from itertools import combinations
import json
n=5
Q=S.eye(n)
for data in [[1,-2,1,0,0],[1,1,-1,-1,0],[1,0,1,-1,-1],[2,-1,0,-2,1]]:
 v=S.Matrix(data);Q=Q*(S.eye(n)-2*v*v.T/(v.T*v)[0])
H=S.Rational(61,65)*S.eye(n)+S.Rational(18,325)*S.ones(n)
U=S.eye(n).col_join(-Q)*H
assert Q*Q.T==S.eye(n) and Q*S.ones(n,1)==S.ones(n,1)
assert U.T*S.ones(2*n,1)==S.zeros(n,1)
assert all(sum(a*a for a in U[i,:])==1 for i in range(2*n))
assert len(set(tuple(U[i,:]) for i in range(2*n)))==2*n
verts={}
for F in combinations(range(2*n),n):
 A=U[list(F),:]
 if A.det()==0:continue
 x=A.inv()*S.ones(n,1)
 if all(t<=1 for t in U*x):verts[tuple(x)]=sum(t*t for t in x)
assert verts
lo=min(verts.values());hi=max(verts.values());x=next(x for x,t in verts.items() if t==hi)
assert hi>n
z=S.Rational(3,11)
edge=(n-2)**2/(n*n*z)+4*(n-1)**2/(n*n*(1-z))
outer=(n-1)/(1-z)+(1-n*z)/(n*n*z*(1-z))
assert edge==S.Rational(121,25)<n and outer==S.Rational(407,75)>n
print(json.dumps({'rational_nonsymmetric_example':{'dimension':n,'normal_count':2*n,'normals':[[str(t) for t in U[i,:]] for i in range(2*n)],'centered':True,'unit_normals':True,'frame_isotropic':U.T*U==2*S.eye(n),'vertex_count':len(verts),'minimum_vertex_squared_norm':str(lo),'maximum_vertex_squared_norm':str(hi),'maximum_vertex':list(map(str,x)),'conjecture_counterexample':False},'edge_only_shortcut':{'dimension':n,'height_squared':str(z),'one_flip_squared_norm':str(edge),'two_flip_squared_norm':str(outer),'edge_only_check_insufficient':True},'all_exact_checks_passed':True},indent=2))
