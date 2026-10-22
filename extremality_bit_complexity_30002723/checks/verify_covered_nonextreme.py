"""Replay one stored exact continuous covered/non-extreme example; no LP discovery."""
from pathlib import Path
from fractions import Fraction
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'structural'))
from test_continuous_reduction import coarse_reduce,dense_ref
p=Path(__file__).resolve().parents[1]/'structural'/'COVERED_NONEXTREME_TEST.json'
data=json.loads(p.read_text())
values=list(map(Fraction,data['values']))
assert len(values)==data['q']
assert values[0]==0 and values[data['f']]==1
assert all(values[i]+values[(data['f']-i)%len(values)]==1 for i in range(len(values)))
assert all(values[i]+values[j]>=values[(i+j)%len(values)] for i in range(len(values)) for j in range(len(values)))
assert coarse_reduce(values,data['f'])==data['compressed']
assert dense_ref(values,data['f'])==data['reference']
print(json.dumps({'status':'PASS','saved_exact_case_count':1,'nullity':data['reference']['nullity']}))
