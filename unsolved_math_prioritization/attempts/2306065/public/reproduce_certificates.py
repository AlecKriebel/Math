#!/usr/bin/env python3
"""Optional discovery replay, AFTER both search scripts, in a disposable copy.
Search solvers may vary by platform. Frozen verifiers do not need this script.
"""
import json
from pathlib import Path
D=Path(__file__).parent
p=json.loads((D/'polynomial-search.json').read_text())
ns=[round(x*.999*10**9) for x in p['coefficients']]
w={'M':3,'L_numerator':549,'L_denominator':500,'coefficient_denominator':10**9,'coefficient_numerators':ns,'definition':'f(z)=z*exp(sum(c[n]*z**n,n=1..40))','role':'Strictly admissible lower-bound example, not a global optimizer'}
(D/'WITNESS.json').write_text(json.dumps(w,indent=2)+'\n')
u=json.loads((D/'upper-search.json').read_text());den=10**12
out={k:v for k,v in u.items() if k!='rows'};out['dual_denominator']=den;out['rows']=[]
for row in u['rows']:
 r={'k':row['k']}
 for name in ['inequality_dual','lower_dual','upper_dual']:
  r[name]=[[i,max(0,round(float(v)*den))] for i,v in enumerate(row[name]) if round(float(v)*den)>0]
 out['rows'].append(r)
(D/'UPPER_CERTIFICATE.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
print('Run verify.py against the generated candidates; discovery output alone is not a certificate.')
