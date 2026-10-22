#!/usr/bin/env python3
"""Verify audit binding and replay both portable test suites, without network access."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument('--submission',type=Path,default=Path(__file__).resolve().parent.parent/'submission')
a=p.parse_args();root=Path(__file__).resolve().parent;submission=a.submission.resolve()
def digest(path):
    data=path.read_bytes()
    return {'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
manifest=json.loads((root/'SHA256SUMS.json').read_text())
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json' and '__pycache__' not in p.parts}
assert actual==set(manifest['files']),{'unexpected':sorted(actual-set(manifest['files'])),'missing':sorted(set(manifest['files'])-actual)}
for name,binding in manifest['files'].items():
    path=root/name
    assert path.resolve().is_relative_to(root)
    assert digest(path)==binding,name
bound=json.loads((root/'INPUT_BINDING.json').read_text())
assert digest(submission/'SHA256SUMS.json')==bound['manifest_file']
assert json.loads((submission/'SHA256SUMS.json').read_text())==bound['manifest_contents']
for name,binding in bound['manifest_contents']['files'].items():
    path=submission/name
    assert path.resolve().is_relative_to(submission)
    assert digest(path)==binding,name
verified=json.loads(subprocess.check_output([sys.executable,str(submission/'verify_manifest.py')],cwd=submission,text=True))
author=json.loads(subprocess.check_output([sys.executable,str(submission/'verify.py')],cwd=submission,text=True))
assert verified['passed'] and verified['files_verified']==11
assert author==json.loads((root/'AUTHOR_REPLAY_RESULTS.json').read_text())
assert author==json.loads((submission/'CONTROL_RESULTS.json').read_text())
independent=json.loads(subprocess.check_output([sys.executable,str(root/'independent_checks.py')],cwd=root,text=True))
assert independent==json.loads((root/'INDEPENDENT_RESULTS.json').read_text())
print(json.dumps({'passed':True,'bound_submission_manifest_sha256':bound['manifest_file']['sha256'],'author_assertions':author['assertions'],'independent_assertions':independent['assertions'],'audit_files':len(manifest['files'])},indent=2))
