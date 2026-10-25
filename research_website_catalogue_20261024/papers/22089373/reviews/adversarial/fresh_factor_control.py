#!/usr/bin/env python3
"""Fresh exact Bernstein/product verifier for all supplied n3 strict factors.
Checks certificates themselves; does not replace graph-to-polynomial replay.
"""
import gzip,json,hashlib
from pathlib import Path
from fractions import Fraction
from itertools import product
from math import comb
from datetime import datetime,timezone
base=Path(__file__).parent
bundle=base/'cache/replay-bundle'
fp=bundle/'reviews/base_gate_adversarial_referee_n3/strict_factor_certificate.json'
pp=bundle/'primary/certificates/hard_cover_polynomials_n3_schema3_n3_full.jsonl.gz'
factors=json.loads(fp.read_text())['records']
with gzip.open(pp,'rt') as f: polys={r['polynomial_id']:r for r in map(json.loads,f)}
def mul(p,q):
 r={}
 for a,c in p.items():
  for b,d in q.items():
   e=tuple(x+y for x,y in zip(a,b));r[e]=r.get(e,0)+c*d
 return {a:c for a,c in r.items() if c}
def sign(poly):
 width=len(next(iter(poly)))
 active=[i for i in range(width) if any(a[i] for a in poly)]
 compressed={tuple(a[i] for i in active):c for a,c in poly.items()}
 degrees=[max(a[i] for a in compressed) for i in range(len(active))]
 signs=set()
 for beta in product(*(range(d+1) for d in degrees)):
  value=Fraction(0)
  for alpha,c in compressed.items():
   if all(a<=b for a,b in zip(alpha,beta)):
    term=Fraction(c)
    for a,b,d in zip(alpha,beta,degrees):term*=Fraction(comb(b,a),comb(d,a))
    value+=term
  if value:signs.add(1 if value>0 else -1)
 assert len(signs)==1,(degrees,signs)
 return signs.pop()
rows=[]; total=0
for key,record in factors.items():
 width=record['variable_count']; p={(0,)*width:record['content']}; sg=1 if record['content']>0 else -1
 for row in record['factors']:
  q={tuple(a):c for a,c in row['terms']};sg*=sign(q)**row['multiplicity'];total+=1
  for _ in range(row['multiplicity']):p=mul(p,q)
 target={tuple(a):c for a,c in polys[key]['terms']}
 assert p==target,key
 assert sg==record['strict_sign'],key
 assert sg!=-record['strict_sign'],'negative sign mutation was not rejected'
 rows.append({'polynomial_id':key,'strict_sign':sg,'factor_count':len(record['factors']),'expanded_terms':len(p)})
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','polynomials':len(rows),'factors':total,'rows':rows,'source_sha256':{str(p.relative_to(bundle)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [fp,pp]},'scope':'Exact all-factor multiplication and strictly signed rational Bernstein coefficients over the open cube. Independent of supplied verification code; graph binding checked by separate full replay.'}
base.joinpath('fresh_factor_control.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','polynomials':len(rows),'factors':total}))
