#!/usr/bin/env python3
"""Replay author code, compare all product values, and mutation-test copies.

This is explicitly author-code replay, separate from the independent verifier.
It never edits the author's directory or source ZIP and makes no network calls.
"""
from pathlib import Path
import hashlib
import json
import runpy
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
AUTHOR=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE.parent/'polynomial_2200006'

def fingerprint(root):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir()}

def main():
    before=fingerprint(AUTHOR)
    receipt={}
    with tempfile.TemporaryDirectory(prefix='sos-audit-') as td:
        t=Path(td)
        valid=subprocess.run([sys.executable,'-B',str(AUTHOR/'verify_package.py')],cwd=t,capture_output=True,check=True)
        receipt['author_replay_unrelated_cwd']={'returncode':valid.returncode,'result':json.loads(valid.stdout)}
        tests={
          'changed_proof_bytes':lambda q:(q/'PROOFS.md').write_bytes((q/'PROOFS.md').read_bytes()+b'\n'),
          'changed_frozen_count':lambda q:(q/'results.json').write_text((q/'results.json').read_text().replace('1152','1153',1)),
          'extra_file':lambda q:(q/'extra.txt').write_text('unexpected'),
          'missing_file':lambda q:(q/'APPROACHES.md').unlink(),
          'symlink':lambda q:(q/'extra.link').symlink_to('README.md'),
        }
        receipt['mutation_rejections']=[]
        for name,fn in tests.items():
            target=t/name
            shutil.copytree(AUTHOR,target)
            fn(target)
            run=subprocess.run([sys.executable,'-B',str(target/'verify_package.py')],cwd=t,capture_output=True)
            if run.returncode==0:
                raise AssertionError('Author verifier accepted '+name)
            receipt['mutation_rejections'].append({'mutation':name,'rejected':True,'returncode':run.returncode})
        independent=subprocess.run([sys.executable,'-B',str(HERE/'verify_independent.py'),str(AUTHOR)],cwd=t,capture_output=True,check=True)
        same=independent.stdout==(HERE/'independent_results.json').read_bytes()
        if not same:
            raise AssertionError('Independent receipt differs')
        receipt['independent_replay_unrelated_cwd']={'returncode':0,'byte_identical_to_receipt':same}
        expected=json.loads(independent.stdout)['restricted_product_optima_all_dimensions']
        author_values=runpy.run_path(str(AUTHOR/'verify_math.py'))['best_blocks'](60)[0]
        if author_values!=expected:
            raise AssertionError('Full author product series differs from independent knapsack')
        receipt['all_author_product_values_compared']=61
    if before!=fingerprint(AUTHOR):
        raise AssertionError('Author freeze changed')
    receipt['freeze_preserved']=True
    return receipt

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
