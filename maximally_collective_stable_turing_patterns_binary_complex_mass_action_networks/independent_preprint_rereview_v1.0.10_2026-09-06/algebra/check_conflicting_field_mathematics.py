"""Independent mathematical cross-check of the coefficient-key mutation."""
from pathlib import Path
import json
import re
import sympy as S

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
x, y, z, s, A = S.symbols('x y z s A', real=True)
la = x + S.I*y
t = 1+s
g1 = la+2+S.Rational(23,63)*t
gm = la+5+t/7
gz = la+4+S.Rational(16,45)*t
F = g1*gm*gz-4*g1-4*gm+gz
G = gz*(4*g1+gm)-36
raw = S.Poly(S.expand(S.Rational(91,90)**2*(1+A*x+y*y/3)*F*S.conjugate(F)-G*S.conjugate(G)), y)
if any(power[0] % 2 for power, coefficient in raw.terms()):
    raise RuntimeError('Expected even polynomial in y')
defined = S.expand(sum(coefficient*z**(power[0]//2) for power, coefficient in raw.terms()))

def parse_spatial_table(path):
    text = path.read_text().split('84-term equilibrium-scaled spatial certificate',1)[1]
    result = S.Integer(0)
    count = 0
    for line in text.splitlines():
        match = re.fullmatch(r'(\d+) & (\d+) & (\d+) & \$(.*?)\$\\\\',line)
        if not match:
            continue
        px,pz,ps = map(int,match.groups()[:3])
        coefficient = S.Integer(0)
        for part in match.group(4).split('+'):
            piece = re.fullmatch(r'(?:(\d+))?(A)?(?:\^\{(\d+)\})?(?:/(\d+))?',part)
            if not piece or (piece.group(1) is None and piece.group(2) is None):
                raise RuntimeError('Unrecognized exact coefficient: '+part)
            numerator = int(piece.group(1) or 1)
            exponent = int(piece.group(3) or 1) if piece.group(2) else 0
            denominator = int(piece.group(4) or 1)
            coefficient += S.Rational(numerator,denominator)*A**exponent
        result += coefficient*x**px*z**pz*s**ps
        count += 1
    if count != 84:
        raise RuntimeError('Wrong parsed row count')
    return S.expand(result)

shipped = parse_spatial_table(AUDIT/'source_snapshot/data/certificate_tables.tex')
mutant = parse_spatial_table(AUDIT/'certificates/conflicting_coefficient_fields_table.tex')
delta = S.expand(mutant-defined)
expected = S.Rational(16019,24300)*x**6*z
if S.expand(shipped-defined) != 0 or delta != expected:
    raise RuntimeError('Cross-check mismatch')
coefficient = S.Poly(defined,x,z,s).coeff_monomial(x**6*z)
if coefficient != S.Rational(8281,24300):
    raise RuntimeError('Defining coefficient mismatch')
result = {'status':'PASS', 'imports_project_implementation':False,
          'shipped_table_equals_defining_modulus':True, 'parsed_rows_each_table':84,
          'defining_coefficient_x6_z_s0':str(coefficient),
          'mutant_minus_defining_modulus':str(delta),
          'point_x1_z1_s0_A4_difference':str(delta.subs({x:1,z:1,s:0,A:4})),
          'interpretation':'Shipped table correct; mutated generated table is a false exact identity, not harmless ignored metadata.'}
(HERE/'CONFLICTING_FIELD_MATH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
