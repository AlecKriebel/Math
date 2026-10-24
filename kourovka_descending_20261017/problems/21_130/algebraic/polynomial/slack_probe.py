#!/usr/bin/env python3
"""Drop automatically noncolliding adjacent edge-sum factors; exact truncated content."""
import argparse
import json
from pathlib import Path
from collections import defaultdict
from functools import reduce
from math import gcd
from time import perf_counter


def truncated_slack_polynomial(n):
    poly = {(0,) * n: 1}
    factors = []
    for i in range(n):
        for j in range(i + 1, n):
            factors.append({j: 1, i: -1})
    for i in range(n):
        for j in range(i + 1, n):
            if (j - i) in (1, n - 1):
                continue
            f = defaultdict(int)
            for k,c in ((j,1),((j+1)%n,1),(i,-1),((i+1)%n,-1)):
                f[k] += c
            factors.append({k:c for k,c in f.items() if c})
    for f in factors:
        updated = defaultdict(int)
        for exponent,c in poly.items():
            for k,d in f.items():
                if exponent[k] >= n-1:
                    continue
                ee=list(exponent);ee[k]+=1
                updated[tuple(ee)] += c*d
        poly={e:c for e,c in updated.items() if c}
    assert all(sum(e)==n*(n-2) for e in poly)
    return poly


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n',type=int,default=7)
    parser.add_argument('--json-dir',type=Path)
    args=parser.parse_args()
    if args.json_dir:
        args.json_dir.mkdir(parents=True,exist_ok=True)
    for n in range(3,args.max_n+1):
        start=perf_counter();poly=truncated_slack_polynomial(n)
        content=reduce(gcd,map(abs,poly.values()),0)
        smallest=min(poly.items(),key=lambda item:abs(item[1])) if poly else None
        print(n,'monomials',len(poly),'content',content,'smallest',smallest,'seconds',perf_counter()-start,flush=True)

        if args.json_dir:
            output={'n':n,'degree':n*(n-2),'content':content,'terms':[[list(e),c] for e,c in sorted(poly.items())]}
            with (args.json_dir/f'slack_n{n}.json').open('w') as handle:
                json.dump(output,handle,separators=(',',':'))
