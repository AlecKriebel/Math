"""Independent orbit-index and projective-homogeneity audit of inert templates."""
from pathlib import Path
from itertools import product,permutations
from collections import Counter
from datetime import datetime,timezone
import json,ast,functools
b=Path(__file__).resolve().parents[3]/'sources/related-record-22064121/published-source/stc_jc_sharp_boundary_atlas_certificates_v1.1.7'
f=b/'strong_level2_phylo_identifiability/src/jc_root_spanning_atlas_data.py'
module=ast.parse(f.read_text());base=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INVARIANT_TEMPLATES' for t in n.targets))
sev=json.loads((b/'primary/seventh_invariant.json').read_text())['invariant'];templates=list(base)+[[(tuple(i+1 for i in mon),c) for c,mon in sev]]
autos=[(0,)+p for p in permutations((1,2,3))]
def canon(g):return min(tuple(a[i] for i in g) for a in autos)
reps=sorted({canon(g) for g in product(range(4),repeat=4) if functools.reduce(int.__xor__,g,0)==0});assert len(reps)==15
lookup={g:i for i,g in enumerate(reps)};allpolys=set()
def degree(mon):return tuple(sum(reps[j][i]!=0 for j in mon) for i in range(4))
for polynomial in templates:
 assert len({degree(mon) for mon,c in polynomial if c})==1
 for perm in permutations(range(4)):
  out=Counter()
  for mon,c in polynomial:
   mm=tuple(sorted(lookup[canon(tuple(reps[i][k] for k in perm))] for i in mon));out[mm]+=c
  out={m:c for m,c in out.items() if c};assert len({degree(m) for m in out})==1
  out=tuple(sorted(out.items()));sgn=1 if out[0][1]>0 else -1;allpolys.add(tuple((m,c*sgn) for m,c in out))
assert len(allpolys)==84
# Deliberately fail to shift the seventh invariant's nonconstant-coordinate indexing.
bad=[(tuple(mon),c) for c,mon in sev];assert len({degree(m) for m,c in bad if c})>1
Path(__file__).with_name('fresh-invariants.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','templates':7,'transported_polynomials':84,'all_port_multihomogeneous':True,'unshifted_seventh_index_negative_control_rejected':True},indent=2)+'\n')
print('PASS 7 templates, 84 transported polynomials, exact arm multihomogeneity, index-shift negative control')
