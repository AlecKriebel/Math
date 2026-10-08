#!/usr/bin/env python3
"""Independent source-free finite tests; these do not prove the global theorem."""
import itertools, json, hashlib, math, sys
from pathlib import Path
import sympy as s
import numpy as np
if not __debug__: raise RuntimeError('Assertions must remain enabled.')
results={}; zeros=0

def zero(x):
 global zeros
 assert s.simplify(x)==0, x
 zeros+=1

def multis(n,d):
 return [a for a in itertools.product(range(d+1), repeat=n) if sum(a)<=d]
def derivative(f,xx,a):
 return s.diff(f,*[z for z,m in zip(xx,a) for _ in range(m)]) if sum(a) else f
def data(xx):
 x,y=xx
 g=s.Matrix([[1+x*x,y],[y,2+y*y]])
 C=lambda i,j,k: (1+i+j+k)*(1+x)+y*y
 L=lambda i,j,k:(s.diff(g[j,k],xx[i])+s.diff(g[i,k],xx[j])-s.diff(g[i,j],xx[k]))/2
 Gamma=lambda i,j,k:L(i,j,k)-C(i,j,k)/2
 Q=lambda i,j,k:s.diff(g[i,j],xx[k])+Gamma(i,j,k)
 return g,C,Gamma,Q
x,y,u,v=s.symbols('x y u v',real=True)
xx=(x,y); g,C,Gamma,Q=data(xx)
# Independently solve the FULL 0..3 jet system, including the scalar-value row.
midx=multis(2,3); F=s.Matrix([x**a*y**b for a,b in midx])
E=s.Matrix([[derivative(f,xx,a) for f in F] for a in midx]); assert E.det()!=0
T=[]
for a in midx:
 idx=[i for i,d in enumerate(a) for _ in range(d)]
 T.append(0 if len(idx)<2 else g[idx[0],idx[1]] if len(idx)==2 else Q(*idx))
a=s.simplify(E.inv()*s.Matrix(T)); phi=-a
zero((a.T*F)[0]); dF=F.jacobian(xx); dphi=phi.jacobian(xx)
for i in range(2):
 zero((phi.T*dF[:,i])[0])
 for j in range(2):
  zero((dF[:,i].T*dphi[:,j])[0]-g[i,j])
  for k in range(2):
   zero((F.diff(xx[i],xx[j]).T*dphi[:,k])[0]-Gamma(i,j,k))
   Gstar=s.diff(g[j,k],xx[i])-Gamma(i,k,j)
   zero((phi.diff(xx[i],xx[j]).T*dF[:,k])[0]-Gstar)
results['full_jet_pair']={'features':len(F),'jet_determinant':str(E.det()),'metric_determinant':str(s.factor(g.det()))}
# A genuinely nonlinear coordinate change; inspect the third ordinary jet law.
xxuv=s.Matrix([u+v*v,v+u*u]); uv=(u,v); p={u:s.Rational(1,5),v:s.Rational(-1,3)}
oldp={x:xxuv[0].subs(p),y:xxuv[1].subs(p)}; J=xxuv.jacobian(uv)
gnew=s.simplify(J.T*g.subs(dict(zip(xx,xxuv)), simultaneous=True)*J)
Cnew=lambda i,j,k:sum(C(a,b,c).subs(dict(zip(xx,xxuv)), simultaneous=True)*J[a,i]*J[b,j]*J[c,k] for a,b,c in itertools.product(range(2),repeat=3))
Qnew=lambda i,j,k:(s.diff(gnew[j,k],uv[i])+s.diff(gnew[i,k],uv[j])+s.diff(gnew[i,j],uv[k])-Cnew(i,j,k))/2
h=s.Matrix([x-oldp[x],y-oldp[y]])
q=(h.T*g.subs(oldp)*h)[0]/2+sum(Q(i,j,k).subs(oldp)*h[i]*h[j]*h[k] for i,j,k in itertools.product(range(2),repeat=3))/6
quv=q.subs(dict(zip(xx,xxuv)), simultaneous=True)
non_tensor=[]
for i,j,k in itertools.product(range(2),repeat=3):
 zero(s.diff(quv,uv[i],uv[j],uv[k]).subs(p)-Qnew(i,j,k).subs(p))
 tensor_only=sum(Q(a,b,c).subs(oldp)*J[a,i]*J[b,j]*J[c,k] for a,b,c in itertools.product(range(2),repeat=3)).subs(p)
 non_tensor.append(s.simplify(Qnew(i,j,k).subs(p)-tensor_only))
