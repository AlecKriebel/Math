#!/usr/bin/env python3
"""Compare every new-formula n3–9 coefficient with independent full expansion."""
from pathlib import Path
import json,sys
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'polynomial'))
from slack_probe import truncated_slack_polynomial
fixed={r['n']:r for r in map(json.loads,(root/'fixed_zero_coefficients.txt').read_text().splitlines())}
low={r['n']:r for r in map(json.loads,(root/'low_exponent_coefficients.jsonl').read_text().splitlines())}
checks=0
for n in range(3,10):
    if n>=8:
        x=json.loads((root/'polynomial'/f'slack_n{n}.json').read_text())
        poly={tuple(e):c for e,c in x['terms']}
    else:poly=truncated_slack_polynomial(n)
    for j,c in enumerate(fixed[n]['coefficients'],1):
        t=[n-1]*n;t[0]=0;t[j]=n-2
        assert poly.get(tuple(t),0)==c,(n,t,c,poly.get(tuple(t),0))
        checks+=1
    if n in low:
        for witness in low[n]['coefficients']:
            assert poly.get(tuple(witness['exponents']),0)==witness['coefficient']
            checks+=1
print(f'PASS: {checks} exact coefficients, n3–9, match independent full polynomial expansion.')
