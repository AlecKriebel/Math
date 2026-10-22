#!/usr/bin/env python3
"""Independent audit-integrity negative controls; modifies disposable copies only."""
import hashlib,importlib.util,json,shutil,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
root=Path(__file__).parent
spec=importlib.util.spec_from_file_location('audit_verifier',root/'verify_audit.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def manifest_change(d,fn):
    p=d/'MANIFEST.json';obj=json.loads(p.read_text());fn(obj);p.write_text(json.dumps(obj))

def main():
    anchor=hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()
    v.verify_directory(root,anchor)
    tests=[
      ('changed payload',lambda d:(d/'AUDIT.md').write_text((d/'AUDIT.md').read_text()+'X'),False),
      ('missing payload',lambda d:(d/'AUDIT.md').unlink(),False),
      ('extra payload',lambda d:(d/'unexpected.txt').write_text('extra'),False),
      ('payload symlink',lambda d:((d/'AUDIT.md').unlink(),(d/'AUDIT.md').symlink_to('STATUS.json')),False),
      ('directory symlink',lambda d:(d/'link').symlink_to('.',target_is_directory=True),False),
      ('manifest symlink',lambda d:((d/'MANIFEST.json').unlink(),(d/'MANIFEST.json').symlink_to('STATUS.json')),False),
      ('changed external manifest anchor',lambda d:(d/'MANIFEST.json').write_text((d/'MANIFEST.json').read_text()+' '),False),
      ('duplicate path with recomputed test anchor',lambda d:manifest_change(d,lambda m:m['files'].append(m['files'][0])),True),
      ('traversal path with recomputed test anchor',lambda d:manifest_change(d,lambda m:m['files'][0].update(path='../escape')),True),
      ('absolute path with recomputed test anchor',lambda d:manifest_change(d,lambda m:m['files'][0].update(path='/escape')),True),
      ('duplicate JSON key with recomputed test anchor',lambda d:(d/'MANIFEST.json').write_text('{"schema":"sha256-bytes-v1","schema":"sha256-bytes-v1","files":[]}'),True)
    ]
    out=[]
    for name,change,reanchor in tests:
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)/'audit';shutil.copytree(root,d);change(d)
            expected=hashlib.sha256((d/'MANIFEST.json').read_bytes()).hexdigest() if reanchor else anchor
            try:v.verify_directory(d,expected)
            except Exception as e:out.append({'mutation':name,'rejected':True,'reason':str(e)})
            else:raise ValueError('accepted corruption: '+name)
    result={'status':'PASS','control_count':len(out),'controls':out,'scope':'integrity only, not mathematical proof'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
