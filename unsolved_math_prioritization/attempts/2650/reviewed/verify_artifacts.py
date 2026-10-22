#!/usr/bin/env python3
"""Verify the corrected portable release and replay controls in a temporary copy."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
entries=manifest['files']
expected={e['path'] for e in entries}|{'MANIFEST.json'}
actual={p.name for p in base.iterdir() if p.is_file()}
assert actual==expected, {'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for e in entries:
    p=base/e['path']
    assert len(p.read_bytes())==e['bytes'],p.name
    assert digest(p)==e['sha256'],p.name
    assert p.suffix in {'.md','.json','.py'},p.name
original_pin='93334356491d6719b98b628ebb4b011fcb6438428b46e454935d544702fd1ff7'
audit_pin='5df150120443ae3ae0901407bff19dd2fa402cf10760ea692f655e2faa62b4e4'
assert digest(base/'AUTHOR_MANIFEST.json')==original_pin
assert digest(base/'INDEPENDENT_AUDIT.md')==audit_pin
initial=json.loads((base/'initial_audit_status.json').read_text())
assert initial['verdict']=='HOLD'
assert initial['audited_manifest_sha256']==original_pin
assert initial['report_sha256']==audit_pin
original={e['path']:e for e in json.loads((base/'AUTHOR_MANIFEST.json').read_text())['files']}
changes=json.loads((base/'CHANGE_MAP.json').read_text())
assert changes['original_manifest_sha256']==original_pin
assert changes['sixth_attempt'] is False
modified={e['path']:e for e in changes['modified_author_files']}
unchanged=set(changes['unchanged_author_files'])
assert set(original)==set(modified)|unchanged
assert not (set(modified)&unchanged)
for name,e in modified.items():
    assert e['original_sha256']==original[name]['sha256']
    assert e['release_sha256']==digest(base/name)
for name in unchanged:
    assert original[name]['sha256']==digest(base/name)
status=json.loads((base/'status.json').read_text())
assert status['numeric_id']==2650
assert status['substantive_attempts']==status['budget']==5
assert status['research_status']=='exhausted'
assert status['mathematical_status']=='unresolved'
assert status['full_candidate'] is False
assert status['novelty_established'] is False
assert status['sixth_attempt'] is False
assert status['remote_writes'] is False
assert {p.name for p in base.glob('turn_*.md')}=={f'turn_{i:02}.md' for i in range(1,6)}
assert 'For a faithful K-action' in (base/'turn_01.md').read_text()
assert 'Lemma E of Attempt 2' in (base/'turn_01.md').read_text()
assert 'checks/chain_obstruction.py' not in (base/'turn_04.md').read_text()
assert 'checks/power_commutator_frontier.py' not in (base/'turn_05.md').read_text()
with tempfile.TemporaryDirectory(prefix='kou-21-141-verify-') as temp:
    temp=Path(temp)
    for script in ('chain_obstruction.py','power_commutator_frontier.py'):
        shutil.copy2(base/script,temp/script)
        subprocess.run([sys.executable,str(temp/script)],check=True,cwd=temp)
        result=script.removesuffix('.py')+'_results.json'
        assert (temp/result).read_bytes()==(base/result).read_bytes(),result
# Replay must not modify any release file.
for e in entries:
    assert digest(base/e['path'])==e['sha256'],e['path']
print(json.dumps({'id':2650,'manifest_files':len(entries),'attempts':5,
                  'mathematical_status':'unresolved','checks_passed':True,
                  'initial_audit':'preserved HOLD','repair_review':'pending',
                  'scope':'Integrity, provenance and finite arithmetic only; not narrow mathematical review.'}))
