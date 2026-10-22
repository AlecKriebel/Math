"""Independent audit controls of supplied claims; no search for new solutions."""
from itertools import combinations,product
from collections import Counter
import json,sys,platform
from pathlib import Path
import sympy as S
import numpy as np
import scipy
from scipy.spatial import ConvexHull,HalfspaceIntersection
out={}
# Differentiate A(t)x(t)=1 twice directly for all symbolic tangent variables in n=3.
n=3
ps=S.symbols('p0:6');qs=S.symbols('q0:6');idx=[(i,j) for i in range(n) for j in range(n) if i!=j]
P=S.zeros(n);Q=S.zeros(n)
for (i,j),p,q in zip(idx,ps,qs):P[i,j]=p;Q[i,j]=q
coef=0
for ss in product([-1,1],repeat=n):
 D=S.diag(*ss);s=S.Matrix(ss);Aprime=P+D*Q
 Asecond=S.diag(*[-sum(Aprime[i,j]**2 for j in range(n)) for i in range(n)])*D
 dx=-D*Aprime*s;ddx=-D*(Asecond*s+2*Aprime*dx)
 coef+=(dx.dot(dx)+s.dot(ddx))/2**n
coef=S.expand(coef);target=S.expand(2*sum(x*x for x in P)+4*sum(x*x for x in (Q+Q.T)/2))
assert S.expand(coef-target)==0
Hessian=S.hessian(coef,(*ps,*qs))
out['symbolic_hessian_n3']={'variables':12,'coefficient_identity':True,'hessian_eigenvalues':{str(k):v for k,v in Hessian.eigenvals().items()}}
# Independent linear solve (RREF instead of inverse), plus dual hull/halfspace package control.
def enumerate_vertices(U):
 n=U.cols;N=U.rows;verts={};sing=0;infeas=0;feas=0
 for ids in combinations(range(N),n):
  A=U[list(ids),:];aug=A.row_join(S.ones(n,1));reduced,pivots=aug.rref()
  if pivots!=tuple(range(n)):
   sing+=1;continue
  x=reduced[:,-1];vals=U*x
  if any(v>1 for v in vals):infeas+=1;continue
  feas+=1;key=tuple(x);verts[key]={'norm2':str(x.dot(x)),'active':[i for i,v in enumerate(vals) if v==1]}
 F=np.array(U,float);hull=ConvexHull(F);hv=HalfspaceIntersection(np.column_stack((F,-np.ones(N))),np.zeros(n)).intersections
 exact=np.array(list(verts),float)
 assert len(hv)==len(verts)
 err=max(min(np.linalg.norm(v-e) for e in exact) for v in hv)
 assert err<1e-8
 return {'row_subsets':len(list(combinations(range(N),n))),'singular':sing,'infeasible_nonsingular':infeas,'feasible_nonsingular':feas,'distinct_vertices':len(verts),'unit_normals':all(U.row(i).dot(U.row(i))==1 for i in range(N)),'antipodal_pairs':sum(U.row(i)==-U.row(j) for i in range(N) for j in range(i)),'max_norm2':str(max(S.Rational(v['norm2']) for v in verts.values())),'min_norm2':str(min(S.Rational(v['norm2']) for v in verts.values())),'active_count_distribution':dict(Counter(len(v['active']) for v in verts.values())),'dual_triangulated_facets':len(hull.simplices),'independent_halfspace_vertex_count':len(hv),'crosscheck_max_error':float(err),'vertices':[{'x':[str(t) for t in key],**v} for key,v in sorted(verts.items())]}
n=5;Q=S.eye(n)
for data in [[1,-2,1,0,0],[1,1,-1,-1,0],[1,0,1,-1,-1],[2,-1,0,-2,1]]:
 v=S.Matrix(data);Q=Q*(S.eye(n)-2*v*v.T/v.dot(v))
