"""Post-seal comparison only; no independent formulas are imported from author code."""
import json, hashlib
from pathlib import Path
import sympy as S
P=Path(__file__).resolve().parent
own=json.loads((P/'independent_symbolic_stdout.json').read_text())
old=json.loads((P/'author_full_hessian_certificate_stdout.json').read_text())
count=0
for a,b in zip(own['fourier_blocks'],old['fourier_trace_certificates']):
    assert(a['kx'],a['ky'])==(b['kx'],b['ky']);count+=1
    expected=sum(c*v for c,v in zip(b['numerator'],[1,S.sqrt(2),S.sqrt(3),S.sqrt(6)]))/b['denominator']
    assert S.expand(S.sympify(a['trace'])-expected)==0;count+=1
assert own['hessian_positive']==old['physical_dimension']==65;count+=1
assert own['hessian_nullity']==old['gauge_kernel_dimension']==63;count+=1
print(json.dumps({'status':'PASS','post_seal_exact_comparisons':count,'all_fourier_trace_values_match':True,'scope':'Comparison occurs after sealed independent verdict; prior review outcome was not used to construct own evidence.'},indent=2,sort_keys=True))
