#!/usr/bin/env python3
"""Replay nine exact corruption controls without changing the release."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,shutil,tempfile
from pathlib import Path
root=Path(__file__).parent
spec=importlib.util.spec_from_file_location('vm',root/'verify_manifest.py')
vm=importlib.util.module_from_spec(spec);spec.loader.exec_module(vm)

def change_manifest(dst,fn):
    p=dst/'MANIFEST.json';d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d))

def run():
    vm.verify(root);results=[]
    muts=[
      ('modified bytes',lambda d:(d/'PROOF.md').write_bytes((d/'PROOF.md').read_bytes()+b'X')),
      ('deleted file',lambda d:(d/'PROOF.md').unlink()),
      ('extra file',lambda d:(d/'EXTRA.txt').write_text('unexpected')),
      ('duplicate manifest path',lambda d:change_manifest(d,lambda m:m['files'].append(m['files'][0].copy()))),
      ('path traversal',lambda d:change_manifest(d,lambda m:m['files'][0].update(path='../PROOF.md'))),
      ('absolute path',lambda d:change_manifest(d,lambda m:m['files'][0].update(path='/tmp/PROOF.md'))),
      ('symlink payload',lambda d:((d/'PROOF.md').unlink(),(d/'PROOF.md').symlink_to('README.md'))),
      ('nested manifest extra file',lambda d:((d/'extra').mkdir(),(d/'extra'/'MANIFEST.json').write_text('{}'))),
      ('manifest symlink',lambda d:((d/'MANIFEST.json').unlink(),(d/'MANIFEST.json').symlink_to('README.md')))
    ]
    for label,mutation in muts:
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'release';shutil.copytree(root,d);mutation(d)
            try:vm.verify(d)
            except Exception as e:results.append({'mutation':label,'rejected':True,'reason':str(e)})
            else:raise ValueError('accepted mutation '+label)
    return {'status':'PASS','controls':results,'scope':'integrity corruption tests, not mathematical proof'}
if __name__=='__main__':
    out=run();recorded=json.loads((root/'MANIFEST_TESTS.json').read_text())
    if out!=recorded:raise ValueError('control results differ from recorded results')
    print(json.dumps(out,indent=2,sort_keys=True))
