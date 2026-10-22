#!/usr/bin/env python3
"""Read pinned public data only. Requires installed xlrd; no source executables."""
from pathlib import Path
import json,hashlib,sys,re
import xlrd
root=Path(__file__).resolve().parent
src=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent.parent/'sources'
m=json.loads((root/'SOURCE_ADDITION_TURN_5.json').read_text());pins={x['file']:x['sha256'] for x in m['sources']}
# Turn-4 table pins are immutable and reused.
pins.update({x['file']:x['sha256'] for x in json.loads((root/'SOURCE_ADDITION_TURN_4.json').read_text())['sources']})
for f in ['knotinfo_data_complete.xls','12mut.out','13mut.out']:
 assert hashlib.sha256((src/f).read_bytes()).hexdigest()==pins[f],f
s=xlrd.open_workbook(src/'knotinfo_data_complete.xls',on_demand=True).sheet_by_index(0)
h=s.row_values(0);rows={s.cell_value(i,0):dict(zip(h,s.row_values(i))) for i in range(2,s.nrows)}
def bounds(v):
 if isinstance(v,(int,float)):
  assert int(v)==v;return int(v),int(v)
 a=[int(x) for x in re.findall(r'\d+',v)];assert a;return min(a),max(a)
groups=[]
for n in [12,13]:
 for block in (src/f'{n}mut.out').read_text().strip().split('\n\n'):
  names=[]
  for line in block.splitlines():
   k,idx,*dt=map(int,line.split());off={11:367,12:1288,13:4878}[k]
   names.append(f'{k}{"a" if idx<=off else "n"}_{idx if idx<=off else idx-off}')
  groups.append(names)
different=[];disjoint=[];controls=0
for g in groups:
 vals=[bounds(rows[name]['unknotting_number']) for name in g];controls+=len(g)
 if len(set(vals))>1:different.append({'knots':g,'displayed_intervals':vals,'reference_cells':[str(rows[name]['unknotting_number_anon']) for name in g]})
 if max(x[0] for x in vals)>min(x[1] for x in vals):disjoint.append(g)
controls+=len(groups)
# Bind the positive certificate's source word, without claiming the DT identification was recomputed.
source_word=json.loads(rows['11n_78']['braid_notation']);cert=json.loads((root/'braid_upper_certificate.json').read_text());assert source_word==cert['source_word'];controls+=1
print(json.dumps({'status':'PASS_PINNED_DATA_SCREEN_ONLY','groups_joined':len(groups),'knot_rows_joined':sum(map(len,groups)),'exact_data_controls':controls,'groups_with_different_displayed_intervals':different,'groups_with_disjoint_displayed_intervals':disjoint,'source_word_matches_certificate':True,'scope':'A snapshot data join, not independent proofs of the table unknotting values, mutation identifications, completeness, or absence of an actual counterexample. The sole differing pair has an unverified lower-bound provenance.'},indent=2))
