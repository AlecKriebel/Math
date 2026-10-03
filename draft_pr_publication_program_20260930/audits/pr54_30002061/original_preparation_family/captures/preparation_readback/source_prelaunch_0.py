#!/usr/bin/env python3
"""Preparer readback of complete source bodies, streams and immutable raw pins."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
from packet_common import HERE,load,pin,validate_content
checks=validate_content();account=load(HERE/'SOURCE_ACCOUNTING.json')
for row in account['raw_corpus_references'].values():
    p=Path(row['path']);h=hashlib.sha256()
    with p.open('rb') as f:
        while True:
            b=f.read(1048576)
            if not b:break
            h.update(b)
    assert p.stat().st_size==row['bytes'] and h.hexdigest()==row['sha256'];checks+=1
external=HERE.parents[1]/'pr45_9900007/root_pr54_initial_metadata_readonly_actual_capture'
assert external.is_dir()
pins=[pin(p) for p in sorted(external.iterdir()) if p.is_file()]
assert len(pins)==4;checks+=1
for p in (HERE/'original').rglob('*'):
    if p.is_file():
        b=p.read_bytes();b.decode('utf-8');checks+=1
        if p.suffix=='.json':json.loads(b);checks+=1
for d in (HERE/'captures').iterdir():
    if d.is_dir() and (d/'CAPTURE.json').exists():
        for name in ['CAPTURE.json','stdout.bin','stderr.bin','operator_prelaunch.py']:
            (d/name).read_bytes();checks+=1
assert not (HERE/'SELF_MANIFEST.json').exists();checks+=1
out={'schema':'pr54-original-preparer-source-readback/v1','actual_verifier_pid':os.getpid(),
 'utc':datetime.now(timezone.utc).isoformat(),'source_integrity_checks':checks,
 'immutable_external_ROOT_metadata_pins':pins,'original_science_file_count':19,
 'complete_original_diff_file_count':20,'source_body_and_stream_readback':True,
 'new_mathematical_verdict':None,'ROOT_closer_or_reader_executed':False,
 'native_or_remote_acceptance':False,'raw_corpus_references_rehashed_in_place':True}
(HERE/'SOURCE_READBACK.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
