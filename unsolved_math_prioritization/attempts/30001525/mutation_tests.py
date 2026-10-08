#!/usr/bin/env python3
"""Real corrupted-copy child executions; never modifies the frozen publication."""
import argparse, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MODES=('normal','-O','-OO')
def change(root,name):
    p=root/name;p.write_bytes(p.read_bytes()+b'\nsynthetic mutation\n')
def repin(root,outer):
    name='packet/PROOF.md';change(root,name)
    p=root/('PUBLIC_MANIFEST.json' if outer else 'packet/MANIFEST.json');m=json.loads(p.read_bytes());b=(root/name).read_bytes()
    meta={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    if outer:m['files'][name]=meta
    else:
        for e in m['files']:
            if e['path']=='PROOF.md':e.update(meta)
    p.write_text(json.dumps(m,indent=2)+'\n')
def linked(root,directory=False):
    name='packet' if directory else 'packet/PROOF.md';p=root/name
    if directory:shutil.rmtree(p)
    else:p.unlink()
    p.symlink_to(ROOT/name,target_is_directory=directory)
def run(anchor):
    tests=[(name,lambda p,n=name:change(p,n)) for name in ('packet/PROOF.md','packet/MANIFEST.json','packet/verify.py','independent_audit/INDEPENDENT_AUDIT.md','independent_audit/MATHEMATICAL_SUPPLEMENT.md','independent_audit/PATCHES.diff','independent_audit/AUDIT_MANIFEST.json','independent_audit/patched/MANIFEST.json','independent_audit/patched/verify.py','PUBLIC_MANIFEST.json')]
    tests += [('missing_member',lambda p:(p/'packet/AUDIT.md').unlink()),('extra_file',lambda p:(p/'extra.txt').write_text('synthetic')),('extra_empty_directory',lambda p:(p/'extra').mkdir()),('same_byte_symlink',lambda p:linked(p)),('directory_symlink',lambda p:linked(p,True)),('repinned_inner_manifest',lambda p:repin(p,False)),('repinned_outer_manifest',lambda p:repin(p,True))]
    cases=[]
    for name,edit in tests:
        with tempfile.TemporaryDirectory(prefix='skyline-public-corruption-') as td:
            p=Path(td)/'moved package';shutil.copytree(ROOT,p);edit(p)
            for mode in MODES:
                cmd=[sys.executable,'-I','-B']+([] if mode=='normal' else [mode])+[str(p/'verify_publication.py'),'--manifest-sha256',anchor]
                r=subprocess.run(cmd,cwd=td,text=True,capture_output=True,timeout=60)
                if r.returncode==0 or not any(s in r.stderr for s in ('RuntimeError: External manifest anchor mismatch','RuntimeError: Payload mismatch','RuntimeError: Exact inventory mismatch','RuntimeError: Nonregular or linked member')):
                    raise RuntimeError('Corruption was not rejected by the integrity gate: '+name+' '+mode+' '+r.stderr)
                cases.append({'case':name,'mode':mode,'returncode':r.returncode,'rejected':True})
    return {'result':'PASS','actual_corruption_child_rejections':len(cases),'cases':cases,'frozen_original_unchanged':True}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--manifest-sha256',required=True);args=parser.parse_args();print(json.dumps(run(args.manifest_sha256),indent=2,sort_keys=True))