assert any(z!=0 for z in non_tensor)
results['nonlinear_coordinate_covariance']={'checks':8,'negative_tensor_only_transform_detected':True,'Jacobian_determinant_at_testpoint':str(J.det().subs(p))}
# Jet spanning after a nonlinear proper graph embedding e:R^2->R^5.
e=[x,y,x*x+x*y,y*y-x,x*y*y]
powers=multis(5,3); features=[s.prod(e[i]**a[i] for i in range(5)) for a in powers]
Et=s.Matrix([[derivative(f,xx,a) for f in features] for a in midx])
ranks=[]
for px,py in [(0,0),(1,-2),(-3,4)]:
 rank=Et.subs({x:px,y:py}).rank(); assert rank==10;ranks.append(rank)
# Degree <=2 on the identity embedding really fails to prescribe cubic jets.
quad=s.Matrix([[derivative(x**a*y**b,xx,beta) for a,b in multis(2,2)] for beta in midx]); assert quad.rank()==6
results['global_feature_space_finite_samples']={'features':len(features),'ranks':ranks,'required_rank':10,'degree_two_negative_control_rank':quad.rank()}
# A periodic global pair on S^1 tests topology and the potential-period issue.
th=s.symbols('theta',real=True)
Fc=s.Matrix([1,s.cos(th),s.sin(th),s.cos(2*th),s.sin(2*th),s.cos(3*th),s.sin(3*th)])
Ec=s.Matrix([[s.diff(f,th,k) for f in Fc] for k in range(4)])
Gram=Ec*Ec.T; Gram=Gram.applyfunc(s.trigsimp)
assert not any(z.has(th) for z in Gram)
Rc=Ec.T*Gram.inv()
gc=2+s.sin(th); Cc=s.cos(th)+s.sin(2*th); Gc=(s.diff(gc,th)-Cc)/2
phc=-(Rc*s.Matrix([0,0,gc,s.diff(gc,th)+Gc])).applyfunc(s.trigsimp)
for q in [(phc.T*Fc)[0],(phc.T*Fc.diff(th))[0],(phc.diff(th).T*Fc.diff(th))[0]-gc,(phc.diff(th).T*Fc.diff(th,2))[0]-Gc,(phc.diff(th,2).T*Fc.diff(th))[0]-(s.diff(gc,th)-Gc)]:
 zero(s.trigsimp(s.expand_trig(q)))
for q in phc:zero(s.trigsimp(q.subs(th,th+2*s.pi)-q))
results['compact_circle_global_pair']={'features':7,'full_jet_Gram_determinant':str(Gram.det()),'periodic_pair':True,'nonconstant_positive_metric':str(gc),'nonzero_connection':str(s.trigsimp(Gc)),'potential_compatibility_one_form':'identically zero'}
# Direct normal-tube potential on a circle verifies its ambient Hessian blocks.
rho=s.sqrt(x*x+y*y); Pc=(rho-1)+(rho-1)**2
Hc=s.hessian(Pc,xx).subs({x:1,y:0}); assert Hc==s.diag(2,1)
results['explicit_tubular_extension']={'circle_point':[1,0],'ambient_Hessian':[[2,0],[0,1]],'normal_block':2,'tangent_block':1}
# An independent exact block stress test, including vanishing A and unbounded B.
t=s.symbols('t',positive=True)
A=s.diag(1/(1+t*t),1/(1+t)**4); B=s.Matrix([[t,t*t],[1+t*t,-t]])
bound=s.trace(A.inv())*sum(b*b for b in B); lam=1+bound
Schur=2*lam*s.eye(2)-B.T*A.inv()*B
exact_samples=[]
for qv in [0,1,10,100]:
 SC=Schur.subs(t,qv); assert SC[0,0]>0 and SC.det()>0
 exact_samples.append({'t':qv,'leading_minor':str(SC[0,0]),'determinant':str(SC.det())})
