#!/usr/bin/env python3
"""Verify the explicit own-root public manifest, seals and complete replay."""
from pathlib import Path
import hashlib,json

root=Path(__file__).resolve().parent
mf=json.loads((root/'PUBLIC_MANIFEST.json').read_text())
assert mf['self_excluded']=='PUBLIC_MANIFEST.json'
listed=set()
for row in mf['files']:
    p=Path(row['path'])
    assert not p.is_absolute() and '..' not in p.parts and 'private' not in p.parts
    assert p.as_posix()!='PUBLIC_MANIFEST.json' and p.as_posix() not in listed
    listed.add(p.as_posix())
    f=root/p
    assert f.is_file() and not f.is_symlink()
    raw=f.read_bytes()
    assert len(raw)==row['bytes']
    assert hashlib.sha256(raw).hexdigest()==row['sha256']
for value in json.loads((root/'SEALS.json').read_text()).values():
    assert hashlib.sha256((root/value['path']).read_bytes()).hexdigest()==value['sha256']
replay=json.loads((root/'AUTHOR_REPLAY_RECEIPTS.json').read_text())
assert replay['all_five_complete'] and replay['all_exits_zero']
assert [r['turn'] for r in replay['receipts']]==[1,2,3,4,5]
assert sum(r['parsed_json']['assertions'] for r in replay['receipts'])==15618
for r in replay['receipts']:
    assert r['exit_code']==0 and r['stderr']=='' and r['parse_error'] is None
    assert json.loads(r['stdout'])==r['parsed_json']
    assert hashlib.sha256(r['stdout'].encode()).hexdigest()==r['stdout_sha256']
    assert hashlib.sha256(r['stderr'].encode()).hexdigest()==r['stderr_sha256']
history=json.loads((root/'HISTORY_SOURCE_AND_REPLAY_COMPARISON.json').read_text())
assert history['all_byte_identical'] and len(history['author_turn_history'])==5
controls=json.loads((root/'GEOMETRIC_CONTROL_RECEIPT.json').read_text())
assert controls['status']=='PASS' and controls['assertions']==3775
print(json.dumps({'status':'PASS','public_files':len(listed),'seals_valid':True,
                  'complete_author_replays':5,'author_assertions':15618,
                  'new_geometric_controls':3775},indent=2))
