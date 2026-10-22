#!/usr/bin/env python3
"""Corruption controls in disposable source-free packet copies."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parent
cases=['same_size_proof_mutation','missing_proof','extra_file','extra_directory','symlink_member','truncated_results']
def run(directory,optimized):
    args=[sys.executable,'-I','-B']
    if optimized:
        args.append('-O')
    args += [str(directory/'verify_packet.py'),'--replay']
    return subprocess.run(args,cwd=directory.parent,capture_output=True)

with tempfile.TemporaryDirectory(prefix='boundary-frequency-controls-') as tmp:
    base=Path(tmp)
    for optimized in (False,True):
        baseline=base/('baseline_'+str(optimized))
        shutil.copytree(root,baseline)
        outcome=run(baseline,optimized)
        if outcome.returncode:
            raise RuntimeError('Clean baseline failed: '+outcome.stderr.decode())
        for name in cases:
            p=base/(name+'_'+str(optimized))
            shutil.copytree(root,p)
            if name=='same_size_proof_mutation':
                q=p/'PROOF.md';b=q.read_bytes();q.write_bytes(bytes([b[0]^1])+b[1:])
            elif name=='missing_proof':
                (p/'PROOF.md').unlink()
            elif name=='extra_file':
                (p/'unexpected.txt').write_text('unexpected')
            elif name=='extra_directory':
                (p/'unexpected').mkdir()
            elif name=='symlink_member':
                q=p/'PROOF.md';q.unlink();q.symlink_to(root/'PROOF.md')
            elif name=='truncated_results':
                q=p/'check_results.json';q.write_bytes(q.read_bytes()[:-1])
            result=run(p,optimized)
            if result.returncode==0:
                raise RuntimeError('Undetected corruption: '+name)
print(json.dumps({'status':'PASS','baseline_replays':2,'rejected_corruptions':2*len(cases),'cases':cases},sort_keys=True))
