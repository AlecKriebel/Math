"""Read-only evidence consistency checker for foster_recheck_02."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
m=json.loads((p/'EVIDENCE_MANIFEST.json').read_text())
n=0
for e in m['files']:
    b=(p/e['path']).read_bytes()
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
    n+=1
integrity=json.loads((p/'REPLAY_AND_SOURCE_INTEGRITY.json').read_text())
root=p.parents[1]
for e in integrity['source_files']:
    b=(root/e['path']).read_bytes()
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
    assert e['matches_snapshot']
    n+=1
x=json.loads((p/'exact_falsification_output.json').read_text())
r=json.loads((p/'FINAL_REVIEW.json').read_text())
assert x['assertions']==315600==r['new_exact_assertions']
assert sum(x['counts'].values())==x['assertions']
assert sum(z['states'] for z in x['loads'])==11330==r['new_state_evaluations']
assert len(x['negative_controls'])==20
assert r['exact_remaining_mathematical_gap'] is None and not r['publication_clearance']
for z in integrity['control_replays']:
    assert z['exit_code']==0 and z['status'].startswith('PASS')
    assert hashlib.sha256((p/z['output']).read_bytes()).hexdigest()==z['sha256']
    if 'equal_to_frozen_saved_output' in z: assert z['equal_to_frozen_saved_output']
print(json.dumps({'status':'PASS_REVIEW_EVIDENCE_CONSISTENCY','hashed_files_checked':n,
                  'new_exact_assertions':x['assertions'],'state_evaluations':11330,
                  'source_files_unchanged':40,'scope':'Evidence integrity and consistency, not a substitute for mathematical verification.'},sort_keys=True))
