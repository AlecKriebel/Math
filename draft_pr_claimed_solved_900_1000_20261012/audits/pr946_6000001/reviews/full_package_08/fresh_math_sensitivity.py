"""Replayed seventh-review finite sensitivity check; corroborates rather than proves."""
import sympy as s,json,datetime
from pathlib import Path
x=s.symbols('x',real=True);g=s.exp(x*x)+x**4+1;C=x**7+s.exp(-x);Q=(3*s.diff(g,x)-C)/2;Gamma=(s.diff(g,x)-C)/2
f=s.Matrix([1,x,x*x,x**3]);a=s.Matrix([x*x*g/2-x**3*Q/6,-x*g+x*x*Q/2,g/2-x*Q/2,Q/6]);phi=-a
zero=lambda z:s.simplify(s.expand(z))==0
expressions=[(a.dot(f),0),(a.dot(f.diff(x)),0),(a.dot(f.diff(x,2)),g),(a.dot(f.diff(x,3)),Q),(f.diff(x).dot(phi.diff(x)),g),(f.diff(x,2).dot(phi.diff(x)),Gamma)]
if not all(zero(v-e) for v,e in expressions):raise RuntimeError('jet/pair identity')
if zero(f.diff(x).dot(a.diff(x))-g):raise RuntimeError('wrong sign not detected')
if zero(f.diff(x,2).dot(phi.diff(x))-s.diff(g,x)-Gamma):raise RuntimeError('missing derivative term not detected')
out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'adapted_from_sealed_review07':True,'authored_new_in_review08':False,'exact_identities':6,'negative_controls':['phi wrong sign','missing metric derivative term'],'noncompact_unbounded_g_and_C':True,'finite_checks_do_not_replace_universal_proof':True}
(Path(__file__).resolve().parent/'FRESH_MATH_SENSITIVITY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
