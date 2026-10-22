import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use nonoptimized -I')
import sympy as s,json,pathlib,datetime,itertools
O=pathlib.Path(__file__).resolve().parent
checks=[]
def need(c,m):
 if not c:raise RuntimeError(m)
def zero(x):return s.cancel(s.expand(x))==0
# New nonconstant metric/cubic and a proper cubic curve; exact global polynomial coefficient field.
t=s.symbols('t',real=True);f=s.Matrix([t,t*t/2,t**3/6,1]);g=2+t*t;C=1+t;Gamma=(s.diff(g,t)-C)/2;Q=s.diff(g,t)+Gamma
E=s.Matrix.vstack(f.T,f.diff(t).T,f.diff(t,2).T,f.diff(t,3).T);a=E.inv()*s.Matrix([0,0,g,Q]);phi=-a
need(zero((f.diff(t).T*phi.diff(t))[0]-g),'metric sign');need(zero((f.diff(t,2).T*phi.diff(t))[0]-Gamma),'connection');need(zero((phi.T*f.diff(t))[0]),'zeroform');need(not zero((f.diff(t).T*(-phi).diff(t))[0]-g),'sign sensitivity')
checks.append({'case':'variable_metric_cubic_exact_curve_pair','rank':E.rank(),'determinant':str(E.det()),'all_jet_metric_connection_zeroform_identities':True,'flipped_phi_detected':True})
z=s.symbols('z0:4',real=True);q=s.Matrix([z[1]-z[0]**2/2,z[2]-z[0]**3/6,z[3]-1]);ps0=sum(phi[i].subs(t,z[0])*s.Matrix([0,q[0],q[1],q[2]])[i] for i in range(4));H0=s.hessian(ps0,z);sub=dict(zip(z,f));V=s.Matrix.hstack(f.diff(t),s.eye(4)[:,1],s.eye(4)[:,2],s.eye(4)[:,3]);B=(V.T*H0.subs(sub)*V)[0,1:];lam=1+(B*B.T)[0]/g
ps=ps0+lam.subs(t,z[0])*sum(x*x for x in q);H=s.hessian(ps,z).subs(sub);G=V.T*H*V
need(all(zero(G[0,i]-(g if i==0 else B[i-1])) for i in range(4)),'preserved tangent column');need(all(zero(G[i,j]-(2*lam if i==j else 0)) for i in range(1,4) for j in range(1,4)),'normal block')
for tv in [-100,-3,s.Rational(2,7),20]:
 M=G.subs(t,tv);need(all(M[:i,:i].det()>0 for i in range(1,5)),'exact Schur positivity')
checks.append({'case':'nonorthogonal_graph_extension_variable_penalty','symbolic_preserved_tangent_columns':True,'normal_block_twice_lambda':True,'rational_sylvester_points':['-100','-3','2/7','20'],'without_penalty_degenerate_or_indefinite':H0.subs(sub).det()==0 or H0.subs(sub).subs(t,0).det()<0})
# New 2D nonlinear change of chart; all eight third-jet components and inhomogeneous terms.
x,y,u,v=s.symbols('x y u v');xx=[x,y];yy=[u,v];X=[u+v*v,v+u*u];J=s.Matrix(X).jacobian(yy);gg=s.Matrix([[2+x*x,x*y],[x*y,3+y*y]])
def cv(i,j,k):return [1+x,2+y,3+x*y,4+x-y][i+j+k]
def qq(i,j,k):return (s.diff(gg[j,k],xx[i])+s.diff(gg[i,k],xx[j])+s.diff(gg[i,j],xx[k])-cv(i,j,k))/2
def gam(i,j,k):return qq(i,j,k)-s.diff(gg[i,j],xx[k])
xy={x:X[0],y:X[1]};gp=J.T*gg.subs(xy,simultaneous=True)*J;count=0;tensor_wrong=[]
for a0,b0,c0 in itertools.product(range(2),repeat=3):
 cubic=sum(J[i,a0]*J[j,b0]*J[k,c0]*cv(i,j,k).subs(xy,simultaneous=True) for i,j,k in itertools.product(range(2),repeat=3))
 target=(s.diff(gp[b0,c0],yy[a0])+s.diff(gp[a0,c0],yy[b0])+s.diff(gp[a0,b0],yy[c0])-cubic)/2
 tensor=sum(J[i,a0]*J[j,b0]*J[k,c0]*qq(i,j,k).subs(xy,simultaneous=True) for i,j,k in itertools.product(range(2),repeat=3))
 inh=sum(gg[i,j].subs(xy,simultaneous=True)*(s.diff(X[i],yy[a0],yy[b0])*J[j,c0]+s.diff(X[i],yy[a0],yy[c0])*J[j,b0]+s.diff(X[i],yy[b0],yy[c0])*J[j,a0]) for i,j in itertools.product(range(2),repeat=2))
 need(zero(target-tensor-inh),'nonlinear coordinate law');count+=1;tensor_wrong.append(not zero(target-tensor))
need(any(tensor_wrong),'Q incorrectly tensor sensitivity')
checks.append({'case':'2D_polynomial_metric_cubic_nonlinear_chart','components':count,'all_exact_chain_laws':True,'pretending_Q_tensor_detected':True,'jacobian_determinant':str(J.det())})
# Finite-simplex predecessor implication with exact Fisher/Hessian/cubic sign.
p0,p1=s.symbols('p0 p1',positive=True);probs=[p0,p1,1-p0-p1];coords=[p0,p1];Psi=sum(p*s.log(p) for p in probs);metric=s.hessian(Psi,coords)
for i,j,k in itertools.product(range(2),repeat=3):
 fisher=sum(s.diff(p,coords[i])*s.diff(p,coords[j])/p for p in probs)
 AC=sum(s.diff(p,coords[i])*s.diff(p,coords[j])*s.diff(p,coords[k])/p**2 for p in probs)
 need(zero(metric[i,j]-fisher),'simplex Fisher');need(zero(s.diff(metric[i,j],coords[k])+AC),'simplex cubic sign')
checks.append({'case':'finite_simplex_stronger_predecessor_implication','fisher_is_Hessian':True,'derivative_cubic_minus_Amari_Chentsov':True,'sign_must_be_chosen_for_ordered_pair':True})
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'sympy':s.__version__,'limitation':'New exact finite identities and sensitivity tests, not the universal existence proof or a priority certificate.'};(O/'INDEPENDENT_FINITE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
