#!/usr/bin/env python3
"""Reproduce optimization, corruption, relocation, and nonroot read-only controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

MODES=[[],['-O'],['-OO']]

def fail(message):
    raise RuntimeError(message)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def run(root,pin,mode):
    return subprocess.run([sys.executable,'-B',*mode,str(root/'verify.py'),'--root',str(root),'--manifest-sha256',pin],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})

def repin(root):
    p=root/'MANIFEST.json';m=json.loads(p.read_text())
    for e in m['files']:
        q=root/e['path']
        if q.is_file() and not q.is_symlink():
            b=q.read_bytes();e['bytes']=len(b);e['sha256']=sha(b)
    b=(json.dumps(m,indent=2)+'\n').encode();p.write_bytes(b);return sha(b)

def json_change(root,name,fn):
    p=root/name;x=json.loads(p.read_text());fn(x);p.write_text(json.dumps(x,indent=2,allow_nan=True)+'\n')

def change_manifest(root,fn):
    json_change(root,'MANIFEST.json',fn)
    return sha((root/'MANIFEST.json').read_bytes())

def mutator(label,root,pin):
    if label=='payload_bit_change':
        p=root/'REPORT.md';p.write_bytes(p.read_bytes()+b'changed\n')
    elif label=='missing_payload':
        (root/'REPORT.md').unlink()
    elif label=='extra_payload':
        (root/'EXTRA.txt').write_text('extra')
    elif label=='payload_symlink':
        p=root/'REPORT.md';p.unlink();p.symlink_to(root/'README.md')
    elif label=='untrusted_manifest_change':
        (root/'MANIFEST.json').write_bytes((root/'MANIFEST.json').read_bytes()+b' ')
    elif label=='boolean_byte_count':
        pin=change_manifest(root,lambda m:m['files'][0].__setitem__('bytes',True))
    elif label=='float_byte_count':
        pin=change_manifest(root,lambda m:m['files'][0].__setitem__('bytes',1.0))
    elif label=='negative_byte_count':
        pin=change_manifest(root,lambda m:m['files'][0].__setitem__('bytes',-1))
    elif label=='unsafe_parent_path':
        pin=change_manifest(root,lambda m:m['files'][0].__setitem__('path','../REPORT.md'))
    elif label=='absolute_path':
        pin=change_manifest(root,lambda m:m['files'][0].__setitem__('path','/REPORT.md'))
    elif label=='duplicate_member':
        pin=change_manifest(root,lambda m:m['files'].append(dict(m['files'][0])))
    elif label=='wrong_hash':
        pin=change_manifest(root,lambda m:m['files'][0].__setitem__('sha256','0'*64))
    elif label=='duplicate_json_key':
        p=root/'MANIFEST.json';b=p.read_bytes().replace(b'"schema": 1',b'"schema": 1, "schema": 1',1);p.write_bytes(b);pin=sha(b)
    elif label=='nan_fixture':
        json_change(root,'FIXTURES.json',lambda x:x['lacunary'].__setitem__('coefficient_base',float('nan')));pin=repin(root)
    elif label=='infinity_fixture':
        json_change(root,'FIXTURES.json',lambda x:x['lacunary'].__setitem__('coefficient_base',float('inf')));pin=repin(root)
    elif label=='boolean_fixture_integer':
        json_change(root,'FIXTURES.json',lambda x:x['log_square_coefficients'][0].__setitem__('n',True));pin=repin(root)
    elif label=='forged_coefficient':
        json_change(root,'FIXTURES.json',lambda x:x['log_square_coefficients'][1].__setitem__('numerator',5));pin=repin(root)
    elif label=='forged_tail':
        json_change(root,'FIXTURES.json',lambda x:x['lacunary'].__setitem__('tail_denominator',64));pin=repin(root)
    elif label=='invalid_direction':
        json_change(root,'FIXTURES.json',lambda x:x['geometry']['directions'].__setitem__(0,[1,1,1]));pin=repin(root)
    elif label=='solution_overclaim':
        json_change(root,'CLAIMS.json',lambda x:x.__setitem__('full_solution_claimed',True));pin=repin(root)
    elif label=='source_overclaim':
        json_change(root,'SOURCES.json',lambda x:x['scholarly_sources'][1].__setitem__('original_full_theorem_inspected',True));pin=repin(root)
    else:
        fail('unknown mutation')
    return pin

def unlock(root):
    for p in root.rglob('*'):
        if not p.is_symlink():
            p.chmod(0o755 if p.is_dir() else 0o644)
    root.chmod(0o755)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True);ap.add_argument('--manifest-sha256',required=True);a=ap.parse_args()
    root=a.root.absolute();baseline=[]
    for mode in MODES:
        r=run(root,a.manifest_sha256,mode)
        if r.returncode!=0:fail('baseline rejected: '+r.stderr)
        baseline.append(r.stdout)
    if len(set(baseline))!=1:fail('optimization changed output')
    labels=['payload_bit_change','missing_payload','extra_payload','payload_symlink','untrusted_manifest_change','boolean_byte_count','float_byte_count','negative_byte_count','unsafe_parent_path','absolute_path','duplicate_member','wrong_hash','duplicate_json_key','nan_fixture','infinity_fixture','boolean_fixture_integer','forged_coefficient','forged_tail','invalid_direction','solution_overclaim','source_overclaim']
    rejected=0
    with tempfile.TemporaryDirectory(prefix='slow-inradius-controls-') as t:
        td=Path(t)
        for i,label in enumerate(labels):
            p=td/('case-'+str(i));shutil.copytree(root,p)
            pin=mutator(label,p,a.manifest_sha256)
            for mode in MODES:
                r=run(p,pin,mode)
                if r.returncode==0 or 'REJECT:' not in r.stderr:fail('negative control failed: '+label+' '+str(mode))
                rejected+=1
        ro=td/'read-only-copy';shutil.copytree(root,ro)
        before={p.relative_to(ro).as_posix():sha(p.read_bytes()) for p in ro.rglob('*') if p.is_file()}
        for p in ro.rglob('*'):
            p.chmod(0o555 if p.is_dir() else 0o444)
        ro.chmod(0o555)
        if not hasattr(os,'geteuid') or os.geteuid()==0:
            unlock(ro);fail('genuine nonroot control requires a nonroot POSIX process')
        denied=[]
        for target in [ro/'WRITE_PROBE',ro/'REPORT.md']:
            try:
                with target.open('ab') as fp:fp.write(b'x')
            except PermissionError:
                denied.append(target.name)
            else:
                unlock(ro);fail('read-only write probe unexpectedly succeeded')
        try:
            for mode in MODES:
                r=run(ro,a.manifest_sha256,mode)
                if r.returncode!=0 or r.stdout!=baseline[0]:fail('read-only or relocation replay failed: '+r.stderr)
            after={p.relative_to(ro).as_posix():sha(p.read_bytes()) for p in ro.rglob('*') if p.is_file()}
            if before!=after:fail('read-only content changed')
        finally:
            unlock(ro)
    print(json.dumps({'baseline_modes':['normal','-O','-OO'],'baseline_output_identical':True,'negative_cases':len(labels),'negative_rejections':rejected,'negative_modes':['normal','-O','-OO'],'negative_labels':labels,'read_only_modes':['normal','-O','-OO'],'nonroot_verified':True,'write_probes_denied':denied,'relocated_output_identical':True,'read_only_inventory_unchanged':True},sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    try:main()
    except (RuntimeError,ValueError,KeyError,TypeError,OSError) as e:
        print('CONTROL FAILURE: '+str(e),file=sys.stderr);sys.exit(1)
