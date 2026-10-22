#!/usr/bin/env python3
"""Publication-specific mutation controls; all mutations stay in temp copies."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verifier',ROOT/'verify_publication.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
PIN=hashlib.sha256((ROOT/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()

def tests():
    v.integrity(ROOT,PIN)
    out=[]
    names=['changed_payload','missing_payload','extra_file','extra_directory','symlink_payload',
           'rebound_publication_manifest','wrong_external_pin','damaged_zip','changed_author_copy']
    for name in names:
        with tempfile.TemporaryDirectory(prefix='triangle-spread-publication-control-') as td:
            root=Path(td)/'packet';shutil.copytree(ROOT,root)
            target=root/'README.md';pin=PIN
            if name in ['changed_payload','rebound_publication_manifest']:
                target.write_bytes(target.read_bytes()+b'mutation\n')
            elif name=='missing_payload': target.unlink()
            elif name=='extra_file': (root/'EXTRA').write_text('unexpected')
            elif name=='extra_directory': (root/'EXTRA').mkdir()
            elif name=='symlink_payload': target.unlink();target.symlink_to(ROOT/'README.md')
            elif name=='wrong_external_pin': pin='0'*64
            elif name=='damaged_zip':
                p=root/'frozen_archives/TRIANGLE_REMOVAL_SPREAD_30005114_AUTHOR_SAFE_FREEZE.zip.b64'
                p.write_bytes(b'bad archive\n')
            elif name=='changed_author_copy':
                p=root/'audit/author_frozen/README.md';p.write_bytes(p.read_bytes()+b'\n')
            if name=='rebound_publication_manifest':
                p=root/'PUBLICATION_MANIFEST.json';m=json.loads(p.read_bytes())
                for r in m['files']:
                    if r['path']=='README.md':r.update(v.meta(target.read_bytes()))
                p.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
            try: v.integrity(root,pin)
            except (ValueError,OSError): out.append({'test':name,'rejected':True})
            else: raise AssertionError('Mutation escaped: '+name)
    result=subprocess.run([sys.executable,'-B','-O',str(ROOT/'verify_publication.py')],capture_output=True)
    v.require(result.returncode!=0 and b'Assertions must remain enabled' in result.stderr,'Optimized mode accepted')
    out.append({'test':'optimized_python','rejected':True})
    v.integrity(ROOT,PIN)
    return {'status':'PASS','publication_negative_controls':out,'count':len(out)}

if __name__=='__main__':
    print(json.dumps(tests(),indent=2,sort_keys=True))
