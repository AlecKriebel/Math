"""New eighth-review exact checks; no numerical result substitutes for proof."""
import sympy as s,itertools,json
from datetime import datetime,timezone
from pathlib import Path
x,y,u,v=s.symbols('x y u v',real=True);g=(1+x*x)**2;C=x**5+2;Q=(3*s.diff(g,x)-C)/2;gam=(s.diff(g,x)-C)/2
f=s.Matrix([1,x,x*x,x**3]);a=s.Matrix([x*x*g/2-x**3*Q/6,-x*g+x*x*Q/2,g/2-x*Q/2,Q/6]);ph=-a
expr=[a.dot(f),a.dot(f.diff(x)),a.dot(f.diff(x,2))-g,a.dot(f.diff(x,3))-Q,f.diff(x).dot(ph.diff(x))-g,f.diff(x,2).dot(ph.diff(x))-gam]
assert all(s.expand(z)==0 for z in expr)
assert s.expand(f.diff(x).dot(a.diff(x))-g)!=0
# A non-affine chart: compare full scalar chain rule and detect tensor-only law.
F=s.Rational(5,2)*x*x+2*x*y+3*y*y+s.Rational(1,6)*(7*x**3-9*x*x*y+15*x*y*y+11*y**3)
coords=[u+u*v+v*v,v+u*u];old=[x,y];new=[u,v];pt={u:0,v:0};H=s.hessian(F,old).subs({x:0,y:0});T=[[[s.diff(F,i,j,k).subs({x:0,y:0}) for k in old]for j in old]for i in old];J=s.Matrix(coords).jacobian(new).subs(pt)
checks=[];sensitive=0
for aa,bb,cc in itertools.product(range(2),repeat=3):
 tensor=sum(J[i,aa]*J[j,bb]*J[k,cc]*T[i][j][k] for i,j,k in itertools.product(range(2),repeat=3))
 inh=sum(H[i,j]*(s.diff(coords[i],new[aa],new[bb]).subs(pt)*J[j,cc]+s.diff(coords[i],new[aa],new[cc]).subs(pt)*J[j,bb]+s.diff(coords[i],new[bb],new[cc]).subs(pt)*J[j,aa]) for i,j in itertools.product(range(2),repeat=2))
 actual=s.diff(F.subs({x:coords[0],y:coords[1]},simultaneous=True),new[aa],new[bb],new[cc]).subs(pt);assert s.simplify(actual-tensor-inh)==0;sensitive+=int(actual!=tensor);checks.append(str(actual))
# Three-coordinate finite simplex: Hessian equals direct Fisher and derivative cubic=-AC.
p=s.symbols('p1:4',positive=True);pall=[*p,1-sum(p)];ent=sum(z*s.log(z) for z in pall);G=s.hessian(ent,p);count=0
for i,j,k in itertools.product(range(3),repeat=3):
 fisher=sum(s.diff(z,p[i])*s.diff(z,p[j])/z for z in pall);AC=sum(s.diff(z,p[i])*s.diff(z,p[j])*s.diff(z,p[k])/z**2 for z in pall)
 assert s.simplify(G[i,j]-fisher)==0 and s.simplify(s.diff(G[i,j],p[k])+AC)==0;count+=1
# Unbounded pointwise Schur construction with a non-diagonal A and large B.
r=s.symbols('r',positive=True);A=s.Matrix([[r*r+1,r],[r,1]]);B=s.Matrix([[r**3,r**-2],[r**2+1,r**4]]);t=s.trace(A.inv())*sum(z*z for z in B);lam=1+t;complement=2*lam*s.eye(2)-B.T*A.inv()*B
schur=[]
for z in [s.Rational(1,10000),1,10,1000]:
 K=complement.subs(r,z);assert K[0,0]>0 and K.det()>0;schur.append({'r':str(z),'diagonal_positive':True,'determinant_positive':True})
tt,ss=s.symbols('t s',positive=True);q=tt**3*(s.log(ss)-s.log(tt))**3/6;assert s.simplify(s.diff(q,ss,3).subs(ss,tt))==1
out={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'new_review08_authored':True,'pair_identities':6,'chart_entries':8,'tensor_only_omissions_detected':sensitive,'simplex_entropy_cubic_entries':count,'unbounded_schur_exact_samples':schur,'log_germ_third_derivative':1,'finite_supplementary_checks_only':True};(Path(__file__).resolve().parent/'INDEPENDENT08_MATH.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
