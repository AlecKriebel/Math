#!/usr/bin/env python3
"""Replay this audit with the unchanged candidate directory as the argument."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,shutil
root=Path(__file__).resolve().parent
submission=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'submission'
def sha(data): return hashlib.sha256(data).hexdigest()
inputs=json.loads((root/'AUDITED_INPUTS.json').read_text())
expected={r['path']:r for r in inputs['files']}
actual={str(p.relative_to(submission)) for p in submission.rglob('*') if p.is_file() or p.is_symlink()}
assert actual==set(expected), 'Candidate inventory differs'
for name,row in expected.items():
    p=submission/name
    assert not p.is_symlink(),name
    b=p.read_bytes()
    assert len(b)==row['bytes'] and sha(b)==row['sha256'],name
assert sum(x['bytes'] for x in inputs['files'])==37232

def run_json(p):
    r=subprocess.run([sys.executable,'-B',str(p)],capture_output=True,text=True,check=True)
    return json.loads(r.stdout)
author=run_json(submission/'verify.py')
assert author==json.loads((submission/'CONTROL_RESULTS.json').read_text()),'Author replay differs from recorded result'
manifest=run_json(submission/'verify_manifest.py')
independent=run_json(root/'independent_checks.py')
assert independent==json.loads((root/'INDEPENDENT_CHECK_RESULTS.json').read_text()),'Independent replay differs'
controls={}
# Mutations are made only in temporary copies, never in the candidate.
for mutation in ['edited_proof','extra_file','missing_file','same_bytes_symlink']:
    with tempfile.TemporaryDirectory(prefix='rank643-audit-') as tmp:
        copy=Path(tmp)/'submission'; shutil.copytree(submission,copy)
        if mutation=='edited_proof':
            with (copy/'FULL_PROOF.md').open('ab') as f:f.write(b'\n')
        elif mutation=='extra_file':(copy/'EXTRA.txt').write_text('audit control\n')
        elif mutation=='missing_file':(copy/'CONTROL_RESULTS.json').unlink()
        elif mutation=='same_bytes_symlink':
            (copy/'FULL_PROOF.md').unlink();(copy/'FULL_PROOF.md').symlink_to(submission/'FULL_PROOF.md')
        r=subprocess.run([sys.executable,'-B',str(copy/'verify_manifest.py')],capture_output=True,text=True)
        controls[mutation]=r.returncode!=0
assert all(controls.values())
# Verify that all original bytes still match after replay and mutations.
for name,row in expected.items():
    assert sha((submission/name).read_bytes())==row['sha256'],name
print(json.dumps({'result':'PASS','candidate_files':len(expected),'candidate_bytes':37232,'candidate_manifest_sha256':expected['MANIFEST.json']['sha256'],'candidate_proof_sha256':expected['FULL_PROOF.md']['sha256'],'original_manifest_replay':manifest,'original_exact_checks':author['exact_checks'],'original_negative_controls_passed':len(author['negative_controls']),'independent_exact_checks':independent['new_exact_checks'],'independent_algebra_controls_passed':len(independent['additional_negative_controls']),'manifest_mutation_controls':controls,'candidate_unchanged_after_replay':True},indent=2,sort_keys=True))
