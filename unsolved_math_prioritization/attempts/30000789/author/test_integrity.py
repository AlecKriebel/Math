#!/usr/bin/env python3
"""Adversarial replay tests; all edits occur only in temporary package copies."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise ValueError(message)

def run(root,pin,optimize=False):
    args=[sys.executable,'-B']+(['-O'] if optimize else [])+[str(root/'verify_package.py'),'--expected-manifest',pin]
    return subprocess.run(args,cwd=root.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)

def alter(root,case):
    if case=='changed_proof':
        p=root/'ATTEMPT_1.md';p.write_bytes(p.read_bytes()+b'\nChanged.\n')
    elif case=='missing_certificate':(root/'certificates.json').unlink()
    elif case=='extra_file':(root/'unexpected.txt').write_text('extra')
    elif case=='truncated_checker':(root/'math_check.py').write_text('')
    elif case=='symlink_result':
        (root/'results.json').unlink();(root/'results.json').symlink_to(ROOT/'results.json')
    elif case=='self_rehashed_payload':
        p=root/'certificates.json';p.write_bytes(p.read_bytes().replace(b'2662/2187',b'2661/2187'))
        m=root/'MANIFEST.json';spec=json.loads(m.read_text())
        for item in spec['files']:
            if item['path']=='certificates.json':
                data=p.read_bytes();item['bytes']=len(data);item['sha256']=hashlib.sha256(data).hexdigest()
        m.write_text(json.dumps(spec,indent=2,sort_keys=True)+'\n')
    elif case=='changed_manifest_whitespace':
        p=root/'MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
    elif case=='truncated_result':(root/'results.json').write_text('{}\n')
    elif case=='missing_manifest':(root/'MANIFEST.json').unlink()
    elif case=='symlink_manifest':
        (root/'MANIFEST.json').unlink();(root/'MANIFEST.json').symlink_to(ROOT/'MANIFEST.json')
    elif case=='extra_directory':(root/'unexpected').mkdir()
    else:raise ValueError('Unknown mutation')

def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);args=p.parse_args()
    positive=[];negative=[]
    cases=['changed_proof','missing_certificate','extra_file','truncated_checker','symlink_result','self_rehashed_payload','changed_manifest_whitespace','truncated_result','missing_manifest','symlink_manifest','extra_directory']
    with tempfile.TemporaryDirectory(prefix='ricci-independent-location-') as td:
        base=Path(td)
        for opt in (False,True):
            good=run(ROOT,args.expected_manifest,opt)
            require(good.returncode==0,'Original positive replay failed: '+good.stderr.decode())
            positive.append({'mode':'optimized' if opt else 'normal','location':'original','status':'PASS'})
            relocated=base/('relocated_opt' if opt else 'relocated_normal');shutil.copytree(ROOT,relocated)
            good=run(relocated,args.expected_manifest,opt)
            require(good.returncode==0,'Relocated positive replay failed: '+good.stderr.decode())
            positive.append({'mode':'optimized' if opt else 'normal','location':'unrelated_temporary_directory','status':'PASS'})
            for case in cases:
                dest=base/(case+('_opt' if opt else '_normal'));shutil.copytree(ROOT,dest);alter(dest,case)
                result=run(dest,args.expected_manifest,opt)
                require(result.returncode!=0,'Accepted corruption '+case)
                negative.append({'mode':'optimized' if opt else 'normal','case':case,'status':'REJECTED'})
            result=run(relocated,'0'*64,opt)
            require(result.returncode!=0,'Accepted wrong external anchor')
            negative.append({'mode':'optimized' if opt else 'normal','case':'wrong_external_anchor','status':'REJECTED'})
    print(json.dumps({'status':'PASS','positive_replays':positive,'mutation_rejections':negative,'scope':'Transport and integrity controls do not establish the unproved global Weyl inequality; independent mathematical audit is pending.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