H=S.Rational(61,65)*S.eye(n)+S.Rational(18,325)*S.ones(n)
U=S.eye(n).col_join(-Q)*H
out['turn4_exact_example']=enumerate_vertices(U)
assert out['turn4_exact_example']['distinct_vertices']==34
assert out['turn4_exact_example']['max_norm2']=='340657525/23222761'
out['cube_control_n5']=enumerate_vertices(S.eye(5).col_join(-S.eye(5)))
assert out['cube_control_n5']['distinct_vertices']==32 and out['cube_control_n5']['max_norm2']=='5'
U3=S.eye(3).col_join(-(S.Rational(2,3)*S.ones(3)-S.eye(3)))
out['turn2_and_5_example']=enumerate_vertices(U3)
# Cauchy-Binet identity in an explicitly noncentered unit-row input.
U=S.Matrix([[1,0],[0,1],[S.Rational(-3,5),S.Rational(-4,5)],[S.Rational(5,13),S.Rational(-12,13)]])
G=U.T*U;b=U.T*S.ones(4,1);W=Y=0
for ids in combinations(range(4),2):
 A=U[list(ids),:];det=A.det();assert det!=0
 x=A.LUsolve(S.ones(2,1));W+=det**2;Y+=det**2*x.dot(x)
theory=(G.inv()*b).dot(G.inv()*b)+(4-(b.T*G.inv()*b)[0])*S.trace(G.inv())
assert S.factor(Y/W-theory)==0
out['noncentered_determinant_identity']={'b':[str(t) for t in b],'total_weight':str(W),'mean_norm2':str(Y/W),'identity_passed':True}
# Singular-basis control at square: do not discard Cramer numerators.
U=S.eye(2).col_join(-S.eye(2));weighted_actual=0;cramer_all=0;singular_contribution=0
for ids in combinations(range(4),2):
 A=U[list(ids),:];v=A.adjugate()*S.ones(2,1);term=v.dot(v);cramer_all+=term
 if A.det()!=0:weighted_actual+=term
 else:singular_contribution+=term
assert (weighted_actual,cramer_all,singular_contribution)==(8,16,8)
out['singular_basis_square_control']={'actual_invertible_numerator':str(weighted_actual),'all_cramer_numerator':str(cramer_all),'singular_numerator':str(singular_contribution)}
# Exact stationarity/Markov control on n=3 cross-polytope.
n=3;N=6;U=S.eye(n).col_join(-S.eye(n));AA=S.zeros(N);d=S.zeros(N,1);WW=S.zeros(n)
for ss in product([-1,1],repeat=n):
 alpha=S.zeros(N,1);w=S.Matrix(ss)/S.sqrt(n);lam=S.Rational(1,2**n)
 for i,sign in enumerate(ss):alpha[i if sign==1 else i+n]=S.Rational(1,n)
 AA+=lam*alpha*alpha.T;d+=lam*alpha;WW+=lam*w*w.T
D=S.diag(*d);B=2*n*AA;r2=S.Rational(1,n)
assert AA*U==r2*D*U and AA*S.ones(N,1)==d and U.T*d==S.zeros(n,1)
assert WW==U.T*D*U
out['stationarity_cube_control']={'trace_B':str(S.trace(B)),'eigenvalues':{str(k):v for k,v in B.eigenvals().items()},'stationary_identity':True,'second_moment_identity':True}
# Exact combinatorial enumeration independent hull facets and all vertices present.
n=4;V=[S.zeros(n,1)]+[S.eye(n)[:,i] for i in range(n)]
for i in range(3):V.append(S.Matrix([S.Rational(-1,100) if j==i else S.Rational(1,4) for j in range(n)]))
F=ConvexHull(np.array([list(x) for x in V],float));facets=sorted(tuple(sorted(x.tolist())) for x in F.simplices)
w=[S.Rational(1,5)]*5+[S.Integer(1)]*3
assert len(F.vertices)==8 and len(facets)==14 and max(sum(w[i] for i in f) for f in facets)==S.Rational(8,5)
out['combinatorial_hull_control']={'dimension':4,'vertices':F.vertices.tolist(),'facet_count':len(facets),'facets':facets,'max_mass':'8/5','total_mass':'4'}
out['environment']={'python':sys.version,'sympy':S.__version__,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:({kk:vv for kk,vv in v.items() if kk!='vertices'} if isinstance(v,dict) else v) for k,v in out.items()},indent=2))
