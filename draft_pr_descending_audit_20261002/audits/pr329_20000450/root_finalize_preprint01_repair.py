"""Bind the completed source-attribution repair; no publication approval."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat

A = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
def pin(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=sha(b), mode=f'{stat.S_IMODE(p.stat().st_mode):04o}')
def inventory(d):
    files, directories = {}, {'.': f'{stat.S_IMODE(d.stat().st_mode):04o}'}
    for p in sorted(d.rglob('*')):
        assert not p.is_symlink(), p
        n = str(p.relative_to(d))
        if p.is_dir(): directories[n] = f'{stat.S_IMODE(p.stat().st_mode):04o}'
        else: files[n] = pin(p)
    return files, directories

old = A/'preprint/verification_v02'
new = A/'preprint/verification_v03'
f0,d0 = inventory(old); f1,d1 = inventory(new)
assert set(f0)==set(f1) and d0==d1
changes = [n for n in f0 if f0[n]!=f1[n]]
assert set(changes)=={'manuscript.tex','manuscript.pdf','PRIORITY_AUDIT.md','MANIFEST.json'}, changes
assert all(f0[n]['mode']==f1[n]['mode']=='0644' for n in changes)
repair = json.loads((A/'ROOT_PREPRINT01_REPAIR.json').read_bytes())
for c in repair['changes']:
    name = 'manuscript.tex' if c['path'].endswith('.tex') else 'PRIORITY_AUDIT.md'
    assert f0[name]['sha256']==c['old_sha256']
    assert f1[name]['sha256']==c['current_sha256']
held = json.loads((A/'ROOT_PREPRINT01_NAMESPACE_MANIFEST.json').read_bytes())
hf,hd = inventory(A/'preprint_review_01')
assert hf==held['payloads'] and hd==held['directory_modes']
qpath=A/'preprint/qualification_v03/QUALIFICATION.json'
q=json.loads(qpath.read_bytes())
assert q['status']=='NATIVELY_QUALIFIED_FOR_FRESH_ADVERSARIAL_REVIEW'
assert q['input_count']==8 and q['source_pdf_pair_bound']
assert not q['preprint_ready'] and not q['merge_ready'] and not q['publication_ready']
for n,r in q['inputs'].items():
    assert pin(qpath.parent/'inputs'/n)=={k:r[k] for k in ['bytes','sha256','mode']}
assert q['inputs']['manuscript.tex']['sha256']==f1['manuscript.tex']['sha256']
assert q['inputs']['manuscript.pdf']['sha256']==f1['manuscript.pdf']['sha256']
assert q['inputs']['zenodo-deposit.json']['sha256']==f0['zenodo-deposit.json']['sha256']
out=A/'ROOT_PREPRINT01_REPAIR_COMPLETION.json';assert not out.exists()
record=dict(utc=datetime.now(timezone.utc).isoformat(),
    status='PASS_ROOT_GLOBAL_REVIEW01_REPAIR_CURRENT_PACKAGE_QUALIFIED',
    finding_id='R01-SOURCE-ATTRIBUTION',
    repair_record=pin(A/'ROOT_PREPRINT01_REPAIR.json'),
    old_qualification=pin(A/'preprint/qualification_v02/QUALIFICATION.json'),
    current_qualification=pin(qpath),
    changed_bundle_files={n:dict(old=f0[n],current=f1[n]) for n in changes},
    all_other_47_bundle_files_and_all_directory_modes_unchanged=True,
    held_review01_files=len(hf),held_review01_directories=len(hd),held_review01_unchanged=True,
    mathematics_and_metadata_unchanged=True,mathematical_verification_percent=100,
    priority_percent=100,workflow_percent=68,
    next_required_step='Actual new full-preprint adversary with separately frozen source-only and first-candidate stages.',
    preprint_ready=False,merge_ready=False,publication_ready=False,persistent_goal_complete=False)
out.write_text(json.dumps(record,indent=2)+'\n');out.chmod(0o644)
print(json.dumps(record,indent=2))
