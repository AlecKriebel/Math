"""Read every bound closed JSON/JSONL input completely; execute no foreign code."""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

F=Path(__file__).resolve().parent
A=F.parent
R=A.parents[2]
inspection=json.loads((F/'INSPECTION_RESULT.json').read_bytes())
def strict(raw):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result: raise ValueError('duplicate key '+k)
            result[k]=v
        return result
    def constant(v): raise ValueError('nonfinite '+v)
    def floating(v):
        f=float(v)
        if not math.isfinite(f): raise ValueError('nonfinite float')
        return f
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
def visit(v):
    counts={}
    stack=[v]
    while stack:
        x=stack.pop()
        k=type(x).__name__
        counts[k]=counts.get(k,0)+1
        if type(x) is dict: stack.extend(x.values())
        elif type(x) is list: stack.extend(x)
    return counts
parsed=[]
for row in inspection['all_bound_files']:
    if not row['path'].startswith('draft_pr_publication_program_20260930/audits/pr42_2233/'):
        continue
    p=R/row['path']
    if p.suffix not in {'.json','.jsonl'}:
        continue
    raw=p.read_bytes()
    if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:
        raise ValueError('closed JSON changed '+row['path'])
    v=[strict(line) for line in raw.splitlines()] if p.suffix=='.jsonl' else strict(raw)
    parsed.append(dict(path=row['path'],bytes=len(raw),sha256=row['sha256'],type_counts=visit(v),schema=v.get('schema') if type(v) is dict else None,top_level_keys=sorted(v) if type(v) is dict else None))
result=dict(schema='PR42_CURRENT_SOURCE_ADVERSARY_COMPLETE_CLOSED_JSON_READ_v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='PASS_COMPLETE_STRICT_JSON_STRUCTURAL_READ',files_count=len(parsed),files=parsed,all_bytes_fully_parsed=True,all_keys_and_values_visited=True,builder_or_scientific_helper_import_compile_execute=False,semantic_claim_limit='Complete structural reading is not full semantic proof certification of imported external papers or every historical stdout. Current builder/contract/drafts/qualifications and original scoped proofs are separately reviewed.')
(F/'COMPLETE_CLOSED_JSON_READ.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],files_count=len(parsed),all_bytes_fully_parsed=True,all_keys_and_values_visited=True,builder_or_scientific_helper_import_compile_execute=False),indent=2))
