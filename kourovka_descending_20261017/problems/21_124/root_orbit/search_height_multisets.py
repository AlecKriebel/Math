#!/usr/bin/env python3
"""Exploratory extension to the separate six-edge height countermodel."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import search_multisets as search
HERE=Path(__file__).resolve().parent
search.PAIRS=[(0,-2),(1,3),(1,-5),(6,10),(6,-12)]
out={'utc':datetime.now(timezone.utc).isoformat(),'pairs':search.PAIRS,'runs':[],'scope':'Only numerical bounded support exploration for HEIGHT_NORM_COUNTERMODEL; no exact witness or theorem until independent exact reconstruction.'}
for box in [(2,3,10),(3,5,20),(4,6,30),(6,9,40)]:
    r=search.search(*box,35);out['runs'].append(r)
    (HERE/'height_multiset_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='support'}),flush=True)
    if r.get('exact_certificate_passed') or r['status']==0:break
