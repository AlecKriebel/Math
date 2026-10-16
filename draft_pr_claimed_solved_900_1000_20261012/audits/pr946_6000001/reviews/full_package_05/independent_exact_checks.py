"""New finite falsifiable identity checks; not a universal existence proof."""
import json,itertools
from pathlib import Path
import sympy as s
O=Path(__file__).resolve().parent
x,y,u,v=s.symbols('x y u v'); xx=[x,y]; yy=[u,v]; mapping={x:u+u*v,y:v+u*u}; X=s.Matrix([mapping[x],mapping[y]]).jacobian(yy)
g=s.eye(2)+s.Matrix([x,y])*s.Matrix([[x,y]])
C=lambda i,j,k: [1+x,2-y,3+x*y,4+x*x][i+j+k]
L=lambda i,j,k:(s.diff(g[j,k],xx[i])+s.diff(g[i,k],xx[j])-s.diff(g[i,j],xx[k]))/2
Gamma=lambda i,j,k:L(i,j,k)-C(i,j,k)/2
Q=lambda i,j,k:s.diff(g[i,j],xx[k])+Gamma(i,j,k)
gp=X.T*g.subs(mapping)*X
rows=[];tensor_only_fails=0
for a,b,c in itertools.product(range(2),repeat=3):
 gamma=sum(X[i,a]*X[j,b]*X[k,c]*Gamma(i,j,k).subs(mapping) for i,j,k in itertools.product(range(2),repeat=3))+sum(s.diff(mapping[xx[i]],yy[a],yy[b])*X[j,c]*g[i,j].subs(mapping) for i,j in itertools.product(range(2),repeat=2))
 direct=s.diff(gp[a,b],yy[c])+gamma
 tensor=sum(X[i,a]*X[j,b]*X[k,c]*Q(i,j,k).subs(mapping) for i,j,k in itertools.product(range(2),repeat=3))
 chain=tensor+sum(g[i,j].subs(mapping)*(s.diff(mapping[xx[i]],yy[a],yy[b])*X[j,c]+s.diff(mapping[xx[i]],yy[a],yy[c])*X[j,b]+s.diff(mapping[xx[i]],yy[b],yy[c])*X[j,a]) for i,j in itertools.product(range(2),repeat=2))
 assert s.expand(direct-chain)==0
 tensor_only_fails+=int(s.expand(direct-tensor)!=0);rows.append([a,b,c])
assert tensor_only_fails>0
e=[x,y,x*x+y**3,x*y,x**3];features=[s.prod(e[i] for i in indices) for deg in range(4) for indices in itertools.combinations_with_replacement(range(5),deg)]
multi=[(i,j) for deg in range(4) for i in range(deg+1) for j in [deg-i]]
E=s.Matrix([[s.diff(f,x,i,y,j).subs({x:2,y:-1}) for f in features] for i,j in multi]);assert E.shape==(10,56) and E.rank()==10
assert s.Matrix([[s.diff(f,x,i,y,j).subs({x:2,y:-1}) for f in [1,*e]] for i,j in multi]).rank()<10
schur=[]
for k in [1,2,7,23,101]:
 A=s.diag(s.Rational(1,k),k*k);B=s.Matrix([[k,-k*k,2],[1,k,3*k]]);t=s.trace(A.inv())*sum(z*z for z in B);S=2*(1+t)*s.eye(3)-B.T*A.inv()*B
 assert all(S[:j,:j].det()>0 for j in range(1,4));assert all((S-(2+t)*s.eye(3))[:j,:j].det()>=0 for j in range(1,4))
 bad=s.Matrix.vstack(s.Matrix.hstack(A,B),s.Matrix.hstack(B.T,s.zeros(3)));assert bad.det()==0 and (s.Matrix.vstack(-A.inv()*B[:,0],s.Matrix([1,0,0])).T*bad*s.Matrix.vstack(-A.inv()*B[:,0],s.Matrix([1,0,0])))[0]<0
 schur.append({'k':k,'t':str(t),'minimum_principal_minor_positive':True})
psi=(x*x+y*y)/2+x*x*y/2+y**4/12;G=s.hessian(psi,xx);Gi=G.inv();star=[[[sum(Gi[k,l]*s.diff(G[j,l],xx[i]) for l in range(2)) for j in range(2)] for i in range(2)] for k in range(2)]
curvature=[]
for a,b,c,d in itertools.product(range(2),repeat=4):
 r=s.diff(star[a][d][b],xx[c])-s.diff(star[a][c][b],xx[d])+sum(star[a][c][m]*star[m][d][b]-star[a][d][m]*star[m][c][b] for m in range(2));assert s.cancel(r)==0;curvature.append([a,b,c,d])
out={'status':'PASS','new_exact_checks':{'nonlinear_2D_jet_chart_law':len(rows),'tensor_only_negative_rejected':tensor_only_fails,'curved_feature_jet_shape':[10,56],'curved_feature_jet_rank':10,'linear_feature_rank_deficiency_detected':True,'unbounded_schur_family':schur,'zero_normal_correction_indefiniteness_detected':True,'nonconstant_hessian_dual_curvature_components_zero':len(curvature)},'limitation':'Finite algebraic checks supplement the separate universal reconstruction.'}
(O/'INDEPENDENT_EXACT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
