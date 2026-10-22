"""Independent negative control for the literal 0062p6 square, no imported checker."""
from pathlib import Path
import sympy as s,json,hashlib
p=Path(__file__).resolve();q=s.sqrt(5);X=s.Matrix([2/q,2/q]);normal=s.Matrix([X[0]/4,X[1]]);incoming=s.Matrix([0,1]);actual=s.Matrix([-1,0]);reflected=incoming-2*incoming.dot(normal)*normal/normal.dot(normal);res=reflected-actual
horizontal_lambda=s.simplify(1-X[1]**2);vertical_lambda=s.simplify(4-X[0]**2)
assert res==s.Matrix([s.Rational(9,17),-s.Rational(15,17)])
assert horizontal_lambda==s.Rational(1,5) and vertical_lambda==s.Rational(16,5)
assert s.simplify(X[0]**2/4+X[1]**2-1)==0
out={'source':'Ferudun0062v1.0 printedp6 literal (+-2/sqrt5,+-2/sqrt5), not the corrected rectangle','boundary_residual':'0','reflection_residual':[str(x) for x in res],'edge_caustic_parameters':[str(horizontal_lambda),str(vertical_lambda)],'genuine_billiard':False,'odd_theorem_refuted':False,'negative_control_pass':True,'program_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(p.parent/'FRESH_SOURCE_FIXTURE_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
