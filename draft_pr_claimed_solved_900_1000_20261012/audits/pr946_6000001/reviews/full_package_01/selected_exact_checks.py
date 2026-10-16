import sys
if not sys.flags.safe_path or sys.flags.optimize:raise SystemExit('safe nonoptimized startup required')
import json,datetime
import sympy as s

def require(ok,why):
 if not ok:raise RuntimeError(why)
def zero(e):require(s.simplify(e)==0,'nonzero exact residual '+str(e))
t=s.symbols('t');g=s.Function('g')(t);C=s.Function('C')(t);gamma=(s.diff(g,t)-C)/2;Q=s.diff(g,t)+gamma
f=s.Matrix([1,t,t*t,t**3]);E=s.Matrix.vstack(*[f.diff(t,k).T for k in range(4)]);a=E.inv()*s.Matrix([0,0,g,Q]);phi=-a
for x in [a.dot(f),phi.dot(f.diff(t)),f.diff(t).dot(phi.diff(t))-g,f.diff(t,2).dot(phi.diff(t))-gamma,f.diff(t).dot(phi.diff(t,2))-(s.diff(g,t)+C)/2]:zero(x)
wrong=E.inv()*s.Matrix([0,0,g,Q]);zero(f.diff(t).dot(wrong.diff(t))+g)
omitted=-E.inv()*s.Matrix([0,0,g,s.diff(g,t)]);zero(f.diff(t,2).dot(omitted.diff(t)))
y=s.symbols('y');x=2*y+3*y*y+5*y**3;q=s.Rational(7,2)*x*x+s.Rational(11,6)*x**3;third=s.diff(q,y,3).subs(y,0);require(third==340 and third!=88,'non-tensor chart law control')
A=s.Matrix([[2,1],[1,1]]);B=s.Matrix([5,-7]);tau=s.trace(A.inv())*sum(z*z for z in B);lam=1+tau;Schur=2*lam-(B.T*A.inv()*B)[0];H=A.row_join(B).col_join(B.T.row_join(s.Matrix([[2*lam]])))
require(tau==222 and Schur==253 and Schur>=2+tau and H.det()==253,'exact completion')
require(2-(B.T*A.inv()*B)[0]<0,'fixed correction negative control')
rot=s.Matrix([[s.Rational(3,5),s.Rational(-4,5)],[s.Rational(4,5),s.Rational(3,5)]]);An=rot.T*A*rot;Bn=rot.T*B;zero(s.trace(An.inv())*sum(z*z for z in Bn)-tau)
print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arbitrary_symbolic_1D_ordered_pair':True,'jet_determinant':str(E.det()),'nonlinear_chart_third_derivative':str(third),'tensor_only_third_derivative':'88','schur_tau':str(tau),'schur_remainder':str(Schur),'ambient_Hessian_determinant':str(H.det()),'frame_invariance':True,'sign_omission_and_fixed_correction_controls_sensitive':True,'scope':'Independent selected algebraic checks of the saved mechanism; no extra proof-search mechanism or universal theorem inferred.'},indent=2))
