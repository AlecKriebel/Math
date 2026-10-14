#!/usr/bin/env python3
"""Exact replay of the legal safe periodic schedule; not a Devil-winning certificate."""
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

origin=(0,0)
points=sorted(set(product((-1,0,1),repeat=2))-{origin})+[(2,0)]
assert len(points)==len(set(points))==9 and origin not in points
cases=0
for H in range(9,201):
    pending=set()
    end=H+1+9*8+8
    for n in range(1,end+1):
        # Move n is the origin, then expired pairs are removed.
        assert (origin,n) not in pending
        pending={(p,t)for p,t in pending if t>n}
        j,i=divmod(n-1,9)
        p,t=points[i],H+1+9*j
        assert 1<=t-n<=H
        assert (p,t) not in pending
        pending.add((p,t))
        if n>=H+1:
            j,s=divmod(n-(H+1),9)
            assert len(pending)==H-8+s
            relevant={(p,t)for p,t in pending if max(abs(p[0]),abs(p[1]))<=t-n}
            wanted=H-8+s if s<8 else H-1
            assert len(relevant)==wanted>=H-8
            # Every pending pair lies at its prescribed heavy timestamp.
            assert all((t-H-1)%9==0 for p,t in pending)
            cases+=1

here=Path(__file__).parent
receipt={
 'status':'PASS',
 'scope':'Exact replay of a safe legal history that defeats automatic-flushing inference',
 'maximum_leads_tested':{'from':9,'through':200},
 'post_transient_states_checked':cases,
 'one_announcement_per_round':True,
 'angel_stays_at_origin_and_survives':True,
 'relevant_pending_minimum_formula':'H-8',
 'heavy_time_spacing':9,
 'report_sha256':sha256((here/'REPORT.md').read_bytes()).hexdigest(),
}
(here/'PERIODIC_SCHEDULE_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
