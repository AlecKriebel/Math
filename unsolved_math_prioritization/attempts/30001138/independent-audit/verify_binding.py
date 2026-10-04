#!/usr/bin/env python3
"""Verify audit-file manifest and exact reviewed ZIP, without extracting it."""
from pathlib import Path
import hashlib,json,sys,zipfile
ROOT=Path(__file__).resolve().parent

def check(raw,size,digest,label):
    if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=digest:raise ValueError(label+' mismatch')

binding=json.loads((ROOT/'AUDIT_BINDING.json').read_text())
manifest=json.loads((ROOT/'AUDIT_MANIFEST.json').read_text())
for f in manifest['files']:check((ROOT/f['path']).read_bytes(),f['bytes'],f['sha256'],f['path'])
p=Path(sys.argv[1]);i=binding['input'];check(p.read_bytes(),i['bytes'],i['sha256'],'input ZIP')
with zipfile.ZipFile(p) as z:
    names=sorted(z.namelist())
    if names!=i['members'] or len(names)!=i['regular_files']:raise ValueError('ZIP members mismatch')
    authored=json.loads(z.read('packet/MANIFEST.json'))
    for f in authored['files']:check(z.read('packet/'+f['path']),f['bytes'],f['sha256'],'packet/'+f['path'])
print('PASS: audit manifest, exact frozen input ZIP, member list, and all authored manifest entries')
