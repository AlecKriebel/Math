"""Exact simplification of the independently verified focal pedal coefficient."""
from pathlib import Path
from datetime import datetime, timezone
import sympy as s
import json

out = Path(__file__).resolve().parent
k, t = s.symbols('k t', positive=True)
C, D = s.symbols('C D', positive=True)
B2 = 1-k*k
den = 1-k*k*t**4
sd = 2*t*C*D/den
cd = (C*C-t*t*D*D)/den
dd = (D*D-k*k*t*t*C*C)/den
p = B2*sd*(dd-k*k*cd-B2)/(k*k*(cd-dd)**2)
n = s.together(p-t*C*D).as_numer_denom()[0]
for x, q in [(C, 1-t*t), (D, 1-k*k*t*t)]:
    n = s.rem(n, x*x-q, x)
remainder = s.factor(n)
assert remainder == 0
result = {'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
          'identity': 'p0=sn(v)cn(v)dn(v)', 'polynomial_remainder': str(remainder),
          'scope': 'Exact algebra; strict 0<k<1,0<v<K. All analytic premises separately verified.',
          'no_novelty_claim': True}
(out / 'ROOT_PEDAL_COEFFICIENT_SIMPLIFICATION.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
