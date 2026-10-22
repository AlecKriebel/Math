#!/usr/bin/env python3
"""Adversarial acceptance-verifier controls in disposable copies."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
if sys.flags.optimize:raise SystemExit('Optimized Python is not supported.')
root=Path(__file__).resolve().parents[1]
anchor=hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()
results={}
with tempfile.TemporaryDirectory(prefix='hairs_delta_integrity_') as tmp:
    def case(name,mutate=None,flags=(),success=False):
        p=Path(tmp)/name;shutil.copytree(root,p)
        if mutate:mutate(p)
        r=subprocess.run([sys.executable,*flags,'-B',str(p/'verify.py'),'--expected-manifest',anchor],capture_output=True,timeout=120)
        if (r.returncode==0)!=success:raise RuntimeError('Unexpected result: '+name)
        results[name]='PASS_ACCEPTED' if success else 'PASS_REJECTED'
    case('relocated_replay',success=True)
    case('changed_acceptance',lambda p:(p/'ACCEPTANCE.md').write_text('altered'))
    case('missing_result',lambda p:(p/'ACCEPTANCE.json').unlink())
    case('extra_file',lambda p:(p/'extra.txt').write_text('extra'))
    case('extra_directory',lambda p:(p/'extra').mkdir())
    case('symlink',lambda p:(p/'link').symlink_to(p/'README.md'))
    def coherent(p):
        (p/'ACCEPTANCE.md').write_text('altered');m=json.loads((p/'MANIFEST.json').read_text())
        for row in m['files']:
            b=(p/row['path']).read_bytes();row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
        (p/'MANIFEST.json').write_text(json.dumps(m))
    case('coherent_rewrite_external_anchor',coherent)
    case('optimized_O',flags=('-O',))
    case('optimized_OO',flags=('-OO',))
print(json.dumps({'result':'PASS_ACCEPTANCE_INTEGRITY_CONTROLS','cases':results,'original_inputs_modified':False},indent=2,sort_keys=True))
