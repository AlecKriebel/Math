#!/usr/bin/env python3
"""Independent Burnside count. Supports are bitmasks; no minimum-key cache."""
from itertools import permutations,product,combinations
import json
from pathlib import Path
from independent_controls import connected,positions

CASES=[('K2_2_2',[2,2],[(0,1),(0,1)]),('D4_2_1_1_1',[2,1,1,1],[(1,0),(2,0),(3,0)]),('A2_2_1_nonroot',[2,1],[(0,1)]),('affine_D4_3_2_2_1_1',[3,2,2,1,1],[(1,0),(2,0),(3,0),(4,0)])]
results={}
for name,d,arrows in CASES:
    slots=positions(d,arrows);index={e:i for i,e in enumerate(slots)}
    trees=[es for es in combinations(slots,sum(d)-1) if connected(d,arrows,es)]
    supports=[sum(1<<index[e] for e in es) for es in trees]
    fixed=[]
    for perm in product(*[list(permutations(range(n))) for n in d]):
        action=[index[(a,perm[arrows[a][1]][r],perm[arrows[a][0]][c])] for a,r,c in slots]
        fixed.append(sum(sum(1<<action[index[e]] for e in es)==mask for es,mask in zip(trees,supports)))
    assert sum(fixed)%len(fixed)==0
    results[name]={'group_order':len(fixed),'fixed_tree_counts':fixed,'basis_permutation_orbits':sum(fixed)//len(fixed),'labelled_supports':len(trees)}
print(json.dumps(results,indent=2))
Path(__file__).with_name('orbit_results.json').write_text(json.dumps(results,indent=2)+'\n')
