"""New independent finite sensitivity checks. They do not prove the universal theorem."""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B')
import sympy as s,json,itertools
from pathlib import Path
from datetime import datetime,timezone
x,y,u,v=s.symbols('x y u v');xx=[x,y];yy=[u,v];z=s.Matrix([u+v**2,v+u**2]);X=z.jacobian(yy);pt={u:0,v:0};sub=dict(zip(xx,z));g=s.Matrix([[2+x+x*x,y*x],[x*y,3+y*y+y]])
C=lambda i,j,k:s.Integer([2,-1,3,4][i+j+k])
Gamma=lambda i,j,k:(s.diff(g[j,k],xx[i])+s.diff(g[i,k],xx[j])-s.diff(g[i,j],xx[k])-C(i,j,k))/2
Q=lambda i,j,k:s.diff(g[i,j],xx[k])+Gamma(i,j,k)
gp=X.T*g.subs(sub,simultaneous=True)*X
q=sum(g[i,j].subs({x:0,y:0})*xx[i]*xx[j]/2 for i,j in itertools.product(range(2),repeat=2))+sum(Q(i,j,k).subs({x:0,y:0})*xx[i]*xx[j]*xx[k]/6 for i,j,k in itertools.product(range(2),repeat=3))
qp=q.subs(sub,simultaneous=True);chart=[]
for a,b,c in itertools.product(range(2),repeat=3):
 connection=sum(X[i,a]*X[j,b]*X[k,c]*Gamma(i,j,k).subs(sub,simultaneous=True) for i,j,k in itertools.product(range(2),repeat=3))+sum(g[i,j].subs(sub,simultaneous=True)*s.diff(z[i],yy[a],yy[b])*X[j,c] for i,j in itertools.product(range(2),repeat=2))
 actual=(s.diff(gp[a,b],yy[c])+connection).subs(pt);scalar=s.diff(qp,yy[a],yy[b],yy[c]).subs(pt);assert s.simplify(actual-scalar)==0
 tensor=sum(X[i,a]*X[j,b]*X[k,c]*Q(i,j,k).subs(sub,simultaneous=True) for i,j,k in itertools.product(range(2),repeat=3)).subs(pt)
 chart.append({'indices':[a,b,c],'third_jet':str(actual),'tensor_only_wrong':s.simplify(actual-tensor)!=0})
assert any(r['tensor_only_wrong'] for r in chart)
f=s.Matrix([1,x,x*x/2,x*x*x/6]);metric=1+x*x;gam=-s.Rational(3,2);qq=s.diff(metric,x)+gam
a=s.Matrix([metric*x*x/2-qq*x*x*x/6,-metric*x+qq*x*x/2,metric-qq*x,qq]);phi=-a
identities={'value':a.dot(f),'first':a.dot(f.diff(x)),'second':a.dot(f.diff(x,2))-metric,'third':a.dot(f.diff(x,3))-qq,'metric':f.diff(x).dot(phi.diff(x))-metric,'ordered_connection':f.diff(x,2).dot(phi.diff(x))-gam}
assert all(s.simplify(q)==0 for q in identities.values());assert s.simplify(f.diff(x).dot(a.diff(x))-metric)!=0
# Curved embedding's full scalar jet rank at a nonzero point.
e=[x,y,x*x+y*y,x*y,x*x*x+y];features=[s.prod(e[i]**p[i] for i in range(5)) for p in itertools.product(range(4),repeat=5) if sum(p)<=3];ders=[(i,j) for i in range(4) for j in range(4-i)];mat=s.Matrix([[s.diff(f,x,i,y,j).subs({x:1,y:-1}) for f in features] for i,j in ders]);assert mat.rank()==10
reduced=s.Matrix([[s.diff(f,x,i,y,j).subs({x:1,y:-1}) for f in [s.Integer(1),*e]] for i,j in ders]);assert reduced.rank()<10
blocks=[]
for k in [1,2,7,100,10000]:
 A=s.diag(s.Rational(1,k*k),1+k*k);B=s.Matrix([[k,-k*k,1],[1,2*k,3]]);t=s.trace(A.inv())*sum(x*x for x in B);S=2*(1+t)*s.eye(3)-B.T*A.inv()*B;assert all(det>0 for det in [S[:i,:i].det() for i in [1,2,3]]);bad=(A.row_join(B)).col_join(B.T.row_join(s.zeros(3)));assert bad.det()==0;assert (B.T*A.inv()*B)[0,0]>0
 blocks.append({'k':k,'schur_positive_exact':True,'without_correction_negative_direction':True,'t':str(t)})
Psi=(x*x+y*y)/2+x**4+y**4+x*x*y*y;G=s.hessian(Psi,[x,y]);Ai=[G.inv()*G.diff(z) for z in [x,y]];curv=s.simplify(Ai[1].diff(x)-Ai[0].diff(y)+Ai[0]*Ai[1]-Ai[1]*Ai[0]);assert curv==s.zeros(2)
logjet=s.symbols('t',positive=True);z=s.symbols('z');ql=logjet**3*(s.log(z)-s.log(logjet))**3/6;assert s.simplify(s.diff(ql,z,3).subs(z,logjet))==1
out={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'nonlinear_chart_entries':chart,'coefficient_pair_six_identities':{k:str(s.simplify(v)) for k,v in identities.items()},'wrong_phi_sign_detected':True,'curved_feature_dimensions':list(mat.shape),'curved_feature_rank':mat.rank(),'reduced_rank_negative':reduced.rank(),'unbounded_exact_schur_checks':blocks,'dual_curvature_matrix':str(curv),'unbounded_log_jet_unit_third_derivative':True,'universal_proof_supplied_separately':True}
Path(__file__).with_name('INDEPENDENT_EXACT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','chart':8,'pair_identities':6,'jet_rank':10,'schur':5,'curvature_entries':4}))
