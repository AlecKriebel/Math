"""Checks the proof's reference original-area identity and N4 examples."""
from pathlib import Path
import json
path=Path(__file__).parent/'independent_exact_geometry.py'
source=path.read_text().split('a,b = z.Integer(3),z.Integer(1)')[0]
exec(compile(source,str(path),'exec'))
f=(z.sqrt(3),0)
root5=z.sqrt(5)
cases=[([(2,0),(0,1),(-2,0),(0,-1)],z.Rational(32,25),z.Integer(8)), ([(4/root5,1/root5),(-4/root5,1/root5),(-4/root5,-1/root5),(4/root5,-1/root5)],z.Rational(8,5),z.Rational(32,5))]
receipt=[]
for vv,ep,eb in cases:
    vv=[tuple(map(z.sympify,p)) for p in vv]
    validate(vv,z.Integer(2),z.Integer(1),z.Rational(4,5))
    ap,ab,_=derived(vv,f)
    assert z.simplify(ap-ep)==0 and z.simplify(ab-eb)==0
    receipt.append({'pedal_area':str(ap),'antipedal_area':str(ab),'product':str(z.simplify(ap*ab))})
k,s,S,c,d,C,D,t=z.symbols('k s S c d C D t')
L=1-k*k*s*s*S*S
ends=[]
for e in [-1,1]:
    ends.append((-d*(S*c*d+e*s*C*D)/(c*L),t*(C*c-e*S*s*D*d)/(c*L)))
expr=det(*ends)-2*(d/c)*(t/c)*s*c*D/L
poly=z.expand(z.fraction(z.cancel(expr))[0])
for variable,relation in [(C,1-S*S),(D,1-k*k*S*S),(d,1-k*k*s*s),(t,1-k*k),(c,1-s*s)]:
    poly=z.rem(poly,variable*variable-relation,variable)
assert z.factor(poly)==0
print(json.dumps({'N4_exact_original_geometry':receipt,'original_endpoint_determinant_identity':'det(P(x-v),P(x+v))=2absc dn(x)/L','original_area_trace_derivation':'dn(x-v)+dn(x+v)=2d dn(x)/L. Thus half the endpoint determinant is absc/(2d) times the sum of endpoint dn values. Each endpoint occurs twice in the cyclic area sum, giving A=absc T/d.','status':'PASS'},indent=2))
