#!/usr/bin/env python3
"""Run manifest negative controls in disposable copies, never mutate the packet."""
import json,pathlib,shutil,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parent
controls=[]
with tempfile.TemporaryDirectory(prefix='seshadri_integrity_') as tmp:
    parent=pathlib.Path(tmp)
    def trial(name, mutate):
        dst=parent/name
        shutil.copytree(root,dst)
        mutate(dst)
        p=subprocess.run([sys.executable,str(dst/'verify_manifest.py')],capture_output=True,text=True)
        if (p.returncode==0)!=(name=='baseline'):
            raise AssertionError((name,p.returncode,p.stdout,p.stderr))
        controls.append({'name':name,'expected':'accept' if name=='baseline' else 'reject','observed':'accept' if p.returncode==0 else 'reject'})
    trial('baseline',lambda p:None)
    trial('changed_byte',lambda p:(p/'README.md').write_bytes((p/'README.md').read_bytes()+b'x'))
    trial('missing_file',lambda p:(p/'PROOFS.md').unlink())
    trial('unexpected_file',lambda p:(p/'unexpected.txt').write_text('x'))
    def nested(p):
        (p/'nested').mkdir();(p/'nested/MANIFEST.json').write_text('{}')
    trial('nested_manifest',nested)
    def sym(p):
        (p/'PROOFS.md').unlink();(p/'PROOFS.md').symlink_to('README.md')
    trial('symlink_file',sym)
    def unsafe(p):
        x=json.loads((p/'MANIFEST.json').read_text());x['files'][0]['path']='../outside.txt';(p/'MANIFEST.json').write_text(json.dumps(x))
    trial('unsafe_path',unsafe)
print(json.dumps({'status':'PASS','controls':controls},indent=2,sort_keys=True))
