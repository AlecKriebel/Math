#!/usr/bin/env python3
"""Verify the compressed finite witness using standard-library integers only."""
from pathlib import Path
from bisect import bisect_right
from collections import defaultdict
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent

def main():
    cp=HERE/'exact_multiset_certificate.json';pp=HERE/'compressed_permutations.json'
    cert=json.loads(cp.read_text());obj=json.loads(pp.read_text());assert obj['input_sha256']==hashlib.sha256(cp.read_bytes()).hexdigest()
    expected=[];cursor=0;moments=defaultdict(int);horizontal=[False,False]
    for x in cert['support']:
        v=x['triple'];m=int(x['pair_multiplicity']);assert len(v)==3 and all(type(z) is int for z in v) and m>0
        for sign in (1,-1):
            expected.append({'start':str(cursor),'length':str(m),'triple':[sign*z for z in v]});cursor+=m
        for i in range(3):
            for j in range(3):moments[i,j]+=2*m*v[i]*v[j]
        horizontal=[horizontal[i] or bool(v[i]) for i in range(2)]
    assert all(horizontal);assert cursor==int(cert['total_list_size'])==int(obj['N']);assert obj['blocks']==expected
    starts=[int(b['start']) for b in obj['blocks']]
    def block(lo,length):
        b=obj['blocks'][bisect_right(starts,lo)-1]
        assert int(b['start'])<=lo<lo+length<=int(b['start'])+int(b['length'])
        return b['triple']
    results=[]
    assert [(p['p'],p['q']) for p in obj['permutations']]==[(3,2),(20,14),(119,84)]
    for perm in obj['permutations']:
        p,q=perm['p'],perm['q'];segments=perm['segments']
        for axis in (0,1):
            end=0
            for seg in sorted(segments,key=lambda x:int(x[axis])):
                assert int(seg[axis])==end and int(seg[2])>0;end+=int(seg[2])
            assert end==cursor
        for s,d,l,value in segments:
            s,d,l=int(s),int(d),int(l);a,b,t=block(s,l);aa,bb,tt=block(d,l)
            assert p*a+t==value==q*bb+tt
        balance=defaultdict(int)
        for item in expected:
            a,b,t=item['triple'];m=int(item['length']);balance[p*a+t]+=m;balance[q*b+t]-=m
        assert all(v==0 for v in balance.values())
        assert p*p*moments[0,0]+2*p*moments[0,2]==q*q*moments[1,1]+2*q*moments[1,2]
        results.append({'p':p,'q':q,'permutation_segments':len(segments),'projection_values':len(balance),'bijection_and_relation':'PASS'})
    out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_EXACT_INTEGER_WITNESS','N':str(cursor),'support_pairs':len(cert['support']),'permutations':results,'A_nonzero':True,'B_nonzero':True,'append_trivial_height_coordinate':True,'input_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [cp,pp]},'scope':'Verifies finite combinatorial object and vertex-rank ingredients; written group-theoretic implication and primary theorems are separate proof obligations. No general21.124 claim.'}
    (HERE/'positive_witness_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
