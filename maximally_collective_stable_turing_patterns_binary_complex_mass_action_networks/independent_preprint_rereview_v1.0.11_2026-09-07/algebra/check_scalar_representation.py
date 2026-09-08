"""Narrow independent check of one scalar coefficient's mathematical rendering."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import importlib.util
import json
import sys
import sympy as S

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'source_snapshot'
spec = importlib.util.spec_from_file_location('scalar_generator_probe',SOURCE/'computation/generate_tables.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)

x,y = S.symbols('x y',real=True)
lam = x+S.I*y
P = lam**4+12*lam**3+42*lam**2+47*lam+16
R = 5*lam**2+33*lam+16
E = S.Poly(S.expand((1+lam)*(1+S.conjugate(lam))*P*S.conjugate(P)-R*S.conjugate(R)),x,y)
expected = E.coeff_monomial(x**10)
if expected != 1:
    raise RuntimeError('Independent leading coefficient mismatch')

baseline = json.loads((SOURCE/'independent_verifier/improved_modulus_certificate.json').read_text())['homogeneous']
records=[]
for value in ['1',True,'1e0']:
    section=deepcopy(baseline)
    row=next(row for row in section['terms'] if row['powers']==[10,0])
    row['coefficient']=value
    rational=S.Rational(value)
    table=generator.cert_table('probe',section['variables'],section['terms'],section['term_count'],('x','z'))
    emitted=next(line for line in table.splitlines() if line.startswith('10 & 0 &'))
    if rational != expected:
        raise RuntimeError('Expected equivalent numeric coercion')
    records.append({'input':value,'input_type':type(value).__name__,
                    'reader_rational_value':str(rational),'emitted_TeX_row':emitted})

result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'target':'137ffa9f1a340f621651395ad0236cf1bdadb51c',
        'defining_coefficient_x10':str(expected),'records':records,
        'scope':'The defining leading coefficient is independently derived; actual rendering routine is observed. Full aggregate and PDF controls belong to certificate reviewer.'}
(HERE/'SCALAR_REPRESENTATION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
