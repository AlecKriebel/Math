#!/usr/bin/env python3
"""Strict, relocatable audit replay. No network and no external packages."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

AUTHOR_PIN = 'ce591fbb475041f39c5b6df4e4bafb535f534f1a6c7abd2dc8e439c2314ddf52'
AUTHOR_NAMES = {
    'README.md','PROOF.md','SOURCE_AND_SCOPE.md','RESULT.json',
    'DATASET_VERIFICATION.json','PRIOR_WORK_CHECK.json','SOURCE_METADATA.json',
    'verify_algebra.py','CHECK_RESULTS.json','verify_manifest.py','MANIFEST.json'
}
ROOT_NAMES = {
    'README.md','AUDIT.md','DIMENSION_CONVENTIONS.md','AUDIT_RESULT.json',
    'DATASET_RECHECK.json','SOURCE_RECHECK.json','PRIOR_WORK_RECHECK.json',
    'verify_independent.py','INDEPENDENT_RESULTS.json','verify_audit.py','MANIFEST.json'
}
FILES = ROOT_NAMES | {'author/'+n for n in AUTHOR_NAMES}

def digest(b):
    return hashlib.sha256(b).hexdigest()

def verify_tree(root, expected=None):
    root=Path(root)
    if root.is_symlink():
        raise ValueError('Root must not be a symlink')
    found=set()
    for p in root.rglob('*'):
        name=p.relative_to(root).as_posix()
        if p.is_symlink():
            raise ValueError('Symlink: '+name)
        if p.is_dir():
            if name!='author':
                raise ValueError('Unexpected directory: '+name)
        elif p.is_file():
            found.add(name)
        else:
            raise ValueError('Non-regular entry: '+name)
    if found!=FILES or not (root/'author').is_dir():
        raise ValueError('Unexpected or missing payload: '+str(sorted(found^FILES)))
    raw=(root/'MANIFEST.json').read_bytes()
    pin=digest(raw)
    if expected and expected!=pin:
        raise ValueError('Manifest differs from external pin')
    rows=json.loads(raw)['files']
    if len(rows)!=len(FILES)-1 or {r['path'] for r in rows}!=FILES-{'MANIFEST.json'}:
        raise ValueError('Manifest payload is not exactly the required set')
    for r in rows:
        b=(root/r['path']).read_bytes()
        if len(b)!=r['bytes'] or digest(b)!=r['sha256']:
            raise ValueError('Hash or byte-count mismatch: '+r['path'])
    return pin

def call(script, *args):
    r=subprocess.run([sys.executable,str(script),*map(str,args)],capture_output=True,text=True)
    if r.returncode:
        raise ValueError(r.stderr or r.stdout)
    return json.loads(r.stdout)

def author_verify(root, pin):
    return call(root/'verify_manifest.py','--root',root,'--expected-manifest',pin)

def controls(root, target, pin, verifier):
    results=[]
    for name in ['changed_payload','missing_payload','extra_file','extra_directory',
                 'symlink_payload','rebound_manifest','wrong_manifest_pin']:
        with tempfile.TemporaryDirectory(prefix='hopf-audit-') as td:
            clone=Path(td)/'packet'
            shutil.copytree(root,clone)
            payload=clone/target
            use_pin=pin
            if name in ['changed_payload','rebound_manifest']:
                payload.write_bytes(payload.read_bytes()+b'\nmutation\n')
            elif name=='missing_payload':
                payload.unlink()
            elif name=='extra_file':
                (clone/'EXTRA.txt').write_text('unexpected')
            elif name=='extra_directory':
                (clone/'EXTRA').mkdir()
            elif name=='symlink_payload':
                payload.unlink();payload.symlink_to((root/target).resolve())
            elif name=='wrong_manifest_pin':
                use_pin='0'*64
            if name=='rebound_manifest':
                manifest=clone/'MANIFEST.json'
                data=json.loads(manifest.read_text())
                for row in data['files']:
                    if row['path']==target:
                        b=payload.read_bytes();row.update(bytes=len(b),sha256=digest(b))
                manifest.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
            try:
                verifier(clone,use_pin)
            except (ValueError,OSError):
                results.append({'test':name,'rejected':True})
            else:
                raise AssertionError('Mutation escaped: '+name)
    return results

def run(root,expected=None):
    root=Path(root).resolve()
    pin=verify_tree(root,expected)
    author_verify(root/'author',AUTHOR_PIN)
    author=call(root/'author/verify_algebra.py')
    if author!=json.loads((root/'author/CHECK_RESULTS.json').read_text()):
        raise ValueError('Author output differs from frozen expected output')
    independent=call(root/'verify_independent.py')
    if independent!=json.loads((root/'INDEPENDENT_RESULTS.json').read_text()):
        raise ValueError('Independent output differs from expected output')
    if author['assertions']!=4543 or independent['assertions']!=2902:
        raise ValueError('Assertion count changed')
    a=controls(root/'author','PROOF.md',AUTHOR_PIN,author_verify)
    b=controls(root,'AUDIT.md',pin,verify_tree)
    verify_tree(root,expected)
    return {'status':'pass','files':len(FILES),'author_files':len(AUTHOR_NAMES),
            'author_assertions':4543,'independent_assertions':2902,
            'author_integrity_negative_controls':a,'audit_integrity_negative_controls':b,
            'author_manifest_sha256':AUTHOR_PIN,'audit_manifest_sha256':pin,
            'externally_pinned':bool(expected)}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',default=str(Path(__file__).resolve().parent))
    p.add_argument('--expected-manifest')
    args=p.parse_args()
    print(json.dumps(run(args.root,args.expected_manifest),indent=2,sort_keys=True))
