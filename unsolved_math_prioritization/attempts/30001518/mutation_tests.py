#!/usr/bin/env python3
"""Adversarial, temporary-copy tests of the externally pinned publication wrapper."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

CASES=('payload_same_size','payload_appended','missing_payload','missing_manifest','invalid_manifest',
       'extra_file','extra_directory','duplicate_manifest_key','omitted_entry','coherent_rehash',
       'symlink_payload','symlink_directory','frozen_manifest_rehash','omitted_frozen_entry',
       'duplicated_frozen_entry','wrong_recorded_size','wrong_recorded_digest','verifier_modified','archive_truncate','audit_payload_modified')

def need(value,message):
    if not value:raise RuntimeError(message)

def change(root,case):
    p=root/'PUBLIC_MANIFEST.json';m=json.loads(p.read_text());target=root/'packet/README.md'
    if case=='payload_same_size':target.write_bytes(b'!'+target.read_bytes()[1:])
    elif case=='payload_appended':target.write_bytes(target.read_bytes()+b'\n')
    elif case=='missing_payload':target.unlink()
    elif case=='missing_manifest':p.unlink()
    elif case=='invalid_manifest':p.write_text('{')
    elif case=='extra_file':(root/'extra.txt').write_text('extra\n')
    elif case=='extra_directory':(root/'empty').mkdir()
    elif case=='duplicate_manifest_key':p.write_text(p.read_text().replace('"files": {','"files": {}, "files": {',1))
    elif case=='omitted_entry':del m['files']['packet/README.md'];p.write_text(json.dumps(m))
    elif case=='coherent_rehash':
        target.write_bytes(target.read_bytes()+b'\n');b=target.read_bytes()
        m['files']['packet/README.md']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};p.write_text(json.dumps(m))
    elif case=='symlink_payload':target.unlink();target.symlink_to(root/'audit_frozen/README.md')
    elif case=='symlink_directory':
        shutil.rmtree(root/'packet');(root/'packet').symlink_to(root/'audit_frozen',target_is_directory=True)
    elif case in ('frozen_manifest_rehash','omitted_frozen_entry','duplicated_frozen_entry'):
        f=root/'packet/AUTHOR_MANIFEST.json';o=json.loads(f.read_text())
        if case=='frozen_manifest_rehash':o['snapshot']='self-consistently substituted snapshot'
        elif case=='omitted_frozen_entry':o['files'].pop()
        else:o['files'].append(o['files'][0].copy())
        f.write_text(json.dumps(o));b=f.read_bytes();m['files']['packet/AUTHOR_MANIFEST.json']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};p.write_text(json.dumps(m))
    elif case=='wrong_recorded_size':m['files']['packet/README.md']['bytes']+=1;p.write_text(json.dumps(m))
    elif case=='wrong_recorded_digest':m['files']['packet/README.md']['sha256']='0'*64;p.write_text(json.dumps(m))
    elif case=='verifier_modified':
        f=root/'verify_publication.py';f.write_bytes(f.read_bytes()+b'\n# altered\n')
    elif case=='archive_truncate':
        f=root/'author_packet.zip';f.write_bytes(f.read_bytes()[:-1])
    elif case=='audit_payload_modified':
        f=root/'audit_frozen/AUDIT_REPORT.md';f.write_bytes(f.read_bytes()+b'\n')
    else:raise RuntimeError('Unknown case')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--expected-manifest-sha256',required=True);a=parser.parse_args()
    source=Path(__file__).resolve().parent;driver=source/'verify_publication.py';results=[]
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    with tempfile.TemporaryDirectory(prefix='retro-corruption-') as temp:
        for case in ('valid',)+CASES:
            root=Path(temp)/case;shutil.copytree(source,root)
            if case!='valid':change(root,case)
            for mode in (0,1,2):
                cmd=[sys.executable,'-I','-S','-B']+(['-'+'O'*mode] if mode else [])+[str(driver),'--root',str(root),'--expected-manifest-sha256',a.expected_manifest_sha256,'--integrity-only']
                p=subprocess.run(cmd,capture_output=True,env=env,cwd=temp,timeout=30)
                need((p.returncode==0)==(case=='valid'),'Unexpected acceptance: '+case+' mode '+str(mode))
                results.append({'case':case,'wrapper_mode':mode,'accepted':p.returncode==0})
    print(json.dumps({'status':'PASS','wrapper_optimization_level':sys.flags.optimize,'cases':len(results),'results':results},indent=2,sort_keys=True))
if __name__=='__main__':main()
