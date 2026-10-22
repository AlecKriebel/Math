import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('requires isolated optimization0')
import sympy as s,itertools,json,datetime,pathlib
O=pathlib.Path(__file__).resolve().parent
x,y,u,v,t,z=s.symbols('x y u v t z');X=s.Matrix([x,y]);Y=s.Matrix([u,v]);coords=(x,y);new=(u,v);h=s.Matrix([2*u+v+u*v+v**3,-u+2*v+u*u+u**2*v]);J=h.jacobian(Y);at={u:s.Rational(1,3),v:s.Rational(-2,5)};base={x:h[0].subs(at),y:h[1].subs(at)}
g=s.Matrix([[3+x*x,x*y],[x*y,4+y*y]]);C=lambda i,j,k: s.Integer(7+2*(i+j+k))+(x+y)**2
Q=lambda i,j,k:(s.diff(g[j,k],coords[i])+s.diff(g[i,k],coords[j])+s.diff(g[i,j],coords[k])-C(i,j,k))/2
q=sum(g[i,j].subs(base)*(coords[i]-base[coords[i]])*(coords[j]-base[coords[j]])/2 for i,j in itertools.product(range(2),repeat=2))+sum(Q(i,j,k).subs(base)*s.prod(coords[a]-base[coords[a]] for a in [i,j,k])/6 for i,j,k in itertools.product(range(2),repeat=3))
qu=q.subs(dict(zip(coords,h)),simultaneous=True);hits=[];bad=0
for a,b,c in itertools.product(range(2),repeat=3):
 actual=s.diff(qu,new[a],new[b],new[c]).subs(at)
 homogeneous=sum(Q(i,j,k).subs(base)*J[i,a]*J[j,b]*J[k,c] for i,j,k in itertools.product(range(2),repeat=3)).subs(at)
 inh=sum(g[i,j].subs(base)*(s.diff(h[i],new[a],new[b])*J[j,c]+s.diff(h[i],new[a],new[c])*J[j,b]+s.diff(h[i],new[b],new[c])*J[j,a]) for i,j in itertools.product(range(2),repeat=2)).subs(at)
 assert s.simplify(actual-homogeneous-inh)==0;bad+=int(actual!=homogeneous);hits.append(str(actual))
assert bad>0
# Fresh scalar cubic-feature pair, with rational functions and nonconstant metric/cubic.
f=s.Matrix([1,t,t*t,t**3]);metric=2+t*t+t**4;cubic=3-2*t+t**5;gam=(s.diff(metric,t)-cubic)/2;E=s.Matrix.vstack(*[f.diff(t,k).T for k in range(4)]);a=E.inv()*s.Matrix([0,0,metric,s.diff(metric,t)+gam]);phi=-a
for r in [a.dot(f),a.dot(f.diff(t)),a.dot(f.diff(t,2))-metric,a.dot(f.diff(t,3))-s.diff(metric,t)-gam,phi.dot(f.diff(t)),phi.diff(t).dot(f.diff(t))-metric,phi.diff(t).dot(f.diff(t,2))-gam]:assert s.expand(r)==0
assert s.expand(a.diff(t).dot(f.diff(t))+metric)==0 and s.expand(phi.diff(t).dot(f.diff(t,2))-gam)==0
# Exact stress cases for independently rotated positive tangent blocks and rectangular mixed blocks.
stress=[];Qrot=s.Matrix([[s.Rational(3,5),s.Rational(-4,5),0],[s.Rational(4,5),s.Rational(3,5),0],[0,0,1]])
for k in [1,3,17,101,10001]:
 A=Qrot.T*s.diag(s.Rational(1,k**6),k*k,1)*Qrot;B=s.Matrix([[k,-k**2],[s.Rational(1,k),3*k],[k**3,2-k]]);tau=s.trace(A.inv())*sum(b*b for b in B);lam=1+tau;Schur=2*lam*s.eye(2)-B.T*A.inv()*B;bound=Schur-(2+tau)*s.eye(2);H=A.row_join(B).col_join(B.T.row_join(2*lam*s.eye(2)))
 assert all(H[:i,:i].det()>0 for i in range(1,6));assert bound[0,0]>=0 and bound[1,1]>=0 and bound.det()>=0
 stress.append({'k':k,'lambda':str(lam),'H_positive_exact':True,'Schur_bound_exact':True})
assert s.Matrix([[s.Rational(1,10**6),100],[100,2]]).det()<0
# Normal exponential germ's cubic coefficient and log(t) third derivative use different variables.
c=s.symbols('c');assert s.diff(-c*z**3/12,z,3)==-c/2;assert s.diff(-c*z**3/6,z,3)!=-c/2
p,b=s.symbols('p b',positive=True);logg=b**3*(s.log(p)-s.log(b))**3/6;assert s.simplify(s.diff(logg,p,3).subs(p,b))==1
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version.split()[0],'sympy':s.__version__,'new_chart_basepoint':[str(base[x]),str(base[y])],'chart_Jacobian':str(J.subs(at).det()),'ordered_chart_entries':8,'tensor_only_failures':bad,'third_derivatives':hits,'fresh_curve_metric':str(metric),'fresh_curve_cubic':str(cubic),'all_pair_sign_and_connection_identities_exact':True,'Schur_stress_cases':stress,'negative_controls':['tensor-only chart law','reversed conormal sign','constant normal correction','doubled cubic factor'],'log_t_unit_third_jet_exact':True,'limitations':'Fresh finite controls, not universal proof or roundoff/priority certification; no new realization mechanism.'};(O/'INDEPENDENT_FINITE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','chart_entries':8,'Schur_cases':5}))
