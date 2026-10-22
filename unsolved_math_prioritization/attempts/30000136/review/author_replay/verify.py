import sympy as s,json,hashlib
from pathlib import Path
x,y,t=s.symbols('x y t',real=True)
a=s.sin(x);b=s.sin(y)+1-s.cos(x)
f=s.cos(x)+s.cos(y)+s.sin(x)
assert s.simplify(s.diff(b,x)-s.diff(a,y)-s.sin(x))==0
assert s.simplify(a+s.diff(f,x)-s.cos(x))==0
assert s.simplify(b+s.diff(f,y)-(1-s.cos(x)))==0
assert s.expand(t*t+(1-t)**2-(2*(t-s.Rational(1,2))**2+s.Rational(1,2)))==0
J=s.Matrix([a,b]).jacobian([x,y]).subs({x:0,y:0})
assert J==s.eye(2)
assert J.det()==1
P=Path(__file__).parent
r={'status':'PASS','exact_symbolic_assertions':6,'scope':'exterior derivative, exact correction, norm bound identity, local index Jacobian; no general existence theorem','artifact_sha256':hashlib.sha256((P/'PARTIAL_RESULT.md').read_bytes()).hexdigest()}
(P/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
