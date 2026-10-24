#!/usr/bin/env python3
"""Standalone nonsearch checker for odd-rainbow-cycle-v1 JSONL witnesses.

Does not import the search implementation, precomputed tables, or its summaries.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from datetime import datetime, timezone


def group_sum(x, y, moduli):
    # Decode each operand, add the coordinates, re-encode the result.
    value = 0
    place = 1
    for modulus in moduli:
        value += ((x % modulus + y % modulus) % modulus) * place
        x //= modulus
        y //= modulus
        place *= modulus
    assert x == y == 0
    return value


def verify_file(path):
    seen = set()
    counts = {}
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with path.open() as source:
        metadata = json.loads(next(source))
        assert metadata['format'] == 'odd-rainbow-cycle-v1'
        moduli = metadata['moduli']
        assert all(isinstance(m,int) and m>1 and m%2 for m in moduli)
        order = math.prod(moduli)
        assert order == metadata['order']
        for lineno,line in enumerate(source,2):
            record = json.loads(line)
            mask = record['mask']
            cycle = record['cycle']
            assert isinstance(mask,int) and 0 < mask < (1 << order), (path,lineno,'mask')
            assert mask & 1, (path,lineno,'zero')
            assert mask not in seen, (path,lineno,'duplicate mask')
            seen.add(mask)
            vertices = {v for v in range(order) if mask >> v & 1}
            assert len(vertices)>2, (path,lineno,'cardinality')
            assert isinstance(cycle,list) and len(cycle)==len(vertices), (path,lineno,'cycle length')
            assert len(set(cycle))==len(cycle) and set(cycle)==vertices, (path,lineno,'permutation')
            assert cycle[0]==0, (path,lineno,'start')
            sums = [group_sum(cycle[i],cycle[(i+1)%len(cycle)],moduli) for i in range(len(cycle))]
            assert len(set(sums))==len(sums), (path,lineno,'sum collision',sums)
            counts[str(len(cycle))] = counts.get(str(len(cycle)),0)+1
    if metadata.get('domain') == 'listed_samples':
        assert len(seen) == metadata['covered_subsets'], (path,'sample count')
        mode = 'Every listed sample has a valid witness; no exhaustive coverage claim.'
    elif metadata.get('domain') == 'sizes':
        sizes = set(metadata['sizes'])
        assert all(int(k) in sizes for k in counts)
        expected = sum(math.comb(order-1,n-1) for n in sizes)
        assert len(seen) == expected
        assert counts == {str(n):math.comb(order-1,n-1) for n in sorted(sizes)}
        mode = 'Every zero-containing subset in the specified size classes is covered.'
    else:
        expected = {mask for mask in range(1,1 << order,2) if mask.bit_count()>2}
        assert seen == expected, (path,'incomplete or extraneous domain',len(seen),len(expected))
        assert len(seen) == (1 << (order-1))-order
        assert len(seen) == metadata['covered_subsets']
        mode = 'Every zero-containing subset of size >2 is covered.'
    return {'file':path.name,'moduli':moduli,'order':order,'verified_subsets':len(seen),'counts_by_size':counts,'sha256':digest,'coverage':mode}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('files',nargs='+',type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    results=[verify_file(p) for p in args.files]
    report={'verified_utc':datetime.now(timezone.utc).isoformat(),'all_valid':True,'files':results,'total_verified_subsets':sum(r['verified_subsets'] for r in results)}
    text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    print(text,end='')
    if args.report: args.report.write_text(text)

if __name__=='__main__': main()
