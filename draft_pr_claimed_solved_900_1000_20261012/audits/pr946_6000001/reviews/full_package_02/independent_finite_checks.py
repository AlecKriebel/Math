import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use nonoptimized -I')
import datetime,itertools,json
from pathlib import Path
import sympy as s
O=Path(__file__).absolute().parent
def need(x,m):
 if not x:raise RuntimeError(m)
def zero(x):need(s.expand(x)==0,'nonzero polynomial '+str(x))
t=s.symbols('t');f=s.Matrix([1,t,t*t,t**3]);g=2+t*t;C=3-2*t+t**4;gam=(s.diff(g,t)-C)/2;Q=s.diff(g,t)+gam
E=s.Matrix.vstack(*[f.diff(t,k).T for k in range(4)]);a=E.inv()*s.Matrix([0,0,g,Q]);phi=-a
for value in [a.dot(f),a.dot(f.diff(t)),a.dot(f.diff(t,2))-g,a.dot(f.diff(t,3))-Q,f.diff(t).dot(phi.diff(t))-g,f.diff(t,2).dot(phi.diff(t))-gam,f.diff(t).dot(phi.diff(t,2))-(s.diff(g,t)+C)/2]:zero(value)
need(s.expand(f.diff(t).dot(a.diff(t))-g)!=0,'wrong sign insensitive');wrong=-E.inv()*s.Matrix([0,0,g,s.diff(g,t)]);zero(wrong.diff(t).dot(f.diff(t,2)));need(gam!=0,'omitted connection insensitive')
x,y,u,v=s.symbols('x y u v');xx=[x,y];uv=[u,v];h=s.Matrix([2*u+u*u+v**3,u+v+u*v]);J=h.jacobian(uv);at={x:0,y:0};base={u:0,v:0};metric=s.Matrix([[3+x+x*x,x*y],[x*y,2+y+y*y]]);cc=lambda i,j,k:s.Integer(2+sum([i,j,k]))+x+y
qq=lambda i,j,k:(s.diff(metric[j,k],xx[i])+s.diff(metric[i,k],xx[j])+s.diff(metric[i,j],xx[k])-cc(i,j,k))/2
q=sum(metric[i,j].subs(at)*xx[i]*xx[j]/2 for i,j in itertools.product(range(2),repeat=2))+sum(qq(i,j,k).subs(at)*xx[i]*xx[j]*xx[k]/6 for i,j,k in itertools.product(range(2),repeat=3));sub=dict(zip(xx,h));qy=q.subs(sub,simultaneous=True);gy=J.T*metric.subs(sub,simultaneous=True)*J;entries=0;non_tensor=0
for i,j,k in itertools.product(range(2),repeat=3):
 newc=sum(cc(a,b,c).subs(sub,simultaneous=True)*J[a,i]*J[b,j]*J[c,k] for a,b,c in itertools.product(range(2),repeat=3));wanted=(s.diff(gy[j,k],uv[i])+s.diff(gy[i,k],uv[j])+s.diff(gy[i,j],uv[k])-newc)/2;actual=s.diff(qy,uv[i],uv[j],uv[k]).subs(base);zero(actual-wanted.subs(base));entries+=1
 tensoronly=sum(qq(a,b,c).subs(at)*J[a,i]*J[b,j]*J[c,k] for a,b,c in itertools.product(range(2),repeat=3)).subs(base);non_tensor+=int(actual!=tensoronly)
need(non_tensor>0,'missing inhomogeneous terms insensitive')
rows=[]
for n in [1,2,3]:
 for k in [1,11,1000]:
  A=s.diag(*[s.Rational(1,k**(2*(i+1))) for i in range(n)]);B=s.Matrix(n,3,lambda i,j:s.Rational((-1)**(i+j)*k**(j+1),i+1));tau=s.trace(A.inv())*sum(b*b for b in B);lam=1+tau;H=A.row_join(B).col_join(B.T.row_join(2*lam*s.eye(3)));S=2*lam*s.eye(3)-B.T*A.inv()*B;L=S-(2+tau)*s.eye(3)
  need(all(H[:j,:j].det()>0 for j in range(1,n+4)),'H not positive')
  need(all(L.extract(I,I).det()>=0 for j in range(1,4) for I in itertools.combinations(range(3),j)),'Schur bound')
  rows.append({'n':n,'k':k,'all_exact_positive':True,'claimed_Schur_lower_bound_verified':True})
need(s.Matrix([[s.Rational(1,10**6),100],[100,2]]).det()<0,'fixed correction negative lost')
r={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'one_dimensional_pair_exact':True,'nonlinear_chart_entries':entries,'tensor_only_mutations_detected':non_tensor,'Schur_stress_cases':rows,'wrong_sign_and_omitted_connection_detected':True,'limits':'Finite exact formula controls, not proof of arbitrary-manifold existence or priority.'};(O/'INDEPENDENT_FINITE_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'PASS','chart_entries':entries,'Schur_cases':len(rows)}))
