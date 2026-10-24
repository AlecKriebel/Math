#!/usr/bin/env python3
"""Find exact positive weights on a numerical LP support, then verify integrally."""
from pathlib import Path
from fractions import Fraction
from math import gcd,lcm
from datetime import datetime,timezone
import hashlib,json,time
from flint import fmpq_mat
HERE=Path(__file__).resolve().parent
PAIRS=[(3,2),(20,14),(119,84)]
def main():
    source=HERE/'multiset_results.json';raw=json.loads(source.read_text())['runs'][-1]
    triples=[tuple(x['triple']) for x in raw['support']]; n=len(triples)
    rows={}
    for j,(a,b,t) in enumerate(triples):
        for i,(p,q) in enumerate(PAIRS):
            x,y=abs(p*a+t),abs(q*b+t)
            if x!=y:
                rows.setdefault((i,x),{})[j]=rows.setdefault((i,x),{}).get(j,0)+1
                rows.setdefault((i,y),{})[j]=rows.setdefault((i,y),{}).get(j,0)-1
    sparse=[v for v in rows.values() if any(v.values())]
    dense=[[r.get(j,0) for j in range(n)]+[0] for r in sparse]
    dense.append([a*a for a,b,t in triples]+[1])
    start=time.monotonic(); print(json.dumps({'rows':len(dense),'columns':n+1,'phase':'exact_rref'}),flush=True)
    rref,rank=fmpq_mat(dense).rref()
    print(json.dumps({'rank':rank,'seconds':time.monotonic()-start}),flush=True)
    weights=[None]*n;pivots=[]
    for i in range(rank):
        p=next((j for j in range(n+1) if rref[i,j]),None)
        assert p is not None and p<n,'No exact solution on stored support'
        pivots.append(p)
    free=set(range(n))-set(pivots)
    for j in free: weights[j]=Fraction(raw['support'][j]['weight'])
    for i,p in reversed(list(enumerate(pivots))):
        weights[p]=Fraction(str(rref[i,n]))-sum(Fraction(str(rref[i,j]))*weights[j] for j in free)
    assert all(w>0 for w in weights), 'Exact solution is not strictly positive'
    assert sum(a*a*w for (a,b,t),w in zip(triples,weights))==1
    den=lcm(*(x.denominator for x in weights)); multiplicities=[int(w*den) for w in weights]
    common=gcd(*multiplicities);multiplicities=[w//common for w in multiplicities]
    for p,q in PAIRS:
        bal={}
        for (a,b,t),w in zip(triples,multiplicities):
            x,y=abs(p*a+t),abs(q*b+t)
            bal[x]=bal.get(x,0)+w;bal[y]=bal.get(y,0)-w
        assert all(x==0 for x in bal.values())
    payload={'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS_EXACT_POSITIVE_MULTISET','pairs':PAIRS,'symmetric_pair_count':n,'total_list_size':str(2*sum(multiplicities)),'support':[{'triple':list(v),'pair_multiplicity':str(w)} for v,w in zip(triples,multiplicities)],'exact_linear_rank':rank,'free_columns':sorted(free),'seconds':round(time.monotonic()-start,4),'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite symmetric integer multiset with exact matched projections. This needs independent verification and full implication audit. No full Kourovka resolution or novelty claim.'}
    out=HERE/'exact_multiset_certificate.json';out.write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k!='support'}),flush=True)
if __name__=='__main__':main()
