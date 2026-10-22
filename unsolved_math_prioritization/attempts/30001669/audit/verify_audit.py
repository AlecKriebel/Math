#!/usr/bin/env python3
"""Strict pinned inventory checker; not a mathematical proof checker."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import stat
import zipfile

PAYLOAD={'AUTHOR_SAFE_FREEZE.zip','INDEPENDENT_AUDIT.md','ACCEPTANCE.json','PUBLIC_PROVENANCE.json','AUDIT_VERIFICATION.json','independent_checks.py','verify_audit.py'}
AUTHOR_SHA='15bb36b2d492b2ace008a6b851b31a3893ec0a559ccc3853a2d709f58f3ed96f'
AUTHOR_MANIFEST='d1d79514b2851823f47345677bfa66f53152f1922562b1040f7dd8882028c620'

def need(ok,message):
    if not ok:raise ValueError(message)

def sha(b):return hashlib.sha256(b).hexdigest()

def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'Duplicate JSON key');d[k]=v
    return d

def read_json(b):return json.loads(b,object_pairs_hook=unique)

def verify(root,pin):
    need(not root.is_symlink() and root.is_dir(),'Root is not a real directory')
    entries=list(root.iterdir());need({p.name for p in entries}==PAYLOAD|{'MANIFEST.json'},'Inventory differs')
    for p in entries:
        s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'Nonregular or aliased entry')
    raw=(root/'MANIFEST.json').read_bytes();need(sha(raw)==pin,'External manifest pin differs')
    m=read_json(raw);need(set(m)=={'schema','files'} and m['schema']=='strict-flat-sha256-v1','Manifest schema differs')
    need(set(m['files'])==PAYLOAD,'Manifest inventory differs')
    for name in PAYLOAD:
        b=(root/name).read_bytes();r=m['files'][name]
        need(type(r.get('bytes')) is int and r=={'bytes':len(b),'sha256':sha(b)},'Payload mismatch: '+name)
    b=(root/'AUTHOR_SAFE_FREEZE.zip').read_bytes();need(len(b)==10114 and sha(b)==AUTHOR_SHA,'Author pin differs')
    members={'MANIFEST.json','REPORT.md','PUBLIC_METADATA.json','VERIFICATION.json','audit_checks.py','verify.py'}
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        infos=z.infolist();need(len(infos)==6 and {i.filename for i in infos}==members,'Author ZIP inventory differs')
        for i in infos:need('/' not in i.filename and stat.S_ISREG(i.external_attr>>16),'Nonregular author ZIP member')
        raw=z.read('MANIFEST.json');need(sha(raw)==AUTHOR_MANIFEST,'Author manifest differs');am=read_json(raw)
        need(set(am['files'])==members-{'MANIFEST.json'},'Author manifest inventory differs')
        for name in members-{'MANIFEST.json'}:
            b=z.read(name);need(am['files'][name]=={'bytes':len(b),'sha256':sha(b)},'Author payload differs')
    a=read_json((root/'ACCEPTANCE.json').read_bytes())
    need(a['problem_id']==30001669 and a['classification']=='already_solved' and a['answer']=='negative','Disposition differs')
    need(a['approaches_used']==1 and a['novel_resolution_claim'] is False,'Credit/count differs')
    need(a['mathematical_objections']==[] and a['author_archive_sha256']==AUTHOR_SHA,'Acceptance differs')
    v=read_json((root/'AUDIT_VERIFICATION.json').read_bytes())
    need(v['status']=='pass' and len(v['replays'])==4 and len(v['integrity_controls'])==14 and len(v['semantic_controls'])==24,'Verification summary differs')
    return {'status':'pass','payload_files':len(PAYLOAD),'author_archive_verified':True,'scope':'Pinned artifact integrity and acceptance metadata only; not a formal theorem proof.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--manifest-sha256',required=True)
    a=p.parse_args();print(json.dumps(verify(a.root,a.manifest_sha256),sort_keys=True))
