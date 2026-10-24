#!/usr/bin/env python3
"""Independent integer-only check of root's proposed positive Pell multiset."""
from pathlib import Path
from collections import defaultdict
from math import gcd
from functools import reduce
from datetime import datetime,timezone
import json,hashlib

def run():
 source=Path(__file__).parent.parent/'root_orbit/exact_multiset_certificate.json'
 data=json.loads(source.read_text());pairs=((3,2),(20,14),(119,84));support=[]
 assert data['pairs']==[list(v) for v in pairs]
 for item in data['support']:
  v=tuple(item['triple']);m=int(item['pair_multiplicity']);assert len(v)==3 and all(type(x) is int for x in v) and m>0;support.append((v,m))
 assert len(support)==len(set(v for v,m in support))
 balances=[]
 for p,q in pairs:
  # Full signed measure, rather than reusing root's absolute-value folding.
  bal=defaultdict(int)
  for (a,b,t),m in support:
   for sign in (1,-1):
    bal[sign*(p*a+t)]+=m;bal[sign*(q*b+t)]-=m
  assert all(x==0 for x in bal.values());balances.append({'pair':[p,q],'distinct_signed_projection_values':len(bal),'nonzero_balances':0})
 n=2*sum(m for v,m in support);assert n==int(data['total_list_size'])
 alpha=2*sum(m*a*a for (a,b,t),m in support);beta=2*sum(m*b*b for (a,b,t),m in support)
 gamma=2*sum(m*a*t for (a,b,t),m in support);delta=2*sum(m*b*t for (a,b,t),m in support)
 assert alpha>0 and beta==2*alpha and 2*gamma==alpha and delta==alpha
 return {'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS_INTEGER_POSITIVE_MULTISET','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'symmetric_pair_types':len(support),'full_signed_list_size':str(n),'multiplicity_gcd':reduce(gcd,(m for v,m in support)),'balances':balances,'moment_identities':{'A_squared_norm':str(alpha),'B_squared_norm':str(beta),'A_dot_T':str(gamma),'B_dot_T':str(delta)},'scope':'Independent check of the exact finite positive certificate only, using full signed projection balances. The finite-holonomy construction and prior VRC implications require their own proof audit; this is not a full21.124 solution.'}
if __name__=='__main__':
 out=run();Path(__file__).with_name('independent_positive_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
