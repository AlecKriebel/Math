#!/usr/bin/env python3
"""Isolated manifest controls. Never modifies an author or audit freeze."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
VERIFY=HERE/'verify_manifest.py'
CASES=('clean','content_edit','truncate','delete','ordinary_extra','nested_manifest_extra',
       'nested_symlink','manifest_symlink','duplicate_path','traversal','absolute_path',
       'noncanonical_path','bad_size','bad_hash','external_binding_mismatch')
results=[]
for name in CASES:
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'packet'; p.mkdir()
        (p/'payload.txt').write_text('independent control\n')
        data=(p/'payload.txt').read_bytes()
        m={'schema':1,'files':[{'path':'payload.txt','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}]}
        (p/'MANIFEST.json').write_text(json.dumps(m))
        expected=None
        if name=='content_edit': (p/'payload.txt').write_text('changed\n')
        if name=='truncate': (p/'payload.txt').write_bytes(b'')
        if name=='delete': (p/'payload.txt').unlink()
        if name=='ordinary_extra': (p/'extra.txt').write_text('extra')
        if name=='nested_manifest_extra':
            (p/'extra').mkdir(); (p/'extra'/'MANIFEST.json').write_text('extra')
        if name=='nested_symlink': (p/'link').symlink_to(p/'payload.txt')
        if name=='manifest_symlink':
            q=Path(td)/'outside.json'; shutil.copy2(p/'MANIFEST.json',q)
            (p/'MANIFEST.json').unlink(); (p/'MANIFEST.json').symlink_to(q)
        if name in ('duplicate_path','traversal','absolute_path','noncanonical_path','bad_size','bad_hash'):
            if name=='duplicate_path': m['files'].append(m['files'][0].copy())
            if name=='traversal': m['files'][0]['path']='../payload.txt'
            if name=='absolute_path': m['files'][0]['path']='/payload.txt'
            if name=='noncanonical_path': m['files'][0]['path']='./payload.txt'
            if name=='bad_size': m['files'][0]['bytes']+=1
            if name=='bad_hash': m['files'][0]['sha256']='0'*64
            (p/'MANIFEST.json').write_text(json.dumps(m))
        if name=='external_binding_mismatch': expected='0'*64
        args=[sys.executable,str(VERIFY),str(p)]+([expected] if expected else [])
        r=subprocess.run(args,capture_output=True)
        accepted=r.returncode==0
        if accepted != (name=='clean'): raise AssertionError(name)
        results.append({'case':name,'accepted':accepted})
out={'status':'PASS','cases':results,'case_count':len(results)}
print(json.dumps(out,indent=2,sort_keys=True))
