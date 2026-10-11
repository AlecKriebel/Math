#!/usr/bin/env python3
"""Verify the owned audit evidence before a self-only immutable closure."""
import datetime as dt
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
captures=[]
for name,expected in [('complex_checks_actual_capture',1),('complex_checks_repaired_actual_capture',0),('input_bindings_actual_capture',0)]:
    directory=root/name
    receipt=json.loads((directory/'CAPTURE.json').read_bytes())
    assert receipt['exit_code']==expected
    assert receipt['actual_pid']>0
    start=dt.datetime.fromisoformat(receipt['started_utc'])
    finish=dt.datetime.fromisoformat(receipt['finished_utc'])
    assert start.utcoffset()==finish.utcoffset()==dt.timedelta(0) and finish>=start
    assert sha((directory/'prelaunch_source.py').read_bytes())==receipt['source_sha256']
    assert sha((directory/'prelaunch_operator.py').read_bytes())==receipt['operator_sha256']
    for stream in ['stdout','stderr']:
        raw=(directory/(stream+'.bin')).read_bytes()
        assert sha(raw)==receipt[stream+'_sha256'] and len(raw)==receipt[stream+'_bytes']
    assert receipt['source_unchanged'] and receipt['complete_streams']
    captures.append({'capture':name,'actual_pid':receipt['actual_pid'],'exit_code':expected,'validated_complete_streams':True})
out=json.loads((root/'complex_checks_repaired_actual_capture/stdout.bin').read_bytes())
assert out['passed']==101 and out['failed']==0 and len(out['checks'])==101
assert set(out['checks'].values())=={'PASS'}
bindings=json.loads((root/'ORIGINAL_INPUT_BINDINGS.json').read_bytes())
assert bindings['original_scientific_files_read']==13
for row in bindings['bindings']:
    p=Path(row['path']);raw=p.read_bytes()
    assert sha(raw)==row['sha256'] and len(raw)==row['bytes'] and p.stat().st_mode & 0o7777==0o444
assert 'No mandatory correction' in (root/'COMPLEX_DYNAMICS_AUDIT.md').read_text()
assert all(not p.is_symlink() for p in root.rglob('*'))
initial=root/'INDEPENDENT_PRE_SOURCE_DERIVATION.md'
summary={'schema':'pr46-complex-dynamics-closure-check/v1','mathematical_claim_verified':True,
 'mandatory_mathematical_corrections':[],'mathematical_remaining_gap':'none identified for exact sufficient existence claim',
 'acceptance_verdict':None,'original_head':bindings['head'],'original_scientific_files':13,
 'independent_exact_controls_passed':101,'preserved_failed_control_runs':1,
 'initial_derivation_original_mtime_utc':dt.datetime.fromtimestamp(initial.stat().st_mtime,dt.timezone.utc).isoformat(),
 'captures':captures,'foreign_raw_bodies_copied':False,'novel_discovery_credit_percent':0,
 'research_audit_completion_estimate_percent':100}
(root/'CLOSURE_CHECK.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
