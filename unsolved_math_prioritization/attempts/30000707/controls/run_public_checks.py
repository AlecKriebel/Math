#!/usr/bin/env python3
"""Strict safe public inventory plus all 36 unchanged independent mathematical checks."""
from pathlib import Path
import contextlib, hashlib, io, json, tempfile
ROOT=Path(__file__).resolve().parents[1]
SCRIPT_HASH='7e18dd98b757e569577e8e4e9c1f041fcd27700723324abafafa3a6ef9c0643f'
RESULTS_HASH='f174d4f98e13b057e8f67260c57bfe4d790cbb6e022139bff47853551b786e86'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'PUBLIC_PAYLOADS.json').read_text())
assert manifest['scope']=='safe public payloads excluding inventory, replay receipt and outer manifest'
expected={row['path'] for row in manifest['files']}
assert len(expected)==len(manifest['files'])
actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
assert actual-{'PUBLIC_PAYLOADS.json','PUBLIC_REPLAY.json','RELEASE_SHA256SUMS'}==expected, 'public allowlist mismatch'
for row in manifest['files']:
    p=ROOT/row['path']
    assert not p.is_symlink() and '..' not in Path(row['path']).parts
    assert not any(part in ['private','rerun'] for part in Path(row['path']).parts)
    assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'], 'payload mismatch: '+row['path']
script=ROOT/'audit/controls/independent_checks.py'
result_path=ROOT/'audit/controls/INDEPENDENT_RESULTS.json'
assert sha(script)==SCRIPT_HASH and sha(result_path)==RESULTS_HASH
held=json.loads(result_path.read_text());assert held['check_count']==36
with tempfile.TemporaryDirectory(prefix='four-value-public-replay-') as td:
    td=Path(td);(td/'controls').mkdir()
    filename=td/'controls/independent_checks.py'
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(script.read_text(),str(filename),'exec'),{'__file__':str(filename),'__name__':'__main__'})
    replay=json.loads((td/'controls/INDEPENDENT_RESULTS.json').read_text())
assert replay['check_count']==36 and replay['checks']==held['checks'], 'mathematical result records differ'
assert sha(script)==SCRIPT_HASH and sha(result_path)==RESULTS_HASH
print(json.dumps({'status':'PASS','public_payload_files':len(expected),'historical_checks':45,
'historical_private_integrity_checks':9,'portable_mathematical_checks':36,'same_mathematical_records':True,
'projected_files_unchanged':True,'python':replay['python'],'sympy':replay['sympy'],
'scope':'Safe public inventory and the same 36 mathematical checks; no full classification.'},sort_keys=True))
