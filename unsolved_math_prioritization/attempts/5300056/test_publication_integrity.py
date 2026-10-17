#!/usr/bin/env python3
"""Run non-destructive mutations against fresh copies of the publication."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parent
PIN=hashlib.sha256((ROOT/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()
def append(root,name):
    p=root/name;p.write_bytes(p.read_bytes()+b'\nmutation')
def remove(root,name):(root/name).unlink()
def add(root,name):(root/name).write_bytes(b'unexpected')
def mkdir(root,name):(root/name).mkdir()
def symlink(root,name):(root/name).symlink_to(root/'README.md')
CASES=[('proof_change',lambda r:append(r,'author_v2/PROOF.md')),
 ('v1_change',lambda r:append(r,'author_v1/PROOF.md')),
 ('code_change',lambda r:append(r,'author_v2/verify.py')),
 ('result_change',lambda r:append(r,'author_v2/verification_results.json')),
 ('prior_audit_change',lambda r:append(r,'independent_audit/AUDIT.md')),
 ('acceptance_change',lambda r:append(r,'delta_acceptance/ACCEPTANCE.md')),
 ('full_patch_change',lambda r:append(r,'delta_acceptance/FULL_DELTA.patch')),
 ('missing_revision',lambda r:remove(r,'author_v2/REVISION_PROVENANCE.json')),
 ('archive_change',lambda r:append(r,'archives/JACOBIAN_COCYCLE_5300056_V2_SAFE_FREEZE.zip')),
 ('unexpected_file',lambda r:add(r,'extra.txt')),
 ('unexpected_directory',lambda r:mkdir(r,'unexpected')),
 ('unexpected_symlink',lambda r:symlink(r,'shortcut')),
 ('scope_change',lambda r:append(r,'PUBLICATION_STATUS.json')),
 ('manifest_change',lambda r:append(r,'PUBLICATION_MANIFEST.json'))]
results={}
with tempfile.TemporaryDirectory(prefix='jacobian publication mutations ') as tmp:
    for name,mutate in CASES:
        dest=Path(tmp)/name;shutil.copytree(ROOT,dest);mutate(dest)
        args=[sys.executable]+(['-O'] if sys.flags.optimize else [])+['-B',str(dest/'verify_publication.py'),'--expected-manifest-sha256',PIN,'--integrity-only']
        p=subprocess.run(args,cwd=tmp,capture_output=True,text=True)
        if p.returncode==0:raise SystemExit('Mutation accepted: '+name)
        results[name]='REJECTED'
print(json.dumps({'status':'PASS','controls':results,'rejected':len(results)},indent=2,sort_keys=True))