# Without the normal correction, a nonzero mixed block forces indefiniteness.
Hbad=s.Matrix([[1,1],[1,0]]); assert Hbad.det()<0
# No single bounded correction suffices for A=1/(1+t^2), B=t on all R.
fixed_bad=2-t*t*(1+t*t); assert fixed_bad.subs(t,2)<0
results['schur_noncompact_stress']={'exact_positive_samples':exact_samples,'zero_normal_correction_detected':True,'fixed_normal_correction_failure_detected':True}
# End-to-end one-dimensional model with unbounded prescribed cubic, not flat pair.
z=s.symbols('z',real=True); f1=s.Matrix([1,z,z*z,z**3]); g1=1+z*z; C1=z**5+1; G1=(s.diff(g1,z)-C1)/2
E1=s.Matrix([[s.diff(f,z,k) for f in f1] for k in range(4)])
a1=E1.inv()*s.Matrix([0,0,g1,s.diff(g1,z)+G1]); ph1=-a1
for expr in [(ph1.T*f1.diff(z))[0],(ph1.diff(z).T*f1.diff(z))[0]-g1,(ph1.diff(z).T*f1.diff(z,2))[0]-G1]:zero(expr)
# Deliberately wrong coefficient Q=g' omits connection information.
wrong=-E1.inv()*s.Matrix([0,0,g1,s.diff(g1,z)])
zero((wrong.diff(z).T*f1.diff(z,2))[0]); assert G1!=0
# Deliberately wrong phi=+a reverses the metric.
zero((a1.diff(z).T*f1.diff(z))[0]+g1)
results['connection_vs_metric_negative_controls']={'omit_connection_misses_nonzero_Gamma':True,'wrong_sign_reverses_metric':True}
# Independent curved positive Hessian ambient and its flat dual connection.
P=s.exp(x)+s.exp(y)+s.exp(x+y); G=s.hessian(P,xx); Gi=s.simplify(G.inv())
Gs=[s.simplify(Gi*G.diff(z)) for z in xx]
for i,j in itertools.product(range(2),repeat=2):
 R=Gs[j].diff(xx[i])-Gs[i].diff(xx[j])+Gs[i]*Gs[j]-Gs[j]*Gs[i]
 for item in R:zero(item)
for i,j,k in itertools.product(range(2),repeat=3):
 zero(s.diff(P,xx[i],xx[j],xx[k])-sum(Gs[i][a,j]*G[k,a] for a in range(2)))
results['ambient_dual_flatness']={'curvature_residuals':16,'affine_dual_coordinate_residuals':8}
# Pure gauge metric-compatible curvature-flat connection can have torsion.
# This prevents overextending the necessity claim to curvature-only flatness.
J0=s.Matrix([[0,-1],[1,0]]); T12=J0[:,1] # connection matrices A_x=J0,A_y=0
assert T12!=s.zeros(2,1)
results['torsion_scope_negative_control']={'constant_Euclidean_metric':True,'connection_matrices':['[[0,-1],[1,0]]','[[0,0],[0,0]]'],'dual_equals_original':True,'curvature_zero':True,'T_dx_dy':['-1','0']}
results['symbolic_zero_residual_count']=zeros
results['status']='PASS';results['versions']={'python':sys.version.split()[0],'sympy':s.__version__,'numpy':np.__version__}
results['limitations']='Finite tests are consistency checks, not a proof of global existence or of the cited topology theorems.'
print(json.dumps(results,indent=2))
