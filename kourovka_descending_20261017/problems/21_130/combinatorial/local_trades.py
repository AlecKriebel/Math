#!/usr/bin/env python3
"""Exact support-minimal rainbow-cycle trades against the doubled identity coloring."""
import itertools, json
from pathlib import Path

def search(p):
    for k in range(3,p+1):
        total=0
        for rest in itertools.combinations(range(1,p), k-1):
            A=(0,)+rest
            target={2*a%p for a in A}
            # Connected trades only: a directed k-cycle, normalized at 0 and reversal.
            for tail in itertools.permutations(rest):
                if tail[0]>tail[-1]: continue
                cyc=(0,)+tail
                if {(cyc[i]+cyc[(i+1)%k])%p for i in range(k)}==target:
                    return {'p':p,'minimum_cycle_trade_support':k,'subset':A,'cycle':cyc}
    return None
if __name__=='__main__':
    out=[search(p) for p in [3,5,7,11,13]]
    Path('local_trades.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
