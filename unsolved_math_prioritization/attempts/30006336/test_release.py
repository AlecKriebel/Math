#!/usr/bin/env python3
"""Negative controls run only on temporary copies, never the frozen packet."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parent

def run(path):
    return subprocess.run([sys.executable,'-B','verify_release.py'],cwd=path,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
assert run(root).returncode==0
cases=('author_tamper','audit_tamper','release_tamper','missing_file','extra_file','unexpected_directory','symlink','traversal_manifest','extra_manifest_field')
results=[]
for name in cases:
    with tempfile.TemporaryDirectory(prefix='prismatic-packet-control-') as tmp:
        dest=Path(tmp)/'packet';shutil.copytree(root,dest)
        if name=='author_tamper':(dest/'author/README.md').write_text('altered\n')
        elif name=='audit_tamper':(dest/'audit/AUDIT_REPORT.md').write_text('altered\n')
        elif name=='release_tamper':(dest/'RELEASE_NOTES.md').write_text('altered\n')
        elif name=='missing_file':(dest/'audit/CORRECTIONS.md').unlink()
        elif name=='extra_file':(dest/'unexpected.txt').write_text('extra\n')
        elif name=='unexpected_directory':(dest/'extra').mkdir()
        elif name=='symlink':
            (dest/'author/README.md').unlink();(dest/'author/README.md').symlink_to(dest/'README.md')
        else:
            file=dest/'RELEASE_BINDING.json';data=json.loads(file.read_text())
            if name=='traversal_manifest':data['files']['../outside']=data['files'].pop('README.md')
            else:data['unexpected']='extra'
            file.write_text(json.dumps(data))
        r=run(dest);assert r.returncode!=0,f'Unexpected acceptance: {name}'
        results.append({'case':name,'rejected':True})
print(json.dumps({'baseline_pass':True,'negative_controls':results,'all_rejected':True},sort_keys=True))
