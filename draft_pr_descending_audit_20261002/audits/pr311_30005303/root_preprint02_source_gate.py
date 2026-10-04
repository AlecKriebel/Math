"""Authenticate the source-only freeze and release precisely named immutable inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat, zipfile

A = Path(__file__).resolve().parent
R = A / 'preprint_review_02'
Q = A / 'preprint_package_v02'
O = A / 'submission_v02'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()

def pin(p):
    return {'path': str(p), 'bytes': p.stat().st_size,
            'sha256': sha(p.read_bytes()), 'mode': format(stat.S_IMODE(p.stat().st_mode), '04o')}

def check(p, expected, mode=None):
    got = pin(p)
    for k in ['bytes', 'sha256']:
        if k in expected:
            assert got[k] == expected[k], (str(p), k, got[k], expected[k])
    if mode or 'mode' in expected:
        assert got['mode'] == (mode or expected['mode']), got
    return got

source_pins = {
    'SOURCE_ONLY_CRITERIA.md': '859686a09d3de0ada933168b46326e7236cd4a345dd841af30df6208e92eb2c0',
    'FIRST_INDEPENDENT_CONCLUSION.md': '1536e88664d32c1a81667c8727713f7aa4d20858bf848cada96c6b54721ca8ba',
    'SOURCE_ONLY_FREEZE_MANIFEST.json': '971d6696d0edf0c765865d5fc8402eaf849f0f1d38e2ecce23bf0648b29ebeab',
    'SOURCE_ONLY_FREEZE_VERIFICATION.json': '79a1202dee1926c185c5d5bccc413260d5d65c3169f56bea7c84d9036e8b1ea3'}
gate = [check(R/n, {'sha256': h}, '0444') for n,h in source_pins.items()]
m = json.loads((R/'SOURCE_ONLY_FREEZE_MANIFEST.json').read_text())
v = json.loads((R/'SOURCE_ONLY_FREEZE_VERIFICATION.json').read_text())
assert not m['candidate_access'] and not m['external_communication']
rows = m['reports'] + m['private_evidence']
assert len(rows) == 27 and len({r['path'] for r in rows}) == 27
assert v['result'] == 'PASS' and v['verified_entries'] == rows
check(R/'SOURCE_ONLY_FREEZE_MANIFEST.json', v['manifest'], '0444')
for r in rows:
    assert Path(r['path']).is_relative_to(R)
    check(Path(r['path']), r, '0444')
original = [r for r in rows if r['path'].endswith('EMS_OWR_2022_55_original.pdf')]
assert len(original) == 1 and original[0]['sha256'] == '56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65'

qm = check(Q/'MANIFEST.json', {'sha256': 'e08af5edc9c4aed6ccb4b92b3b2e8ea0505a02e762b27c31efbacf00d7b8f683'}, '0444')
q = json.loads((Q/'MANIFEST.json').read_text())
assert len(q) == 12
assert {str(p.relative_to(Q)) for p in Q.rglob('*') if p.is_file()} == set(q) | {'MANIFEST.json'}
package = [check(Q/n, r, '0444') for n,r in sorted(q.items())] + [qm]
om = check(O/'SUBMISSION_MANIFEST.json', {'sha256': '043de76e326db5b5ba1af7fe2c7442bef1eed2d04de36654605045ce61f40383'}, '0444')
o = json.loads((O/'SUBMISSION_MANIFEST.json').read_text())
assert o['source_package_manifest_sha256'] == qm['sha256']
assert len(o['formal_files']) == 4
assert {p.name for p in O.iterdir() if p.is_file()} == set(o['formal_files']) | {'SUBMISSION_MANIFEST.json'}
formal = [check(O/n, r, '0444') for n,r in sorted(o['formal_files'].items())] + [om]
assert o['archive_member_sha256'] == {str(Path(p['path']).relative_to(Q)): p['sha256'] for p in package}
with zipfile.ZipFile(O/'mtp2-edge-closure-verification.zip') as z:
    assert len(z.namelist()) == 13 and set(z.namelist()) == set(o['archive_member_sha256'])
    for n,h in o['archive_member_sha256'].items():
        assert sha(z.read(n)) == h and z.read(n) == (Q/n).read_bytes()
        assert stat.S_IMODE(z.getinfo(n).external_attr >> 16) == 0o644

builder = check(A/'root_build_preprint_v01.py', {'sha256': '85020339f2a629d3aafb62f63699c4e9c17be2997e910aaeb6630886663a5d03'})
historical = [builder]
jobs = json.loads((Q/'BUILD_RECEIPT.json').read_text())['native_jobs']
for label, current in zip(['compile','pdfinfo','extract','render'], jobs, strict=True):
    D = A/'preprint_build_private_v01'
    original_job = json.loads((D/(label+'_execution.json')).read_text())
    corrected = dict(original_job)
    corrected['orchestration_script_sha256'] = corrected.pop('program_sha256')
    assert corrected == current and corrected['orchestration_script_sha256'] == builder['sha256']
    historical.append(pin(D/(label+'_execution.json')))
    for stream in ['stdout','stderr']:
        historical.append(check(D/(label+'.'+stream), {'bytes': current[stream+'_bytes'], 'sha256': current[stream+'_sha256']}))
assert len(historical) == 13
out = {'recorded_utc': utc(), 'status': 'PASS_SOURCE_ONLY_GATE_EXACT_PACKAGE_SUBMISSION_AND_BUILD_EVIDENCE_RELEASE',
       'reviewer': '/root/pr311_preprint_02', 'source_gate_pins': gate,
       'source_only_frozen_entries_authenticated': 27,
       'root_read_scope': 'Complete source-only criteria and first conclusion read before this gate; evidence entries authenticated mechanically. No claim of full primary-source or stream reads at this gate.',
       'named_package_files': package, 'named_formal_submission_files': formal,
       'named_historical_build_evidence_files': historical,
       'release_scope': 'Exactly these 31 named files (13 package, 5 formal submission, 13 authentic historical build source/captures). Independent primary-source acquisition allowed. No root or sibling review verdicts or other candidate material released.',
       'package_review_complete': False, 'publication_ready': False, 'workflow_percent': 65}
p = A/'ROOT_PREPRINT02_SOURCE_GATE.json'
with p.open('x') as f:
    f.write(json.dumps(out, indent=2)+'\n')
print(json.dumps({'receipt':str(p),'sha256':sha(p.read_bytes()),'source_entries':27,
                  'released_files':len(package)+len(formal)+len(historical),
                  'actual_utc':out['recorded_utc'],'publication_ready':False},indent=2))
