#!/usr/bin/env python3
"""Compressed interval permutations for a finite integer multiset certificate."""
from pathlib import Path
from collections import defaultdict
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent

def build():
    path=HERE/'exact_multiset_certificate.json';cert=json.loads(path.read_text());blocks=[];start=0
    for item in cert['support']:
        v=item['triple'];m=int(item['pair_multiplicity']);assert m>0
        for sign in [1,-1]:
            blocks.append({'start':str(start),'length':str(m),'triple':[sign*x for x in v]});start+=m
    assert str(start)==cert['total_list_size'];perms=[]
    for p,q in cert['pairs']:
        left,right=defaultdict(list),defaultdict(list)
        for block in blocks:
            a,b,t=block['triple'];st=int(block['start']);ln=int(block['length'])
            left[p*a+t].append([st,ln]);right[q*b+t].append([st,ln])
        assert set(left)==set(right);segments=[]
        for value in sorted(left):
            ll,rr=left[value],right[value];i=j=0;lo=ro=0
            assert sum(x[1] for x in ll)==sum(x[1] for x in rr)
            while i<len(ll):
                take=min(ll[i][1]-lo,rr[j][1]-ro)
                segments.append([str(ll[i][0]+lo),str(rr[j][0]+ro),str(take),value]);lo+=take;ro+=take
                if lo==ll[i][1]:i+=1;lo=0
                if ro==rr[j][1]:j+=1;ro=0
            assert j==len(rr)
        # Both source and destination intervals partition every coordinate.
        for axis in [0,1]:
            end=0
            for seg in sorted(segments,key=lambda x:int(x[axis])):
                assert int(seg[axis])==end;end+=int(seg[2])
            assert end==start
        perms.append({'p':p,'q':q,'segments':segments})
    result={'utc':datetime.now(timezone.utc).isoformat(),'N':str(start),'blocks':blocks,'permutations':perms,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'scope':'On source interval [s,s+l), permutation sends j to j+(d-s). Each generated permutation acts on exactly N coordinates. No expansion or group-order computation is required.'}
    (HERE/'compressed_permutations.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'result':'PASS_COMPRESSED_PERMUTATIONS','N':str(start),'coordinate_blocks':len(blocks),'segments':[len(p['segments']) for p in perms]}))
if __name__=='__main__':build()
